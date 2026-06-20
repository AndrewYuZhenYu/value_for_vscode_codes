% 第一型曲线积分：防漂白·真·三大实体基准平面版
clear; clc; close all;

% ================= 设置图形窗口 =================
fig = figure('Name', '曲线积分对称性', 'Color', 'w', 'Position', [100, 100, 1300, 600]);

% 定义积分曲线 L
t = linspace(0, pi, 150); 
x_L = 2*cos(t);   
y_L = 2*sin(t);   

[X_grid, Y_grid] = meshgrid(linspace(-2.5, 2.5, 60), linspace(0, 2.5, 60));

% ================= 左图：奇函数对称性 =================
subplot(1, 2, 1); hold on; grid on; view(-35, 30);
f_odd = @(x, y) x; 

% 【核心修复】：强制关闭基准面的反光 ('FaceLighting', 'none')，提高不透明度
% 1. 深灰色地板 (Z=0)
fill3([-2.5 2.5 2.5 -2.5], [0 0 2.5 2.5], [0 0 0 0], [0.4 0.4 0.4], 'FaceAlpha', 0.6, 'FaceLighting', 'none', 'EdgeColor', 'k', 'LineWidth', 1.5);
% 2. 深蓝色侧墙/对称面 (X=0)
fill3([0 0 0 0], [0 2.5 2.5 0], [-2.5 -2.5 2.5 2.5], [0.1 0.3 0.8], 'FaceAlpha', 0.65, 'FaceLighting', 'none', 'EdgeColor', 'b', 'LineWidth', 1.5);
% 3. 深红色背墙 (Y=0)
fill3([-2.5 2.5 2.5 -2.5], [0 0 0 0], [-2.5 -2.5 2.5 2.5], [0.8 0.2 0.2], 'FaceAlpha', 0.6, 'FaceLighting', 'none', 'EdgeColor', 'r', 'LineWidth', 1.5);

% 绘制上方曲面和积分墙
surf(X_grid, Y_grid, f_odd(X_grid, Y_grid), 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'FaceColor', [0.5 0.5 0.5]);
v = linspace(0, 1, 40); 
[T_wall, V_wall] = meshgrid(t, v);
X_wall = 2*cos(T_wall); Y_wall = 2*sin(T_wall);
Z_wall_odd = V_wall .* f_odd(X_wall, Y_wall);
surf_odd = surf(X_wall, Y_wall, Z_wall_odd, Z_wall_odd);
surf_odd.EdgeColor = 'none'; surf_odd.FaceAlpha = 0.95;
colormap(gca, turbo); clim([-2 2]);         

% 绘制曲线
plot3(x_L, y_L, zeros(size(t)), 'k', 'LineWidth', 4);
plot3(x_L, y_L, f_odd(x_L, y_L), 'r', 'LineWidth', 3);

shading interp; camlight('headlight'); lighting gouraud;
xlabel('X 轴'); ylabel('Y 轴'); zlabel('Z 轴');
title('奇函数：空间正负体积/面积抵消', 'FontSize', 14, 'FontWeight', 'bold');
axis([-2.5 2.5 0 2.5 -2.5 2.5]);


% ================= 右图：偶函数对称性 =================
subplot(1, 2, 2); hold on; grid on; view(-35, 30);
f_even = @(x, y) 0.5*x.^2 + 1; 

% 【核心修复】：同样处理右图的基准面
% 1. 深灰色地板 (Z=0)
fill3([-2.5 2.5 2.5 -2.5], [0 0 2.5 2.5], [0 0 0 0], [0.4 0.4 0.4], 'FaceAlpha', 0.6, 'FaceLighting', 'none', 'EdgeColor', 'k', 'LineWidth', 1.5);
% 2. 深蓝色侧墙/对称面 (X=0)
fill3([0 0 0 0], [0 2.5 2.5 0], [0 0 5 5], [0.1 0.3 0.8], 'FaceAlpha', 0.65, 'FaceLighting', 'none', 'EdgeColor', 'b', 'LineWidth', 1.5);
% 3. 深红色背墙 (Y=0)
fill3([-2.5 2.5 2.5 -2.5], [0 0 0 0], [0 0 5 5], [0.8 0.2 0.2], 'FaceAlp·ha', 0.6, 'FaceLighting', 'none', 'EdgeColor', 'r', 'LineWidth', 1.5);

% 绘制上方曲面和积分墙
surf(X_grid, Y_grid, f_even(X_grid, Y_grid), 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'FaceColor', [0.5 0.5 0.5]);
Z_wall_even = V_wall .* f_even(X_wall, Y_wall);
surf_even = surf(X_wall, Y_wall, Z_wall_even, Z_wall_even);
surf_even.EdgeColor = 'none'; surf_even.FaceAlpha = 0.95;
colormap(gca, parula); 

% 绘制曲线 (包含绿色高亮一半)
plot3(x_L, y_L, zeros(size(t)), 'k', 'LineWidth', 4);
t_half = linspace(0, pi/2, 75); 
plot3(2*cos(t_half), 2*sin(t_half), zeros(size(t_half)), 'g', 'LineWidth', 5); 
plot3(x_L, y_L, f_even(x_L, y_L), 'r', 'LineWidth', 3);

shading interp; camlight('headlight'); lighting gouraud;
xlabel('X 轴'); ylabel('Y 轴'); zlabel('Z 轴');
title('偶函数：沿深蓝对称面镜像翻倍', 'FontSize', 14, 'FontWeight', 'bold');
axis([-2.5 2.5 0 2.5 0 5]);

sgtitle('真·三大显色实体基准平面 (修复光照漂白)', 'FontSize', 18, 'FontWeight', 'bold', 'Color', [0.2 0.2 0.2]);