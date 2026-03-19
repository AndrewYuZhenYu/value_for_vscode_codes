#include<stdio.h>
int wanshu(int x)
{
    int tem=0;
    for(int i=1;i<x;i++)
    {
        if (x%i==0){
        tem+=i;
       
        }
       
    }
    if  (x==tem)
    {
        
        return 1;
    }
    else return 0;
}
int sumWanshu(int m, int n)
{
    int mem[10000];
    if(m>=n)
    {
        int temp=m;
        m=n;
        n=temp;
    }
    int result=0;
    int j=0;
    for (int i=m;i<=n;i++)
    {
        if(wanshu(i)==1)
        {
            mem[j]=i;
            j++;
            result+=i;
        }
      
    }
    printf("完数和为%d\n共找到%d个完数\n",result,j);
    printf("运算过程如下:\n");
    for (int k=0;k<j;k++)
    {
        if (k!=(j-1))
        printf("%d+",mem[k]);
        else printf("%d=",mem[k]);
    }

    return result;
}
int main()
{
    int m=0,n=0;
    printf("请输入上下界\t");
    scanf("%d%d",&m,&n);
    printf("%d\n",sumWanshu(m,n));
  
    return 0;

}