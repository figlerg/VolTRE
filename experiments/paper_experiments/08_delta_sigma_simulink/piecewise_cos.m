function [t_all, s_all] = piecewise_cos(time_points, freq, samples_per_interval)
t_all = [];
s_all = [];

for i = 1:length(time_points)-1
    t0 = time_points(i);
    t1 = time_points(i+1);
    
    % Skip zero-length intervals
    if t1 <= t0
        continue;
    end
    
    % Generate samples
    t_segment = linspace(t0, t1, samples_per_interval)';
    local_t = t_segment - t0;
    s_segment = - cos(2*pi*(local_t - 0)/(t1 - t0)); %cos(2*pi*freq*local_t);
    
    % Remove first sample of the segment except for the first interval
    if i > 1
        t_segment = t_segment(2:end);
        s_segment = s_segment(2:end);
    end
    
    t_all = [t_all; t_segment];
    s_all = [s_all; s_segment];
end
end