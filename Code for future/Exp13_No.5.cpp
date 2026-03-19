#include <stdio.h>
#define ROW 3   // 假设矩阵有 3 行，可根据需要修改
#define COL 4   // 假设矩阵有 4 列，可根据需要修改

// 函数声明：查找并输出矩阵的鞍点；若无鞍点则打印提示
void findSaddlePoint(int mat[ROW][COL], int row, int col);

int main(void) {
    // 示例矩阵，可自行替换测试
    int matrix[ROW][COL] = {
        {11, 12, 13, 14},
        {15, 16, 17, 18},
        {19, 20, 21, 22}
    };
    
    findSaddlePoint(matrix, ROW, COL);
    return 0;
}

void findSaddlePoint(int mat[ROW][COL], int row, int col) {
    int i, j, k;
    int isSaddleFound = 0;  // 标记是否找到鞍点
    
    for (i = 0; i < row; i++) {
        // 1. 先找第 i 行的最大值，以及它所在的列下标 maxCol
        int maxInRow = mat[i][0];
        int maxCol = 0;
        for (j = 1; j < col; j++) {
            if (mat[i][j] > maxInRow) {
                maxInRow = mat[i][j];
                maxCol = j;
            }
        }
        
        // 2. 检查 maxInRow 是否是其所在列的最小值
        int isMinInCol = 1;  // 先假设是列最小
        for (k = 0; k < row; k++) {
            if (mat[k][maxCol] < maxInRow) {
                isMinInCol = 0;
                break;
            }
        }
        
        if (isMinInCol) {
            printf("找到鞍点：%d，位于第 %d 行、第 %d 列\n", 
                   maxInRow, i + 1, maxCol + 1);  // 行、列从 1 开始计数更直观
            isSaddleFound = 1;
            // 若只需找第一个鞍点，可在此处 break；若需找所有鞍点则去掉 break 继续循环
        }
    }
    
    if (!isSaddleFound) {
        printf("该矩阵中没有鞍点。\n");
    }
}