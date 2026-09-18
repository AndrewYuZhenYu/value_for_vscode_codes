#include<iostream>
#include"CComplex.h"
using namespace std;
CComplex::CComplex(double zR, double zI)
{
    mR = zR;
    mI = zI;

    cout << "<==";
    ShowValue();
    cout << endl;
}

// 析构函数
CComplex::~CComplex()
{
    ShowValue();
    cout << "=>" << endl;
}

// 无参数设置
void CComplex::SetValue()
{
    cin >> mR >> mI;
}

// 有参数设置
void CComplex::SetValue(double zR, double zI)
{
    mR = zR;
    mI = zI;
}

// 显示复数
void CComplex::ShowValue()
{
    if(mI >= 0)
        cout << mR << "+" << mI << "i";
    else
        cout << mR << mI << "i";
}

// 加法
CComplex CComplex::Add(const CComplex& zC) const
{
    return CComplex(
        mR + zC.mR,
        mI + zC.mI
    );
}

// 减法
CComplex CComplex::Substract(const CComplex& zC) const
{
    return CComplex(
        mR - zC.mR,
        mI - zC.mI
    );
}

// 乘法
CComplex CComplex::Multiply(const CComplex& zC) const
{
    double r;
    double i;
    r = mR * zC.mR - mI * zC.mI;
    i = mR * zC.mI + mI * zC.mR;
    return CComplex(r, i);
}

// 除法
CComplex CComplex::Divide(const CComplex& zC) const
{
    double denominator;
    denominator=zC.mR*zC.mR+zC.mI*zC.mI;
    double newR,newI;
    newR=(mR*zC.mR+mI*zC.mI)/denominator;
    newI=(mI*zC.mR-mR*zC.mI)/denominator;
    return CComplex(newR,newI);
}



