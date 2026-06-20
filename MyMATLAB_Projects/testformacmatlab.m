% 剥离所有光影特效，绝对强制显色版
clear; clc; close all;

figure('Name', '曲线积分对称性', 'Color', 'w', 'Position', [100, 100, 1200, 550]);

% 基础数据
t = linspace(0, pi, 150); 
x_L = 2*cos(t);   
y_L = 2*sin(t);   
v = linspace(0, 1, 40); 
[T_wall, V_wall] = meshgrid(t, v);
X_wall = 2*cos(T_wall); 
Y_wall = 2*sin(T_wall);

% ================= 左图：奇函数 =================
subplot(1, 2, 1); hold on; grid on; view(-35, 30);
f_odd = @(x, y) x; 

% 【暴力涂色：没有任何光照干扰的纯色块】
% 1. X=0 平面 (深蓝)
fill3([0 0 0 0], [0 2.5 2.5 0], [-2.5 -2.5 2.5 2.5], [0 0 0.8], 'FaceAlpha', 0.5);
% 2. Y=0 平面 (深红)
fill3([-2.5 2.5 2.5 -2.5], [0 0 0 0], [-2.5 -2.5 2.5 2.5], [0.8 0 0], 'FaceAlpha', 0.5);
% 3. Z=0 平面 (深灰)
fill3([-2.5 2.5 2.5 -2.5], [0 0 2.5 2.5], [0 0 0 0], [0.5 0.5 0.5], 'FaceAlpha', 0.5);

% 面积墙
Z_wall_odd = V_wall .* f_odd(X_wall, Y_wall);
surf(X_wall, Y_wall, Z_wall_odd, Z_wall_odd, 'EdgeColor', 'none', 'FaceAlpha', 0.9);
colormap(gca, turbo); 

% 曲线
plot3(x_L, y_L, zeros(size(t)), 'k', 'LineWidth', 3);
plot3(x_L, y_L, f_odd(x_L, y_L), 'r', 'LineWidth', 3);

xlabel('X 轴'); ylabel('Y 轴'); zlabel('Z 轴');
title('奇函数对称');
axis([-2.5 2.5 0 2.5 -2.5 2.5]); 


% ================= 右图：偶函数 =================
subplot(1, 2, 2); hold on; grid on; view(-35, 30);
f_even = @(x, y) 0.5*x.^2 + 1; 

% 【暴力涂色：没有任何光照干扰的纯色块】
% 1. X=0 平面 (深蓝)
fill3([0 0 0 0], [0 2.5 2.5 0], [0 0 5 5], [0 0 0.8], 'FaceAlpha', 0.5);
% 2. Y=0 平面 (深红)
fill3([-2.5 2.5 2.5 -2.5], [0 0 0 0], [0 0 5 5], [0.8 0 0], 'FaceAlpha', 0.5);
% 3. Z=0 平面 (深灰)
fill3([-2.5 2.5 2.5 -2.5], [0 0 2.5 2.5], [0 0 0 0], [0.5 0.5 0.5], 'FaceAlpha', 0.5);

% 面积墙
Z_wall_even = V_wall .* f_even(X_wall, Y_wall);
surf(X_wall, Y_wall, Z_wall_even, Z_wall_even, 'EdgeColor', 'none', 'FaceAlpha', 0.9);
colormap(gca, parula); 

% 曲线
plot3(x_L, y_L, zeros(size(t)), 'k', 'LineWidth', 3);
t_half = linspace(0, pi/2, 75); 
plot3(2*cos(t_half), 2*sin(t_half), zeros(size(t_half)), 'g', 'LineWidth', 4); 
plot3(x_L, y_L, f_even(x_L, y_L), 'r', 'LineWidth', 3);

xlabel('X 轴'); ylabel('Y 轴'); zlabel('Z 轴');
title('偶函数对称');
axis([-2.5 2.5 0 2.5 0 5]); 

sgtitle('暴力显色版：X=0(蓝), Y=0(红), Z=0(灰)', 'FontSize', 16, 'FontWeight', 'bold');