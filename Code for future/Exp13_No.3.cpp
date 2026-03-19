#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100

// ====================== 数组写法 ======================
// 使用数组判断矩阵是否对称
int isArraySymmetric(int matrix[][MAX_SIZE], int n) {
    for(int i = 0; i < n; i++) {
        for(int j = i+1; j < n; j++) {
            if(matrix[i][j] != matrix[j][i]) {
                return 0; // 发现不对称元素，返回0
            }
        }
    }
    return 1; // 全部对称，返回1
}

// 指针写法
// 使用指针判断矩阵是否对称
int isPointerSymmetric(int *mat, int n) {
    for(int i = 0; i < n; i++) {
        for(int j = i+1; j < n; j++) {
            // 通过指针算术运算访问矩阵元素
            if(*(mat + i*n + j) != *(mat + j*n + i)) {
                return 0; // 发现不对称元素，返回0
            }
        }
    }
    return 1; // 全部对称，返回1
}

int main() {
    int n;
    int arrayMatrix[MAX_SIZE][MAX_SIZE]; // 静态二维数组
    int *pointerMatrix; // 指向整型的指针
    
    // ============= 输入矩阵 =============
    printf("请输入矩阵的阶数n: ");
    scanf("%d", &n);
    
    if(n <= 0 || n > MAX_SIZE) {
        printf("无效的矩阵阶数！\n");
        return 1;
    }
    
    printf("请输入%d×%d矩阵的元素:\n", n, n);
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            scanf("%d", &arrayMatrix[i][j]);
        }
    }
    
    // 将数组的首地址赋给指针，使两种方法可以共享输入数据
    pointerMatrix = &arrayMatrix[0][0];
    
    // ============= 测试数组写法 =============
    int arrayResult = isArraySymmetric(arrayMatrix, n);
    if(arrayResult == 1) {
        printf("【数组写法】该矩阵是对称矩阵\n");
    } else {
        printf("【数组写法】该矩阵不是对称矩阵\n");
    }
    
    // ============= 测试指针写法 =============
    int pointerResult = isPointerSymmetric(pointerMatrix, n);
    if(pointerResult == 1) {
        printf("【指针写法】该矩阵是对称矩阵\n");
    } else {
        printf("【指针写法】该矩阵不是对称矩阵\n");
    }
    
    return 0;
}