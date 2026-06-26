% =========================================================================
% 三种典型电容器的 3D 几何结构可视化 (终极防报错 tex 版)
% 请直接运行此脚本
% =========================================================================
function plot_typical_capacitors_safe()
    % 创建主图窗，设置纯白背景
    fig = figure('Name', '三种典型电容器模型', 'Position', [100, 100, 1400, 500], 'Color', 'w');
    
    % ==================== 1. 平行板电容器 ====================
    ax1 = subplot(1, 3, 1);
    hold(ax1, 'on'); grid(ax1, 'on');
    view(ax1, [30, 25]); axis(ax1, 'equal');
    
    d = 2;       % 极板间距
    L = 5; W = 5; % 极板长宽 (面积 S)
    
    % 绘制下极板 (蓝色)
    fill3([-L -L L L]/2, [-W W W -W]/2, [-d -d -d -d]/2, [0.2 0.6 1], ...
        'FaceAlpha', 0.7, 'EdgeColor', [0.2 0.2 0.2], 'LineWidth', 1);
    % 绘制上极板 (红色)
    fill3([-L -L L L]/2, [-W W W -W]/2, [d d d d]/2, [1 0.4 0.4], ...
        'FaceAlpha', 0.7, 'EdgeColor', [0.2 0.2 0.2], 'LineWidth', 1);
    
    % 标注 d 和 S (使用纯文本或基础 tex)
    plot3([L/2+0.5 L/2+0.5], [0 0], [-d/2 d/2], 'k|-', 'LineWidth', 1.5);
    text(L/2+1, 0, 0, 'd', 'FontSize', 14, 'FontWeight', 'bold');
    text(0, 0, d/2+0.5, 'S', 'FontSize', 14, 'HorizontalAlignment', 'center');
    
    % 公式标题 (使用原生 tex 解释器，斜杠表示分数)
    title(ax1, {'(1) 平行板电容器', 'C = \epsilon S / d'}, 'Interpreter', 'tex', 'FontSize', 16);
    xlabel(ax1, 'X'); ylabel(ax1, 'Y'); zlabel(ax1, 'Z');
    
    
    % ==================== 2. 球形电容器 ====================
    ax2 = subplot(1, 3, 2);
    hold(ax2, 'on'); grid(ax2, 'on');
    view(ax2, [30, 25]); axis(ax2, 'equal');
    
    R1 = 2; % 内球半径
    R2 = 4; % 外球壳半径
    [X, Y, Z] = sphere(40);
    
    % 绘制完整的内球
    surf(R1*X, R1*Y, R1*Z, 'FaceColor', [1 0.4 0.4], 'EdgeColor', 'none', 'FaceAlpha', 1);
    
    % 绘制完整的外球壳
    surf(R2*X, R2*Y, R2*Z, 'FaceColor', [0.2 0.6 1], 'EdgeColor', 'none', 'FaceAlpha', 0.25);
    
    % 标注 R1, R2
    plot3([0 R1], [0 0], [0 0], 'k.-', 'LineWidth', 2, 'MarkerSize', 15);
    text(R1/2, 0, 0.5, 'R_1', 'Interpreter', 'tex', 'FontSize', 14);
    plot3([0 0], [0 -R2], [0 0], 'k.-', 'LineWidth', 2, 'MarkerSize', 15);
    text(0, -R2/2, 0.5, 'R_2', 'Interpreter', 'tex', 'FontSize', 14);
    
    camlight(ax2, 'right'); lighting(ax2, 'gouraud');
    
    % 公式标题 (使用原生 tex 解释器)
    title(ax2, {'(2) 球形电容器', 'C = 4\pi\epsilon R_1 R_2 / (R_2 - R_1)'}, 'Interpreter', 'tex', 'FontSize', 16);
    
    
    % ==================== 3. 圆柱形电容器 ====================
    ax3 = subplot(1, 3, 3);
    hold(ax3, 'on'); grid(ax3, 'on');
    view(ax3, [30, 25]); axis(ax3, 'equal');
    
    Rc1 = 1.5; % 内圆柱半径
    Rc2 = 3.5; % 外圆柱筒半径
    H = 6;     % 长度 l
    
    [Xc, Yc, Zc] = cylinder([1 1], 40);
    Zc = Zc * H - H/2;
    
    % 绘制完整的内圆柱
    surf(Rc1*Xc, Rc1*Yc, Zc, 'FaceColor', [1 0.4 0.4], 'EdgeColor', 'none', 'FaceAlpha', 1);
    
    % 绘制完整的外圆柱筒
    surf(Rc2*Xc, Rc2*Yc, Zc, 'FaceColor', [0.2 0.6 1], 'EdgeColor', 'none', 'FaceAlpha', 0.25);
    
    % 标注 R1, R2, l
    plot3([0 Rc1], [0 0], [H/2 H/2], 'k.-', 'LineWidth', 2);
    text(Rc1/2, 0, H/2+0.6, 'R_1', 'Interpreter', 'tex', 'FontSize', 14);
    plot3([0 0], [0 -Rc2], [H/2 H/2], 'k.-', 'LineWidth', 2);
    text(0, -Rc2/2, H/2+0.6, 'R_2', 'Interpreter', 'tex', 'FontSize', 14);
    plot3([0 0], [0 0], [-H/2 H/2], 'k-.', 'LineWidth', 1.5);
    text(0, 0, 0, '  l', 'FontSize', 14, 'HorizontalAlignment', 'left');
    
    camlight(ax3, 'right'); lighting(ax3, 'gouraud');
    
    % 公式标题 (使用原生 tex 解释器)
    title(ax3, {'(3) 圆柱形电容器', 'C = 2\pi\epsilon l / ln(R_2/R_1)'}, 'Interpreter', 'tex', 'FontSize', 16);

    % 美化坐标轴
    set([ax1, ax2, ax3], 'FontName', 'Helvetica', 'FontSize', 10);
end