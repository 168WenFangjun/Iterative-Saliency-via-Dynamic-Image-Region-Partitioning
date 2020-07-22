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
    
    %% ����ĸ�����ɨ��Ľ��
    %% scanningResult Ϊ�ĸ������ϵ�ɨ�������ͼ
    %% indsΪ�����ر�Ǿ���
    [ scanningResult, inds ] = ISDIP (spPixels,superpixels, spnum, w, h, d, imgIn);
   
    %% 4 �������ϵ�����ͼ�ں϶Ա�ʵ�� 
    %% ˵����
    %% left to right ���Ϊ 1
    %% right to left ���Ϊ 2
    %% top to down ���Ϊ 3
    %% down to top ���Ϊ 4
    %% ��Ϊ 1 �� 2 �����ںϣ����Ϊ 12��
    %% ��Ϊ 1��2��3�໥�ں����Ϊ 123���������ơ�
    
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


