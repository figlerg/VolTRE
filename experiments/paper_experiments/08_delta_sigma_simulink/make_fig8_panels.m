% Recreates the three panels of Fig. 8 of the paper.
%
% Left to right in the paper: an input sampled from e_C (no falsification,
% sample s_050), from e_B (falsifies, s_044), and from e_A (falsifies,
% s_099), each with its quantizer output, at input scaling 5.745e-8.
% Prerequisites are the same as for testUniform.m (see README.md), run
% this script from this folder. Each panel is also saved as
% fig8_panel<N>_<class>_s<id>.png next to this script.

close all;
clear all;
clc;
warning('OFF', 'ALL')

rootdir = ".";
addpath(rootdir + "/Functions")
addpath(rootdir + "/ExampleBand-Pass")
addpath(rootdir + "/breach-dev")

InitBreach;
BP2param;

model_name = 'BP2_in';
BrSD = BreachSimulinkSystem(model_name);

% panel definitions: signal class folder, sample id, paper panel position
panels = {"SigExpC", 50; "SigExpB", 44; "SigExpA", 99};
scaling = 5.745e-8;

phi = STL_Formula('notsaturation', 'alw(OutSat[t]<=2 and OutSat[t]>=-2)');
myzero = 1e-10;

for p = 1:3
    sigdir = rootdir + "/" + panels{p,1} + "/";
    sigId = panels{p,2};

    % make sure the continuous signals exist (regenerates from the
    % committed timed words s_* if needed, same as testUniform.m)
    if ~isfile(sigdir + sprintf('f1cos_clean_s_%03d.txt', sigId))
        data_cleaning(sigdir);
        continuous_signal_generation(sigdir);
    end

    In1 = load(sigdir + sprintf('f1cos_clean_s_%03d.txt', sigId), '-ascii');
    In1(:,1) = scaling*In1(:,1);
    time = In1(:,1);
    time = time - time(1);

    sg_in = from_workspace_signal_gen({'In1'});
    BrSD_temp = BrSD.copy();
    BrSD_temp.SetInputGen({sg_in});
    BrSD_temp.Sim(time);
    rob = BrSD_temp.CheckSpec(phi);

    if rob < myzero
        verdict = 'Falsified';
    else
        verdict = 'No falsification';
    end
    fprintf('%s s_%03d: robustness %g -> %s\n', panels{p,1}, sigId, rob, verdict);

    figure;
    Fig = BrSD_temp.PlotSignals({'In1', 'OutSat'});
    set(gca, 'YLim', [-2.1 2.1]);
    set(Fig, 'LineWidth', 1.5);
    saveas(gcf, sprintf('fig8_panel%d_%s_s%03d.png', p, panels{p,1}, sigId));
end

fprintf(['\nExpected, matching Fig. 8 of the paper: no falsification for ' ...
         'SigExpC s_050, falsified for SigExpB s_044 and SigExpA s_099.\n']);
