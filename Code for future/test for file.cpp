#include<stdio.h>
#include<stdlib.h>
int main(){
//   char c;  FILE *fp;
//   if(( fp=fopen("f1.txt", "r"))==NULL)
//      {printf(“Can’t open this file! \n”); exit(1);}

//   while( (c=fgetc(fp))!=EOF)  printf( "%c", c);
//   printf("\n");
//   fclose(fp);
FILE *fp;
if (fp=(fopen("FUN.txt","r"))==EOF)
printf("Error");
char c;
c=getc("FUN.txt");
fclose(fp);
}
