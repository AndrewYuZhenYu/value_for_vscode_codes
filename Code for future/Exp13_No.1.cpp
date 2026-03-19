#include <stdio.h>
#include <string.h>

// 函数原型：s 为源串，c 为目标串，m 为起始位置，n 为总长度
void fun(char *s, char *c, int m, int n);

int main() {
    char s[100];  // 定义源字符串数组
    char c[100];  // 定义目标字符串数组
    int m, n;

    printf("请输入字符串: ");
    fgets(s, sizeof(s), stdin);
    s[strcspn(s, "\n")] = '\0'; // 去除 fgets 读入的换行符

    printf("请输入起始位置 m (从1开始): ");
    scanf("%d", &m);
    
    // 获取源字符串的总长度
    n = strlen(s);

    // 调用函数：从第 m 个字符开始，复制到末尾
    fun(s, c, m, n);

    printf("复制后的字符串为: %s\n", c);

    return 0;
}

void fun(char *s, char *c, int m, int n) {
    int i = 0;
    int len = strlen(s);

    // 参数合法性检查：起始位置不能大于字符串长度
    if (m > len || m <= 0) {
        c[0] = '\0'; 
        return;
    }

    // 从第 m 个字符（下标为 m-1）开始复制，直到字符串结束
    // 这里使用 s[m-1+i] 定位源字符串位置
    for (i = 0; s[m - 1 + i] != '\0'; i++) {
        c[i] = s[m - 1 + i];
    }

    // 关键一步：在目标字符串末尾加上结束符
    c[i] = '\0';
}