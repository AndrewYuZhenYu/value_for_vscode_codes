#include<stdio.h>
#include<math.h>
double jiecheng(int x)
{
    double result=1;
    for (int i=1;i<=x;i++)
    {
        result*=i;
    }
    return result;
}
double sumFunc(double x)
{
double s=0;
for(int i=1;fabs(pow(x,i)/jiecheng(i))>=1e-5;i++)
{
    s+=pow(-1,i+1)*pow(x,i)/jiecheng(i);
}
return s;
}
int main()
{
    double x;
    printf("请输入x的数值\n");
    scanf("%lf",&x);
    printf("%.2lf\n",sumFunc(x));
    return 0;
}