// #include <stdio.h>
// #include <stdlib.h>

// int main() {
//     int n;
//     // 读取矩阵阶数
//     if (scanf("%d", &n) != 1) return 0;

//     // 如果 n 为 1 的特殊情况处理
//     if (n == 1) {
//         printf("1\n1\n");
//         return 0;
//     }

//     // 动态分配二维数组，初始化为 0
//     int **matrix = (int **)calloc(n, sizeof(int *));
//     for (int i = 0; i < n; i++) {
//         matrix[i] = (int *)calloc(n, sizeof(int));
//     }

//     // 初始位置设定在矩阵中心
//     int x = n / 2;
//     int y = n / 2;
//     int num = 1;
//     matrix[x][y] = num++;

//     int step = 1; // 每次转向前移动的步长
//     while (num <= n * n) {
//         // 方向 1：向右走 step 步
//         for (int i = 0; i < step && num <= n * n; i++) matrix[x][++y] = num++;
//         // 方向 2：向上走 step 步
//         for (int i = 0; i < step && num <= n * n; i++) matrix[--x][y] = num++;
        
//         step++; // 转向后，步长增加 1
        
//         // 方向 3：向左走 step 步
//         for (int i = 0; i < step && num <= n * n; i++) matrix[x][--y] = num++;
//         // 方向 4：向下走 step 步
//         for (int i = 0; i < step && num <= n * n; i++) matrix[++x][y] = num++;
        
//         step++; // 转向后，步长再次增加 1
//     }

//     // 计算对角线数字之和并输出矩阵
//     long long sum = 0;
//     for (int i = 0; i < n; i++) {
//         for (int j = 0; j < n; j++) {
//             // 严格控制格式：数字之间一个空格，行末无空格
//             printf("%d", matrix[i][j]);
//             if (j < n - 1) {
//                 printf(" ");
//             }
//             // 判断是否在对角线上
//             if (i == j || i + j == n - 1) {
//                 sum += matrix[i][j];
//             }
//         }
//         printf("\n"); // 换行
//     }

//     // 最后一行输出对角线之和
//     printf("%lld\n", sum);

//     // 释放内存
//     for (int i = 0; i < n; i++) free(matrix[i]);
//     free(matrix);

//     return 0;
// }
/*===以上为动态内存分配写法===*/


#include <stdio.h>

// 静态数组，最大支持 105*105 规模
int matrix[105][105];

int main() {
    int n;
    // 读取输入
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    // 1阶矩阵特殊处理
    if (n == 1) {
        printf("1\n1\n");
        return 0;
    }

    // 初始参数设置
    int x = n / 2;      // 中心行索引
    int y = n / 2;      // 中心列索引
    int num = 1;        // 当前要填入的数字
    
    // 填入中心点并更新 num
    matrix[x][y] = num;
    num = num + 1;

    int step = 1;       // 每次转弯前移动的步长
    while (num <= n * n) {
        // --- 1. 向右移动 ---
        for (int i = 0; i < step; i++) {
            if (num <= n * n) {
                y = y + 1;
                matrix[x][y] = num;
                num++;
            }
        }
        // --- 2. 向上移动 ---
        for (int i = 0; i < step; i++) {
            if (num <= n * n) {
                x = x - 1;
                matrix[x][y] = num;
                num = num + 1;
            }
        }
        
        // 走完右和上，步长加 1
        step = step + 1;
        
        // --- 3. 向左移动 ---
        for (int i = 0; i < step; i++) {
            if (num <= n * n) {
                y = y - 1;
                matrix[x][y] = num;
                num = num + 1;
            }
        }
        // --- 4. 向下移动 ---
        for (int i = 0; i < step; i++) {
            if (num <= n * n) {
                x = x + 1;
                matrix[x][y] = num;
                num = num + 1;
            }
        }
        
        // 走完左和下，步长再次加 1
        step = step + 1;
    }

    // 输出矩阵并计算对角线之和
    long long diagonalSum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            // 打印当前数字
            printf("%3d", matrix[i][j]);
            
            // 关键格式控制：如果不是该行最后一个数字，打印空格
            if (j < n - 1) {
                printf(" ");
            }
            
            // 对角线判断：主对角线 (i==j) 或 副对角线 (i+j==n-1)
            if (i == j || i + j == n - 1) {
                diagonalSum = diagonalSum + matrix[i][j];
            }
        }
        // 行末换行
        printf("\n");
    }

    // 输出最终对角线之和
    printf("%lld\n", diagonalSum);

    return 0;
}