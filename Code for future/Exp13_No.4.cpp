#include <stdio.h>
#define ROWS 10  // 可自行修改要打印的行数

int main(void) {
    int arr[ROWS][ROWS] = {0};  // 初始化为全 0，方便后续赋值
    
    // 1. 计算杨辉三角各位置的元素值
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j <= i; j++) {
            if (j == 0 || j == i) {  // 每行首尾元素为 1
                arr[i][j] = 1;
            } else {                 // 中间元素由“上一行左上方 + 上一行正上方”得到
                arr[i][j] = arr[i-1][j] + arr[i-1][j-1];
            }
        }
    }

    // 2. 左对齐打印杨辉三角
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j <= i; j++) {
            printf("%-6d", arr[i][j]);  // %-6d 表示左对齐，占 6 个字符宽度
        }
        printf("\n");  // 每行结束后换行
    }

    return 0;
}