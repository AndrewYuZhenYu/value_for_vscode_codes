#include<iostream>
#include"CComplex.h"

using namespace std;

int main()
{
    cout << "===== 1.创建复数对象(调用构造函数,默认初始化为0+0i) =====" << endl;
    CComplex c1;
    CComplex c2;
    CComplex result;

    cout<<"=====请依次输入第一个复数的实部和虚部，用空格分隔====="<<endl;
    c1.SetValue();
    cout<<"=====请依次输入第二个复数的实部和虚部，用空格分隔====="<<endl;
    c2.SetValue();
    cout << "===== 显示两个复数(调用ShowValue) =====" << endl;
    cout << "c1 = ";
    c1.ShowValue();
    cout <<endl;
    cout << "c2 = ";
    c2.ShowValue();
    cout << endl;

    cout << "===== 四则运算 =====" << endl;

    cout << "加法结果: ";
    result = c1.Add(c2);
    result.ShowValue();
    cout << endl;

    cout << "减法结果: ";
    result = c1.Substract(c2);
    result.ShowValue();
    cout << endl;

    cout << "乘法结果: ";
    result = c1.Multiply(c2);
    result.ShowValue();
    cout << endl;

    cout << "除法结果: ";
    result = c1.Divide(c2);
    result.ShowValue();
    cout << endl;

    cout << "===== 程序结束,以下为对象析构(调用析构函数) =====" << endl;

    return 0;
}
