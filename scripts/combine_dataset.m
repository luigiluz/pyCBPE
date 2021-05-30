%% Combine dataset files
% This script purpose is to combine all dataset files into one unique file
% to avoid combining them multiple times through the process

%% Clean the workspace
clear all;
close all;
clc;

%% Load files

load('Part_1.mat');
load('Part_2.mat');
load('Part_3.mat');
load('Part_4.mat');

%% Operations

Part = [Part_1 Part_2 Part_3 Part_4];

%% Export file

save('Part.mat', '-v7.3', 'Part');
