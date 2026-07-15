% =========================================================================
% 霍尔效应原理推导与 3D 示意图 (科研质感版)
% =========================================================================

% 1. 全局设置 LaTeX 解析器，确保所有文本正常渲染
set(groot, 'defaultTextInterpreter', 'latex');
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');
set(groot, 'defaultLegendInterpreter', 'latex');

% 创建高分辨率、宽屏比例的图形窗口
fig = figure('Name', 'Hall Effect Derivation', 'Position', [100, 100, 1400, 700], 'Color', 'w');

% =========================================================================
% 左侧区域：3D 霍尔元件与物理量标注
% =========================================================================
ax1 = axes('Position', [0.02, 0.05, 0.55, 0.9]);
hold on; axis off; grid off;
view(3); % 开启 3D 视角
view(ax1, 35, 25);
axis equal;

% 定义长方体参数 (长 L, 宽 W, 厚 T)
L = 10; W = 5; T = 2;

% 定义长方体的 8 个顶点
vertices = [0 0 0; L 0 0; L W 0; 0 W 0; 0 0 T; L 0 T; L W T; 0 W T];
% 定义 6 个面
faces = [1 2 6 5; 2 3 7 6; 3 4 8 7; 4 1 5 8; 1 2 3 4; 5 6 7 8];

% 绘制半透明科研质感长方体
patch('Vertices', vertices, 'Faces', faces, ...
    'FaceColor', [0.7 0.8 0.9], 'FaceAlpha', 0.6, ...
    'EdgeColor', [0.3 0.3 0.3], 'LineWidth', 1.5);

% 打光增加立体感
camlight('headlight');
lighting gouraud;

% --- 绘制坐标轴 (x, y, z) ---
quiver3(-2, 0, 0, 4, 0, 0, 'k', 'LineWidth', 1.5, 'MaxHeadSize', 0.5); % X轴
quiver3(0, -2, 0, 0, 4, 0, 'k', 'LineWidth', 1.5, 'MaxHeadSize', 0.5); % Y轴
quiver3(0, 0, -2, 0, 0, 4, 'k', 'LineWidth', 1.5, 'MaxHeadSize', 0.5); % Z轴
text(2.5, -0.5, 0, '$$x$$', 'FontSize', 16);
text(-0.5, 2.5, 0, '$$y$$', 'FontSize', 16);
text(0, -0.5, 2.5, '$$z$$', 'FontSize', 16);

% --- 绘制磁场 B (蓝色向上箭头) ---
B_x = L/2; B_y = W/2;
quiver3(B_x, B_y, 0, 0, 0, T+3, 'b', 'LineWidth', 3, 'MaxHeadSize', 0.2);
text(B_x, B_y, T+3.5, '$$\mathbf{B} (B_z)$$', 'Color', 'b', 'FontSize', 18, 'FontWeight', 'bold');

% --- 绘制电流 I (红色向右箭头) ---
quiver3(-2, W/2, T/2, 3, 0, 0, 'r', 'LineWidth', 3, 'MaxHeadSize', 0.5);
quiver3(L, W/2, T/2, 3, 0, 0, 'r', 'LineWidth', 3, 'MaxHeadSize', 0.5);
text(-3, W/2, T/2+0.5, '$$I_x$$', 'Color', 'r', 'FontSize', 18, 'FontWeight', 'bold');
text(L+1.5, W/2, T/2+0.5, '$$I_x$$', 'Color', 'r', 'FontSize', 18, 'FontWeight', 'bold');

% --- 绘制载流子与受力 (假设电子向左运动) ---
plot3(L/2, W/2, T/2, 'ko', 'MarkerFaceColor', 'y', 'MarkerSize', 10); % 电子
text(L/2, W/2, T/2-0.5, '$$-e$$', 'FontSize', 14);
% 漂移速度 v_d (向左)
quiver3(L/2, W/2, T/2, -2, 0, 0, 'k', 'LineWidth', 2, 'MaxHeadSize', 0.5);
text(L/2-2, W/2, T/2-0.5, '$$\mathbf{v}_d$$', 'FontSize', 14);
% 洛伦兹力 F_L (向外, +y方向)
quiver3(L/2, W/2, T/2, 0, 2, 0, 'Color', [0.85 0.33 0.1], 'LineWidth', 2, 'MaxHeadSize', 0.5);
text(L/2, W/2+2.5, T/2, '$$\mathbf{F}_L$$', 'Color', [0.85 0.33 0.1], 'FontSize', 16);
% 电场力 F_E (向内, -y方向)
quiver3(L/2, W/2, T/2, 0, -2, 0, 'Color', [0.47 0.67 0.19], 'LineWidth', 2, 'MaxHeadSize', 0.5);
text(L/2, W/2-2.5, T/2, '$$\mathbf{F}_E$$', 'Color', [0.47 0.67 0.19], 'FontSize', 16);

% --- 标注几何尺寸 ---
text(L/2, -0.5, 0, '$$L$$', 'FontSize', 16); % 长度
text(L+0.5, W/2, 0, '$$W$$', 'FontSize', 16); % 宽度
text(L+0.5, 0, T/2, '$$T$$', 'FontSize', 16); % 厚度

% =========================================================================
% 右侧区域：LaTeX 推导公式区
% =========================================================================
ax2 = axes('Position', [0.55, 0.05, 0.4, 0.9]);
hold on; axis off;

% 使用 cell 数组排版详细的推导过程，全部包裹在 LaTeX 语法中
derivation_text = {
    '\textbf{\Large Hall Effect Derivation}',
    '',
    '\textbf{Step 1: The Lorentz Force}',
    'The magnetic force on a charge carrier (electron, $q = -e$) is:',
    '$$ \mathbf{F}_L = q(\mathbf{v}_d \times \mathbf{B}) $$',
    'Magnitude: $$ F_L = e v_d B_z $$',
    '',
    '\textbf{Step 2: Balance of Forces in Steady State}',
    'Charge accumulation creates a transverse Hall Electric Field $\mathbf{E}_H$.',
    '$$ \mathbf{F}_E = q\mathbf{E}_H $$',
    'At equilibrium: $$ \Sigma F = F_L - F_E = 0 \implies e v_d B_z = e E_H $$',
    '$$ E_H = v_d B_z $$',
    '',
    '\textbf{Step 3: Relationship with Hall Voltage ($V_H$)}',
    'Integrating the electric field across the width $W$:',
    '$$ V_H = \int_{0}^{W} E_H \, dy = E_H W = v_d B_z W $$',
    '',
    '\textbf{Step 4: Expressing Current ($I_x$)}',
    'Using charge density $n$ and cross-sectional area $A = W \cdot T$:',
    '$$ I_x = n e v_d A = n e v_d W T $$',
    '$$ \implies v_d = \frac{I_x}{n e W T} $$',
    '',
    '\textbf{Step 5: Final Hall Voltage Equation}',
    'Substitute $v_d$ back into the $V_H$ equation:',
    '$$ V_H = \left( \frac{I_x}{n e W T} \right) B_z W = \frac{I_x B_z}{n e T} $$',
    '',
    'Defining the \textbf{Hall Coefficient} $R_H = \frac{1}{ne}$:',
    '$$ V_H = R_H \frac{I_x B_z}{T} $$'
    };

% 在右侧空白坐标轴的左上角写入文本
text(0.05, 0.95, derivation_text, 'FontSize', 14, ...
    'VerticalAlignment', 'top', 'Interpreter', 'latex');

% 调整背景色与整体排版
set(gcf, 'Color', 'w');