// #include<stdio.h>
// void chose_rank(int a[][3],int n)
// {
//     int i=0,j=0;
//     int max;
//     for(i=0;i<n-1;i++)
//     {
//         max=i;
//         for(j=i+1;j<n;j++)
//         {
//             if (a[j][0]>a[max][0])
//             min=j;
//         }
//         int tem=a[min][0];
//         a[min][0]=a[j][0];
//         a[j][0]=tem;
//     }

// }

// int main()
// {
//     int N;
//     scanf("%d",&N);
//     int a[N];
//     int b[N][3];
//     for (int i=0;i<N;i++)
//     {
//         scanf("%d",&a[i]);
//         b[i][0]=a[i];
//         b[i][1]=i;
//     }
//     chose_rank(b);
//     int R=1;
//     int c[N];
//     for (int i=0;i<N;i++)
//     {
//         c[i]=R;
//         if (b[i][0]>b[i+1][0])R++;
//         b[i][2]=c[i];
//     }
//     chose_rank(b[i][2])

// }

#include <stdio.h>

// 选择排序（按成绩降序，同时保留原始索引）
void chose_rank(int a[][3], int n)
{
    int i, j, maxIndex;
    // 临时变量，交换整行数据（成绩、原始索引、排名）
    int temp[3];
    for (i = 0; i < n - 1; i++)
    {
        maxIndex = i;
        // 找当前最大成绩的位置
        for (j = i + 1; j < n; j++)
        {
            if (a[j][0] > a[maxIndex][0])
            {
                maxIndex = j;
            }
        }
        // 交换整行（保证成绩和原始索引对应）
        temp[0] = a[i][0];
        temp[1] = a[i][1];
        temp[2] = a[i][2];
        a[i][0] = a[maxIndex][0];
        a[i][1] = a[maxIndex][1];
        a[i][2] = a[maxIndex][2];
        a[maxIndex][0] = temp[0];
        a[maxIndex][1] = temp[1];
        a[maxIndex][2] = temp[2];
    }
}

int main()
{
    int N;
    printf("请输入N的数值");
    scanf("%d", &N);
    // b[N][3]：列0=成绩，列1=原始索引（输入顺序），列2=排名
    int b[N][3];
    for (int i = 0; i < N; i++)
    {
        scanf("%d", &b[i][0]);
        b[i][1] = i; // 记录原始输入的索引（用于最终按输入顺序输出）
        b[i][2] = 0; // 排名初始化为0
    }

    // 步骤1：按成绩降序排序
    chose_rank(b, N);

    // 步骤2：处理同名次
    int rank = 1;
    b[0][2] = rank; // 第一个元素排名为1
    for (int i = 1; i < N; i++)
    {
        // 若当前成绩和前一个相同，排名与前一个一致
        if (b[i][0] == b[i - 1][0])
        {
            b[i][2] = b[i - 1][2];
        }
        else
        {
            // 不同则排名为当前位置+1（因为是降序，i+1即当前名次）
            rank = i + 1;
            b[i][2] = rank;
        }
    }

    // 步骤3：按原始输入顺序排序（恢复输入顺序，输出成绩和排名）
    // 用选择排序按原始索引（b[i][1]）升序排列
    for (int i = 0; i < N - 1; i++)
    {
        int minIndex = i;
        for (int j = i + 1; j < N; j++)
        {
            if (b[j][1] < b[minIndex][1])
            {
                minIndex = j;
            }
        }
        // 交换整行
        int temp[3] = {b[i][0], b[i][1], b[i][2]};
        b[i][0] = b[minIndex][0];
        b[i][1] = b[minIndex][1];
        b[i][2] = b[minIndex][2];
        b[minIndex][0] = temp[0];
        b[minIndex][1] = temp[1];
        b[minIndex][2] = temp[2];
    }

    // 输出结果
    for (int i = 0; i < N; i++)
    {
        printf("%d %d\n", b[i][0], b[i][2]);
    }

    return 0;
}