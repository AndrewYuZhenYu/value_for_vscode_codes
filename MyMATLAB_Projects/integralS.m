% =========================================================================
% 六大积分几何意义可视化对比 (高精度科研绘图版 - 修复LaTeX版)
% =========================================================================

% 初始化与窗口设置
close all; clear; clc;
fig = figure('Name', '六大积分可视化对比', 'Position', [100, 100, 1600, 900], 'Color', 'w');
t = tiledlayout(2, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
sgtitle('微积分：六大积分几何与物理意义对比', 'FontSize', 22, 'FontWeight', 'bold');

colormap(turbo); % 采用色彩鲜艳的 turbo 色带

%% 1. 二重积分 (Double Integral)
nexttile; hold on;
[X1, Y1] = meshgrid(linspace(-2, 2, 50));
Z1 = exp(-(X1.^2 + Y1.^2)/2) * 2; 
surf(X1, Y1, Z1, 'EdgeColor', 'none', 'FaceAlpha', 0.8);
surf(X1, Y1, zeros(size(Z1)), 'FaceColor', [0.8 0.8 0.8], 'EdgeColor', 'none', 'FaceAlpha', 0.5);
title('二重积分 (投影体积)', 'FontSize', 15);
% 使用 \int \!\! \int 替代 \iint
subtitle('$$\int \!\! \int_D f(x,y) dA$$', 'Interpreter', 'latex', 'FontSize', 14);
apply_research_style();

%% 2. 第一类曲线积分 (Line Integral of Scalar Field)
nexttile; hold on;
t_val = linspace(0, 4*pi, 100);
x2 = cos(t_val); y2 = sin(t_val); 
z2 = 0.5 + t_val/10; 
surf([x2; x2], [y2; y2], [zeros(1, 100); z2], [z2; z2], 'EdgeColor', 'none', 'FaceAlpha', 0.9);
plot3(x2, y2, zeros(1,100), 'k-', 'LineWidth', 2.5); 
plot3(x2, y2, z2, 'r-', 'LineWidth', 2.5);           
title('第一类曲线积分 (篱笆面积)', 'FontSize', 15);
subtitle('$$\int_C f(x,y) ds$$', 'Interpreter', 'latex', 'FontSize', 14);
apply_research_style();

%% 3. 第二类曲线积分 (Line Integral of Vector Field)
nexttile; hold on;
[X3, Y3] = meshgrid(linspace(-2, 2, 15));
U3 = -Y3; V3 = X3; 
quiver(X3, Y3, U3, V3, 1.5, 'color', [0.5 0.5 0.5], 'LineWidth', 1); 
theta = linspace(0, pi, 50);
x_c = 1.5*cos(theta); y_c = 1.5*sin(theta);
plot(x_c, y_c, 'r-', 'LineWidth', 3); 
quiver(x_c(25), y_c(25), x_c(26)-x_c(25), y_c(26)-y_c(25), 0, 'r', 'MaxHeadSize', 5, 'LineWidth', 3);
title('第二类曲线积分 (向量场做功)', 'FontSize', 15);
subtitle('$$\int_C \vec{F} \cdot d\vec{r}$$', 'Interpreter', 'latex', 'FontSize', 14);
axis tight; grid on; set(gca, 'LineWidth', 1.2, 'FontSize', 12, 'Box', 'off');
view(2); 

%% 4. 第一类曲面积分 (Surface Integral of Scalar Field)
nexttile; hold on;
[U4, V4] = meshgrid(linspace(0, 2*pi, 60), linspace(0, pi, 60));
X4 = sin(V4).*cos(U4); Y4 = sin(V4).*sin(U4); Z4 = cos(V4); 
ScalarField = X4.^2 + Y4.^2; 
surf(X4, Y4, Z4, ScalarField, 'EdgeColor', 'none', 'FaceAlpha', 0.9);
title('第一类曲面积分 (面密度分布)', 'FontSize', 15);
% 使用 \int \!\! \int 替代 \iint
subtitle('$$\int \!\! \int_{\Sigma} f(x,y,z) dS$$', 'Interpreter', 'latex', 'FontSize', 14);
apply_research_style();

%% 5. 第二类曲面积分 (Surface Integral of Vector Field)
nexttile; hold on;
[X5, Y5] = meshgrid(linspace(-1.5, 1.5, 20));
Z5 = X5.^2 - Y5.^2; 
surf(X5, Y5, Z5, 'FaceColor', 'cyan', 'EdgeColor', 'none', 'FaceAlpha', 0.5);
[U5, V5, W5] = surfnorm(X5, Y5, Z5); 
quiver3(X5, Y5, Z5, U5, V5, W5+1, 0.8, 'r', 'LineWidth', 1.5);
title('第二类曲面积分 (向量场通量)', 'FontSize', 15);
% 使用 \int \!\! \int 替代 \iint
subtitle('$$\int \!\! \int_{\Sigma} \vec{F} \cdot d\vec{S}$$', 'Interpreter', 'latex', 'FontSize', 14);
apply_research_style();

%% 6. 三重积分 (Triple Integral)
nexttile; hold on;
[X6, Y6, Z6] = meshgrid(linspace(-2, 2, 30));
V_data = X6.*exp(-X6.^2 - Y6.^2 - Z6.^2); 
h = slice(X6, Y6, Z6, V_data, [0], [0], [-1, 0, 1]);
set(h, 'EdgeColor', 'none', 'FaceAlpha', 0.8);
title('三重积分 (体密度切片)', 'FontSize', 15);
% 使用 \int \!\! \int \!\! \int 替代 \iiint
subtitle('$$\int \!\! \int \!\! \int_{\Omega} f(x,y,z) dV$$', 'Interpreter', 'latex', 'FontSize', 14);
apply_research_style();

colorbar('Position', [0.93 0.1 0.015 0.8]); 

% =========================================================================
% 局部函数：统一定义渲染样式 (必须放在脚本文件的最末尾)
% =========================================================================
function apply_research_style()
    grid on;
    view(3);
    axis tight;
    set(gca, 'LineWidth', 1.2, 'FontSize', 12, 'TickDir', 'out', 'Box', 'off');
    camlight('headlight');
    lighting gouraud;
    material shiny;
end