%% 磁矩与磁力矩模型可视化
% Magnetic dipole torque visualization
clear; clc; close all;

%% 参数
mu = 1;       % 磁矩大小
B = 1;        % 磁场大小

theta = 45;   % 当前角度
theta_rad = deg2rad(theta);

%% 创建窗口
figure('Color','w','Position',[100 100 1300 600])


%% ============================
% 1. 磁矩模型
% =============================

subplot(1,2,1)
hold on
grid on
axis equal

% 坐标轴
quiver3(0,0,0,2,0,0,'k','LineWidth',1.5)
quiver3(0,0,0,0,2,0,'k','LineWidth',1.5)
quiver3(0,0,0,0,0,2,'k','LineWidth',1.5)

xlabel('x')
ylabel('y')
zlabel('z')

xlim([-2 2])
ylim([-2 2])
zlim([-1 2])


% 磁场方向 B
quiver3(0,0,0,0,1.6,0,...
    'Color',[0 0.4 1],...
    'LineWidth',4,...
    'MaxHeadSize',0.3)

text(0,1.7,0,'B','FontSize',16)


% 磁矩方向 mu
mu_x = mu*cos(theta_rad);
mu_y = mu*sin(theta_rad);


quiver3(0,0,0,...
    mu_x,mu_y,0,...
    'Color',[1 0 0],...
    'LineWidth',4,...
    'MaxHeadSize',0.4)

text(mu_x,mu_y,0,'\mu',...
    'FontSize',18)


% 力矩方向 tau
tau = cross([mu_x mu_y 0],[0 B 0]);

quiver3(0,0,0,...
    tau(1),tau(2),tau(3),...
    'Color',[0 0.7 0],...
    'LineWidth',4,...
    'MaxHeadSize',0.4)

text(tau(1),tau(2),tau(3),'\tau',...
    'FontSize',18)


title(['磁矩模型  \theta=',num2str(theta),'^\circ'])



%% ============================
% 2. 三种特殊角度
% =============================

subplot(1,2,2)

theta_list=[0 90 180];

tau_list=zeros(size(theta_list));


hold on
grid on


for i=1:length(theta_list)

    th=theta_list(i);

    tau_value=mu*B*sind(th);

    tau_list(i)=tau_value;


end


% 绘制曲线
theta_curve=linspace(0,180,300);

tau_curve=mu*B*sind(theta_curve);


plot(theta_curve,tau_curve,...
    'LineWidth',3)

hold on


% 特殊点
plot(theta_list,tau_list,...
    'ro',...
    'MarkerSize',10,...
    'LineWidth',2)


for i=1:length(theta_list)

    text(theta_list(i),tau_list(i)+0.05,...
        ['\theta=',num2str(theta_list(i)),...
        '^\circ'],...
        'FontSize',12)

end


xlabel('\theta (角度)')
ylabel('\tau=\mu B sin\theta')

title('磁力矩随角度变化')

xlim([0 180])
ylim([-0.2 1.2])



%% 总标题
sgtitle('磁矩在外磁场中的磁力矩模型',...
    'FontSize',18,...
    'FontWeight','bold')