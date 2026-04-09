#include <stdio.h>
int main()
{
    char x;
    scanf("%c", &x);
    printf("%c", x);
    int i, j, k;
    for (i = 1; i <= 9; i++)
    {
        printf("%4d", i);
    }
    printf("\n");
    for (i = 1; i <= 9; i++)
    {
        printf("%d", i);
        for (j = 1; j <= i; j++)
        {
            k = i * j;
            printf("%4d", k);
        }
        printf("\n");
    }
}
// #include <stdio.h>
// int main() {
//     int a, b;
//     while (scanf_s("%d %d", &a, &b) != EOF) {
//         long long sum = (long long)a + b;
//         printf("%lld\n", sum);
//     }
//     return 0;
// }
// #include<stdio.h>
// int main()
//{
//	int chn, math, eng, pe;
//	scanf("%d%d%d%d", &chn, &math, &eng, &pe);
//	int num = 0;
//	if (chn >= 60)num++;
//	if (math >= 60)num++;
//	if (eng >= 60)num++;
//	if (pe >= 60)num++;
//	if (num == 4)printf("优");
//	else if (num == 3 && pe >= 60)printf("良");
//	else if (num == 2 && pe >= 60)printf("中");
//	else if (num == 1 || num == 0 || pe < 60)printf("差");
//
// }
// #include<stdio.h>
// int weishu(long x)
//{
//	int num = 0;
//	while (x > 0)
//	{
//		num++;
//		x /= 10;
//	}
//	return num;
// }
// int main()
//{
//
//	long int a;
//	scanf("%ld", &a);
//	if (a >= -9 && a <= 9)
//	{
//		printf("TRUE");
//		return 0;
//	}
//	if (a < 0)a = -a;
//	int num = weishu(a);
//	int tem[100];
//	int i = 0;
//	for(i=0;i<num;i++)
//	{
//		tem[i] =a % 10;
//
//		a /= 10;
//	}
//	int test = 0;
//	for (int i = 0; i < num; i++)
//	{
//		/*printf("%d ", tem[i]);*/
//		if (tem[i] > tem[i + 1])test++;
//	}
//	/*printf("%d\n", test); */
//	if (test != 0)printf("FALSE");
//	else printf("TRUE");
//
//
// }

/*冒泡排序测试函数*/
// #include<stdio.h>
// #define N 10
// int main()
//{
//	int a[N];
//	for (int k = 0; k < N; k++)
//	{
//		scanf_s("%d", &a[k]);
//	}
//	int i;
//	for (i = 0; i < N-1; i++)
//	{
//		for (int j = 0; j < N-i-1; j++)
//		{
//			if (a[j] > a[j + 1])
//			{
//				int tem = a[j];
//				a[j] = a[j + 1];
//				a[j + 1] = tem;
//			}
//		}
//	}
//	for (int i = 0; i < N; i++)
//	{
//		printf("%d ", a[i]);
//	}
// }
/*选择排序测试*/
// #include<stdio.h>
// #define n 10
// int main()
//{
//	int a[n];
//	int i, j;
//	int min;
//	for (i = 0; i < n; i++)
//	{
//		scanf_s("%d", &a[i]);
//	}
//	for (i = 0; i < n-1; i++)
//	{
//		min = i;
//		for (j = i+1; j < n; j++)
//		{
//			if (a[j] < a[min])
//			{ min = j; }
//
//		}
//		if (min != i)
//		{
//		int tem = a[i];
//		a[i] = a[min];
//		a[min] = tem;
//
//		}
//	}
//	for (i = 0; i < n; i++)
//	{
//		printf("%d ", a[i]);
//	}
// }
//  #define NUM 5
//  #include<stdio.h>

// struct Stud {
//     int No;
//     int Score[2];
// };
//
// int main()
//{
//     struct Stud StudAll[NUM], StudTmp;
//     int ScoreSum[NUM] = { 0 };
//     int i;
//
//     for (i = 0; i < NUM; i++)
//         scanf_s("%d%d%d", &StudAll[i].No, &StudAll[i].Score[0], &StudAll[i].Score[1]);
//
//     for (i = 0; i < NUM; i++)
//         if (StudAll[i].Score[0] < 60 || StudAll[i].Score[1] < 60)
//             printf("%d\n", StudAll[i].No);
// }
//  #include<stdio.h>
//  // #define _CRT_SECURE_NO_WARNINGS
//  //# define n_Len 5
//  typedef struct
//  {
//  	char Name[50]; //书名
//  	double Price;  //价钱
//  	int Pages; //页数
//  }BOOK;
//  int MaxPages(BOOK* pBook, int nLen)
//  {
//  	int max=0;
//  	for (int i = 0; i < nLen; i++)
//  	{
//  		if ((pBook + i)->Pages > (pBook + max)->Pages)
//  			max = i;
//  	}
//  	return (pBook + max)->Pages;
//  }
//  int main()
//  {
//  	int n_Len;
//  	scanf("%d", &n_Len);
//  	BOOK zrj[100];

// 	for (int i = 0; i < n_Len; i++)
// 	{
// 	scanf("%s%lf%d", zrj[i].Name, &zrj[i].Price, &zrj[i].Pages);
// 	}
// 	printf("%d", MaxPages(zrj, n_Len));
// }

// #include <stdio.h>
// struct student
// {	long  num;
// 	char name[20];
// 	char sex;
// 	int age;
// 	double score;
// 	char addr[30];
// }a[3]={{99641,"Li Ping",'M',20,56, "Tianjin Street"},
//         {99341,"Zhang Fan",'F',21,78, "Beijing Road"},
//         {99441,"Ren Zhong",'M',19,84, "Shenyang Road"}};

// int main()
// { struct student *p;
//   for(p=a;p<a+3;p++)
// 	printf("%ld, %-20s, %2c, %4d, %5.2f, %-20s\n",
// 	p->num,p->name,p->sex,p->age,p->score,p->addr);
//   return 0;
// }

// #include<stdio.h>
// int main()
// {
// 	char w[][10]={"ABCD","EFGH","IJKL","MNOP"};
// 	for(int k=1;k<3;k++)
// 	{
// 		printf("%s\n",w[k]);
// 	}
// }
