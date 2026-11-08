%% 标准卡诺循环 P-V 图（清晰美观版）
clear; clc; close all;

% ===================== 参数设置 =====================
Th = 600;          % 高温热源温度 (K)
Tc = 300;          % 低温热源温度 (K)
R  = 8.314;        % 气体常数
n  = 1;            % 物质的量 (mol)
V1 = 0.01;         % 状态1体积 (m³)
V2 = 0.03;         % 状态2体积 (m³) —— 等温膨胀终点
gamma = 1.4;       % 绝热指数

% 计算其余状态点体积
% 绝热过程：TV^{γ-1} = const
V3 = V2 * (Th/Tc)^(1/(gamma-1));   % 状态3
V4 = V1 * (Th/Tc)^(1/(gamma-1));   % 状态4

% 计算各过程压力
P1 = n*R*Th / V1;
P2 = n*R*Th / V2;
P3 = n*R*Tc / V3;
P4 = n*R*Tc / V4;

% ===================== 生成曲线数据 =====================
N = 300;   % 曲线点数，越大越平滑

% 1→2 等温膨胀 (T=Th)
V12 = linspace(V1, V2, N);
P12 = n*R*Th ./ V12;

% 2→3 绝热膨胀
V23 = linspace(V2, V3, N);
P23 = P2 * (V2 ./ V23).^gamma;

% 3→4 等温压缩 (T=Tc)
V34 = linspace(V3, V4, N);
P34 = n*R*Tc ./ V34;

% 4→1 绝热压缩
V41 = linspace(V4, V1, N);
P41 = P4 * (V4 ./ V41).^gamma;

% ===================== 图1：经典清晰版 =====================
figure('Color','w','Position',[100 100 900 700]);
hold on; box on; grid on;

plot(V12, P12, 'b-', 'LineWidth', 2.8);
plot(V23, P23, 'r-', 'LineWidth', 2.8);
plot(V34, P34, 'b-', 'LineWidth', 2.8);
plot(V41, P41, 'r-', 'LineWidth', 2.8);

% 关键状态点
plot([V1 V2 V3 V4], [P1 P2 P3 P4], 'ko', ...
    'MarkerFaceColor','y', 'MarkerSize',10, 'LineWidth',1.5);

% 文字标注
text(V1*0.92, P1*1.08, '1', 'FontSize',16, 'FontWeight','bold');
text(V2*1.02, P2*1.08, '2', 'FontSize',16, 'FontWeight','bold');
text(V3*1.02, P3*0.85, '3', 'FontSize',16, 'FontWeight','bold');
text(V4*0.88, P4*0.85, '4', 'FontSize',16, 'FontWeight','bold');

% 过程说明
text(mean(V12), max(P12)*1.12, '等温膨胀 (T_h)', ...
    'FontSize',13, 'Color','b', 'HorizontalAlignment','center');
text(mean(V23)*1.05, mean(P23), '绝热膨胀', ...
    'FontSize',13, 'Color','r', 'Rotation',-35);
text(mean(V34), min(P34)*0.82, '等温压缩 (T_c)', ...
    'FontSize',13, 'Color','b', 'HorizontalAlignment','center');
text(mean(V41)*0.85, mean(P41), '绝热压缩', ...
    'FontSize',13, 'Color','r', 'Rotation',35);

xlabel('体积 V (m^3)', 'FontSize',14, 'FontWeight','bold');
ylabel('压力 P (Pa)', 'FontSize',14, 'FontWeight','bold');
title('标准卡诺循环 P-V 图', 'FontSize',18, 'FontWeight','bold');

xlim([V1*0.7, V3*1.15]);
ylim([min(P34)*0.6, max(P12)*1.25]);
set(gca, 'FontSize',12, 'LineWidth',1.2, 'GridAlpha',0.3);
legend({'等温过程','绝热过程'}, 'Location','northeast', 'FontSize',12);

% ===================== 图2：带箭头与阴影的增强版 =====================
figure('Color','w','Position',[150 80 950 720]);
hold on; box on;

% 填充循环区域（半透明）
fill([V12, fliplr(V23), fliplr(V34), fliplr(V41)], ...
    [P12, fliplr(P23), fliplr(P34), fliplr(P41)], ...
    [0.85 0.92 1], 'EdgeColor','none', 'FaceAlpha',0.45);

% 绘制曲线
h1 = plot(V12, P12, 'Color',[0 0.45 0.74], 'LineWidth',3.2);
h2 = plot(V23, P23, 'Color',[0.85 0.33 0.10], 'LineWidth',3.2);
h3 = plot(V34, P34, 'Color',[0 0.45 0.74], 'LineWidth',3.2);
h4 = plot(V41, P41, 'Color',[0.85 0.33 0.10], 'LineWidth',3.2);

% 关键点
plot([V1 V2 V3 V4], [P1 P2 P3 P4], 'o', ...
    'MarkerSize',11, 'MarkerFaceColor',[1 0.85 0], ...
    'MarkerEdgeColor','k', 'LineWidth',1.8);

% 添加方向箭头
addArrow(V12, P12, 0.55);   % 1→2
addArrow(V23, P23, 0.55);   % 2→3
addArrow(V34, P34, 0.55);   % 3→4
addArrow(V41, P41, 0.55);   % 4→1

% 状态点标注
text(V1, P1, '  1', 'FontSize',15, 'FontWeight','bold', 'VerticalAlignment','bottom');
text(V2, P2, '  2', 'FontSize',15, 'FontWeight','bold', 'VerticalAlignment','bottom');
text(V3, P3, '  3', 'FontSize',15, 'FontWeight','bold', 'VerticalAlignment','top');
text(V4, P4, '  4', 'FontSize',15, 'FontWeight','bold', 'VerticalAlignment','top');

% 温度与过程标注
text(mean(V12), max(P12)*1.13, sprintf('等温膨胀\nT = %d K', Th), ...
    'FontSize',12, 'Color',[0 0.45 0.74], 'HorizontalAlignment','center', 'FontWeight','bold');
text(V3*1.08, mean(P23), sprintf('绝热膨胀'), ...
    'FontSize',12, 'Color',[0.85 0.33 0.10], 'FontWeight','bold', 'Rotation',-40);
text(mean(V34), min(P34)*0.78, sprintf('等温压缩\nT = %d K', Tc), ...
    'FontSize',12, 'Color',[0 0.45 0.74], 'HorizontalAlignment','center', 'FontWeight','bold');
text(V1*0.75, mean(P41), '绝热压缩', ...
    'FontSize',12, 'Color',[0.85 0.33 0.10], 'FontWeight','bold', 'Rotation',40);

xlabel('比体积 / 体积  V', 'FontSize',14, 'FontWeight','bold');
ylabel('压力  P', 'FontSize',14, 'FontWeight','bold');
title({'标准卡诺循环 P-V 图（增强版）'; ...
    '蓝色：等温过程　橙色：绝热过程'}, ...
    'FontSize',16, 'FontWeight','bold');

xlim([V1*0.65, V3*1.2]);
ylim([min(P34)*0.55, max(P12)*1.3]);
set(gca, 'FontSize',12, 'LineWidth',1.3, 'GridAlpha',0.25);
grid on;
legend([h1 h2], {'等温过程 (T=const)', '绝热过程 (Q=0)'}, ...
    'Location','northeast', 'FontSize',12, 'Box','on');

% ===================== 辅助函数：添加箭头 =====================
function addArrow(V, P, pos)
% 在曲线约 pos 位置添加方向箭头
idx = round(pos * length(V));
idx = max(2, min(idx, length(V)-1));
quiver(V(idx), P(idx), V(idx+1)-V(idx), P(idx+1)-P(idx), ...
    0, 'MaxHeadSize',1.2, 'Color','k', 'LineWidth',1.5, ...
    'AutoScale','off');
end