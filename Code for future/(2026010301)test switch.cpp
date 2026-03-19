// // #include <stdio.h>
// // int main(){ 
// //   int a;
// //   printf("input integer number: ");
// //   scanf("%d",&a);
// //   switch (a)
// //  {  /*对表达式a做多次判断，根据不同的条件做不同的语句*/
// //      case 1:printf("Mon\n");break;/*break的作用是跳出该结构*/
// //      case 2:printf("Tue\n"); break;
// //      case 3:printf("Wed\n"); break;
// //      case 4:printf("Thu\n"); break;
// //      case 5:printf("Fri\n"); break;
// //      case 6:printf("Sat\n"); break;
// //      case 7:printf("Sun\n"); break;
// //      default:printf("error\n");/*输入的不是0至7的整数时执行*/
// //    }
// // }
// #include<stdio.h>
// #include<math.h>

// int weishu(int x)
// { 
//   int num=0;
//   while(x>0)
//   {
//     num++;
//     x/=10;
//   }
//   return num;
// }
// void zhengshuchu(int x)

// {
  
//   int tem=x;
//   int num=weishu(x);
//   // while(x>0)
//   // {
//   //   printf("%d",tem/(int)pow(10,num-1));
//   //   tem%=(int)pow(10,num-1);
//   //   num--;
  
//   // }
//   while(x > 0)
//   {
//     int divisor = (int)pow(10, num-1);  // 先计算除数
//     printf("%d", tem / divisor);        // 获取最高位数字
//     tem %= divisor;                     // 更新tem的值
//     num--;
//   }
// // }
// #include<stdio.h>




#include <stdio.h>
#include <math.h>  // 添加数学库头文件

int mi(int x)
{
  int num=10;
  for (int i=1;i<=x;i++)
  {
    num*=10;
  }
  return num;
}
void zhengshuchu(int x) {
    int temp = x;
    int num = 0;
    
    // 计算数字位数
    while(temp > 0) {
        temp /= 10;
        num++;
    }
    
    temp = x;
    
    // 输出每一位数字
    while(num > 0) {
        int divisor = mi(10, num-1);  // 添加类型转换
        printf("%d ", temp / divisor);
        temp %= divisor;
        num--;
    }
}

int main() {
    zhengshuchu(1314521);
    return 0;  // 添加返回值
}