% 典型电流模型 3D 几何与物理矢量标注可视化
clear; clc; close all;

% 创建全屏大图以便观察细节
figure('Name', '典型电流模型 3D 物理标注', 'Position', [50, 50, 1400, 700]);

% ==========================================
% 子图 1：直导线模型 (无限长圆柱 + 环形磁场)
% ==========================================
subplot(1, 3, 1);
R_wire = 0.1; L_wire = 8;

% 1. 画导线圆柱
[THETA, Z] = meshgrid(linspace(0, 2*pi, 50), linspace(-L_wire/2, L_wire/2, 2));
X = R_wire * cos(THETA); Y = R_wire * sin(THETA);
surf(X, Y, Z, 'EdgeColor', 'none', 'FaceColor', [0.6 0.6 0.6], 'FaceAlpha', 0.5); hold on;

% 2. 标注电流 I (红色中心直线箭头)
quiver3(0, 0, -L_wire/3, 0, 0, L_wire/1.5, 0, 'Color', 'r', 'LineWidth', 3, 'MaxHeadSize', 0.5);
text(0.3, 0, L_wire/4, '电流 I', 'Color', 'r', 'FontSize', 12, 'FontWeight', 'bold');

% 3. 标注磁场 B (蓝色环绕箭头，展示右手定则)
R_B = 1.5; % 磁场线半径
theta_B = linspace(0, 2*pi, 40);
plot3(R_B*cos(theta_B), R_B*sin(theta_B), zeros(size(theta_B)), 'b--', 'LineWidth', 1.5); % 虚线圆环
% 在圆环上取几个点画箭头表示环绕方向
for idx = 1:8:40
    t = theta_B(idx);
    % 切向矢量 (-sin, cos, 0)
    quiver3(R_B*cos(t), R_B*sin(t), 0, -0.5*sin(t), 0.5*cos(t), 0, 0, 'Color', 'b', 'LineWidth', 2, 'MaxHeadSize', 2);
end
text(R_B, 1, 0.5, '磁场 \vec{B}', 'Color', 'b', 'FontSize', 12, 'FontWeight', 'bold');

title('模型 1: 直导线 (安培定则)'); 
axis equal; grid on; view(30, 30);
xlabel('X'); ylabel('Y'); zlabel('Z');

% ==========================================
% 子图 2：圆电流模型 (环体 + 轴线磁场)
% ==========================================
subplot(1, 3, 2);
R_loop = 2; R_ring = 0.1;

% 1. 画圆环体
theta_loop = linspace(0, 2*pi, 60); phi_loop = linspace(0, 2*pi, 30);
[THETA, PHI] = meshgrid(theta_loop, phi_loop);
X = (R_loop + R_ring * cos(PHI)) .* cos(THETA);
Y = (R_loop + R_ring * cos(PHI)) .* sin(THETA);
Z = R_ring * sin(PHI);
surf(X, Y, Z, 'EdgeColor', 'none', 'FaceColor', [0.8 0.6 0.2], 'FaceAlpha', 0.8); hold on;

% 2. 标注环形电流 I (红色切向箭头)
for idx = 1:12:60
    t = theta_loop(idx);
    quiver3(R_loop*cos(t), R_loop*sin(t), 0, -1*sin(t), 1*cos(t), 0, 0, 'Color', 'r', 'LineWidth', 3, 'MaxHeadSize', 1);
end
text(R_loop*1.2, 0, 0.5, '环形电流 I', 'Color', 'r', 'FontSize', 12, 'FontWeight', 'bold');

% 3. 标注中心轴线磁场 B (蓝色直线箭头)
quiver3(0, 0, -2, 0, 0, 4, 0, 'Color', 'b', 'LineWidth', 3, 'MaxHeadSize', 0.5);
text(0.2, 0.2, 2.5, '中心磁场 \vec{B}', 'Color', 'b', 'FontSize', 12, 'FontWeight', 'bold');

title('模型 2: 圆电流环'); 
axis equal; grid on; view(30, 45);
xlabel('X'); ylabel('Y'); zlabel('Z');



% ==========================================
% 子图 3：螺线管模型 (螺旋线 + 内部均匀磁场)
% ==========================================
subplot(1, 3, 3);
R_sol = 1.5; L_sol = 6; N_turns = 8;

% 1. 画螺旋线
t_sol = linspace(0, 2*pi*N_turns, 500);
Z_sol = linspace(-L_sol/2, L_sol/2, 500);
X_sol = R_sol * cos(t_sol); Y_sol = R_sol * sin(t_sol);
plot3(X_sol, Y_sol, Z_sol, 'Color', [0.5 0 0.5], 'LineWidth', 2); hold on;

% 2. 标注螺旋线上的电流 I (红色切向箭头)
% 选几个特定高度的点加箭头
idx_arrows = [100, 250, 400];
for i = 1:length(idx_arrows)
    idx = idx_arrows(i);
    % 螺旋线切向量计算
    dx = -R_sol * sin(t_sol(idx)); dy = R_sol * cos(t_sol(idx)); dz = L_sol / (2*pi*N_turns);
    % 归一化后画箭头
    vec_len = sqrt(dx^2 + dy^2 + dz^2);
    quiver3(X_sol(idx), Y_sol(idx), Z_sol(idx), 2*dx/vec_len, 2*dy/vec_len, 2*dz/vec_len, 0, 'Color', 'r', 'LineWidth', 2, 'MaxHeadSize', 1);
end
text(R_sol*1.2, 0, L_sol/3, '线圈电流 I', 'Color', 'r', 'FontSize', 12, 'FontWeight', 'bold');

% 3. 标注内部磁场 B (蓝色直线箭头，表示均匀磁场)
quiver3(0, 0, -L_sol/2, 0, 0, L_sol, 0, 'Color', 'b', 'LineWidth', 3, 'MaxHeadSize', 0.2);
% 添加两条辅助内部磁场线
quiver3(0.5, 0.5, -L_sol/2, 0, 0, L_sol, 0, 'Color', 'b', 'LineWidth', 1.5, 'MaxHeadSize', 0.2);
quiver3(-0.5, -0.5, -L_sol/2, 0, 0, L_sol, 0, 'Color', 'b', 'LineWidth', 1.5, 'MaxHeadSize', 0.2);
text(0, 0, L_sol/2 + 0.8, '内部均匀磁场 \vec{B}', 'Color', 'b', 'FontSize', 12, 'FontWeight', 'bold');

title('模型 3: 长直螺线管'); 
axis equal; grid on; view(30, 20);
xlabel('X'); ylabel('Y'); zlabel('Z');

% 调整整体标题
sgtitle('大学物理：典型电流模型的 3D 几何与电磁场矢量标注', 'FontSize', 16, 'FontWeight', 'bold');