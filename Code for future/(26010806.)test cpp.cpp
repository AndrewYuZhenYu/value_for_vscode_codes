#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <complex>
#include <set>

using namespace std;

const double EPS = 1e-12;
const int MAX_ITER = 1000;

// 三次函数
double f(double a, double b, double c, double d, double x) {
    return a*x*x*x + b*x*x + c*x + d;
}

// 三次函数的导数
double df(double a, double b, double c, double x) {
    return 3*a*x*x + 2*b*x + c;
}

// 牛顿迭代法求一个根
double newton_method(double a, double b, double c, double d, double x0) {
    double x = x0;
    for (int i = 0; i < MAX_ITER; ++i) {
        double fx = f(a, b, c, d, x);
        double dfx = df(a, b, c, x);
        
        // 如果导数接近0，尝试小幅扰动
        if (fabs(dfx) < EPS) {
            x += 0.1;
            continue;
        }
        
        double x_new = x - fx / dfx;
        
        // 防止迭代发散：重置初始值而非返回错误值
        if (fabs(x_new) > 1e6) {
            x = x0 + (i % 5) * 0.5; // 尝试附近的初始值
            continue;
        }
        
        if (fabs(x_new - x) < EPS) {
            return x_new;
        }
        x = x_new;
    }
    // 迭代次数用尽，返回无效值
    return NAN;
}

// 使用卡尔达诺公式求解三次方程（复数形式）
vector<complex<double>> solve_cubic_cardano(double a, double b, double c, double d) {
    vector<complex<double>> roots;
    
    // 归一化：除以a，使首项系数为1
    double p = b/a, q = c/a, r = d/a;
    
    // 计算判别式相关量
    double Q = (p*p - 3*q) / 9.0;
    double R = (2*p*p*p - 9*p*q + 27*r) / 54.0;
    double discriminant = R*R - Q*Q*Q;
    
    if (discriminant > EPS) { // 一个实根，两个共轭复根
        double A = -cbrt(fabs(R) + sqrt(discriminant));
        if (R < 0) A = -A;
        double B = (fabs(A) < EPS) ? 0 : Q/A;
        
        complex<double> root1(A + B - p/3.0, 0);
        complex<double> root2(-(A+B)/2.0 - p/3.0, (A-B)*sqrt(3.0)/2.0);
        complex<double> root3(-(A+B)/2.0 - p/3.0, -(A-B)*sqrt(3.0)/2.0);
        
        roots.push_back(root1);
        roots.push_back(root2);
        roots.push_back(root3);
    }
    else { // 三个实根（可能包含重根）
        // 修复Q=0的情况
        if (fabs(Q) < EPS) {
            // Q=0时，方程简化为 x³ + px + r = 0
            double root = cbrt(-r);
            roots.push_back({root - p/3.0, 0});
            roots.push_back({root - p/3.0, 0});
            roots.push_back({root - p/3.0, 0});
        } else {
            double theta = acos(min(max(R / sqrt(Q*Q*Q), -1.0), 1.0)); // 限制范围避免acos输入越界
            double sqrtQ = sqrt(Q);
            
            complex<double> root1(2*sqrtQ*cos(theta/3.0) - p/3.0, 0);
            complex<double> root2(2*sqrtQ*cos((theta + 2*M_PI)/3.0) - p/3.0, 0);
            complex<double> root3(2*sqrtQ*cos((theta + 4*M_PI)/3.0) - p/3.0, 0);
            
            roots.push_back(root1);
            roots.push_back(root2);
            roots.push_back(root3);
        }
    }
    
    return roots;
}

// 辅助函数：检查根是否已存在（去重）
bool root_exists(const vector<double>& roots, double new_root) {
    for (double r : roots) {
        if (fabs(r - new_root) < 1e-5) {
            return true;
        }
    }
    return false;
}

// 寻找区间内的实根
vector<double> find_real_roots(double a, double b, double c, double d) {
    vector<double> roots;
    
    // 扩大搜索范围，提高找到所有根的概率
    const double step = 0.1;
    const double left = -100, right = 100;
    
    // 先使用符号变化法
    double prev = f(a, b, c, d, left);
    for (double x = left + step; x <= right; x += step) {
        double curr = f(a, b, c, d, x);
        
        if (fabs(curr) < EPS) { // 直接命中根
            if (!root_exists(roots, x)) {
                roots.push_back(x);
            }
        }
        else if (prev * curr < 0) { // 符号变化，有根
            double root = newton_method(a, b, c, d, x - step/2);
            // 过滤无效值和重复值
            if (!isnan(root) && !root_exists(roots, root)) {
                roots.push_back(root);
            }
        }
        prev = curr;
    }
    
    // 使用卡尔达诺公式验证并补充实根
    auto complex_roots = solve_cubic_cardano(a, b, c, d);
    for (const auto& root : complex_roots) {
        if (fabs(root.imag()) < EPS) { // 实根
            double real_root = root.real();
            // 检查是否在合理范围内且未重复
            if (real_root >= left && real_root <= right && !root_exists(roots, real_root)) {
                roots.push_back(real_root);
            }
        }
    }
    
    // 排序并去重
    sort(roots.begin(), roots.end());
    vector<double> unique_roots;
    for (size_t i = 0; i < roots.size(); ++i) {
        if (i == 0 || fabs(roots[i] - roots[i-1]) > 1e-5) {
            unique_roots.push_back(roots[i]);
        }
    }
    
    return unique_roots;
}

// 判断是否为整数（考虑浮点误差）
bool is_integer(double x) {
    return fabs(x - round(x)) < 1e-6;
}

// 检测重根类型
void check_multiple_roots(double a, double b, double c, double d, const vector<double>& real_roots) {
    if (real_roots.empty()) return;
    
    for (double root : real_roots) {
        double df_val = df(a, b, c, root);
        double d2f_val = 6*a*root + 2*b; // 二阶导数
        
        if (fabs(df_val) < 1e-6) {
            if (fabs(d2f_val) < 1e-6) {
                cout << "\n检测到 x = " << root << " 是三重根。" << endl;
            } else {
                cout << "\n检测到 x = " << root << " 是二重根。" << endl;
            }
        }
    }
}

int main() {
    double a, b, c, d;
    cout << "=== 一元三次方程求解器 ===" << endl;
    cout << "方程形式: ax³ + bx² + cx + d = 0" << endl;
    cout << "请输入系数 a, b, c, d：" << endl;
    
    // 输入验证
    while (!(cin >> a >> b >> c >> d)) {
        cout << "输入错误，请重新输入四个数字：" << endl;
        cin.clear();
        cin.ignore(10000, '\n');
    }
    
    if (fabs(a) < EPS) {
        cout << "警告：a ≈ 0，这不是三次方程！" << endl;
        return 1;
    }
    
    // 求解实根
    vector<double> real_roots = find_real_roots(a, b, c, d);
    
    // 求解所有根（包括复数）
    auto all_roots = solve_cubic_cardano(a, b, c, d);
    
    cout << fixed << setprecision(8);
    
    // 输出实根
    if (!real_roots.empty()) {
        cout << "\n实根：" << endl;
        for (size_t i = 0; i < real_roots.size(); ++i) {
            double root = real_roots[i];
            cout << "x" << (i+1) << " = " << root;
            
            // 如果是整数，特别标注
            if (is_integer(root)) {
                cout << " (整数)";
            }
            
            // 验证根的准确性
            double residual = f(a, b, c, d, root);
            if (fabs(residual) > 1e-6) {
                cout << " [残差: " << residual << "]";
            }
            cout << endl;
        }
    } else {
        cout << "\n该方程没有实根。" << endl;
    }
    
    // 输出复根（去重）
    set<complex<double>, bool(*)(const complex<double>&, const complex<double>&)> complex_roots_set(
        [](const complex<double>& a, const complex<double>& b) {
            return fabs(a.real() - b.real()) > 1e-5 || fabs(a.imag() - b.imag()) > 1e-5;
        }
    );
    
    bool has_complex = false;
    for (const auto& root : all_roots) {
        if (fabs(root.imag()) > EPS) {
            complex_roots_set.insert(root);
            has_complex = true;
        }
    }
    
    if (has_complex) {
        cout << "\n复根：" << endl;
        for (const auto& root : complex_roots_set) {
            cout << "x = " << root.real();
            if (root.imag() >= 0) cout << " + ";
            else cout << " - ";
            cout << fabs(root.imag()) << "i" << endl;
        }
    }
    
    // 重根检测
    check_multiple_roots(a, b, c, d, real_roots);
    
    return 0;
}