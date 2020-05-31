% Cyclone Reactor Model for Biiomass Pyrolysis
% Mathematical Model
% by Santiago D. Salas
% Optimized by Dany De Cecchis

close all;
clearvars;
clc;

tic

% global GSA

%% Sample generator

mean_values = [0.2 30 2.5E6 550 0.15E6 4.75E-2 3.65E-2 1140 2.5]; % four variable
% mean_values = [0.2 25 2.5E6 700 0.2E6 5.12E-2 3.58E-2 1400 2];% two variables
% Dimensions
nd = length(mean_values); % determines number of variables considered in sensitivity analysis
np = 500; %sample size 
nstep = 100; % Discretization of ODE45

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


% Uncertainty index
unc = 5; % Measured in percentage

ub1 = mean_values*(1 + unc/100);% 5% up mean
lb1 = mean_values.*(1 - unc/100);% 5% below mean

ub2 = ub1;
lb2 = lb1;

sample = 1+(2*rand(np,nd)-1)*unc/100; % The % moved between plus or minus the unc%
M1 = sample.*(ones(np,1)*mean_values); % sample 1
%rand(np,nd).*(ones(np,1)*(ub1-lb1)) + (ones(np,1)*lb1); % random matrix M1 generated for the variables (random number for each variable in their range)

sample = 1+(2*rand(np,nd)-1)*unc/100; % The % moved between plus or minus the unc%
M2 = sample.*(ones(np,1)*mean_values); % sample 2
%rand(np,nd).*(ones(np,1)*(ub2-lb2)) + (ones(np,1)*lb2); % random matrix M2 generated for the variables (random number for each variable in their range)

% Sample 3 to subsitute a NaN sample
sample = 1+(2*rand(np,nd)-1)*unc/100; % The % moved between plus or minus the unc%
M3 = sample.*(ones(np,1)*mean_values); % sample 3
repo=0; % How many subtitutions are being performed.

%% Process Parameters
GSA.moBi = 5; % FIXED! Flujo flujo másico de alimentación Biomasa (g/s)
GSA.U = 400; % Coeficiente global de transferencia de calor ¡¡ GSA - VERIFICAR VARIACIÓN !!
GSA.L0 = 0;
GSA.L = [];   % ODE45 time stepping
% GSA.costs = costs;    % vector of costs

% Sizing the output vectors
Y = zeros(np,1);
YR = zeros(np,1);
Yp = zeros(np,nd);
YTp = zeros(np,nd);

for sample = 1:np
    %GSA.moBi = M1(sample,1);
    GSA.H2Bi = M1(sample,1);
    GSA.mso = M1(sample,2);
    GSA.dso = M1(sample,3);
    GSA.Tgi = M1(sample,4);
    GSA.P = M1(sample,5);
    GSA.D1 = M1(sample,6);
    GSA.D2 = M1(sample,7);
    GSA.Ts = M1(sample,8);
    GSA.Lfin = M1(sample,9);
    
    Y(sample) = inputRCU_2(GSA);
    
    while (isnan(Y(sample)) && (repo<=np))
        repo = repo+1;
        %GSA.moBi = M3(repo,1);
        GSA.H2Bi = M3(repo,1);
        GSA.mso = M3(repo,2);
        GSA.dso = M3(repo,3);
        GSA.Tgi = M3(repo,4);
        GSA.P = M3(repo,5);
        GSA.D1 = M3(repo,6);
        GSA.D2 = M3(repo,7);
        GSA.Ts = M3(repo,8);
        GSA.Lfin = M3(repo,9);
        
        Y(sample) = inputRCU_2(GSA);
        if ~isnan(Y(sample))
            M1(sample,:) = M3(repo,:);
        end
    end

end

fprintf('\n The first random Matrix with all samples is executed\n');

for sample=1:np %sample size
    %GSA.moBi = M2(sample,1);
    GSA.H2Bi = M2(sample,1);
    GSA.mso = M2(sample,2);
    GSA.dso = M2(sample,3);
    GSA.Tgi = M2(sample,4);
    GSA.P = M2(sample,5);
    GSA.D1 = M2(sample,6);
    GSA.D2 = M2(sample,7);
    GSA.Ts = M2(sample,8);
    GSA.Lfin = M2(sample,9);
    
    YR(sample) = inputRCU_2(GSA);
    
    while (isnan(YR(sample)) && (repo<=np))
        repo = repo+1;
        %GSA.moBi = M3(repo,1);
        GSA.H2Bi = M3(repo,1);
        GSA.mso = M3(repo,2);
        GSA.dso = M3(repo,3);
        GSA.Tgi = M3(repo,4);
        GSA.P = M3(repo,5);
        GSA.D1 = M3(repo,6);
        GSA.D2 = M3(repo,7);
        GSA.Ts = M3(repo,8);
        GSA.Lfin = M3(repo,9);
        
        YR(sample) = inputRCU_2(GSA);
        if ~isnan(YR(sample))
            M2(sample,:) = M3(repo,:);
        end
    end
    
end

% over2np = 0.5/np;
% f0 = over2np .* (sum(YR) + sum(Y));
% Variance = over2np .* (sum(Y.^2) + sum(YR.^2)) - f0.^2;

f0 = 0.5 .* (mean(YR) + mean(Y));
Variance = 1/(2*np) .* (sum(Y.^2) + sum(YR.^2)) - f0.^2;

fprintf('\n The second random Matrix with all samples is executed\n');

repo2=0;

for i=1:nd %variables or parameters in sensitivity analysis
    
    N = M2;
    N(:,i) = M1(:,i);
    NT = M1;
    NT(:,i) = M2 (:,i);
    
    for sample = 1:np % number of samples
        
        %GSA.moBi = N(sample,1);
        GSA.H2Bi = N(sample,1);
        GSA.mso = N(sample,2);
        GSA.dso = N(sample,3);
        GSA.Tgi = N(sample,4);
        GSA.P = N(sample,5);
        GSA.D1 = N(sample,6);
        GSA.D2 = N(sample,7);
        GSA.Ts = N(sample,8);
        GSA.Lfin = N(sample,9);
      
        Yp(sample,i) = inputRCU_2(GSA);
        while isnan(Yp(sample,i))
            repo2 = repo2+1;
            Yp(sample,i) = f0;
        end
                
        %GSA.moBi = NT(sample,1);
        GSA.H2Bi = NT(sample,1);
        GSA.mso = NT(sample,2);
        GSA.dso = NT(sample,3);
        GSA.Tgi = NT(sample,4);
        GSA.P = NT(sample,5);
        GSA.D1 = NT(sample,6);
        GSA.D2 = NT(sample,7);
        GSA.Ts = NT(sample,8);
        GSA.Lfin = NT(sample,9);
        
        YTp(sample,i) = inputRCU_2(GSA);
        while isnan(YTp(sample,i))
            repo2 = repo2+1;
            YTp(sample,i) = f0;
        end
       
        %fprintf('\n iteration %f\n Sample %f\n',i,sample);

    end
    
end

% Estas son las cuentas verificadas en los papers
% Verificar calculos de V y Vp. Y su correspondencia
% con el First y Total index.
%
% gama2 = over2np * (sum(Y.*YR) + sum(Yp .* YTp))';
% 
% V = over2np .* (Yp'*Y+ YTp'*YR);    % V_{-p}
% Vp = over2np .* (YTp'*Y + Yp'*YR);  % V_{p}
% 
% s = (V - f0.^2)/Variance;
% st = 1 - (Vp - f0.^2)/Variance;
% 
% sHS = (Vp - gama2)/Variance;
% stHS = 1 - (V - gama2)/Variance;

gama2 = 1/(2 .* np) * (sum(Y.*YR) + sum(Yp .* YTp))';

V = 1/(2 .* np) .* (Yp'*Y+ YTp'*YR);
Vp = 1/(2 .* np) .* (YTp'*Y + Yp'*YR);

s = (V - f0.^2)/Variance;
st = 1 - (Vp - f0.^2)/Variance;

sHS = (V - gama2)/Variance;
stHS = 1 - (Vp - gama2)/Variance;

figure()
subplot(2,1,1);
bar(s, 'b')
title('First sensitivity indices (HS)')
subplot(2,1,2);
bar(st, 'g')
title('Total sensitivity indices (HS)')

figure()
subplot(2,1,1);
bar(sHS, 'b')
title('First sensitivity indices (Wu)')
subplot(2,1,2);
bar(stHS, 'g')
title('Total sensitivity indices (Wu)')

t1 = toc;

