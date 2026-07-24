function data_cleaning(folder)
% Folder where your s_i files are stored


% Get all files starting with s_
files = dir(fullfile(folder, 's_*'));

for k = 1:length(files)
    infile  = fullfile(folder, files(k).name);
    outfile = fullfile(folder, ['clean_' files(k).name]); % or overwrite
    
    fin  = fopen(infile, 'r');
    fout = fopen(outfile, 'w');
    
            % --- Read the whole file first ---
            data = {};
            line = fgetl(fin);
            while ischar(line)
                % Remove u/d
                cleaned = regexprep(line, '[ud]', '');
                
                % Split into time and value
                parts = strsplit(strtrim(cleaned));
                t = str2double(parts{1});
                v = str2double(parts{2});
                
                data{end+1,1} = t;
                data{end,2}   = v;
                
                line = fgetl(fin);
            end
            fclose(fin);
            
            % --- Time shifting ---
        %     if ~isempty(data)
        %         t0 = data{1,1};                 % original starting time
        %         for n = 1:size(data,1)
        %             data{n,1} = data{n,1} - t0; % shift
        %         end
        %     end
            
            % --- Write cleaned & shifted data ---
            fprintf(fout, '%.10f %d\n', 0, 0);
            for n = 1:size(data,1)
        
                fprintf(fout, '%.10f %d\n', data{n,1}, data{n,2});
            end 
            
            fclose(fout); 
end

fprintf('\n Data cleaning + time shifting completed');