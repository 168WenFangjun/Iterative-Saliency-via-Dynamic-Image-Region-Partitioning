%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This code can only be used for non-comercial purpose.
%
% Code Author: Fangjun Wen
% Email: wfj268@qq.com
% Date: 04/07/2016
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [ scanningResult, inds ] = ISDIP (spPixels,superpixels, spnum, w, h, d, imgIn)

%%
input_vals=reshape(imgIn, h*w, d);
rgb_vals=zeros(spnum,1,3);
inds=cell(spnum,1);

%% location information
location_vals=zeros(spnum,2);
for i=1:spnum
    inds{i}=find(superpixels==i);
    rgb_vals(i,1,:)=mean(input_vals(inds{i},:),1);
    %         [hh,ww]=ind2sub(size(superpixels),inds{i});
    %         location_vals(i,1)=mean(hh/h);
    %         location_vals(i,2)=mean(ww/w);
end

%% colorspace transform
lab_vals=colorspace('Lab<-', rgb_vals);
xyz_vals=colorspace('XYZ<-',rgb_vals);

%% feature in RGB,LAB,XYZ
seg_vals_rgb=reshape(rgb_vals,spnum,3); % feature for each superpixel in RGB
seg_vals_lab=reshape(lab_vals,spnum,3); % feature for each superpixel in LAB
seg_vals_xyz=reshape(xyz_vals,spnum,3); % feature for each superpixel in XYZ

%% construct the feature vector using seg_vals
feature=cell(spnum,1);
for loopCount=1:spnum
    feature{loopCount}=[seg_vals_rgb(loopCount,1),seg_vals_rgb(loopCount,2),seg_vals_rgb(loopCount,3),...
        seg_vals_xyz(loopCount,1),seg_vals_xyz(loopCount,2),seg_vals_xyz(loopCount,3),...
        seg_vals_lab(loopCount,1),seg_vals_lab(loopCount,2),seg_vals_lab(loopCount,3)];
end

featureLength=length(feature{spnum});

%% scanning information
scanningGap=floor(sqrt(spPixels))-1;  %
% scanningGap  24
scanningResult=cell(4,1);
for i=1:4
    scanningResult{i}=zeros(spnum,1);
end



%% four direction scanning
for scanningLabel=1:4
    
    if scanningLabel==1
        %% left to right
        loopsCount=w;
        bg_left=cell(1,loopsCount);
        
        for i=1:scanningGap:loopsCount
            bg_left{i}=unique(superpixels(1:h,1:i));
        end
    end
    
    if scanningLabel==2
        %% right to left
        loopsCount=w;
        bg_right=cell(1,loopsCount);
        
        for i=1:scanningGap:loopsCount
            bg_right{i}=unique(superpixels(1:h,(loopsCount-i+1):w));
        end
    end
    
    if scanningLabel==3
        %% top to bottom
        loopsCount=h;
        
        for i=1:scanningGap:loopsCount
            bg_top{i}=unique(superpixels(1:i,1:w));
        end
    end
    
    if scanningLabel==4
        %% bottom to top
        loopsCount=h;
        bg_bottom=cell(1,loopsCount);
        
        for i=1:scanningGap:loopsCount
            bg_bottom{i}=unique(superpixels((loopsCount-i+1):h,1:w));
        end
    end
    
    %         salmap=cell(spnum,1);
    %         for i=1:spnum
    %             salmap{i}=zeros(h,w);
    %         end
    
    %% weight matrix construction
    weightMatrixOnObjectSeeds=cell(int8(loopsCount),1);
    for i=1:scanningGap:loopsCount
        weightMatrixOnObjectSeeds{i}=zeros(spnum,1);
    end
    
    %% loopsCount iterate times
    loopsCount=loopsCount*1/2; %
    
    spSeeds=[1:spnum];
    for loopCount=1:scanningGap:loopsCount
        %% choose the right bgSeeds
        switch(scanningLabel)
            case 1
                bgSeeds=bg_left{loopCount};
            case 2
                bgSeeds=bg_right{loopCount};
            case 3
                bgSeeds=bg_top{loopCount};
            case 4
                bgSeeds=bg_bottom{loopCount};
        end
        
        sumBgSeedsFeature=zeros(1,featureLength);
        for i=1:spnum
            if ismember(i,bgSeeds)==1
                sumBgSeedsFeature=sumBgSeedsFeature+feature{i};
            end
        end
        avgBgSeedsFeature=sumBgSeedsFeature/length(bgSeeds); % edge seeds average color feature vector
        
        if loopCount >= 2
            weightMatrixOnObjectSeeds{loopCount}=weightMatrixOnObjectSeeds{loopCount-scanningGap};
        end
        
        if loopCount > spnum
            break;
        end
        
        %         %% location_vals of center seeds
        centerSeeds=setdiff(spSeeds,bgSeeds);
        %         avgCenterSeedsLocationVals=zeros(1,2);
        %         for j=1:spnum
        %             if ismember(j,centerSeeds)==1
        %                 avgCenterSeedsLocationVals=avgCenterSeedsLocationVals+location_vals(j,:);
        %             end
        %         end
        %         avgCenterSeedsLocationVals=avgCenterSeedsLocationVals/length(centerSeeds);
        
        %% calculate color difference and spatial difference
        %             spatialDiff=0;
        for i=1:spnum
            if ismember(i,centerSeeds)==1
                colorDiff=pdist2(feature{i},avgBgSeedsFeature); % color difference
                
                %                     spatialDiff=pdist2(location_vals(i,:),avgCenterSeedsLocationVals); % spatial difference
                %                     weightMatrixOnObjectSeeds{loopCount}(i)=weightMatrixOnObjectSeeds{loopCount}(i)+colorDiff*exp(-spatialDiff);
                weightMatrixOnObjectSeeds{loopCount}(i)=weightMatrixOnObjectSeeds{loopCount}(i)+colorDiff;
            end
        end
        
        %             %% assign the saliency value to each pixel
        %             for i=1:spnum
        %                 salmap{loopCount}(inds{i})=weightMatrixOnObjectSeeds{loopCount}(i);
        %             end
        %             salmap{loopCount}=(salmap{loopCount}-min(salmap{loopCount}(:)))/(max(salmap{loopCount}(:))-min(salmap{loopCount}(:)));
        %
        %             salMapOut=salmap{loopCount};
        %             salMapOut=uint8(salMapOut*255);
        %
        %             outname=[saldir imgInNames(ii).name(1:end-4)  '_' num2str(loopCount)  '.png'];
        %             imwrite(salMapOut,outname);
        
    end
    
    scanningResult{scanningLabel}=weightMatrixOnObjectSeeds{loopCount};
end

end