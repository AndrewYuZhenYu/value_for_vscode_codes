#include <stdio.h>

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);

    int a, b;
    printf("请输入一个八进制数和一个十六进制数\n");
    scanf("%o %x", &a, &b);
    printf("a的八进制形式: %o\n", a);
    printf("b的十六进制形式: %X\n", b);
    return 0;
}