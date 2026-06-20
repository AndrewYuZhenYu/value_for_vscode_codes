% ============================================================
% 球面坐标系 交互式示意图 (改进版)
% 纯脚本，无任何 function 定义，任何 MATLAB 版本都能跑
% 直接 F5 / Ctrl+Enter / 复制粘贴到命令行均可
% 拖动滑动条后点击 "刷新绘图" 按钮更新图形
% ============================================================
clf; clear; clc;

%% ==================== 颜色定义 ====================
CR  = [0.95 0.30 0.25];   % 红 - r
CP  = [0.20 0.55 0.95];   % 蓝 - 投影
CPH = [0.75 0.30 0.85];   % 紫 - phi
CTH = [0.20 0.75 0.30];   % 绿 - theta
CD  = [0.45 0.45 0.45];   % 灰 - 虚线
CZ  = [1.00 0.55 0.10];   % 橙色 - z分量(rcosphi)

%% ==================== 创建窗口和控件 ====================
fig = figure('Color','w','Position',[80 80 1050 750],...
    'Name','球面坐标系 - 交互式','NumberTitle','off');

ax = axes('Parent',fig,'Position',[0.05 0.18 0.62 0.78]);

% --- 滑动条 ---
uicontrol('Style','text','String','r =','FontSize',11,...
    'FontWeight','bold','Position',[60 82 30 22],...
    'BackgroundColor','w','ForegroundColor',CR);
sl_r = uicontrol('Style','slider','Min',0.2,'Max',2.0,'Value',1.0,...
    'Position',[95 82 300 20],'SliderStep',[0.05/1.8 0.2/1.8]);
txt_r = uicontrol('Style','text','String','1.00','FontSize',11,...
    'Position',[400 82 50 22],'BackgroundColor','w',...
    'ForegroundColor',CR,'FontWeight','bold');

uicontrol('Style','text','String','phi =','FontSize',11,...
    'FontWeight','bold','Position',[52 52 38 22],...
    'BackgroundColor','w','ForegroundColor',CPH);
sl_phi = uicontrol('Style','slider','Min',0,'Max',180,'Value',35,...
    'Position',[95 52 300 20],'SliderStep',[1/180 10/180]);
txt_phi = uicontrol('Style','text','String','35 deg','FontSize',11,...
    'Position',[400 52 55 22],'BackgroundColor','w',...
    'ForegroundColor',CPH,'FontWeight','bold');

uicontrol('Style','text','String','theta =','FontSize',11,...
    'FontWeight','bold','Position',[42 22 48 22],...
    'BackgroundColor','w','ForegroundColor',CTH);
sl_theta = uicontrol('Style','slider','Min',0,'Max',360,'Value',60,...
    'Position',[95 22 300 20],'SliderStep',[1/360 10/360]);
txt_theta = uicontrol('Style','text','String','60 deg','FontSize',11,...
    'Position',[400 22 55 22],'BackgroundColor','w',...
    'ForegroundColor',CTH,'FontWeight','bold');

% --- 刷新按钮 ---
uicontrol('Style','pushbutton','String','刷新绘图','FontSize',13,...
    'FontWeight','bold','Position',[470 40 100 50],...
    'BackgroundColor',[0.25 0.55 0.95],'ForegroundColor','w',...
    'Callback','set(gcf,''UserData'',''refresh'')');

% --- 信息面板 ---
info_panel = uicontrol('Style','text','FontSize',11,'FontName','Consolas',...
    'HorizontalAlignment','left','Position',[720 240 300 240],...
    'BackgroundColor','w');

% --- 图例 ---
uicontrol('Style','text','String',{...
    '[ 图 例 ]',...
    '红 —— r 矢量',...
    '蓝 —— r sin(phi) 投影',...
    '紫 —— phi 天顶角',...
    '绿 —— theta 方位角',...
    '橙 —— r cos(phi) z分量',...
    '灰 -- 辅助虚线'},...
    'FontSize',11,'HorizontalAlignment','left',...
    'Position',[720 120 260 110],'BackgroundColor','w');

uicontrol('Style','text','String','拖动滑动条 → 点击 [刷新绘图]',...
    'FontSize',10,'Position',[460 15 120 22],'BackgroundColor','w',...
    'ForegroundColor',[0.5 0.5 0.5]);

%% ==================== 绘图主逻辑（用 while 循环 + 按钮触发）====================
prev_r = -1; prev_phi = -1; prev_theta = -1;
view(ax, 130, 25);

while ishandle(fig)
    % 读取当前值
    r         = get(sl_r, 'Value');
    phi_deg   = round(get(sl_phi, 'Value'));
    theta_deg = round(get(sl_theta, 'Value'));

    % 更新数字显示（轻量操作，每次都做）
    set(txt_r,     'String', sprintf('%.2f', r));
    set(txt_phi,   'String', sprintf('%d deg', phi_deg));
    set(txt_theta, 'String', sprintf('%d deg', theta_deg));

    % 只在值变化时重绘
    need_draw = false;
    if abs(r - prev_r) > 0.001 || phi_deg ~= prev_phi || theta_deg ~= prev_theta
        need_draw = true;
    end
    % 也响应按钮
    if strcmp(get(fig,'UserData'), 'refresh')
        need_draw = true;
        set(fig,'UserData','');
    end

    if need_draw
        prev_r = r; prev_phi = phi_deg; prev_theta = theta_deg;
        phi_rad   = deg2rad(phi_deg);
        theta_rad = deg2rad(theta_deg);

        px = r * sin(phi_rad) * cos(theta_rad);
        py = r * sin(phi_rad) * sin(theta_rad);
        pz = r * cos(phi_rad);
        rsinphi = r * sin(phi_rad);

        [az_v, el_v] = view(ax);

        cla(ax); hold(ax, 'on');
        axis(ax, 'equal'); grid(ax, 'on');
        ax.GridAlpha = 0.15; ax.FontSize = 11;
        ax.Projection = 'perspective';
        xlabel(ax,'X','FontSize',13,'FontWeight','bold');
        ylabel(ax,'Y','FontSize',13,'FontWeight','bold');
        zlabel(ax,'Z','FontSize',13,'FontWeight','bold');

        lim = max(r*1.3, 1.3);
        axis(ax, [-0.3 lim -0.3 lim -0.3 lim]);

        % ======== 半透明球面 ========
        [Xs,Ys,Zs] = sphere(40);
        surf(ax, r*Xs, r*Ys, r*Zs, 'FaceColor',[0.6 0.75 1],...
            'EdgeColor','none','FaceAlpha',0.05,'FaceLighting','gouraud');

        % 赤道圈 + 经线
        tc = linspace(0, 2*pi, 100);
        plot3(ax,r*cos(tc),r*sin(tc),zeros(size(tc)),'Color',[0.6 0.7 0.85 0.3],'LineWidth',0.8);
        plot3(ax,r*cos(tc),zeros(size(tc)),r*sin(tc),'Color',[0.6 0.7 0.85 0.2],'LineWidth',0.5);
        plot3(ax,zeros(size(tc)),r*cos(tc),r*sin(tc),'Color',[0.6 0.7 0.85 0.2],'LineWidth',0.5);

        % ======== 半透明底面 ========
        [Xg,Yg] = meshgrid(linspace(-0.3,lim,2));
        surf(ax,Xg,Yg,zeros(size(Xg)),'FaceColor',[0.5 0.5 0.8],'EdgeColor','none','FaceAlpha',0.04);

        % ======== 坐标轴 ========
        al = lim * 0.95;
        quiver3(ax,0,0,0,al,0,0,0,'Color','k','LineWidth',2,'MaxHeadSize',0.06);
        quiver3(ax,0,0,0,0,al,0,0,'Color','k','LineWidth',2,'MaxHeadSize',0.06);
        quiver3(ax,0,0,0,0,0,al,0,'Color','k','LineWidth',2,'MaxHeadSize',0.06);
        text(ax,al+0.08,0,0,'\bf X','FontSize',14);
        text(ax,0,al+0.08,0,'\bf Y','FontSize',14);
        text(ax,0,0,al+0.08,'\bf Z','FontSize',14);

        % ======== 主矢量 r ========
        quiver3(ax,0,0,0,px,py,pz,0,'Color',CR,'LineWidth',3.5,'MaxHeadSize',0.15);
        plot3(ax,px,py,pz,'o','MarkerSize',9,'MarkerFaceColor',CR,'MarkerEdgeColor','w','LineWidth',1.5);

        % r 标注
        np = cross([px py pz],[0 0 1]);
        if norm(np)<1e-6, np = cross([px py pz],[0 1 0]); end
        if norm(np)>1e-6, np = np/norm(np)*0.07; else, np = [0.07 0 0]; end
        text(ax,0.48*px+np(1),0.48*py+np(2),0.48*pz+np(3),...
            '$\mathbf{r}$','FontSize',18,'Color',CR,'Interpreter','latex');

        % P 点坐标
        text(ax,px+0.08,py+0.05,pz+0.1,...
            sprintf('$P(%.2f,\\,%.2f,\\,%.2f)$',px,py,pz),...
            'FontSize',11,'Interpreter','latex','Color',[0.2 0.2 0.2]);

        % ======== 投影和辅助线 ========
        plot3(ax,[px px],[py py],[0 pz],'--','Color',CD,'LineWidth',1.2);

        if rsinphi > 0.02
            quiver3(ax,0,0,0,px,py,0,0,'Color',CP,'LineWidth',2.5,'MaxHeadSize',0.12);
            text(ax,px*0.45,py*0.45,-0.08,'$r\sin\phi$','FontSize',14,...
                'Color',CP,'Interpreter','latex','HorizontalAlignment','center');
            plot3(ax,px,py,0,'s','MarkerSize',7,'MarkerFaceColor',CP,'MarkerEdgeColor','w');
            text(ax,px+0.06,py+0.04,-0.06,"$P'$",'FontSize',12,'Color',CP,'Interpreter','latex');
        end

        plot3(ax,[px px],[0 py],[0 0],':','Color',CP,'LineWidth',1);
        plot3(ax,[0 px],[py py],[0 0],':','Color',CP,'LineWidth',1);

        % ======== r*cos(phi) — Z轴分量（醒目橙红色）========
        if abs(pz) > 0.05
            % Z轴上的粗实线段
            plot3(ax,[0 0],[0 0],[0 pz],'-','Color',CZ,'LineWidth',3.5);
            % P 点向 Z 轴的水平虚线 → 突出 r*cos(phi) 在 Z 轴上的位置
            plot3(ax,[px 0],[py 0],[pz pz],'--','Color',CZ,'LineWidth',2);
            % Z轴上端点标记
            plot3(ax,0,0,pz,'o','MarkerSize',7,'MarkerFaceColor',CZ,'MarkerEdgeColor','w','LineWidth',1.5);
            % 带背景框的标注
            text(ax,-0.15,-0.06,pz*0.5,...
                '$r\cos\phi$','FontSize',15,'Color',CZ,...
                'Interpreter','latex','HorizontalAlignment','right',...
                'BackgroundColor',[1 1 1 0.7],'EdgeColor',CZ,'Margin',2);
        end

        % ======== 直角标记 ========
        if rsinphi > 0.08 && abs(pz) > 0.05
            srt = 0.06;
            dxy = [px py 0]/rsinphi;
            cpt = [px py 0];
            q1 = cpt - srt*dxy;
            q2 = q1 + [0 0 srt];
            q3 = cpt + [0 0 srt];
            plot3(ax,[q1(1) q2(1)],[q1(2) q2(2)],[q1(3) q2(3)],'k-','LineWidth',1);
            plot3(ax,[q2(1) q3(1)],[q2(2) q3(2)],[q2(3) q3(3)],'k-','LineWidth',1);
        end

        % ======== phi 弧线（天顶角）========
        nn = 50;
        if phi_deg > 1
            ra1 = 0.35*r;
            tp = linspace(0, phi_rad, nn);
            apx = ra1*sin(tp)*cos(theta_rad);
            apy = ra1*sin(tp)*sin(theta_rad);
            apz = ra1*cos(tp);
            plot3(ax,apx,apy,apz,'Color',CPH,'LineWidth',3);
            fill3(ax,[0 apx 0],[0 apy 0],[0 apz 0],CPH,'FaceAlpha',0.08,'EdgeColor','none');
            mp = phi_rad*0.5; lr1 = ra1+0.1;
            text(ax,lr1*sin(mp)*cos(theta_rad),lr1*sin(mp)*sin(theta_rad),lr1*cos(mp),...
                '$\phi$','FontSize',20,'Color',CPH,'Interpreter','latex');
        end

        % ======== theta 弧线（方位角）========
        if theta_deg > 1 && rsinphi > 0.02
            ra2 = 0.18*r;
            tt = linspace(0, theta_rad, nn);
            atx = ra2*cos(tt);
            aty = ra2*sin(tt);
            atz = zeros(size(tt));
            plot3(ax,atx,aty,atz,'Color',CTH,'LineWidth',2.5);
            fill3(ax,[0 atx 0],[0 aty 0],[0 atz 0],CTH,'FaceAlpha',0.06,'EdgeColor','none');
            mt = theta_rad*0.5; lr2 = ra2+0.08;
            text(ax,lr2*cos(mt),lr2*sin(mt),0.03,...
                '$\theta$','FontSize',16,'Color',CTH,'Interpreter','latex');
        end

        % ======== 标题 ========
        title(ax, sprintf('球面坐标系   r = %.2f,  \\phi = %d°,  \\theta = %d°',...
            r,phi_deg,theta_deg),'FontSize',14,'FontWeight','bold');

        % ======== 信息面板 ========
        set(info_panel, 'String', {
            '====== 球面坐标 ======'
            sprintf('  r     = %.3f', r)
            sprintf('  phi   = %d deg  (%.3f rad)', phi_deg, phi_rad)
            sprintf('  theta = %d deg  (%.3f rad)', theta_deg, theta_rad)
            ''
            '====== 笛卡尔坐标 ======'
            sprintf('  x = r*sin(phi)*cos(theta) = %.4f', px)
            sprintf('  y = r*sin(phi)*sin(theta) = %.4f', py)
            sprintf('  z = r*cos(phi)            = %.4f', pz)
            ''
            '====== 中间量 ======'
            sprintf('  r*sin(phi) = %.4f', rsinphi)
            sprintf('  r*cos(phi) = %.4f', r*cos(phi_rad))
        });

        lighting(ax,'gouraud'); camlight(ax,'headlight');
        view(ax, az_v, el_v);
        hold(ax,'off');
    end

    % 暂停一小段时间，让 UI 响应（不卡 MATLAB）
    pause(0.15);
end

disp('窗口已关闭。');