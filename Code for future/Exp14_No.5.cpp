#include <stdio.h>
#include <string.h>

typedef struct {
    char Name[50];  // 书名
    double Price;   // 价钱
    int Pages;      // 页数
} BOOK;

// 函数声明
int MaxPages(BOOK *pBook, int nLen);
double MeanPages(BOOK *pBook, int nLen);

int main() {
    int nLen;
    
    // 输入书的数量
    printf("请输入书的数量 (1-10): ");
    scanf("%d", &nLen);
    
    // 验证输入
    if (nLen <= 0 || nLen > 10) {
        printf("错误：书的数量必须在1到10之间\n");
        return 1;
    }
    
    // 创建书籍数组
    BOOK books[nLen];
    
    // 输入书籍信息
    printf("请输入%d本书的信息（格式：书名 价格 页数）:\n", nLen);
    for (int i = 0; i < nLen; i++) {
        // 清空输入缓冲区
        while (getchar() != '\n');
        
        printf("第%d本书: ", i + 1);
        
        // 读取书名（可能包含空格）
        char name[50];
        double price;
        int pages;
        
        // 使用fgets读取整行，包括可能包含空格的书名
        fgets(name, sizeof(name), stdin);
        // 去除换行符
        name[strcspn(name, "\n")] = '\0';
        
        // 读取价格和页数
        scanf("%lf %d", &price, &pages);
        
        // 保存到结构体
        strcpy(books[i].Name, name);
        books[i].Price = price;
        books[i].Pages = pages;
    }
    
    printf("\n========== 书籍信息 ==========\n");
    for (int i = 0; i < nLen; i++) {
        printf("书%d: %-20s 价格: %6.2f 页数: %4d\n", 
               i + 1, books[i].Name, books[i].Price, books[i].Pages);
    }
    
    // 测试 MaxPages 函数
    printf("\n========== 查找页数最多的书 ==========\n");
    int maxPages = MaxPages(books, nLen);
    printf("最多页数: %d\n", maxPages);
    
    // 测试 MeanPages 函数
    printf("\n========== 计算平均页数 ==========\n");
    double average = MeanPages(books, nLen);
    printf("平均页数: %.2f\n", average);
    
    return 0;
}

// 函数1：找出页数最多的书并打印其信息
int MaxPages(BOOK *pBook, int nLen) {
    if (nLen <= 0 || pBook == NULL) {
        printf("错误：无效的书籍数据\n");
        return 0;
    }
    
    int maxIndex = 0;  // 假设第一本书页数最多
    int maxPages = pBook[0].Pages;
    
    // 遍历所有书籍，查找页数最多的
    for (int i = 1; i < nLen; i++) {
        if (pBook[i].Pages > maxPages) {
            maxPages = pBook[i].Pages;
            maxIndex = i;
        }
    }
    
    // 打印页数最多的书籍信息
    printf("页数最多的书是:\n");
    printf("书名: %s\n", pBook[maxIndex].Name);
    printf("价格: %.2f\n", pBook[maxIndex].Price);
    printf("页数: %d\n", pBook[maxIndex].Pages);
    
    return maxPages;
}

// 函数2：计算平均页数
double MeanPages(BOOK *pBook, int nLen) {
    if (nLen <= 0 || pBook == NULL) {
        printf("错误：无效的书籍数据\n");
        return 0.0;
    }
    
    int totalPages = 0;
    
    // 计算总页数
    for (int i = 0; i < nLen; i++) {
        totalPages += pBook[i].Pages;
    }
    
    // 计算平均页数
    return (double)totalPages / nLen;
}