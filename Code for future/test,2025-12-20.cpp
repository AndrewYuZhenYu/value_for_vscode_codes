#include <stdio.h>
int yuzhenyuniubi;
int *area()
{
    return &yuzhenyuniubi;
}
int max(int a, int b)
{
    if (a >= b)
        return a;
    else
        return b;
}
// 主函数入口
int main()
{
    int x, y;              // 定义两个整型变量x和y
    scanf("%d%d", &x, &y); // 从标准输入读取两个整数，分别存入x和y
    int (*p)(int, int);    // 定义一个函数指针p，该指针指向返回值为int，参数为两个int的函数
    p = max;               // 将函数max的地址赋值给指针p
    int m;                 // 定义整型变量m
    m = (*p)(x, y);        // 通过函数指针p调用max函数，将结果存入m
    printf("%d\n", m);     // 输出m的值
    printf("%p\n", &m);    // 输出变量m的内存地址
    printf("%p", area());
    return 0;
}