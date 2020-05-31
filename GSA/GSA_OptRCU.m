% Cyclone Reactor Model for Biiomass Pyrolysis
% Optimization Mathematical Model
% by Santiago D. Salas
% Optimized by Dany De Cecchis

% close all;
% clearvars;
% clc;


% global GSA

%% Sample generator

function z=GSA_OptRCU(x)

%mean_values = [5 0.1 25 2.5E6 554.44 0.2E6 5.12E-2 3.58E-2 2800 6.7];
mean_values = [5 0.2 30 2.5E6 550 0.15E6 4.75E-2 3.65E-2 1140 8.95];

%% Process Parameters
GSA.U = 400; % Coeficiente global de transferencia de calor ¡¡ GSA - VERIFICAR VARIACIÓN !!
GSA.L0 = 0;
GSA.L = [];   % ODE45 time stepping

GSA.moBi = mean_values(1); %3 + x(1)*4;% significant
GSA.H2Bi = mean_values(2);
GSA.mso = 25 + 10*x(1); % significant
GSA.dso = mean_values(4);
GSA.Tgi = mean_values(5);
GSA.P = mean_values(6);
GSA.D1 = mean_values(7); % 4E-2 + (5.5E-2 - 4E-2)*x(3); % significant
GSA.D2 = mean_values(8); % 3.1E-2 + (4.2E-2 - 3.1E-2)*x(4); % significant
GSA.Ts = 880 + (1400-880)*x(2); % significant
GSA.Lfin = mean_values(10);
    
z = -inputRCU(GSA);
