#include <stdio.h>
long long a[100005];
int main()
{
    int t;
    int n, m;
    int i, j;
    long long l, r, max;
    char op[5];
    scanf("%d", &t);
    while (t--)
    {
        scanf("%d %d", &n, &m);
        for (i = 0; i < n; i++)
        {
            scanf("%lld", &a[i]);
        }
        for (j = 0; j < m; j++)
        {
            scanf("%s %lld %lld", op, &l, &r);
            for (i = 0; i < n; i++)
            {
                if (a[i] >= l && a[i] <= r)
                {
                    if (op[0] == '+')
                        a[i]++;
                    else
                        a[i] = a[i] - 1;
                }
            }
            max = a[0];
            for (i = 1; i < n; i++)
            {
                if (a[i] > max)
                {
                    max = a[i];
                }
            }
            if (j == m - 1)
                printf("%lld\n", max);
            else
                printf("%lld ", max);
        }
    }
    return 0;
}