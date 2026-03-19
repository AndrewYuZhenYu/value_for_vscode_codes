#include<stdio.h>
int main()
{
   void link_string(char *p1,char *p2);
   char a[100]="I am a SJTUer.";
   char b[100]="I am WuYaoYin's husband.";
   char *arr1,*arr2;
   arr1=a;
   arr2=b;
   printf("before the link,\na==%s\nb==%s\n",arr1,arr2);
   link_string(arr1,arr2);
   printf("After the link,\na==%s\nb==%s\n",arr1,arr2);
}
void link_string(char *p1,char *p2)
{
   int i=0;
   for (i=0;*p1!='\0';i++)
   p1++;
   for (;*p2!='\0';p1++,p2++)
   {
      *p1=*p2;
   }
   *p1='\0';
}