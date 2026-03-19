#include<stdio.h>
#include<stdlib.h>
int main()
{
    FILE *fp;
    char ch,filename[20];
    printf("请输入所用的文件名：");
    scanf("%s",filename);
    if((fp=fopen(filename,"w"))==NULL)
    {

        printf("无法打开此文件\n");
        exit(0);
    }
    ch=getchar();
    while(ch!='#')
    {
        fputc(ch,fp);
        putchar(ch);
        ch=getchar();
    }
    fclose(fp);
    putchar(10);
    return 0;
}