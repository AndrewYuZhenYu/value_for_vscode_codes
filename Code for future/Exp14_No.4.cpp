#include <stdio.h>
#include <string.h>
char *StrCat(char *Str1, char *Str2)
{
    char *p = Str1;
    while (*p != '\0')
        p++;
    *p = ' ';
    p++;
    while (*Str2 != '\0')
    {
        *p = *Str2;
        p++;
        Str2++;
    }
    *p = '!';
    p++;
    *p = '\0';
    return Str1;
}
int main()
{
    char str1[100];
    char str2[100];
    char *a = str1;
    char *b = str2;
    printf("请输入字符串1\n");
    fgets(str1, sizeof(str1), stdin);
    str1[strcspn(str1, "\n")] = '\0';
    printf("请输入字符串2\n");
    fgets(str2, sizeof(str2), stdin);
    str2[strcspn(str2, "\n")] = '\0';
    StrCat(a, b);
    printf("%s", a);
}