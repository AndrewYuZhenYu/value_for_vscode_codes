#include<stdio.h>
#include<string.h>
int main ()
{
    char str1[100];
    strcpy(str1,"I love SJTU");
    // scanf("%s%s%s",str1,str2,str3);
   printf("%d\n",strlen(str1));
   puts(str1);
   printf("\n");
   printf("%s\n",strlwr(str1));
//    printf("%s\n",str2);
//     printf("%s\n",str3);
    return 0;


}