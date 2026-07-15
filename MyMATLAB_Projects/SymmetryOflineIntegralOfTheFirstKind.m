clear; clc; close all;

R = 2;
nPhi = 50;
nTheta = 80;

% 球面网格
phi = linspace(0, pi, nPhi);
theta = linspace(0, 2*pi, nTheta);
[Phi, Theta] = meshgrid(phi, theta);
X = R * sin(Phi) .* cos(Theta);
Y = R * sin(Phi) .* sin(Theta);
Z = R * cos(Phi);

% ========= 修复1：对称平面 维度匹配（30×30矩阵）=========
nPlane = 30;
xp = linspace(-0.05, 0.05, nPlane);
yp = linspace(-R, R, nPlane);
zp = linspace(-R, R, nPlane);
[Xp, Yp] = meshgrid(xp, yp);
[~, ~, Zp] = meshgrid(xp, yp, zp);
Zp = squeeze(Zp(:,:,round(nPlane/2))); % 提取中间层，转为二维矩阵

% ========= 创建双图窗口 =========
fig = figure('Name', '第一类曲面积分对称性对比', 'Color', 'w', 'Position', [100, 100, 1400, 600]);
viewAngle1 = 45; viewAngle2 = 25; % 统一视角

% ------------------- 左图：奇函数 f = x -------------------
subplot(1,2,1);
hold on; grid on;
view(viewAngle1, viewAngle2);
axis equal;
axis([-2.5, 2.5, -2.5, 2.5, -2.5, 2.5]);

% 球面（红正蓝负）
C_odd = X;
surf(X, Y, Z, C_odd, ...
    'FaceAlpha', 0.85, ...
    'EdgeAlpha', 0.1, ...
    'FaceLighting', 'gouraud');

% 对称平面 yOz 面 (x=0)
surf(Xp, Yp, Zp, ...
    'FaceColor', [0.3 0.3 0.3], ...
    'FaceAlpha', 0.4, ...
    'EdgeColor', 'none');

% 正负标注
text(1.6, 0, 0.2, '+', 'FontSize', 24, 'FontWeight', 'bold', 'Color', 'r', 'HorizontalAlignment', 'center');
text(-1.8, 0, 0.2, '-', 'FontSize', 24, 'FontWeight', 'bold', 'Color', 'b', 'HorizontalAlignment', 'center');

% 配色与色条
colormap(gca, redbluecmap(256));
clim([-R, R]);
c1 = colorbar;
c1.Label.String = 'f(x,y,z) = x';
c1.Label.FontSize = 11;

xlabel('X'); ylabel('Y'); zlabel('Z');
title('奇函数  f(x,y,z) = x', 'FontSize', 13, 'FontWeight', 'bold');
text(0, -2.5, -2.7, '∬_S x dS = 0  (正负抵消)', ...
    'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', [1 1 0.9]);

camlight('headlight');
lighting gouraud;
hold off;

% ------------------- 右图：偶函数 g = x² 修复版 -------------------
subplot(1,2,2);
hold on; grid on;
view(viewAngle1, viewAngle2);
axis equal;
axis([-2.5, 2.5, -2.5, 2.5, -2.5, 2.5]);

% 球面函数值
C_even = X.^2;
% 先绘制完整球面
surf(X, Y, Z, C_even, ...
    'FaceAlpha', 0.7, ...
    'EdgeAlpha', 0.1, ...
    'FaceLighting', 'gouraud');

% ========= 修复2：半侧球面高亮（替换NaN叠加，改用遮罩单独绘制）=========
mask = X >= 0;
X_half = X(mask);
Y_half = Y(mask);
Z_half = Z(mask);
C_half = C_even(mask);
% 单独绘制右半侧，高亮强化
scatter3(X_half, Y_half, Z_half, 15, C_half, ...
    'filled', 'MarkerEdgeAlpha', 0);

% 对称平面
surf(Xp, Yp, Zp, ...
    'FaceColor', [0.3 0.3 0.3], ...
    'FaceAlpha', 0.4, ...
    'EdgeColor', 'none');

% 配色与色条
colormap(gca, 'turbo');
clim([0, R^2]);
c2 = colorbar;
c2.Label.String = 'g(x,y,z) = x^2';
c2.Label.FontSize = 11;

xlabel('X'); ylabel('Y'); zlabel('Z');
title('偶函数  g(x,y,z) = x^2', 'FontSize', 13, 'FontWeight', 'bold');
text(0, -2.5, -2.7, '∬_S x^2 dS = 2 ∬_{S_{x≥0}} x^2 dS  (对称翻倍)', ...
    'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', [1 1 0.9]);

camlight('headlight');
lighting gouraud;
hold off;

% 总标题
sgtitle('第一类曲面积分对称性：奇函数 vs 偶函数', ...
    'FontSize', 16, 'FontWeight', 'bold', 'Color', [0.2 0.2 0.8]);

% ========= 修复3：局部函数移至代码【最末尾】（MATLAB标准规范）=========
function cmap = redbluecmap(n)
    if nargin < 1, n = 256; end
    n2 = floor(n/2);
    r = [ones(n2,1); linspace(1,0,n-n2)'];
    g = [linspace(0,1,n2)'; linspace(1,0,n-n2)'];
    b = [linspace(0,1,n2)'; ones(n-n2,1)];
    cmap = [r, g, b];
end