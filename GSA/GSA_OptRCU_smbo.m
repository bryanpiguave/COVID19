% Cyclone Reactor Model for Biiomass Pyrolysis
% Optimization Mathematical Model
% by Santiago D. Salas
% Optimized by Dany De Cecchis

% close all;
% clearvars;
% clc;


% global GSA

%% Sample generator

function z=GSA_OptRCU_smbo(x)

%mean_values = [5 0.1 25 2.5E6 554.44 0.2E6 5. 12E-2 3.58E-2 2800 6.7];
% mean_values = [5 0.2 30 2.5E6 550 0.15E6 4.75E-2 3.65E-2 1140 8.95];
mean_values = [0.2 30 2.5E6 550 0.15E6 4.75E-2 3.65E-2 1140 2.5]; % Four variables
% optimus_values = [0.2 35 2.5E6 550 0.15E6 5.5E-2 4.2E-2 1400 2]; % Four variables
% mean_values = [0.2 25 2.5E6 700 0.2E6 5.12E-2 3.58E-2 1400 2];
% Dimensions
nd = length(mean_values); % determines number of variables considered in sensitivity analysis

% costs = zeros(nd+2,1);
% Costs asociated with each variable
% costs(1) = 0; % mBidL
% costs(2) = 0.01; % mInt1dL
% costs(3) = 1; % mTar1dL
% costs(4) = 0.001; % mChar1dL
% costs(5) = 0.1; % mgasdL
% costs(6) = 2; % mTar2dL
% costs(7) = 0.001; % mChar2dL
% costs(8) = 0; % maguadL
% costs(9) = 0; % TgdL
% costs(10) = 0; % TsdL
% costs(11) = -0.001; % moBi Biomass initial value
% costs(12) = -0.05; % mso Flujo másico del sólido (g/s) 


%% Process Parameters
GSA.moBi = 5; % FIXED! Flujo flujo másico de alimentación Biomasa (g/s)
GSA.U = 400; % Coeficiente global de transferencia de calor ¡¡ GSA - VERIFICAR VARIACIÓN !!
GSA.L0 = 0;
GSA.L = [];   % ODE45 time stepping
% GSA.costs = costs;    % vector of costs


%GSA.moBi = mean_values(1); %3 + x(1)*4;% significant
GSA.H2Bi = mean_values(1);
GSA.mso = 25 + 10*x(1); % significant
GSA.dso = mean_values(3);
GSA.Tgi = mean_values(4);
GSA.P = mean_values(5);
GSA.D1 = 4E-2 + (5.5E-2 - 4E-2)*x(2); % mean_values(6); % significant
GSA.D2 = 3.1E-2 + (4.2E-2 - 3.1E-2)*x(3); % mean_values(7); % significant
GSA.Ts = 880 + (1400-880)*x(4); % significant
GSA.Lfin = mean_values(9);
    
z = -inputRCU_2(GSA);
