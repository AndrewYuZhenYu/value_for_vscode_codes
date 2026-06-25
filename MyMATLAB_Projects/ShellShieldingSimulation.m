function ProfessionalShellShielding()
    % PROFESSIONALSHELLSHIELDING 空腔导体屏蔽全场景科研级数值仿真看板
    % 核心算法：自适应电荷密度种子投放 + 矢量场防爆奇点内核 + 等势面柔化渲染 + 镜像电荷法
    
    % 1. 视窗骨架搭建与初始化
    fig = figure('Name', '高精空腔导体屏蔽数值仿真看板', ...
                 'Position', [50, 40, 1150, 800], 'Color', [0.96, 0.96, 0.96]);
             
    % 2. 严谨物理参数配置
    data = struct();
    data.R_in = 1.0;       % 球壳内半径
    data.R_out = 1.6;      % 球壳外半径
    data.q = 2.5;          % 内腔中心放置的点电荷量
    data.Q_she = 1.5;      % 壳体自身携带的初始净电荷
    data.x_ext = 3.4;      % 外部点电荷的 X 轴坐标 (假设 y=0)
    data.q_ext = -4.5;     % 外部点电荷量
    data.case_idx = 3;     % 默认选中最具代表性的极化情形：Case 3
    
    % 3. UI 交互组件规范化（已全部汉化）
    uicontrol('Parent', fig, 'Style', 'text', 'Position', [40, 75, 120, 20], ...
              'String', '选择仿真情景:', 'FontWeight', 'bold', 'HorizontalAlignment', 'right');
    data.dp_case = uicontrol('Parent', fig, 'Style', 'popupmenu', ...
        'String', { ...
            '情景 1: [未接地] q = 0, 外部 = 0 (纯球壳电荷分布)', ...
            '情景 2: [未接地] q > 0, 外部 = 0 (内部屏蔽与经典静电感应)', ...
            '情景 3: [未接地] q > 0, 外部 != 0 (外部极化与边界层电荷响应)', ...
            '情景 4: [已接地] q = 0, 外部 = 0 (大地吸收并中和所有过剩电荷)', ...
            '情景 5: [已接地] q > 0, 外部 = 0 (内部束缚电场隔离与屏蔽)', ...
            '情景 6: [已接地] q > 0, 外部 != 0 (完全独立的双层静电屏蔽)'}, ...
        'Value', data.case_idx, 'Position', [170, 77, 400, 20]);
    
    uicontrol('Parent', fig, 'Style', 'text', 'Position', [600, 75, 140, 20], ...
              'String', '球壳初始电荷 Q_she:', 'HorizontalAlignment', 'right');
    data.sl_Q = uicontrol('Parent', fig, 'Style', 'slider', 'Min', -5.0, 'Max', 5.0, ...
                          'Value', data.Q_she, 'Position', [750, 75, 220, 20]);
                      
    % 4. 视窗和 LaTeX 渲染状态栏分配
    data.ax = axes('Parent', fig, 'Position', [0.06, 0.20, 0.88, 0.74], 'FontName', 'Times New Roman');
    data.status_ax = axes('Parent', fig, 'Position', [0.05, 0.02, 0.9, 0.05], 'Visible', 'off');
    data.status_text = text(0.5, 0.5, '', 'Parent', data.status_ax, 'Interpreter', 'latex', ...
                            'FontSize', 13, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');

    % 5. UI 状态双向绑定
    set(data.dp_case, 'UserData', data);
    set(data.sl_Q, 'UserData', data);
    data.dp_case.Callback = @on_param_changed;
    data.sl_Q.Callback = @on_param_changed;
    
    % 6. 执行首次渲染
    render_kernel(data);
end

function on_param_changed(src, ~)
    % 监听下拉菜单和滑块的变动
    data = get(src, 'UserData');
    data.case_idx = get(data.dp_case, 'Value');
    data.Q_she = get(data.sl_Q, 'Value');
    
    set(data.dp_case, 'UserData', data);
    set(data.sl_Q, 'UserData', data);
    render_kernel(data); % 触发重绘
end

function render_kernel(data)
    ax = data.ax;
    cla(ax);
    hold(ax, 'on');
    
    % --- 1. 状态物理决策机 (解析当前设定的物理边界条件) ---
    q_curr = data.q;
    ext_active = false;
    grounded = false;
    
    switch data.case_idx
        case 1, q_curr = 0;
        case 2, % 基础感应，维持默认
        case 3, ext_active = true;
        case 4, q_curr = 0; grounded = true;
        case 5, grounded = true;
        case 6, ext_active = true; grounded = true;
    end
    
    % 计算内/外表面总电荷量的精确代数解
    Q_in = -q_curr; % 高斯定理：内表面始终感应等量异号电荷
    if ~grounded
        Q_out = data.Q_she + q_curr; % 电荷守恒：外表面 = 初始总净电荷 + 内电荷排斥出来的电荷
    else
        if ext_active
            Q_out = -data.q_ext * (data.R_out / data.x_ext); % 接地极化：大地补充电荷抵消外部点电荷电势
        else
            Q_out = 0; % 仅接地且无外部电场：外表面多余电荷流入大地
        end
    end
    
    % --- 2. 构造高精防爆奇点数域网络 ---
    [X, Y] = meshgrid(linspace(-4.5, 4.5, 250), linspace(-4.5, 4.5, 250));
    R = sqrt(X.^2 + Y.^2);
    V = zeros(size(X));
    
    k = 1.0; 
    delta = 1e-4; % 奇点平滑柔化因子，防止 1/0 导致矩阵出现 NaN
    
    % 镜像电荷参数准备
    q_img = 0; x_img = 0;
    if ext_active
        q_img = -data.q_ext * (data.R_out / data.x_ext); % 镜像电荷量
        x_img = (data.R_out^2) / data.x_ext;             % 镜像电荷位置
    end
    
    % 全空间连续解析势场解算
    for i = 1:numel(X)
        r = R(i);
        if r < data.R_in  % 区域 A: 内部空腔
            v_base = k * q_curr / sqrt(r^2 + delta) + k * Q_in / data.R_in + k * Q_out / data.R_out;
            if ext_active && ~grounded
                % 外部电场使得整个金属壳电势抬升
                v_base = v_base + k * data.q_ext / data.x_ext; 
            end
            if grounded && ext_active
                % 接地时金属壳强行拉为0，因此内部等效为孤立电荷
                v_base = k * q_curr / sqrt(r^2 + delta) - k * q_curr / data.R_in; 
            end
            V(i) = v_base;
            
        elseif r >= data.R_in && r <= data.R_out  % 区域 B: 导体内（静电平衡区域）
            if grounded
                V(i) = 0; % 接地导体等势体为 0V
            else
                V(i) = k * Q_out / data.R_out;
                if ext_active
                    V(i) = V(i) + k * data.q_ext / data.x_ext; % 外部电场诱导整个壳体抬升电势
                end
            end
            
        else  % 区域 C: 外部联通空间 (引入严谨的镜像电荷法)
            if ext_active
                v_ext_charge = k * data.q_ext / sqrt((X(i)-data.x_ext)^2 + Y(i)^2 + delta);
                v_img = k * q_img / sqrt((X(i)-x_img)^2 + Y(i)^2 + delta);
                
                if ~grounded
                    % 未接地时，除镜像电荷外，中心还需要放置剩余电荷以保证总外层电量守恒
                    q_center_eff = Q_out - q_img; 
                    v_center = k * q_center_eff / r;
                    V(i) = v_ext_charge + v_img + v_center;
                else
                    % 接地时，仅由外部点电荷与镜像电荷贡献
                    V(i) = v_ext_charge + v_img;
                end
            else
                if ~grounded
                    V(i) = k * Q_out / r;
                else
                    V(i) = 0;
                end
            end
        end
    end
    
    % --- 3. 等势场彩虹渲染层 ---
    contourf(ax, X, Y, V, 50, 'LineColor', 'none');
    colormap(ax, jet(256));
    
    % 动态控制色彩对比度
    clim_min = min(V(:)) * 0.5;
    clim_max = max(V(:)) * 0.5 + 0.2;
    if clim_min >= clim_max, clim_max = clim_min + 1; end 
    set(ax, 'CLim', [clim_min, clim_max]);
    
    % --- 4. 高阶数值梯度求解电场 ---
    [Ex, Ey] = gradient(-V, X(1,2)-X(1,1), Y(2,1)-Y(1,1));
    
    % 绝对清空静电平衡体内及屏蔽钝化区的数值噪声，保证内部场强严格为0
    in_shell = (R >= data.R_in & R <= data.R_out);
    Ex(in_shell) = 0; Ey(in_shell) = 0;
    if grounded && ~ext_active
        Ex(R > data.R_out) = 0; Ey(R > data.R_out) = 0;
    end
    
    % --- 5. 自适应电荷密度种子追踪算法 ---
    sx = []; sy = [];
    
    % 种子类型A：内空腔场线种子（均匀投放）
    if q_curr > 0
        th_in = linspace(0, 2*pi, 17); th_in(end) = [];
        sx = [sx, 0.08 * cos(th_in)];
        sy = [sy, 0.08 * sin(th_in)];
    end
    
    % 种子类型B：外表面场线种子，依据极化面密度非均匀自适应选择投放点
    if abs(Q_out) > 0.05 && (~grounded || (grounded && ext_active))
        th_out = linspace(0, 2*pi, 24); th_out(end) = [];
        for t = th_out
            bias = 1.0;
            if ext_active, bias = 1.0 + 0.65 * cos(t); end 
            if bias > 1.2
                sx = [sx, (data.R_out + 0.02) * cos(t), (data.R_out + 0.02) * cos(t + 0.04)];
                sy = [sy, (data.R_out + 0.02) * sin(t), (data.R_out + 0.02) * sin(t + 0.04)];
            else
                sx = [sx, (data.R_out + 0.02) * cos(t)];
                sy = [sy, (data.R_out + 0.02) * sin(t)];
            end
        end
    end
    
    % 种子类型C：外部独立电荷种子投放
    if ext_active
        th_ext = linspace(0, 2*pi, 16); th_ext(end) = [];
        sx = [sx, data.x_ext + 0.12 * cos(th_ext)];
        sy = [sy, 0.12 * sin(th_ext)];
    end
    
    % --- 6. 流线追踪与方向箭头融合渲染 ---
    if ~isempty(sx)
        h_paths = streamline(X, Y, Ex, Ey, sx, sy);
        set(h_paths, 'Color', [0.12, 0.12, 0.12, 0.70], 'LineWidth', 1.3);
        
        % 动态沿流线矩阵抽取中间点，补齐方向指示箭头
        for idx = 1:numel(h_paths)
            xp = get(h_paths(idx), 'XData');
            yp = get(h_paths(idx), 'YData');
            if ~isempty(xp) && numel(xp) > 25
                mid_node = round(numel(xp) * 0.5); 
                ux = xp(mid_node+1) - xp(mid_node);
                uy = yp(mid_node+1) - yp(mid_node);
                u_len = sqrt(ux^2 + uy^2 + 1e-8);
                quiver(ax, xp(mid_node), yp(mid_node), (ux/u_len)*0.15, (uy/u_len)*0.15, 0, ...
                       'Color', [0.1, 0.1, 0.1], 'LineWidth', 1.5, 'MaxHeadSize', 0.6);
            end
        end
    end
    
    % --- 7. 金属实体及表面微观电荷覆盖层 ---
    th_mesh = linspace(0, 2*pi, 250);
    fill(ax, [data.R_out*cos(th_mesh), fliplr(data.R_in*cos(th_mesh))], ...
             [data.R_out*sin(th_mesh), fliplr(data.R_in*sin(th_mesh))], ...
             [0.92, 0.92, 0.92], 'EdgeColor', [0.15, 0.15, 0.15], 'LineWidth', 2);
         
    % 离散化正负电荷符号刷新
    phi_s = linspace(0, 2*pi, 20); phi_s(end) = [];
    if abs(Q_in) > 0.01
        plot(ax, data.R_in * 0.92 * cos(phi_s), data.R_in * 0.92 * sin(phi_s), 'b_', 'MarkerSize', 5, 'LineWidth', 1.5);
    end
    if abs(Q_out) > 0.01
        for p = phi_s
            b = 1.0; if ext_active, b = 1.0 + 0.65*cos(p); end
            if Q_out * b > 0
                plot(ax, data.R_out * 1.07 * cos(p), data.R_out * 1.07 * sin(p), 'r+', 'MarkerSize', 5, 'LineWidth', 1.5);
            else
                plot(ax, data.R_out * 1.07 * cos(p), data.R_out * 1.07 * sin(p), 'b_', 'MarkerSize', 5, 'LineWidth', 1.5);
            end
        end
    end
    
    % 点源实体和接地排线图示
    if q_curr > 0
        plot(ax, 0, 0, 'wo', 'MarkerFaceColor', [0.75 0.1 0.1], 'MarkerSize', 9);
    end
    if ext_active
        plot(ax, data.x_ext, 0, 'wo', 'MarkerFaceColor', [0.1 0.1 0.75], 'MarkerSize', 9);
    end
    if grounded
        plot(ax, [0, 0], [-data.R_out, -data.R_out - 0.4], 'k-', 'LineWidth', 2);
        for gy = linspace(-data.R_out - 0.4, -data.R_out - 0.6, 3)
            gw = 0.35 * (1 - (abs(gy - (-data.R_out - 0.4)) / 0.25));
            plot(ax, [-gw, gw], [gy, gy], 'k-', 'LineWidth', 2);
        end
    end
    
    % 核心物理结论强力加粗（内部场强恒为零）
    text(ax, 0, (data.R_in + data.R_out)/2, '$\mathbf{E_{\mathrm{导体内部}} \equiv 0}$', ...
         'Interpreter', 'latex', 'Color', [0.1, 0.5, 0.1], 'FontSize', 12, ...
         'HorizontalAlignment', 'center', 'FontWeight', 'bold');

    % --- 8. LaTeX 看板公式实时刷新 ---
    status_str = sprintf('$Q_{\\mathrm{in}} = -q = %.2f \\qquad Q_{\\mathrm{out}} = %.2f \\qquad U_{\\mathrm{shell}} = %s$', ...
                         Q_in, Q_out, calc_pot_string(grounded, ext_active, Q_out, data));
    data.status_text.String = status_str;
    
    % 视窗精细打磨
    title(ax, ['科研级数值仿真框架：情景 ', num2str(data.case_idx)], 'FontSize', 14, 'FontWeight', 'bold');
    axis(ax, [-4.5, 4.5, -3.2, 3.2]); axis(ax, 'equal');
    set(ax, 'Box', 'on', 'XTick', [], 'YTick', []);
    hold(ax, 'off');
end

function s = calc_pot_string(grounded, ext_active, Q_out, data)
    % 实时计算当前的壳体绝对电势
    if grounded
        s = '0.00 \, \mathrm{V} \, \mathrm{(已接地)}';
    else
        U_val = Q_out / data.R_out;
        if ext_active
            U_val = U_val + data.q_ext / data.x_ext; 
        end
        s = [num2str(U_val * 8.99, '%.2f'), ' \, \mathrm{V}'];
    end
end