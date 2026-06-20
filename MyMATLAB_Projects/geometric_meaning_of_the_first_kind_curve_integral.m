% 第一型曲线积分（曲面墙）高级可视化代码
clear; clc; close all;

% ================= 设置高颜值图形窗口 =================
fig = figure('Name', '第一型曲线积分几何意义', 'Color', 'w', 'Position', [150, 150, 900, 700]);
% 设置视角和坐标轴样式
axes('Parent', fig, 'NextPlot', 'add', 'View', [-40, 35], 'GridLineStyle', ':', 'GridAlpha', 0.5);
grid on;

% ================= 1. 定义几何元素 =================
% 定义底面曲线 L 的参数方程 (这里用一个有点弧度的S型曲线，视觉效果更好)
t = linspace(-2.5, 2.5, 200); 
x_L = t;                  
y_L = sin(1.2 * t); 

% 定义上方曲面 z = f(x,y) (造一个有高低起伏的漂亮曲面)
f = @(x, y) 3.5 + 0.8*cos(x) .* sin(y) - 0.1*x.^2; 

% 计算顶端贴合在曲面上的曲线高度
z_L_top = f(x_L, y_L); 

% ================= 2. 绘制顶部半透明曲面 =================
[X_grid, Y_grid] = meshgrid(linspace(-3, 3, 100), linspace(-1.5, 1.5, 100));
Z_grid = f(X_grid, Y_grid);
surf1 = surf(X_grid, Y_grid, Z_grid);
surf1.EdgeColor = 'none';     % 隐藏网格线，使其更平滑
surf1.FaceAlpha = 0.5;        % 设置半透明度
colormap(turbo);              % 使用对比度更好、更现代的 turbo 色谱

% ================= 3. 绘制中间的积分"柱面墙" =================
v = linspace(0, 1, 60); % 垂直方向的插值
[T, V] = meshgrid(t, v);
X_wall = T;
Y_wall = sin(1.2 * T);
Z_wall = V .* f(X_wall, Y_wall); % 从 z=0 拉伸到 z=f(x,y)

surf2 = surf(X_wall, Y_wall, Z_wall);
surf2.EdgeColor = 'none';
surf2.FaceColor = [0.55 0.6 0.65]; % 使用高级冷灰色作为墙面
surf2.FaceAlpha = 0.85;            % 墙面透明度调高一点，增加厚重感

% ================= 4. 绘制底面与顶面的边界线 =================
% 底部地面准线 (黑色加粗)
plot3(x_L, y_L, zeros(size(t)), 'k', 'LineWidth', 3.5); 
% 顶部贴合线 (红色加粗，更醒目)
plot3(x_L, y_L, z_L_top, 'r', 'LineWidth', 3); 

% ================= 5. 添加光照与平滑渲染 (核心美化) =================
shading interp;       % 颜色平滑插值过渡
camlight('headlight');% 添加摄像机视角的补光灯
lighting gouraud;     % 采用 Gouraud 光照算法，让模型有真实的立体阴影
material dull;        % 材质设置为哑光，避免过度反光导致看不清

% ================= 6. 标签与排版 =================
xlabel('X 轴', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Y 轴', 'FontSize', 12, 'FontWeight', 'bold');
zlabel('Z 轴 (函数值)', 'FontSize', 12, 'FontWeight', 'bold');
title('第一型曲线积分柱面面积的可视化', 'FontSize', 16, 'FontWeight', 'bold');

% 调整坐标轴字体和粗细
ax = gca;
ax.FontSize = 11;
ax.LineWidth = 1.1;

hold off;