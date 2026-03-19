#include <stdio.h>
#include <math.h>

// 计算阶乘
double factorial(int n) {
    double result = 1.0;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// 计算序列和
double sumFunc(double x) {
    double sum = 0.0;
    double term = 0.0;
    int n = 1;
    int sign = 1;  // 符号，正负交替
    
    do {
        // 计算当前项的值: sign * (x^n / n!)
        term = sign * pow(x, n) / factorial(n);
        sum += term;
        
        // 更新符号和指数
        sign = -sign;
        n++;
    } while (fabs(term) >= 1e-5);  // 直到最后一项的绝对值小于10^-5
    
    return sum;
}

int main() {
    double x, result;
    
    // 输入实数x
    printf("请输入实数x: ");
    scanf("%lf", &x);
    
    // 调用函数计算结果
    result = sumFunc(x);
    
    // 输出结果，保留两位小数
    printf("计算结果: %.2f\n", result);
    
    return 0;
}