% ==========================================
% 常见二次曲面总览 (高亮鲜艳 - 安全无错版)
% ==========================================
clear; clc; close all;
figure('Name', '常见二次曲面总览 - 高亮电光渲染', 'Position', [100, 50, 1200, 1000], 'Color', 'w');

% 设定通用参数
a = 1; b = 1; c = 1; p = 1;
N = 256; % 渐变高分辨率

% ------------------------------------------
% 1. 椭球面 (配色：电光霓虹紫 Cyber Pink)
subplot(3,3,1);
[U, V] = meshgrid(linspace(0, 2*pi, 80), linspace(-pi/2, pi/2, 80));
X = a * cos(V) .* cos(U); Y = b * cos(V) .* sin(U); Z = c * sin(V);
surf(X, Y, Z, Z, 'EdgeColor', 'none'); 
title('1. 椭球面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.4, 1.0, N)', linspace(0.0, 0.2, N)', linspace(0.6, 1.0, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 2. 椭圆抛物面 (配色：放射毒绿 Toxic Green)
subplot(3,3,2);
[R, Theta] = meshgrid(linspace(0, 2, 70), linspace(0, 2*pi, 70));
X = a * R .* cos(Theta); Y = b * R .* sin(Theta); Z = R.^2;
surf(X, Y, Z, Z, 'EdgeColor', 'none');
title('2. 椭圆抛物面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} = z$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.0, 0.2, N)', linspace(0.8, 1.0, N)', linspace(0.1, 0.3, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 3. 双曲抛物面/马鞍面 (配色：熔岩极光 Volcanic Magma)
subplot(3,3,3);
[X_grid, Y_grid] = meshgrid(linspace(-2, 2, 80), linspace(-2, 2, 80));
Z = (X_grid.^2 / a^2) - (Y_grid.^2 / b^2);
surf(X_grid, Y_grid, Z, Z, 'EdgeColor', 'none');
title('3. 双曲抛物面 (马鞍面)', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} - \frac{y^2}{b^2} = z$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.9, 1.0, N)', linspace(0.1, 0.6, N)', linspace(0.0, 0.1, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 4. 单叶双曲面 (配色：星际星云 Interstellar Blue)
subplot(3,3,4);
[U, V] = meshgrid(linspace(0, 2*pi, 70), linspace(-2, 2, 70));
X = a * cosh(V) .* cos(U); Y = b * cosh(V) .* sin(U); Z = c * sinh(V);
surf(X, Y, Z, Z, 'EdgeColor', 'none');
title('4. 单叶双曲面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} - \frac{z^2}{c^2} = 1$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.0, 0.1, N)', linspace(0.4, 0.9, N)', linspace(0.8, 1.0, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 5. 双叶双曲面 (配色：液态水银 Liquid Silver)
subplot(3,3,5);
[U, V] = meshgrid(linspace(0, 2*pi, 60), linspace(0, 1.5, 40));
X1 = a * sinh(V) .* cos(U); Y1 = b * sinh(V) .* sin(U); Z1 = c * cosh(V);
surf(X1, Y1, Z1, Z1, 'EdgeColor', 'none'); hold on;
surf(X1, Y1, -Z1, -Z1, 'EdgeColor', 'none');
title('5. 双叶双曲面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} - \frac{z^2}{c^2} = -1$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.7, 1.0, N)', linspace(0.7, 1.0, N)', linspace(0.7, 1.0, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 6. 椭圆锥面 (配色：太阳耀斑 Solar Flare)
subplot(3,3,6);
[R, Theta] = meshgrid(linspace(-2, 2, 80), linspace(0, 2*pi, 80));
X = a * R .* cos(Theta); Y = b * R .* sin(Theta); Z = c * R;
surf(X, Y, Z, Z, 'EdgeColor', 'none');
title('6. 椭圆锥面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} = \frac{z^2}{c^2}$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(1.0, 1.0, N)', linspace(0.3, 0.9, N)', linspace(0.0, 0.1, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 7. 椭圆柱面 (配色：赛博鲜橙 Cyber Orange)
subplot(3,3,7);
[U, V] = meshgrid(linspace(0, 2*pi, 60), linspace(-2, 2, 60));
X = a * cos(U); Y = b * sin(U); Z = V;
surf(X, Y, Z, Z, 'EdgeColor', 'none');
title('7. 椭圆柱面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(1.0, 1.0, N)', linspace(0.4, 0.8, N)', linspace(0.0, 0.1, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 8. 抛物柱面 (配色：高能等离子 Hyper Plasma)
subplot(3,3,8);
[Y_grid, Z_grid] = meshgrid(linspace(-2, 2, 60), linspace(-2, 2, 60));
X = (Y_grid.^2) / (2*p);
surf(X, Y_grid, Z_grid, X, 'EdgeColor', 'none'); 
title('8. 抛物柱面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$y^2 = 2px$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.8, 0.2, N)', linspace(0.0, 0.8, N)', linspace(0.9, 1.0, N)']; 
format_bright_surface(cmap); 

% ------------------------------------------
% 9. 双曲柱面 (配色：深海极光 Deep Aurora)
subplot(3,3,9);
[V, Z_grid] = meshgrid(linspace(-1.5, 1.5, 50), linspace(-2, 2, 60));
X1 = a * cosh(V); Y1 = b * sinh(V);
surf(X1, Y1, Z_grid, X1, 'EdgeColor', 'none'); hold on;
surf(-X1, Y1, Z_grid, -X1, 'EdgeColor', 'none');
title('9. 双曲柱面', 'FontWeight', 'bold', 'FontSize', 11);
xlabel('$\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$', 'Interpreter', 'latex', 'FontSize', 13);
cmap = [linspace(0.0, 0.1, N)', linspace(0.8, 1.0, N)', linspace(0.6, 0.9, N)']; 
format_bright_surface(cmap); 

% ==========================================
% 辅助函数：通过调整材质反射率，安全实现高级高亮
% ==========================================
function format_bright_surface(rgb_matrix)
    ax = gca;             
    colormap(ax, rgb_matrix); 
    axis equal;            
    grid on;               
    
    ax.GridColor = [0.8 0.8 0.8];
    ax.LineWidth = 0.9;
    ax.Box = 'on';
    view(135, 25);         
    shading interp;        
    
    % 清理旧光源
    delete(findobj(ax, 'Type', 'light')); 
    
    % 【光源修正】使用合法的最大白光 [1 1 1] 
    light('Position', [8, 5, 12], 'Style', 'local', 'Color', [1 1 1]); 
    light('Position', [-5, 8, 5], 'Style', 'local', 'Color', [0.4 0.4 0.4]); 
    
    lighting gouraud;      
    
    % 【核心黑科技提亮】[环境光 漫反射 镜面反射 高光指数]
    % 环境光（Ambient）从 0.4 拔高到 0.55，让没有照到的暗部整体提亮
    % 漫反射（Diffuse）维持 0.65，镜面反射（Specular）拉满到 0.8，高光聚焦度 45
    % 这样可以在合法光源下，最大化激发颜色的鲜艳度和晶莹的局部高光
    material([0.55 0.65 0.8 45]); 
end