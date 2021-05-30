%% UCI dataset parser
% This is the parser script that parses the UCI dataset into segments
% of specified size.

%% Clean the workspace
clear all;
close all;
clc;

%% Load files

load('Part.mat');

n_of_records = length(Part);

%% Definitions

properties.sampling_freq = 125;
properties.sampling_time = 1/properties.sampling_freq;
properties.segment_size_seg = 5;
properties.segment_size_samples = properties.segment_size_seg*properties.sampling_freq;

%% Preallocation

n_of_segments = 528828;
ppg_matrix = zeros(properties.segment_size_samples, n_of_segments); % todo: mover 528828 para uma constante
abp_matrix = zeros(properties.segment_size_samples, n_of_segments); % todo: mover 528828 para uma constante

seg_id = 1;     % Initial seg_id

%% Parse

tic

for i = 1:n_of_records
    n_of_part_samples = length(Part{i}(1, :));
    n_of_part_segments = floor(n_of_part_samples / properties.segment_size_samples);
    
    for k = 1:n_of_part_segments
        ppg_matrix(:, seg_id) = Part{i}(1, 1 + (k-1)*properties.segment_size_samples : k*properties.segment_size_samples);
        abp_matrix(:, seg_id) = Part{i}(2, 1 + (k-1)*properties.segment_size_samples : k*properties.segment_size_samples);
        
        seg_id = seg_id + 1;
    end
    
end

toc

%% Split and export parsed dataset

n_of_files = 4;
n_of_segments_after_split = floor(n_of_segments / n_of_files);

for i = 0:1:n_of_files - 1
    ppg_matrix_split = ppg_matrix(:, 1 + i*n_of_segments_after_split : (i+1)*n_of_segments_after_split);
    abp_matrix_split = abp_matrix(:, 1 + i*n_of_segments_after_split : (i+1)*n_of_segments_after_split);
    
    i_string = num2str(i+1);
    ppg_matrix_filename = strcat('ppg_matrix_split_', i_string, '.csv');
    abp_matrix_filename = strcat('abp_matrix_split_', i_string, '.csv');
    csvwrite(ppg_matrix_filename, ppg_matrix_split);
    csvwrite(abp_matrix_filename, abp_matrix_split);
end

