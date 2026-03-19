#include<stdio.h>
void nixu(int x)
{
    if(x>=0&&x<=9)printf("%d",x);
    else 
    while(x!=0)
    {
        printf("%d",x%10);
        x/=10;
    }
}
int main()
{
    int x;
    scanf("%d",&x);
    nixu(x);
}