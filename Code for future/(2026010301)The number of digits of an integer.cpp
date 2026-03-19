#include<stdio.h>
int digits(int x)
{
    int num=0;
    if (x<0)x=-x;
   else if (x==0)return 1;
    while(x!=0)
    {
        num++;
        x/=10;
    }
    return num;
}
int main()
{
    int N;
    scanf("%d",&N);
    int tem[N];
    int result[N];
    for (int i=0;i<N;i++)
    {
        scanf("%d",&tem[i]);
        result[i]=digits(tem[i]);
    }
    for (int i=0;i<N;i++)
    {
        printf("%d\n",result[i]);
    }
}