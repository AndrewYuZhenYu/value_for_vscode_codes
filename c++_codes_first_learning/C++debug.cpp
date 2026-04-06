#include <iostream>

using namespace std;

// 一个简单的计算阶乘的函数，用来测试“步入 (Step Into)”
long long factorial(int n)
{
    long long res = 1;
    for (int i = 1; i <= n; i++)
    {
        res *= i; // 可以在这里打断点，观察 res 的累乘过程
    }
    return res;
}

int main()
{
    int limit = 3;
    long long totalSum = 0;

    cout << "开始计算阶乘之和..." << endl;

    for (int i = 1; i <= limit; i++)
    {
        // 1. 运行到这一行时，尝试点“步入 (Step Into)”，进入 factorial 内部
        // 2. 在 factorial 内部待腻了，点“步出 (Step Out)”回到这里
        long long currentFactorial = factorial(i);

        totalSum += currentFactorial;

        // 观察右侧变量栏，看 totalSum 每一轮的变化
        cout << i << "! = " << currentFactorial << endl;
    }

    cout << "最终总和为: " << totalSum << endl;

    return 0;
}