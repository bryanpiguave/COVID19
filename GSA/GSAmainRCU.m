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

%mean_values = [5 0.1 25 2.5E6 554.44 0.2E6 5.12E-2 3.58E-2 1140 6.7];
mean_values = [5 0.3 30 2.5E6 550 0.15E6 4.75E-2 3.65E-2 1140 2];

costs = zeros(10,1);
% Costs asociated with each variable
% costs(1) =  ; % moBi Biomass initial value
% costs(2) =  ; % mBidL
% costs(3) =  ; % mInt1dL
costs(4) = 1; % mTar1dL
% costs(5) =  ; % mChar1dL
% costs(6) =  ; % mgasdL
costs(7) = 6; % mTar2dL
% costs(8) =  ; % mChar2dL
% costs(9) =  ; % maguadL
% costs(10) =  ; % TgdL
% costs(11) =  ; % TsdL


% Uncertainty index
unc = 5; % Measured in percentage

ub1 = mean_values*(1 + unc/100);% 5% up mean
lb1 = mean_values.*(1 - unc/100);% 5% below mean

ub2 = ub1;
lb2 = lb1;

% Dimensions
nd = length(lb1); % determines number of variables considered in sensitivity analysis
np = 1000; %sample size 
nstep = 100; % Discretization of ODE45

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
GSA.U = 400; % Coeficiente global de transferencia de calor ¡¡ GSA - VERIFICAR VARIACIÓN !!
GSA.L0 = 0;
GSA.L = [];   % ODE45 time stepping
GSA.costs = costs;    % vector of costs

% Sizing the output vectors
Y = zeros(np,1);
YR = zeros(np,1);
Yp = zeros(np,nd);
YTp = zeros(np,nd);

for sample = 1:np
    GSA.moBi = M1(sample,1);
    GSA.H2Bi = M1(sample,2);
    %GSA.mhi = GSA.moBi*GSA.H2Bi;  % Calculated inside (not needed!) Flujo másico de hidrógeno (g/s)
    GSA.mso = M1(sample,3);
    GSA.dso = M1(sample,4);
    GSA.Tgi = M1(sample,5);
    GSA.P = M1(sample,6);
    GSA.D1 = M1(sample,7);
    GSA.D2 = M1(sample,8);
    GSA.Ts = M1(sample,9);
    GSA.Lfin = M1(sample,10);
    
    Y(sample) = inputRCU(GSA);
    
    while (isnan(Y(sample)) && (repo<=np))
        repo = repo+1;
        GSA.moBi = M3(repo,1);
        GSA.H2Bi = M3(repo,2);
        GSA.mso = M3(repo,3);
        GSA.dso = M3(repo,4);
        GSA.Tgi = M3(repo,5);
        GSA.P = M3(repo,6);
        GSA.D1 = M3(repo,7);
        GSA.D2 = M3(repo,8);
        GSA.Ts = M3(repo,9);
        GSA.Lfin = M3(repo,10);
        
        Y(sample) = inputRCU(GSA);
        if ~isnan(Y(sample))
            M1(sample,:) = M3(repo,:);
        end
    end

end

fprintf('\n The first random Matrix with all samples is executed\n');

for sample=1:np %sample size
    GSA.moBi = M2(sample,1);
    GSA.H2Bi = M2(sample,2);
    GSA.mso = M2(sample,3);
    GSA.dso = M2(sample,4);
    GSA.Tgi = M2(sample,5);
    GSA.P = M2(sample,6);
    GSA.D1 = M2(sample,7);
    GSA.D2 = M2(sample,8);
    GSA.Ts = M2(sample,9);
    GSA.Lfin = M2(sample,10);
    
    YR(sample) = inputRCU(GSA);
    
    while (isnan(YR(sample)) && (repo<=np))
        repo = repo+1;
        GSA.moBi = M3(repo,1);
        GSA.H2Bi = M3(repo,2);
        GSA.mso = M3(repo,3);
        GSA.dso = M3(repo,4);
        GSA.Tgi = M3(repo,5);
        GSA.P = M3(repo,6);
        GSA.D1 = M3(repo,7);
        GSA.D2 = M3(repo,8);
        GSA.Ts = M3(repo,9);
        GSA.Lfin = M3(repo,10);
        
        YR(sample) = inputRCU(GSA);
        if ~isnan(YR(sample))
            M2(sample,:) = M3(repo,:);
        end
    end
    
end

f0 = 0.5 .* (mean(YR) + mean(Y));
Variance = (0.5 .* 1/np .* (sum(Y.^2) + sum(YR.^2)) - f0.^2);

fprintf('\n The second random Matrix with all samples is executed\n');

repo2=0;

for i=1:nd %variables or parameters in sensitivity analysis
    
    N = M2;
    N(:,i) = M1(:,i);
    NT = M1;
    NT(:,i) = M2 (:,i);
    
    for sample = 1:np
        
        GSA.moBi = N(sample,1);
        GSA.H2Bi = N(sample,2);
        GSA.mso = N(sample,3);
        GSA.dso = N(sample,4);
        GSA.Tgi = N(sample,5);
        GSA.P = N(sample,6);
        GSA.D1 = N(sample,7);
        GSA.D2 = N(sample,8);
        GSA.Ts = N(sample,9);
        GSA.Lfin = N(sample,10);
      
        Yp(sample,i) = inputRCU(GSA);
        while isnan(Yp(sample,i))
            repo2 = repo2+1;
            Yp(sample,i) = f0;
        end
                
        GSA.moBi = NT(sample,1);
        GSA.H2Bi = NT(sample,2);
        GSA.mso = NT(sample,3);
        GSA.dso = NT(sample,4);
        GSA.Tgi = NT(sample,5);
        GSA.P = NT(sample,6);
        GSA.D1 = NT(sample,7);
        GSA.D2 = NT(sample,8);
        GSA.Ts = NT(sample,9);
        GSA.Lfin = NT(sample,10);
        
        YTp(sample,i) = inputRCU(GSA);
        while isnan(YTp(sample,i))
            repo2 = repo2+1;
            YTp(sample,i) = f0;
        end
       
        %fprintf('\n iteration %f\n Sample %f\n',i,sample);

    end
    
end

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
bar(sHS, 'g')
title('Total sensitivity indices (Wu)')

t1 = toc;

