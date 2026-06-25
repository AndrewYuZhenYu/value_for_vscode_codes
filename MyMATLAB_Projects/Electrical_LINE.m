function electric_field_derivation_pro()
% 创建高级几何推导交互看板
fig = figure('Name', 'Finite Line Charge Derivation Model', ...
    'Position', [100, 80, 950, 700], 'Color', [0.97, 0.97, 0.97]);

% 物理与几何基础参数（固定带电直线夹在 x = [-1.5, 1.5]）
x1 = -1.5;
x2 = 1.5;

% 初始 P 点位置
P_init = [0.6, 1.3];

% 建立专业画幅
ax = axes('Parent', fig, 'Position', [0.08, 0.28, 0.84, 0.65], ...
    'FontName', 'Times New Roman', 'FontSize', 11);

% 底部参数交互滑块（大尺寸、清晰标注）
uicontrol('Parent', fig, 'Style', 'text', 'Position', [70, 75, 120, 20], ...
    'String', 'Observation Px:', 'FontSize', 10, 'HorizontalAlignment', 'right');
sl_X = uicontrol('Parent', fig, 'Style', 'slider', 'Min', -3.0, 'Max', 3.0, ...
    'Value', P_init(1), 'Position', [200, 75, 220, 20]);

uicontrol('Parent', fig, 'Style', 'text', 'Position', [480, 75, 140, 20], ...
    'String', 'Distance a (Py):', 'FontSize', 10, 'HorizontalAlignment', 'right');
sl_Y = uicontrol('Parent', fig, 'Style', 'slider', 'Min', 0.3, 'Max', 3.5, ...
    'Value', P_init(2), 'Position', [630, 75, 220, 20]);

% 底部实时 LaTeX 公式同步状态栏
status_ax = axes('Parent', fig, 'Position', [0.05, 0.02, 0.9, 0.08], 'Visible', 'off');
status_text = text(0.5, 0.5, '', 'Parent', status_ax, 'Interpreter', 'latex', ...
    'FontSize', 13, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');

% 绘制角度弧线的专用辅助函数
    function draw_angle_arc(cx, cy, r, start_angle, end_angle, color, label_str)
        th = linspace(start_angle, end_angle, 40);
        ax_x = cx + r * cos(th);
        ax_y = cy + r * sin(th);
        plot(ax, ax_x, ax_y, 'Color', color, 'LineWidth', 1.2, 'LineStyle', '-');
        % 标注文本位置放在弧线中间外侧一点
        mid_th = (start_angle + end_angle) / 2;
        text(cx + (r + 0.15)*cos(mid_th), cy + (r + 0.15)*sin(mid_th), label_str, ...
            'Parent', ax, 'Interpreter', 'latex', 'Color', color, 'FontSize', 12, 'HorizontalAlignment', 'center');
    end

% 核心渲染循环
    function render(~, ~)
        Px = sl_X.Value;
        Py = sl_Y.Value; % 即推导公式中的垂直距离 a

        cla(ax);
        hold(ax, 'on');

        % 1. 绘制基准带电直线 (x 轴) 与两端点
        plot(ax, [-3.5, 3.5], [0, 0], 'k:', 'LineWidth', 0.8); % x基准线
        plot(ax, [x1, x2], [0, 0], 'Color', [0.2 0.2 0.2], 'LineWidth', 5); % 主带电体

        % 端点标记
        plot(ax, x1, 0, 'ro', 'MarkerFaceColor', [1 0.3 0.3], 'MarkerSize', 8);
        plot(ax, x2, 0, 'ro', 'MarkerFaceColor', [1 0.3 0.3], 'MarkerSize', 8);
        text(x1, -0.18, '$x_1$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');
        text(x2, -0.18, '$x_2$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');

        % 2. 绘制观察点 P 与垂直垂线 a
        plot(ax, Px, Py, 'ko', 'MarkerFaceColor', [0.1 0.1 0.1], 'MarkerSize', 7);
        text(Px, Py + 0.18, '$P(x, a)$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');

        plot(ax, [Px, Px], [0, Py], 'b--', 'LineWidth', 1.5); % 垂线a
        text(Px + 0.08, Py/2, '$a$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 13, 'Color', 'blue');
        plot(ax, Px, 0, 'kx', 'MarkerSize', 6); % 垂足

        % 3. 连线到端点并计算角度 \theta_1 和 \theta_2
        plot(ax, [x1, Px], [0, Py], 'Color', [0.4 0.6 0.9], 'LineWidth', 1.2, 'LineStyle', '-.');
        plot(ax, [x2, Px], [0, Py], 'Color', [0.4 0.6 0.9], 'LineWidth', 1.2, 'LineStyle', '-.');

        % 严格按照以端点为原点、x轴正方向为基准计算夹角
        theta1 = atan2(Py, Px - x1);
        theta2 = atan2(Py, Px - x2);

        % 4. 绘制角度指示弧线
        arc_radius = 0.35;
        draw_angle_arc(x1, 0, arc_radius, 0, theta1, [0.1, 0.6, 0.2], '$\theta_1$');
        draw_angle_arc(x2, 0, arc_radius, 0, theta2, [0.8, 0.4, 0.1], '$\theta_2$');

        % 5. 计算物理分量方向（剔除宏观系数后，完全由几何角度确定的核心项）
        Ex_val = sin(theta2) - sin(theta1);
        Ey_val = cos(theta1) - cos(theta2);

        % 6. 精细绘制场强矢量箭头 (为了构图清晰，将矢量起点置于 P 点)
        vec_scale = 0.6; % 缩放因子

        % Ex 分量 (红色)
        quiver(ax, Px, Py, Ex_val * vec_scale, 0, 0, 'r', 'LineWidth', 2, 'MaxHeadSize', 0.4);
        text(Px + Ex_val * vec_scale + 0.1*sign(Ex_val+0.001), Py, '$E_x$', ...
            'Parent', ax, 'Interpreter', 'latex', 'Color', 'r', 'FontSize', 12, 'VerticalAlignment', 'middle');

        % Ey 分量 (绿色)
        quiver(ax, Px, Py, 0, Ey_val * vec_scale, 0, 'g', 'LineWidth', 2, 'MaxHeadSize', 0.4);
        text(Px, Py + Ey_val * vec_scale + 0.12, '$E_y$', ...
            'Parent', ax, 'Interpreter', 'latex', 'Color', 'g', 'FontSize', 12, 'HorizontalAlignment', 'center');

        % 合成总场强 E (品红双倍粗线)
        quiver(ax, Px, Py, Ex_val * vec_scale, Ey_val * vec_scale, 0, 'm', 'LineWidth', 2.5, 'MaxHeadSize', 0.3);
        text(Px + Ex_val * vec_scale + 0.12, Py + Ey_val * vec_scale + 0.12, '$\vec{E}$', ...
            'Parent', ax, 'Interpreter', 'latex', 'Color', 'm', 'FontSize', 13, 'FontWeight', 'bold');

        % 7. 实时更新下方的标准积分推导公式结果，实现数据无缝对齐
        formula_str = sprintf('$E_x = \\frac{\\lambda}{4\\pi\\varepsilon_0 a} (\\sin\\theta_2 - \\sin\\theta_1) \\propto %.3f \\quad | \\quad E_y = \\frac{\\lambda}{4\\pi\\varepsilon_0 a} (\\cos\\theta_1 - \\cos\\theta_2) \\propto %.3f$', ...
            Ex_val, Ey_val);
        status_text.String = formula_str;

        % 视窗美化与范围控制
        title(ax, 'Microscopic Geometric Model for Line Charge Field Derivation', 'FontSize', 13, 'FontWeight', 'bold');
        xlabel(ax, '$x$ (Axis)', 'Interpreter', 'latex', 'FontSize', 12);
        ylabel(ax, '$y$ (Axis)', 'Interpreter', 'latex', 'FontSize', 12);
        axis(ax, [-4, 4, -0.6, 4.0]);
        axis(ax, 'equal');
        grid(ax, 'on');
        set(ax, 'XMinorGrid', 'on', 'YMinorGrid', 'on', 'GridAlpha', 0.15);
        hold(ax, 'off');
    end

% 绑定滑块回调，触发丝滑重绘
sl_X.Callback = @render;
sl_Y.Callback = @render;

% 执行首帧渲染
render();
end