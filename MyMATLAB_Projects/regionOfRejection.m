% =========================================================
% 针对笔记定制：正态总体样本均值的六大拒绝域可视化对照图
% 运行此代码将生成一张完美的记忆卡片，包含你的原版公式
% =========================================================

% 创建大尺寸画布
figure('Name', '样本均值六大拒绝域(骨架与开关对照法)', 'Position', [100, 50, 1200, 850], 'Color', 'w');

% 生成正态分布数据作为底图骨架 (中心点为 mu_0)
x = linspace(-4, 4, 500);
y = exp(-0.5 * x.^2) / sqrt(2*pi); 

% 颜色设定
c_line = [0.2 0.45 0.7];   % 曲线颜色
c_rej  = [0.9 0.35 0.35];  % 拒绝域颜色

% 临界值占位 (仅作可视化示意)
cv_2 = 1.96; % 双侧临界值
cv_1 = 1.65; % 单侧临界值

% ==================== 第一排：双侧检验 (H1: 不等于) ====================

% 笔记(1)：sigma 已知，双侧
subplot(3, 2, 1);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([-4, x(x<=-cv_2), -cv_2], [0, y(x<=-cv_2), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
fill([cv_2, x(x>=cv_2), 4], [0, y(x>=cv_2), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([-cv_2, -cv_2], [0, 0.2], 'r--'); plot([cv_2, cv_2], [0, 0.2], 'r--');
title('笔记(1): \sigma^2 已知, H_1: \mu \neq \mu_0', 'FontSize', 12);
eq1 = '$$(-\infty, \mu_0 - \frac{\sigma}{\sqrt{n}}Z_{\alpha/2}] \cup [\mu_0 + \frac{\sigma}{\sqrt{n}}Z_{\alpha/2}, +\infty)$$';
text(0, -0.08, eq1, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% 笔记(2)：sigma 未知，双侧
subplot(3, 2, 2);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([-4, x(x<=-cv_2), -cv_2], [0, y(x<=-cv_2), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
fill([cv_2, x(x>=cv_2), 4], [0, y(x>=cv_2), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([-cv_2, -cv_2], [0, 0.2], 'r--'); plot([cv_2, cv_2], [0, 0.2], 'r--');
title('笔记(2): \sigma^2 未知, H_1: \mu \neq \mu_0', 'FontSize', 12);
eq2 = '$$(-\infty, \mu_0 - \frac{S}{\sqrt{n}}t_{\alpha/2}(n-1)] \cup [\mu_0 + \frac{S}{\sqrt{n}}t_{\alpha/2}(n-1), +\infty)$$';
text(0, -0.08, eq2, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% ==================== 第二排：右侧检验 (H1: 大于) ====================

% 笔记(3)：sigma 已知，右侧
subplot(3, 2, 3);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([cv_1, x(x>=cv_1), 4], [0, y(x>=cv_1), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([cv_1, cv_1], [0, 0.2], 'r--');
title('笔记(3): \sigma^2 已知, H_1: \mu > \mu_0', 'FontSize', 12);
eq3 = '$$[\mu_0 + \frac{\sigma}{\sqrt{n}}Z_{\alpha}, +\infty)$$';
text(0, -0.08, eq3, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% 笔记(5)：sigma 未知，右侧 (对应你笔记里的第5条)
subplot(3, 2, 4);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([cv_1, x(x>=cv_1), 4], [0, y(x>=cv_1), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([cv_1, cv_1], [0, 0.2], 'r--');
title('笔记(5): \sigma^2 未知, H_1: \mu > \mu_0', 'FontSize', 12);
eq5 = '$$[\mu_0 + \frac{S}{\sqrt{n}}t_{\alpha}(n-1), +\infty)$$';
text(0, -0.08, eq5, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% ==================== 第三排：左侧检验 (H1: 小于) ====================

% 笔记(4)：sigma 已知，左侧
subplot(3, 2, 5);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([-4, x(x<=-cv_1), -cv_1], [0, y(x<=-cv_1), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([-cv_1, -cv_1], [0, 0.2], 'r--');
title('笔记(4): \sigma^2 已知, H_1: \mu < \mu_0', 'FontSize', 12);
eq4 = '$$(-\infty, \mu_0 - \frac{\sigma}{\sqrt{n}}Z_{\alpha}]$$';
text(0, -0.08, eq4, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% 笔记(6)：sigma 未知，左侧
subplot(3, 2, 6);
plot(x, y, 'LineWidth', 2, 'Color', c_line); hold on;
fill([-4, x(x<=-cv_1), -cv_1], [0, y(x<=-cv_1), 0], c_rej, 'FaceAlpha', 0.6, 'EdgeColor','none');
plot([-cv_1, -cv_1], [0, 0.2], 'r--');
title('笔记(6): \sigma^2 未知, H_1: \mu < \mu_0', 'FontSize', 12);
eq6 = '$$(-\infty, \mu_0 - \frac{S}{\sqrt{n}}t_{\alpha}(n-1)]$$';
text(0, -0.08, eq6, 'Interpreter', 'latex', 'FontSize', 13, 'HorizontalAlignment', 'center');
set(gca, 'YTick', [], 'XTick', 0, 'XTickLabel', '\mu_0'); ylim([-0.15, 0.45]); box off;

% 添加总标题
sgtitle('对照记忆：中心点永远是 \mu_0，左列用 \sigma 和 Z，右列用 S 和 t', 'FontSize', 15, 'FontWeight', 'bold', 'Color', [0.2 0.2 0.2]);