// #include<stdio.h>
// int main()
// {
// int a[10];   int i,j,t;
// printf("input 10 numbers :\n");
// for (i=0;i<10;i++)  scanf("%d",&a[i]);                  
// printf("\n");
// for(j=0;j<9;j++)
// 	for(i=0;i<9-j;i++) 
// 	  if (a[i]>a[i+1]) 
// 	    {t=a[i];a[i]=a[i+1];a[i+1]=t;}
// printf("the sorted numbers :\n");
// for(i=0;i<10;i++)  printf("%d ",a[i]);
// printf("\n");
// }

#include<stdio.h>
#include<stdlib.h>
void main(){
  FILE *fp;     char str[10];
  if(( fp = fopen("c3.txt","r"))==NULL)
     {  printf("Cannot open file!");    exit(1); }
  fgets(str,11,fp); 
  puts(str);
  fclose(fp);  
}

