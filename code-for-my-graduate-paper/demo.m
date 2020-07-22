%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This code can only be used for non-comercial purpose.
%
% Code Author: Fangjun Wen
% Email: wfj268@qq.com
% Date: 04/07/2016
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
clear all;
clc;

addpath(genpath('.\others\'));
%%------------------------set parameters---------------------%%
spnumber=200; % superpixel number
% DATASET='MSRA1000';
% DATASET='BSD300';
DATASET='MSRA1000';
METHOD='ISDIP'
% METHOD='ISDIP-RTB';
% imgRoot=fullfile('.\',DATASET,'images','\');
% saldir=fullfile('.\',DATASET,'\saliencymap\',METHOD,'\'); % the output path of the saliency map
% supdir=fullfile('.\',DATASET,'\superpixels\'); % the superpixel label file path
% imgRoot='./test_big/';
% imgRoot='./testTemp/';
imgRoot='./test/';
saldir='./saliencymap/';
supdir=fullfile('./superpixels/'); % the superpixel label file path
if ~exist(supdir)
    mkdir(supdir);
end
if ~exist(saldir)
    mkdir(saldir);
end

imgInNames=dir([imgRoot '*' 'jpg']);

tic;

for ii=1:length(imgInNames)
    disp(ii);
    imname=[imgRoot imgInNames(ii).name];
    
    imgIn=imread(imname);
    imgIn=im2double(imgIn);
    
    %% height,width,dimension
    [h,w,d]=size(imgIn);
    outname=[imname(1:end-4) '.bmp'];
    imwrite(imgIn,outname);
    
    %% ---------------------- generate superpixels -------------------- %%
    imname=[imname(1:end-4) '.bmp']; % the slic software support only the '.bmp' image
    comm=['SLICSuperpixelSegmentation' ' ' imname ' ' int2str(20) ' ' int2str(spnumber) ' ' supdir];
    system(comm);
    spname=[supdir imgInNames(ii).name(1:end-4)  '.dat'];
    superpixels=ReadDAT([h,w],spname); % superpixel label matrix
    spnum=max(superpixels(:)); % the actual superpixel number
    spPixels=h*w/spnum;
    
    %% 获得四个方向扫描的结果
    %% scanningResult 为四个方向上的扫描的显著图
    %% inds为超像素标记矩阵
    [ scanningResult, inds ] = ISDIP (spPixels,superpixels, spnum, w, h, d, imgIn);
   
    %% 4 个方向上的显著图融合对比实验 
    %% 说明：
    %% left to right 标记为 1
    %% right to left 标记为 2
    %% top to down 标记为 3
    %% down to top 标记为 4
    %% 如为 1 和 2 线性融合，则记为 12；
    %% 如为 1，2，3相互融合则记为 123，依此类推。
    
    SuperpixelLevelSaliencyWeightMatrix=scanningResult{1}.*scanningResult{2}.*scanningResult{3}.*scanningResult{4};
%     SuperpixelLevelSaliencyWeightMatrix=scanningResult{1};
%     SuperpixelLevelSaliencyWeightMatrix=scanningResult{1}.*scanningResult{2};
%     SuperpixelLevelSaliencyWeightMatrix=scanningResult{1}.*scanningResult{2}.*scanningResult{3};
    
    %% assign the saliency value to each pixel
    salmap=zeros(h,w);
    for i=1:spnum
        salmap(inds{i})=SuperpixelLevelSaliencyWeightMatrix(i);
    end
    salmap=(salmap-min(salmap(:)))/(max(salmap(:))-min(salmap(:)));
    salmap=uint8(salmap.*255);
    outname=[saldir imgInNames(ii).name(1:end-4)   '.png'];
    imwrite(salmap,outname);
    
    toc;
    
end


