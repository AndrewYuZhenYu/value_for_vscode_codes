#include <stdio.h>
void perfect(int m, int n)
{

    if (m > n)
    {
        int tem = m;
        m = n;
        n = tem;
    }
    // int wanmeishu[n-m+1];
    // int cou=0;
    for (int j = m; j <= n; j++)
    {
        int tem = 0;
        int yinzi[j];
        int k = 0;
        for (int i = 1; i < j; i++)
        {
            if (j % i == 0)
            {
                yinzi[k] = i;
                tem += i;
                k++;
            }
        }

        if (j == 1)
            printf("1: 1\n");
        if (j == tem)
        {
            printf("%d:", j);
            for (int l = 0; l < k; l++)
            {
                printf(" %d", yinzi[l]);
            }
            printf("\n");
        }
    }
}
int main()
{
    int m, n;
    // int num=0;
    scanf("%d%d", &m, &n);
    perfect(m, n);
}