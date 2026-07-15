% =========================================================
% 三大分布(t, Chi-squared, F) 详细可视化记忆卡片 (纯MATLAB代码，无需工具箱)
% =========================================================

% 创建大尺寸画布
figure('Name', '统计学三大分布及上α分位数记忆卡片', 'Position', [100, 50, 1200, 850], 'Color', 'w');

% 定义全局颜色规范
c_line = [0.1 0.45 0.75];  % 概率密度曲线颜色 (深蓝)
c_quantile = [0.9 0.35 0.35];  % 上alpha分位数拒绝域填充颜色 (红色)
c_accept = [0.85 0.9 0.95];  % 接受域背景色 (极浅蓝)

% 设定全局参数
alpha = 0.05;

% =========================================================
% 第一排：t-分布 (Student's t-distribution)
% =========================================================
k_t = 10; % 自由度
% 手写 t-分布 PDF (避免依赖工具箱)
x_t = linspace(-4, 4, 500);
y_t = (gamma((k_t+1)/2) / (sqrt(k_t*pi) * gamma(k_t/2))) * (1 + (x_t.^2)/k_t).^(-(k_t+1)/2);

% t-分布临界值 (对应自由度10, alpha=0.05 的双侧 Z_\alpha/2 = 1.96 示意值)
cv_t = 1.812; % t_0.05(10) 单侧

% 绘图
subplot(3, 1, 1);
fill(x_t, y_t, c_accept, 'EdgeColor', 'none', 'FaceAlpha', 0.5); hold on;
plot(x_t, y_t, 'LineWidth', 2.5, 'Color', c_line);

% 上alpha分位数
idx = x_t >= cv_t;
fill([cv_t, x_t(idx), 4], [0, y_t(idx), 0], c_quantile, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
plot([cv_t cv_t], [0 interp1(x_t,y_t,cv_t)], 'r--', 'LineWidth', 1.5);

% 标签与 LaTeX 排版
title('1. t-分布 (Student''s t-distribution)', 'FontSize', 14, 'Color', [0.2 0.2 0.2]);
t_formula = '$$f(t) = \frac{\Gamma(\frac{k+1}{2})}{\sqrt{k\pi}\Gamma(\frac{k}{2})}\left(1 + \frac{t^2}{k}\right)^{-\frac{k+1}{2}}$$';
text(-3.8, 0.35, t_formula, 'Interpreter', 'latex', 'FontSize', 12);

% 关键标签
text(2.2, 0.03, '拒绝域', 'Color', 'r', 'FontWeight', 'bold');
text(cv_t, -0.02, 't_{\alpha}(k)', 'Color', 'r', 'FontSize', 12);
text(0, -0.02, '\mu=0', 'FontSize', 10);
set(gca, 'YTick', [], 'XTick', [0, cv_t], 'XTickLabel', {'0', ''}); box off;

% =========================================================
% 第二排：Chi-squared 卡方分布
% =========================================================
k_chi = 10; % 自由度
% 手写 Chi-squared PDF (避免依赖工具箱)
x_chi = linspace(0, 30, 500);
y_chi = (1/(2^(k_chi/2)*gamma(k_chi/2))) * x_chi.^(k_chi/2-1) .* exp(-x_chi/2);
y_chi(isnan(y_chi)) = 0; % 处理边界条件

% 卡方分布临界值 (自由度10, alpha=0.05 右侧 \chi^2_0.05(10))
cv_chi = 18.307;

% 绘图
subplot(3, 1, 2);
fill(x_chi, y_chi, c_accept, 'EdgeColor', 'none', 'FaceAlpha', 0.5); hold on;
plot(x_chi, y_chi, 'LineWidth', 2.5, 'Color', c_line);

% 上alpha分位数
idx = x_chi >= cv_chi;
fill([cv_chi, x_chi(idx), 30], [0, y_chi(idx), 0], c_quantile, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
plot([cv_chi cv_chi], [0 interp1(x_chi,y_chi,cv_chi)], 'r--', 'LineWidth', 1.5);

% 标签与 LaTeX 排版
title('2. \chi^2-卡方分布 (Chi-squared distribution)', 'FontSize', 14, 'Color', [0.2 0.2 0.2]);
chi_formula = '$$f(\chi^2) = \frac{1}{2^{k/2}\Gamma(k/2)}(\chi^2)^{k/2-1}e^{-\chi^2/2}$$';
text(10, 0.1, chi_formula, 'Interpreter', 'latex', 'FontSize', 12);

% 关键标签
text(20, 0.015, '拒绝域', 'Color', 'r', 'FontWeight', 'bold');
text(cv_chi, -0.005, '\chi^2_{\alpha}(k)', 'Color', 'r', 'FontSize', 12);
text(0, -0.005, '0', 'FontSize', 10);
set(gca, 'YTick', [], 'XTick', [0, cv_chi], 'XTickLabel', {'0', ''}); box off;

% =========================================================
% 第三排：F-分布
% =========================================================
d1 = 10; d2 = 20; % 自由度 (分子d1, 分母d2)
% 手写 F-分布 PDF (避免依赖工具箱)
x_f = linspace(0.01, 5, 500); % x>=0
y_f = (gamma((d1+d2)/2)/(gamma(d1/2)*gamma(d2/2))) * ...
    ((d1/d2)^(d1/2)) * (x_f.^(d1/2-1)) .* ...
    (1+(d1/d2)*x_f).^(-(d1+d2)/2);

% F-分布临界值 (分子d1=10, 分母d2=20, alpha=0.05 右侧 F_0.05(10, 20))
cv_f = 2.348;

% 绘图
subplot(3, 1, 3);
fill(x_f, y_f, c_accept, 'EdgeColor', 'none', 'FaceAlpha', 0.5); hold on;
plot(x_f, y_f, 'LineWidth', 2.5, 'Color', c_line);

% 上alpha分位数
idx = x_f >= cv_f;
fill([cv_f, x_f(idx), 5], [0, y_f(idx), 0], c_quantile, 'FaceAlpha', 0.8, 'EdgeColor', 'none');
plot([cv_f cv_f], [0 interp1(x_f,y_f,cv_f)], 'r--', 'LineWidth', 1.5);

% 标签与 LaTeX 排版
title('3. F-分布 (Fisher–Snedecor distribution)', 'FontSize', 14, 'Color', [0.2 0.2 0.2]);
f_formula = '$$f(F) = \frac{\Gamma(\frac{d_1+d_1}{2})}{\Gamma(\frac{d_1}{2})\Gamma(\frac{d_2}{2})}\left(\frac{d_1}{d_2}\right)^{\frac{d_1}{2}}F^{\frac{d_1}{2}-1}\left(1+\frac{d_1}{d_2}F\right)^{-\frac{d_1+d_2}{2}}$$';
text(1.5, 0.7, f_formula, 'Interpreter', 'latex', 'FontSize', 12);

% 关键标签
text(3, 0.1, '拒绝域', 'Color', 'r', 'FontWeight', 'bold');
text(cv_f, -0.05, 'F_{\alpha}(d_1, d_2)', 'Color', 'r', 'FontSize', 12);
text(0, -0.05, '0', 'FontSize', 10);
set(gca, 'YTick', [], 'XTick', [0, cv_f], 'XTickLabel', {'0', ''}); box off;

% 添加总标题
sgtitle('三大统计分布详细记忆卡片 (红色阴影 = 上α分位数Reject Region)', 'FontSize', 16, 'FontWeight', 'bold');