figure; hold on;

% 参数范围
x = linspace(0, 1, 60);
y = linspace(0, 1, 60);
[X, Y] = meshgrid(x, y);

% 只保留 x+y<=1, x>=0, y>=0 的区域
mask = (X + Y <= 1) & (X >= 0) & (Y >= 0);

Z_top = X + Y;
Z_bot = X .* Y;

Z_top(~mask) = NaN;
Z_bot(~mask) = NaN;

% 上曲面 z = x+y
surf(X, Y, Z_top, 'FaceColor', [0.2 0.6 1.0], 'FaceAlpha', 0.7, ...
    'EdgeColor', 'none');

% 下曲面 z = xy
surf(X, Y, Z_bot, 'FaceColor', [1.0 0.5 0.2], 'FaceAlpha', 0.7, ...
    'EdgeColor', 'none');

% 侧面1: x=0, y从0到1, z从0到y
t = linspace(0, 1, 60);
[T, Z1] = meshgrid(t, linspace(0, 1, 60));
Zside1_top = T;        % z = 0+y = y
Zside1_bot = zeros(size(T)); % z = 0*y = 0
Xside1 = zeros(size(T));
Yside1 = T;
mask1 = (Yside1 <= 1);
Zside1_top(~mask1) = NaN;
Zside1_bot(~mask1) = NaN;
surf(Xside1, Yside1, Zside1_top, 'FaceColor',[0.4 0.8 0.4],'FaceAlpha',0.6,'EdgeColor','none');
surf(Xside1, Yside1, Zside1_bot, 'FaceColor',[0.4 0.8 0.4],'FaceAlpha',0.6,'EdgeColor','none');

% x=0时 两个曲面之间的侧面
for yi = linspace(0, 1, 40)
    zb = 0;
    zt = yi;
    plot3([0 0], [yi yi], [zb zt], 'g-', 'LineWidth', 0.3);
end

% 侧面2: y=0, x从0到1
for xi = linspace(0, 1, 40)
    zb = 0;
    zt = xi;
    plot3([xi xi], [0 0], [zb zt], 'g-', 'LineWidth', 0.3);
end

% 侧面3: x+y=1 (斜面)
s = linspace(0, 1, 60);
Xs3 = s;
Ys3 = 1 - s;
for i = 1:length(s)
    xi = Xs3(i); yi = Ys3(i);
    zb = xi * yi;
    zt = xi + yi;  % = 1
    plot3([xi xi], [yi yi], [zb zt], 'r-', 'LineWidth', 0.5);
end

% 斜侧面填充
[S3, ZZ] = meshgrid(s, linspace(0, 1, 60));
X3 = S3;
Y3 = 1 - S3;
Z3_top = ones(size(S3));        % z = x+y = 1
Z3_bot = S3 .* (1 - S3);       % z = xy
surf(X3, Y3, Z3_top, 'FaceColor',[0.8 0.3 0.8],'FaceAlpha',0.6,'EdgeColor','none');
surf(X3, Y3, Z3_bot, 'FaceColor',[0.8 0.3 0.8],'FaceAlpha',0.6,'EdgeColor','none');

% 底面 z=xy 和 侧面之间用patch填斜侧面
patch_x = [s, fliplr(s)];
patch_y = [1-s, fliplr(1-s)];
patch_z = [ones(1,length(s)), fliplr(s.*(1-s))];
fill3(patch_x, patch_y, patch_z, [0.8 0.3 0.8], 'FaceAlpha', 0.5, 'EdgeColor','none');

% 坐标轴和标签
xlabel('x'); ylabel('y'); zlabel('z');
title('z = x+y（上）与 z = xy（下）围成的立体');
legend({'上曲面 z=x+y','下曲面 z=xy'}, 'Location','northwest');
grid on; axis tight;
view(45, 30);
camlight; lighting gouraud;