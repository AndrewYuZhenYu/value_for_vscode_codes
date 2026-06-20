% =========================================================================
% 第二类曲面积分通用投影可视化 (General Surface Integral Projections)
% =========================================================================
clear; clc; close all;

%% 1. 生成极具一般性的复合起伏曲面 (General Wavy Surface Generation)
% 定义非对称的空间网格
x_vec = linspace(0, 3, 60);
y_vec = linspace(0, 3, 60);
[X, Y] = meshgrid(x_vec, y_vec);

% 构造一个结合了正弦波动、鞍面波动和二次项的复合通用曲面
% 该曲面曲率多变、高低错落，极具普适性
Z = 1.0 + 0.6 * sin(1.5*X) .* cos(1.5*Y) + 0.08*(X - 1.5).^2 + 0.04*Y.^2;

%% 2. 绘图窗口初始化 (Figure & Axis Setup)
fig = figure('Name', 'General Surface Integral Projections', 'Color', 'w', ...
             'Position', [100, 100, 900, 800]);
ax = axes('Parent', fig);
hold(ax, 'on');
grid(ax, 'on');
view(ax, 50, 28);       % 调整为更能展现曲面起伏的高级视角
axis(ax, 'equal');
ax.GridAlpha = 0.15;    % 软化网格线，突显主体

%% 3. 学术莫兰迪配色方案 (Advanced Academic Color Palette)
colorSurf  = [0.15, 0.55, 0.68];   % 主曲面：深海青
colorXY    = [0.86, 0.45, 0.35];   % dxdy投影：微醺砖红
colorYZ    = [0.92, 0.69, 0.25];   % dydz投影：向日葵金
colorXZ    = [0.55, 0.35, 0.65];   % dzdx投影：紫罗兰灰
colorEdge  = [0.25, 0.25, 0.25];   % 网格线：高级暗灰

%% 4. 绘制三轴投影面与主曲面 (Plotting Surfaces)
% 为了体现积分微元的网格感，我们保留极淡的网格线 (EdgeAlpha=0.1)
% XY 面投影 (Z = 0)
surf(ax, X, Y, zeros(size(Z)), 'FaceColor', colorXY, 'EdgeColor', colorEdge, 'EdgeAlpha', 0.1, 'FaceAlpha', 0.3);
% YZ 面投影 (X = 0)
surf(ax, zeros(size(X)), Y, Z, 'FaceColor', colorYZ, 'EdgeColor', colorEdge, 'EdgeAlpha', 0.1, 'FaceAlpha', 0.3);
% XZ 面投影 (Y = 0)
surf(ax, X, zeros(size(Y)), Z, 'FaceColor', colorXZ, 'EdgeColor', colorEdge, 'EdgeAlpha', 0.1, 'FaceAlpha', 0.3);

% 绘制主曲面 $\Sigma$
surf(ax, X, Y, Z, 'FaceColor', colorSurf, 'EdgeColor', colorEdge, 'EdgeAlpha', 0.15, 'FaceAlpha', 0.85);

%% 5. 增强视觉：绘制几何轮廓外框线 (Perimeter Highlighting)
% 提取边界数据，用加粗的深色线条勾勒边界，这是顶级科研制图的常用手法
lw_bound = 1.2;
% 主曲面边界
plot3(ax, X(1,:), Y(1,:), Z(1,:), 'Color', colorSurf*0.6, 'LineWidth', lw_bound);
plot3(ax, X(end,:), Y(end,:), Z(end,:), 'Color', colorSurf*0.6, 'LineWidth', lw_bound);
plot3(ax, X(:,1), Y(:,1), Z(:,1), 'Color', colorSurf*0.6, 'LineWidth', lw_bound);
plot3(ax, X(:,end), Y(:,end), Z(:,end), 'Color', colorSurf*0.6, 'LineWidth', lw_bound);

% XY 投影边界
plot3(ax, X(1,:), Y(1,:), zeros(1,size(X,2)), 'Color', colorXY*0.7, 'LineWidth', lw_bound);
plot3(ax, X(end,:), Y(end,:), zeros(1,size(X,2)), 'Color', colorXY*0.7, 'LineWidth', lw_bound);
plot3(ax, X(:,1), Y(:,1), zeros(size(X,1),1), 'Color', colorXY*0.7, 'LineWidth', lw_bound);
plot3(ax, X(:,end), Y(:,end), zeros(size(X,1),1), 'Color', colorXY*0.7, 'LineWidth', lw_bound);

%% 6. 空间投影虚线引导线 (Spatial Guidelines)
% 从曲面的周界边缘向下、向后投射引导虚线，强化三维投影的逻辑
[M, N] = size(X);
% 均匀对周界进行降采样抽样，避免虚线过密产生凌乱感
edge_idx = [ones(1, N), M*ones(1, N), 1:M, 1:M; ...
            1:N, 1:N, ones(1, M), N*ones(1, M)]';
step = 8; 
edge_idx = edge_idx(1:step:end, :);

for k = 1:size(edge_idx, 1)
    i = edge_idx(k, 1); j = edge_idx(k, 2);
    % 向 XY 平面连线
    plot3(ax, [X(i,j), X(i,j)], [Y(i,j), Y(i,j)], [0, Z(i,j)], '--', 'Color', [0.6 0.6 0.6], 'LineWidth', 0.6);
    % 向 YZ 平面连线
    plot3(ax, [0, X(i,j)], [Y(i,j), Y(i,j)], [Z(i,j), Z(i,j)], '--', 'Color', [0.6 0.6 0.6], 'LineWidth', 0.6);
    % 向 XZ 平面连线
    plot3(ax, [X(i,j), X(i,j)], [0, Y(i,j)], [Z(i,j), Z(i,j)], '--', 'Color', [0.6 0.6 0.6], 'LineWidth', 0.6);
end

%% 7. 物理材质与多光源系统 (Advanced Lighting)
% 复杂的起伏曲面需要多角度打光才能展现华丽的几何细节
light1 = camlight(ax, 'headlight');
light2 = light(ax, 'Position', [5, -2, 5], 'Style', 'local');
light3 = light(ax, 'Position', [-2, 5, 3], 'Style', 'local');
lighting(ax, 'gouraud');
material(ax, 'shiny'); % 换用微高光的 shiny 材质，完美勾勒出波浪曲面的山脊线

%% 8. 严谨的学术文本排版 (Typography & Axis Formatting)
set(ax, 'TickLabelInterpreter', 'latex', 'FontSize', 13, 'LineWidth', 1.1);
xlabel(ax, '$x$', 'Interpreter', 'latex', 'FontSize', 18);
ylabel(ax, '$y$', 'Interpreter', 'latex', 'FontSize', 18);
zlabel(ax, '$z$', 'Interpreter', 'latex', 'FontSize', 18);

% 动态计算包络范围
xlim(ax, [0, max(x_vec)*1.05]);
ylim(ax, [0, max(y_vec)*1.05]);
zlim(ax, [0, max(Z(:))*1.05]);
box(ax, 'on');

% 精致的 LaTeX 图例
lgd = legend(ax, {'$\iint_{\Sigma} R(x,y,z)dxdy$', ...
                  '$\iint_{\Sigma} P(x,y,z)dydz$', ...
                  '$\iint_{\Sigma} Q(x,y,z)dzdx$', ...
                  'General Surface $\Sigma$'}, ...
             'Interpreter', 'latex', 'FontSize', 11, 'Location', 'northeast');
lgd.ItemTokenSize = [18, 18];
lgd.Box = 'on';