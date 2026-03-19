#include<stdio.h>
int swap(int *a,int *b)
{
    int tem=*a;
    *a=*b;
    *b=tem;
}
int comp(int x, int y)
{   
    int flag;
    if (x>y)  flag=1;
    else if (x<y) flag=-1;
    else flag=0;
    return ( flag );
}

int main()
{

   int a[10] , b[10] ;
   int i , same=0, large=0, small=0, k;
   for( i=0 ; i<10 ; i++) 
      scanf ("%d, %d" , &a[i] , &b[i]);
   for( i=0 ; i<10 ;afs i++){ 
      k = comp(a[i] , b[i]);
      if ( k ==1) large++;
      else if ( k==-1 ) small++;
      else  same++;  
   }
  if (large>small)  printf ("数组a 大于数组b\n ");
  else if (large<small)    printf ("数组a 小于数组b \n");
  else  printf("数组a 等于数组b \n");
}


