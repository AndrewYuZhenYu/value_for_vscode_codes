function ConductorSimulationPro()
    % CONDUCTORSIMULATIONPRO 平行导体板静电平衡高级交互仿真看板
    % 采用标准模块化架构，杜绝嵌套函数，确保数据流透明易读
    
    % 1. 初始化图形视窗
    fig = figure('Name', 'Electrostatic Equilibrium of Conducting Plates', ...
                 'Position', [100, 80, 1000, 720], ...
                 'Color', [0.96, 0.96, 0.96]);
             
    % 2. 构造显式数据对象 (存储所有 UI 句柄及物理变量)
    data = struct();
    data.S = 1.0;          % 导体板的有效面积 S
    data.QA = 5.0;         % 初始 A 板总电荷量
    data.QB = -3.0;        % 初始 B 板总电荷量
    
    % 3. 创建专业科研级画幅
    data.ax = axes('Parent', fig, 'Position', [0.08, 0.28, 0.85, 0.65], ...
                   'FontName', 'Times New Roman', 'FontSize', 11);
               
    % 4. 构造规范的交互控制滑块
    uicontrol('Parent', fig, 'Style', 'text', 'Position', [60, 75, 120, 20], ...
              'String', 'Total Charge Q_A:', 'FontSize', 10, 'HorizontalAlignment', 'right');
    data.sl_A = uicontrol('Parent', fig, 'Style', 'slider', 'Min', -10.0, 'Max', 10.0, ...
                          'Value', data.QA, 'Position', [190, 75, 220, 20]);
                      
    uicontrol('Parent', fig, 'Style', 'text', 'Position', [500, 75, 120, 20], ...
              'String', 'Total Charge Q_B:', 'FontSize', 10, 'HorizontalAlignment', 'right');
    data.sl_B = uicontrol('Parent', fig, 'Style', 'slider', 'Min', -10.0, 'Max', 10.0, ...
                          'Value', data.QB, 'Position', [630, 75, 220, 20]);
                      
    % 5. 构造底部 LaTeX 理论推导同步监视器
    data.status_ax = axes('Parent', fig, 'Position', [0.05, 0.02, 0.9, 0.06], 'Visible', 'off');
    data.status_text = text(0.5, 0.5, '', 'Parent', data.status_ax, 'Interpreter', 'latex', ...
                            'FontSize', 13, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');

    % 6. 将数据对象注入到 UI 的 UserData 中，用作标准状态传递
    set(data.sl_A, 'UserData', data);
    set(data.sl_B, 'UserData', data);
    
    % 7. 绑定标准回调处理函数
    data.sl_A.Callback = @on_slider_changed;
    data.sl_B.Callback = @on_slider_changed;
    
    % 8. 触发首帧纯净渲染
    render_frame(data);
end

function on_slider_changed(src, ~)
    % 统一的回调入口：负责从 UI 中提取并刷新核心数据流
    data = get(src, 'UserData');
    
    % 从两个滑块组件中读取最新的物理参数
    data.QA = get(data.sl_A, 'Value');
    data.QB = get(data.sl_B, 'Value');
    
    % 同步更新所有组件共享的 UserData 缓存
    set(data.sl_A, 'UserData', data);
    set(data.sl_B, 'UserData', data);
    
    % 重新渲染画布
    render_frame(data);
end

function render_frame(data)
    % 核心图形渲染引擎：严格遵循数据驱动，消灭任何乱码与拼凑代码
    ax = data.ax;
    cla(ax);
    hold(ax, 'on');
    
    % --- Step 1: 物理内核运算 (静电平衡精确解) ---
    sigma1 = (data.QA + data.QB) / (2 * data.S);
    sigma4 = sigma1;
    sigma2 = (data.QA - data.QB) / (2 * data.S);
    sigma3 = -sigma2;
    
    % 各空间区域对应的合场强大小（基于无限大均匀带电平面叠加原理）
    E_left   = -(sigma1 + sigma2 + sigma3 + sigma4) / 2;
    E_middle = (sigma1 + sigma2 - sigma3 - sigma4) / 2;
    E_right  = (sigma1 + sigma2 + sigma3 + sigma4) / 2;
    
    % --- Step 2: 绘制平行导体板几何实体 ---
    % 导体A 占据空间 [-1.2, -0.7]， 导体B 占据空间 [0.7, 1.2]
    fill(ax, [-1.2, -0.7, -0.7, -1.2], [-2.2, -2.2, 2.2, 2.2], ...
         [0.9, 0.9, 0.9], 'EdgeColor', [0.2, 0.2, 0.2], 'LineWidth', 2);
    fill(ax, [0.7, 1.2, 1.2, 0.7], [-2.2, -2.2, 2.2, 2.2], ...
         [0.9, 0.9, 0.9], 'EdgeColor', [0.2, 0.2, 0.2], 'LineWidth', 2);
     
    text(-0.95, 2.4, 'Conductor $A$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');
    text(0.95, 2.4, 'Conductor $B$', 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');
    
    % --- Step 3: 绘制高斯定理辅助推导柱面 (Gaussian Pillbox) ---
    % 在导体 A 左侧建立跨越表面的高斯面，用以向学生展示静电平衡的物理本质
    plot(ax, [-1.4, -0.9, -0.9, -1.4, -1.4], [0.6, 0.6, 1.2, 1.2, 0.6], ...
         'LineStyle', '--', 'Color', [0.7, 0.2, 0.2], 'LineWidth', 1.2);
    text(-1.15, 1.35, 'Gaussian Surface', 'Parent', ax, 'Interpreter', 'latex', ...
         'Color', [0.7, 0.2, 0.2], 'FontSize', 10, 'HorizontalAlignment', 'center');
     
    % --- Step 4: 离散化动态渲染表面电荷分布符 ---
    draw_charge_vectors(ax, -1.23, sigma1); % 表面 1
    draw_charge_vectors(ax, -0.67, sigma2); % 表面 2
    draw_charge_vectors(ax, 0.67, sigma3);  % 表面 3
    draw_charge_vectors(ax, 1.23, sigma4);  % 表面 4
    
    % --- Step 5: 强制应用 LaTeX 渲染四个表面的面密度标注 ---
    text(-1.45, 0, ['$\sigma_1 = ', num2str(sigma1, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'right');
    text(-0.45, 0, ['$\sigma_2 = ', num2str(sigma2, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');
    text(0.45, 0, ['$\sigma_3 = ', num2str(sigma3, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'center');
    text(1.45, 0, ['$\sigma_4 = ', num2str(sigma4, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'FontSize', 12, 'HorizontalAlignment', 'left');
    
    % --- Step 6: 绘制各区域电场强度矢量箭头 (E-Field Vectors) ---
    vec_len = 0.5;
    if abs(E_left) > 0.01
        quiver(ax, -2.2, 0, E_left * vec_len, 0, 0, 'Color', [0.5, 0.0, 0.5], 'LineWidth', 2, 'MaxHeadSize', 0.5);
        text(-2.2, -0.3, ['$E = ', num2str(E_left, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'Color', [0.5, 0.0, 0.5], 'HorizontalAlignment', 'center');
    end
    if abs(E_middle) > 0.01
        quiver(ax, -0.2, 0, E_middle * vec_len, 0, 0, 'Color', [0.5, 0.0, 0.5], 'LineWidth', 2, 'MaxHeadSize', 0.5);
        text(0, -0.3, ['$E_{\mathrm{mid}} = ', num2str(E_middle, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'Color', [0.5, 0.0, 0.5], 'HorizontalAlignment', 'center');
    end
    if abs(E_right) > 0.01
        quiver(ax, 1.8, 0, E_right * vec_len, 0, 0, 'Color', [0.5, 0.0, 0.5], 'LineWidth', 2, 'MaxHeadSize', 0.5);
        text(1.8, -0.3, ['$E = ', num2str(E_right, '%.2f'), '$'], 'Parent', ax, 'Interpreter', 'latex', 'Color', [0.5, 0.0, 0.5], 'HorizontalAlignment', 'center');
    end
    
    % 强力突出：导体内场强恒定为 0 (静电平衡的核心)
    text(-0.95, 0, '$E_{\mathrm{in}} = 0$', 'Parent', ax, 'Interpreter', 'latex', 'Color', [0.1, 0.7, 0.2], 'FontWeight', 'bold', 'FontSize', 13, 'HorizontalAlignment', 'center');
    text(0.95, 0, '$E_{\mathrm{in}} = 0$', 'Parent', ax, 'Interpreter', 'latex', 'Color', [0.1, 0.7, 0.2], 'FontWeight', 'bold', 'FontSize', 13, 'HorizontalAlignment', 'center');
    
    % --- Step 7: 同步更新底部状态栏的高级公式看板 ---
    data.status_text.String = sprintf('$\\sigma_1 = \\sigma_4 = \\frac{Q_A+Q_B}{2S} = %.2f \\qquad \\sigma_2 = -\\sigma_3 = \\frac{Q_A-Q_B}{2S} = %.2f$', ...
                                      sigma1, sigma2);
                                  
    % 视窗精细美化
    title(ax, 'Boundary Charge Redistribution in Parallel Conductors', 'FontName', 'Times New Roman', 'FontSize', 14, 'FontWeight', 'bold');
    axis(ax, [-3.2, 3.2, -2.6, 2.6]);
    set(ax, 'Box', 'on', 'XTick', [], 'YTick', []);
    hold(ax, 'off');
end

function draw_charge_vectors(ax, x_pos, sigma_val)
    % 绘制符号辅助函数：依据面密度大小动态改变符号数量与密度分布
    if abs(sigma_val) < 0.02, return; end
    
    % 动态映射符号排布数目
    count = min(max(round(abs(sigma_val) * 2.5), 2), 12);
    y_coords = linspace(-1.8, 1.8, count);
    
    if sigma_val > 0
        plot(ax, ones(size(y_coords)) * x_pos, y_coords, 'r+', 'MarkerSize', 5, 'LineWidth', 1.2);
    else
        plot(ax, ones(size(y_coords)) * x_pos, y_coords, 'b_', 'MarkerSize', 5, 'LineWidth', 1.2);
    end
end