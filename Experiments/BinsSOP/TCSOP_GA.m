


%% ================================================================================================================ 
%
% Structured output prediction for predicting transporter protein classification
% Model is based on Max-margin conditional random field.
% Optimization is throught primal, dual, marginized dual representation.
% Optimization algorithm is gradient ascent.
%
% INPUT PARAMETERS:
%   paramsIn:   input parameters
%   dataIn:     input data e.g., kernel and label matrices for training and testing
%
% USAGE:
%   This function is called by a MATLAB wrapper function single_SOP()
%
% Hongyu Su, hongyu.su@me.com
%
%% ================================================================================================================
function TCSOP_GA (paramsIn, dataIn)

    % Set random seed to make different run comparable.
    rand('twister', 0);

    % input data and parameters
    global data;                % input data
    global params;              % input parameters
    data    = dataIn;
    params  = paramsIn;
    clear dataIn paramsIn;      % destroy input parameters to save memory
    
    % other global variables
    global loss;                % loss defined on the edge of the network
    global mu;                  % marginal dual variables
    global ind_edge_val;        % Ye=u
    global Ye;                  % Denotes the edge-labels 1 <-- [-1,-1], 2 <-- [-1,+1], 3 <-- [+1,-1], 4 <-- [+1,+1]
    global m;                   % the number of training instances
    global l;                   % the number of labels
    global ENum;                % the number of edges
    global primal_ub;           % primal upper bound
    global obj;                 % objective
    global delta_obj;           % delta objective
    global Rmu;                 %
    global Smu;                 %
    global profile;             % 
    global opt_round;           %
    global Kxx_mu_x;            %
    global iter;                %   
    global SrcSpc;              % search space in terms of edge labels
    
    % initialize other global variables
    parameter_init;
    
    % initialize profiling function
    profile_init;
    
    % Optimization
    print_message('Model training with gradient ascent ...',0);

    % Compute dualit gap
    compute_duality_gap;

    % compute the profiling statistics before optimization
    profile_update_tr;
       
    % iterate over example untile reaching the iteration limit
    while opt_round < params.maxiter
        
        opt_round = opt_round + 1;
        profile.NUpdt = 0;
        
        % gradient descent on each individual training example
        if opt_round < 0
            for xi=1:m
                gradient_ascent(xi);
            end
        else
            gradient_ascent(1);
        end
        
        % look the the progress at the fix time interval
        if mod(opt_round,params.profileiter) == 0
            compute_duality_gap;
            profile_update_tr;
        end
        
    end % while

    profile_update_ts;
    
end

%%
function gradient_ascent(xi)

    global loss;
    global ENum;
    global m;
    global mu;
    global delta_obj;
    global params;
    global Ye;
    global Kxx_mu_x;
    global Smu;
    global Rmu;
    global ind_edge_val;
    global obj;
    global profile;
    global opt_round;
        
    loss_size = size(loss);
    loss      = reshape(loss, 4*ENum,m);
    
    Kmu_x    = compute_Kmu_x;
    
    gradient = loss-Kmu_x;
    
    Gcur = sum(-mu.*gradient);

    [~,~,Umax,Gmax] = compute_best_multilabel(gradient);
    
    Gmax = Gmax*params.C;
    
    % select mini batch to update
    I = [1:m]';                         % all training examples will be updated
    
    if sum(Gmax(I)) < sum(Gcur(I))
        return
    end
    
    mu_0 = Umax(:,I) * params.C;        % feasible solution
    mu_d = mu_0 - mu(:,I);              % update direction
    
    smu_1_te = sum(reshape(mu_0.*Ye(:,I),4,ENum*size(I,1)));
    smu_1_te = reshape(smu_1_te(ones(4,1),:),ENum*4,size(I,1));
    Kxx_mu_0 = ~Ye(:,I)*params.C + mu_0 - smu_1_te;
    
    Kmu_0    = Kmu_x(:,I) + Kxx_mu_0 - Kxx_mu_x(:,I);
    Kmu_d    = Kmu_0 - Kmu_x(:,I);
    
    % exact line search
    %nomi   = sum( mu_d .* gradient(:,I) );
    %denomi = sum( mu_d .* Kmu_d );
    %tau    = min(sum(nomi)/sum(denomi),0.1);

    % fixed step size
    %tau = params.stepSize1/(params.stepSize1+params.C/params.stepSize2*opt_round);
    tau = 1/( 1 + ceil(opt_round/params.stepSize1) * params.C / params.stepSize2);

    if tau < 0
        return
    end
   
    delta_obj = sum(sum( tau * mu_d .* gradient(:,I) - tau^2/2 * mu_d .* Kmu_d ));

    if delta_obj < 0 | tau < 0
        return
    end
  
    mu(:,I)  = mu(:,I) + tau*mu_d;
        
    obj = obj + delta_obj;
    
    Kxx_mu_x(:,I) = (1-tau)*Kxx_mu_x(:,I) + tau*Kxx_mu_0;
   
    % update Smu and Rmu
    mu = reshape(mu,4,ENum*m);
    for u=1:4
        Smu{u} = reshape(sum(mu),ENum,m).*ind_edge_val{u};
        Rmu{u} = reshape(mu(u,:),ENum,m);
    end
    mu = reshape(mu,ENum*4,m);
%     mu_x = reshape(mu(:,xi),4,ENum);
%     for u = 1:4
%         Smu{u}(:,xi) = (sum(mu_x)').*ind_edge_val{u}(:,xi);
%         Rmu{u}(:,xi) = mu_x(u,:)';
%     end

    % reshape loss
    loss = reshape(loss,loss_size);
    profile.NUpdt = sum(Gmax>=Gcur');
   
end

%% need to be checked, on training data
function Kmu_x = compute_Kmu_x(xi)
    
    global ind_edge_val;
    global ENum;
    global data;
    global Smu;
    global Rmu;
    global m;

    if nargin == 1
        term12 = zeros(1,ENum);
        term34 = zeros(4,ENum);

        for u=1:4
            H_u = Smu{u}*data.Ktr(:,xi)-Rmu{u}*data.Ktr(:,xi);
            term12(1,ind_edge_val{u}(:,xi)) = H_u(ind_edge_val{u}(:,xi))';
            term34(u,:) = -H_u';
        end
        Kmu_x = reshape(term12(ones(4,1),:) + term34,4*ENum,1);
    else
        term12 = zeros(ENum,m);
        term34 = zeros(4,ENum*m);

        for u=1:4
            H_u = Smu{u}*data.Ktr-Rmu{u}*data.Ktr;
            term12(ind_edge_val{u}) = H_u(ind_edge_val{u});
            term34(u,:) = reshape(-H_u,1,ENum*m);
        end
        term12 = reshape(term12,1,ENum*m);
        Kmu_x = reshape(term12(ones(4,1),:) + term34,4*ENum,m);
    end
end



function gradient_ascent_old(xi)

    global loss;
    global ENum;
    global m;
    global mu;
    global delta_obj;
    global params;
    global Ye;
    global Kxx_mu_x;
    global Smu;
    global Rmu;
    global ind_edge_val;
    global obj;
    global opt_round;
    global profile;
    
    loss_size = size(loss);
    loss      = reshape(loss, 4*ENum,m);
    
    Kmu_x = compute_Kmu_x(xi);

    gradient_x  = loss(:,xi)-Kmu_x;
    
    Gcur = -mu(:,xi)'*gradient_x;

    [~,~,Umax,Gmax] = compute_best_multilabel(gradient_x);
    
    Gmax = Gmax*params.C;
    
    
    if Gmax < Gcur
        return
    end

    mu_0 = Umax * params.C;  % feasible solution
    mu_d = mu_0 - mu(:,xi);  % update direction
    
    
    smu_1_te = sum(reshape(mu_0.*Ye(:,xi),4,ENum),1);
    smu_1_te = reshape(smu_1_te(ones(4,1),:),numel(mu(:,xi)),1);
    Kxx_mu_0 = ~Ye(:,xi)*params.C+mu_0-smu_1_te;
    Kmu_0    = Kmu_x + Kxx_mu_0 - Kxx_mu_x(:,xi);
    Kmu_d    = Kmu_0 - Kmu_x;

    % exact line search
    nomi   = mu_d'  * gradient_x;
    denomi = Kmu_d' * mu_d;
    tau    = min(nomi/denomi,1);

    if tau < 0
        return
    end
   
    delta_obj = mu_d'*gradient_x*tau - tau^2/2*mu_d'*Kmu_d;
   
    [tau,delta_obj]
    
    if xi==2
        asdfasd
    end
    if delta_obj < 0 || tau < 0
        return
    end
  
    mu(:,xi) = mu(:,xi) + tau*mu_d;
        
    obj = obj + delta_obj;
    
    Kxx_mu_x(:,xi) = (1-tau)*Kxx_mu_x(:,xi) + tau*Kxx_mu_0;
   
    % update Smu and Rmu
    mu_x = reshape(mu(:,xi),4,ENum);
    for u = 1:4
        Smu{u}(:,xi) = (sum(mu_x)').*ind_edge_val{u}(:,xi);
        Rmu{u}(:,xi) = mu_x(u,:)';
    end

    % reshape loss
    loss = reshape(loss,loss_size);
    profile.NUpdt = profile.NUpdt + 1;

end

%% need to be checked
function w_phi_e = compute_w_phi_e(Kx)

    global m;
    global mu;
    global Ye;
    global opt_round;
    global ENum;

    Ye_size = size(Ye);
    mu_siz  = size(mu);
    Ye      = reshape(Ye,4,ENum*m);   
    mu      = reshape(mu,4,ENum*m);
    
    m_oup = size(Kx,2);

    if opt_round == 0
        w_phi_e = zeros(4,ENum*m_oup);
    else
        w_phi_e = sum(mu);
        w_phi_e = w_phi_e(ones(4,1),:);
        w_phi_e = Ye.*w_phi_e;
        w_phi_e = w_phi_e-mu;
        w_phi_e = reshape(w_phi_e,4*ENum,m);
        w_phi_e = w_phi_e*Kx;
        w_phi_e = reshape(w_phi_e,4,ENum*m_oup);
    end
    
    mu = reshape(mu,mu_siz);
    Ye = reshape(Ye,Ye_size);
    
end

%%
function [Ypred,YpredVal] = predicting(Y,K)

    global opt_round;
    
    if opt_round == 0
        Ypred = -1*ones(size(Y));
        YpredVal = Ypred*0;
    else
        w_phi_e = compute_w_phi_e(K);
        [Ypred,YpredVal,~,~] = compute_best_multilabel(w_phi_e);
    end
    
end

%% Profile during training
function profile_update_tr

    global params;
    global profile;
    global obj;
    global opt_round;
    global data;
    global m;
    global l;
    global duality_gap;
    global primal_ub;
    
    % remember error from last time
    profile.n_err_microlabel_prev = profile.n_err_microlabel;

    % compute prediction on training
    [Ytr,~] = predicting(data.Ytr,data.Ktr);

    % compute training error
    profile.microlabel_errors   = sum(abs(Ytr-data.Ytr) >0,2);
    profile.n_err_microlabel    = sum(profile.microlabel_errors);
    profile.p_err_microlabel    = profile.n_err_microlabel/m/l;
    profile.n_err               = sum(profile.microlabel_errors > 0);
    profile.p_err               = profile.n_err/m;

    % print message
    print_message(...
        sprintf('iter: %d 1_tr: %d %3.2f %% h_tr: %d %3.2f %% obj: %3.2f gap: %.2f %% updt %d %.2f %% ',...
        opt_round,...
        profile.n_err,...
        profile.p_err*100,...
        profile.n_err_microlabel,...
        profile.p_err_microlabel*100,...
        obj,...
        duality_gap/primal_ub*100,...
        profile.NUpdt,...
        profile.NUpdt/m*100),...
        0,sprintf('%s',params.logFilename));

end

%% Profile after optimization --> prediction
function profile_update_ts

    global params;
    global profile;
    global obj;
    global opt_round;
    global data;
    global l;
    global duality_gap;
    global primal_ub;
    global mu;
    
    % remember error from last time
    profile.n_err_microlabel_prev = profile.n_err_microlabel;

    % compute prediction on training
    [Yts,YtsVal] = predicting(data.Yts,data.Kts);

    % compute training error
    profile.microlabel_errors   = sum(abs(Yts-data.Yts) >0,2);
    profile.n_err_microlabel    = sum(profile.microlabel_errors);
    profile.p_err_microlabel    = profile.n_err_microlabel/size(data.Yts,1)/l;
    profile.n_err               = sum(profile.microlabel_errors > 0);
    profile.p_err               = profile.n_err/size(data.Yts,1);

    % print message
    print_message(...
        sprintf('iter: %d 1_ts: %d %3.2f %% h_ts: %d %3.2f %% obj: %3.2f gap: %.2f %%',...
        opt_round,...
        profile.n_err,...
        profile.p_err*100,...
        profile.n_err_microlabel,...
        profile.p_err_microlabel*100,...
        obj,...
        duality_gap/primal_ub*100),...
        0,sprintf('%s',params.logFilename));

    running_time = [params.foldIndex, cputime-profile.start_time];
    Yts          = [params.exampleIndex,Yts];
    YtsVal       = [params.exampleIndex,YtsVal];
    test_err     = [profile.p_err, profile.p_err_microlabel];
    save(params.outputFilename, 'test_err',  'Yts', 'YtsVal', 'params', 'running_time', 'mu')
    
end

%% Compute best multilabel based on current gradient
function [Ymax,YmaxVal,Umax,Gmax] = compute_best_multilabel (gradient)

    global data;
    global ENum;
    global SrcSpc;
    global opt_round;
    
    gradient        = reshape(gradient,4*ENum,numel(gradient)/4/ENum);
    [Gmax,YmaxInd]  = max(gradient'*SrcSpc,[],2);   % Gmax is in mx1, YmaxInd is in mx1
    Ymax            = data.S(YmaxInd,:);
    Umax            = SrcSpc(:,YmaxInd);
    YmaxVal         = Ymax;
    
end

%% function to compute duality gap
function compute_duality_gap

    % global parameters
    global duality_gap;
    global loss;
    global params;
    global mu;
    global primal_ub;
    global obj;
    global m;
    global Kmu;
    global ENum;
    
    % compute the score of the best multilabel
    loss_size   = size(loss);
    mu_size     = size(mu);
    Kmu_size    = size(Kmu);
    loss        = reshape(loss,4,ENum*m);
    mu          = reshape(mu,4,ENum*m);
    Kmu         = reshape(Kmu,4,ENum*m);
    gradient    = loss - Kmu;
    [~,~,~,Gmax] = compute_best_multilabel(gradient);
    
    % compute duality gap for all examples in the training set
    Gmax        = sum(params.C*Gmax);
    Gcur        = reshape(gradient,1,4*ENum*m) * reshape(mu,4*ENum*m,1);
    duality_gap = Gmax - Gcur;
    
    % compute primal upper bound
    primal_ub = obj + duality_gap;
    
    loss = reshape(loss,loss_size);
    mu   = reshape(mu,mu_size);
    Kmu  = reshape(Kmu,Kmu_size);
    
end

%% initialize parameters
function parameter_init()
    global data;
    global m;
    global l;
    global ENum;
    global loss;
    global Ye;
    global ind_edge_val;
    global mu;
    global Kxx_mu_x;
    global Rmu;
    global Smu;
    global obj;
    global delta_obj;
    global primal_ub;
    global opt_round;
    global Kmu;
    global SrcSpc;
    global params;
        
    l   = size(data.Ytr,2);   
    
    m   = size(data.Ktr,1);   
    
    ENum = size(data.E,1);
    
    loss = ones(4, m*ENum);
    Te1 = data.Ytr(:,data.E(:,1))';
    Te2 = data.Ytr(:,data.E(:,2))';
    u = 0;
    for u_1 = [-1, 1]
        for u_2 = [-1, 1]
            u = u + 1;
            loss(u,:) = reshape((Te1 ~= u_1)+(Te2 ~= u_2),m*ENum,1);
        end
    end
    
    SrcSpc = ones(4,size(data.S,1)*ENum);
    Te1 = data.S(:,data.E(:,1))';
    Te2 = data.S(:,data.E(:,2))';
    u = 0;
    for u_1 = [-1, 1]
        for u_2 = [-1, 1]
            u = u + 1;
            SrcSpc(u,:) = reshape((Te1 == u_1 & Te2 == u_2),size(data.S,1)*ENum,1);
        end
    end
    SrcSpc = reshape(SrcSpc,4*ENum,size(data.S,1));
    
    Ye = reshape(loss==0,4,ENum*m);
    for u = 1:4
        ind_edge_val{u} = reshape(Ye(u,:)~=0,ENum,m);
    end
    Ye = reshape(Ye,4*ENum,m);
    
    mu = zeros(4*ENum,m);
    
    Kxx_mu_x = zeros(4*ENum,m);
    
    Rmu = cell(1,4);
    Smu = cell(1,4);
    for u=1:4
        Smu{u} = zeros(ENum,m);
        Rmu{u} = zeros(ENum,m);       
    end
    
    obj = 0;
    
    delta_obj = 0;
    
    primal_ub = Inf;
    
    opt_round = 0;
    
    Kxx_mu_x = zeros(4*ENum,m);
    
    Kmu = zeros(numel(mu),1);
    
end

%% Initialize the profiling function
function profile_init

    global profile;
    profile.start_time              = cputime;
    profile.NUpdt                   = 0;
    profile.n_err                   = 0;
    profile.p_err                   = 0; 
    profile.n_err_microlabel        = 0; 
    profile.p_err_microlabel        = 0; 
    profile.n_err_microlabel_prev   = 0;
    profile.microlabel_errors       = [];
    profile.iter                    = 0;
    profile.err_ts                  = 0;
    
end

%% Print out message
function print_message(msg,verbosity_level,filename)

    global params;
    global profile;

    if params.verbosity >= verbosity_level
        fprintf('%.1f: %s \n',cputime-profile.start_time,msg);
        if nargin == 3
            fid = fopen(filename,'a');
            fprintf(fid,'%.1f: %s\n',cputime-profile.start_time,msg);
            fclose(fid);
        end
    end
    
end
