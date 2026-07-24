close all;
clear all;
clc;
warning('OFF', 'ALL')

display_option=1
; %to plot falsifiers, set this to a value greater than 0

rootdir = ".";
cdirname = "/SigExpC/";
bdirname = "/SigExpB/";
adirname = "/SigExpA/";

addpath(rootdir + "/Functions")
addpath(rootdir + "/ExampleBand-Pass")
addpath(rootdir + "/breach-dev")
 
      

InitBreach;
BP2param;

model_name = 'BP2_in';

%rng(15000,'twister');
BrSD = BreachSimulinkSystem(model_name);

for expId = 1:3
    switch expId
      case 1
          sigdir = rootdir + adirname;
          fprintf("\n=== Treating the expression exA\n")
      case 2
          sigdir = rootdir + bdirname;
          fprintf("\n=== Treating the expression exB\n")
      case 3
          sigdir = rootdir + cdirname;
          fprintf("\n=== Treating the expression exC\n")
    end


    data_cleaning(sigdir);
    continuous_signal_generation(sigdir);

    fprintf("\n Simulations with the generated input signals\n")


    myzero = 1e-10;
    
    robworst = 100000;
    count = 0;
    sigIdworst=-1;
    
    Id = [];
    for sigId = 0:99 
        fprintf('.');
        if (sigId < 10)
            sigfilename = strcat(sigdir + 'f1cos_clean_s_00', num2str(sigId), '.txt');
        else
            if (sigId < 100)
              sigfilename = strcat(sigdir + 'f1cos_clean_s_0', num2str(sigId), '.txt');
            else
              sigfilename = strcat(sigdir + 'f1cos_clean_s_', num2str(sigId), '.txt');
            end
        end
        
    
       for scalingStep = 0:2
    
            In1 = load(sigfilename, '-ascii');
            
            scaling = 5.0e-8 + scalingStep*0.35e-8;
            
            In1(:,1) = scaling*In1(:,1);
            time = In1(:,1);
            time= time-time(1);
            
            sg_in = from_workspace_signal_gen({'In1'});
          
            
            BrSD_temp=BrSD.copy();
            BrSD_temp.SetInputGen({sg_in}); 
            phi = STL_Formula('notsaturation', 'alw(OutSat[t]<=2 and OutSat[t]>=-2)');
            BrSD_temp.Sim(time);
            rob = BrSD_temp.CheckSpec(phi);
            
            
            if rob<=robworst
                robworst = rob;
                sigIdworst= sigId;
            end
            
            if rob<myzero
                fprintf('\nFalsified!');
                %scaling
                if (display_option>0)
                  new_fig = gcf;
                  Fig= BrSD_temp.PlotSignals({'In1', 'OutSat'});
                  set(gca, 'YLim', [-2.1 2.1]);
                  set(Fig, 'LineWidth', 1.5);
                end
                falsified = true;
                Id = [Id sigId];
                count=count+1;
                %break;
            end
      end
        
    end
    
    %robworst
    %sigIdworst
    %Id
    fprintf('\nNumber of Falsifiers: %d\n', count);  

    if expId<=2 
        input('\n=== Press ENTER to proceed with the next expression', 's');
        close all;
    end

end   