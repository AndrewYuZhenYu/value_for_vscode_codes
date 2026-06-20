%% 二次曲面绘制总览
%  绘制全部 9 种常见二次曲面，仅展示形状，附标准方程
%  Andrew Yu - 考研复习用

clear; clc; close all;

figure('Name', '二次曲面总览', 'Position', [50 50 1500 1000]);

%% ---------- 1. 椭球面 (Ellipsoid) ----------
subplot(3,3,1);
[X, Y, Z] = ellipsoid(0, 0, 0, 2, 1.5, 1, 40);
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('1. 椭球面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'cool'); lighting gouraud; camlight;

%% ---------- 2. 椭圆抛物面 (Elliptic Paraboloid) ----------
subplot(3,3,2);
u = linspace(0, 2, 40);
v = linspace(0, 2*pi, 60);
[U, V] = meshgrid(u, v);
X = U .* cos(V);
Y = 0.7 * U .* sin(V);
Z = U.^2;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('2. 椭圆抛物面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}=z$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'summer'); lighting gouraud; camlight;

%% ---------- 3. 双曲抛物面 / 马鞍面 (Hyperbolic Paraboloid) ----------
subplot(3,3,3);
t = linspace(-2, 2, 60);
[X, Y] = meshgrid(t, t);
Z = X.^2 - Y.^2;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('3. 双曲抛物面（马鞍面）', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}-\frac{y^2}{b^2}=z$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'autumn'); lighting gouraud; camlight;

%% ---------- 4. 单叶双曲面 (Hyperboloid of One Sheet) ----------
subplot(3,3,4);
v = linspace(-2, 2, 40);
theta = linspace(0, 2*pi, 60);
[V, TH] = meshgrid(v, theta);
X = sqrt(1 + V.^2) .* cos(TH);
Y = sqrt(1 + V.^2) .* sin(TH);
Z = V;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('4. 单叶双曲面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=1$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'winter'); lighting gouraud; camlight;

%% ---------- 5. 双叶双曲面 (Hyperboloid of Two Sheets) ----------
subplot(3,3,5);
v = linspace(1, 2.5, 30);
theta = linspace(0, 2*pi, 60);
[V, TH] = meshgrid(v, theta);
R = sqrt(V.^2 - 1);
X = R .* cos(TH);
Y = R .* sin(TH);
Z_up = V;
Z_dn = -V;
surf(X, Y, Z_up, 'FaceAlpha', 0.8, 'EdgeColor', 'none'); hold on;
surf(X, Y, Z_dn, 'FaceAlpha', 0.8, 'EdgeColor', 'none'); hold off;
title('5. 双叶双曲面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=-1$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'copper'); lighting gouraud; camlight;

%% ---------- 6. 椭圆锥面 (Elliptic Cone) ----------
subplot(3,3,6);
v = linspace(-2, 2, 40);
theta = linspace(0, 2*pi, 60);
[V, TH] = meshgrid(v, theta);
X = abs(V) .* cos(TH);
Y = 0.7 * abs(V) .* sin(TH);
Z = V;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('6. 椭圆锥面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}=\frac{z^2}{c^2}$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'hot'); lighting gouraud; camlight;

%% ---------- 7. 椭圆柱面 (Elliptic Cylinder) ----------
subplot(3,3,7);
theta = linspace(0, 2*pi, 60);
z = linspace(-2, 2, 30);
[TH, ZZ] = meshgrid(theta, z);
X = 1.5 * cos(TH);
Y = sin(TH);
Z = ZZ;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('7. 椭圆柱面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'spring'); lighting gouraud; camlight;

%% ---------- 8. 抛物柱面 (Parabolic Cylinder) ----------
subplot(3,3,8);
x = linspace(-2, 2, 50);
z = linspace(-2, 2, 30);
[X, Z] = meshgrid(x, z);
Y = X.^2;
surf(X, Y, Z, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
title('8. 抛物柱面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$y^2 = 2px$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'parula'); lighting gouraud; camlight;

%% ---------- 9. 双曲柱面 (Hyperbolic Cylinder) ----------
subplot(3,3,9);
z = linspace(-2, 2, 30);
t = linspace(-1.5, 1.5, 50);
[T, ZZ] = meshgrid(t, z);
X1 = cosh(T);
Y1 = sinh(T);
surf(X1, Y1, ZZ, 'FaceAlpha', 0.8, 'EdgeColor', 'none'); hold on;
surf(-X1, Y1, ZZ, 'FaceAlpha', 0.8, 'EdgeColor', 'none'); hold off;
title('9. 双曲柱面', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('$$\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$$', ...
    'Interpreter', 'latex', 'FontSize', 11);
axis equal; colormap(gca, 'sky'); lighting gouraud; camlight;

%% 全局美化
sgtitle('常见二次曲面总览', 'FontSize', 16, 'FontWeight', 'bold');