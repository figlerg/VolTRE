
function continuous_signal_generation(folder)
% folder containing your s_i files

   fprintf("\n Generating continuous signals from timed words\n");
    
   % Settings
    freq = 1;                        % cosine frequency
    samplesPerInterval = 200;        % samples per segment

    
    % Get all files starting with s_
    files = dir(fullfile(folder, 'clean_s_*'));
    
    for k = 1:length(files)
        
        % --- Input and output filenames ---
        infile  = fullfile(folder, files(k).name);
        outfile = fullfile(folder, ['f1cos_' files(k).name]);  % output prefix 'cos_'
         

                % --- Load numeric text file ---
                % readmatrix automatically handles spaces, tabs, empty lines, etc.
                dataMatrix = readmatrix(infile); 
                
                % --- Check we have at least 1 column ---
                if isempty(dataMatrix) || size(dataMatrix,2) < 1
                    warning('File %s is empty or invalid. Skipping.', infile);
                    continue;
                end
                
                % --- Extract first column as time points ---
                time_points = dataMatrix(:,1);
                
                time_points = time_points([true; diff(time_points) ~= 0]);
            
                % --- Build piecewise cosine ---
                [t, s] = piecewise_cos(time_points, freq, samplesPerInterval);
                
                % --- Save output as two columns: time and cosine value ---
                outMatrix = [t(:), s(:)];
                writematrix(outMatrix, outfile, 'Delimiter', ' ');
                
                %fprintf('Processed %s -> %s\n', infile, outfile);
         
    end
end