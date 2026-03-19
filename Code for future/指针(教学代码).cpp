
//-------------------------------------------------------
//                   指针的意义
//-------------------------------------------------------
// #include <stdio.h>
// #include <stdlib.h>

// int main() {
//     int a = 10;       // 普通变量：存数值
//     int *p = &a;      // 指针变量p：存a的地址（&a取地址）

//     // 1. 打印a的数值、a的地址
//     printf("a的数值：%d\n", a);
//     printf("a的地址：%p\n", &a); // %p：打印地址格式

//     // 2. 打印指针p的内容（即a的地址）、指针p自身的地址
//     printf("指针p存的地址：%p\n", p);  // p = &a，和上面a的地址一致
//     printf("指针p自身的地址：%p\n", &p); // 指针变量自己也占内存，有独立地址

//     // 3. 通过指针访问a的值（解引用*p）
//     printf("通过*p访问a的值：%d\n", *p);

// 	system("pause");
//     return 0;
// }



//-------------------------------------------------------
//                   指针的移动
//-------------------------------------------------------
// #include <stdio.h>
// #include <stdlib.h>

// int main() {
//     int arr[] = {10, 20, 30, 40, 50};
//     int *p = arr; // 数组名arr等价于数组首元素地址，p指向arr[0]

//     // 指针移动：p++ 等价于 p = p + 1，步长=数组元素类型大小（int=4字节）
//     printf("p指向arr[0]：%d\n", *p);   // 10
//     printf("%p\n",p);
//     p++; // 指针后移1位，指向arr[1]
//     printf("p指向arr[1]：%d\n", *p);   // 20
//     printf("%p\n",p);
//     p += 2; // 指针后移2位，指向arr[3]
//     printf("p指向arr[3]：%d\n", *p);   // 40
//     printf("%p\n",p);
//     p--; // 指针前移1位，指向arr[2]
//     printf("p指向arr[2]：%d\n", *p);   // 30
//     printf("%p\n",p);

//     // system("pause"); 
//     return 0;
// }


// -------------------------------------------------------
//            指针作为函数参数，传递的是地址
// -------------------------------------------------------

// #include <stdio.h>
// #include <stdlib.h>

// // 形参是指针：接收实参的地址
// void test(int *p) 
// {	printf("子函数内部：\n");
//     printf("  形参p存的地址：%p\n", p);
//     printf("  形参p自身的地址：%p\n", &p); // 形参p是局部指针，地址和实参不同
// 	printf("  修改前*p的值：%d\n", *p); 

//     *(p+1) = 108; // 通过地址修改实参的值
// 	printf("  修改后*p的值：%d\n\n", *(p+1)); 
 
// }

// int main() {
//     int a = 10;
//     int *ptr = &a; // 实参是指针变量

// 	printf("主函数内部：\n");
//     printf("  调用前：a的值：%d\n", a);
//     printf("  调用前：实参ptr存的地址：%p\n", ptr);
//     printf("  调用前：实参ptr自身的地址：%p\n\n", &ptr);

//     test(ptr); // 传递指针：本质是把ptr存的地址（&a）复制给形参p

// 	printf("主函数内部：\n");
//     printf("  调用后：a的值：%d\n", a); // a被修改为100

//     system("pause"); return 0;
// }

//-------------------------------------------------------
//            指针作为函数参数，操作int数组
// //-------------------------------------------------------
// #include <stdio.h>
// #include <stdlib.h>

// // 指针操作数组：arr是数组首地址，len是数组长度
// void modifyArr(int *arr, int len) 
// {
//     for(int i=0; i<len; i++) 
// 	{
//         arr[i] *= 2; // 等价于 *(arr + i) *= 2，每个元素乘2
//     }
// }

// int main() {
//     int arr[] = {1, 2, 3, 4, 5};
//     int len = sizeof(arr)/sizeof(arr[0]);/*size of 求得数组的字节数*/

//     printf("修改前数组：");
//     for(int i=0; i<len; i++) printf("%d ", arr[i]);

//     modifyArr(arr, len); // 传递数组名（首地址）

//     printf("\n修改后数组：");
//     for(int i=0; i<len; i+1) printf("%d ", arr[i]);
// 	printf("\n");

//     system("pause"); return 0;
// }


/*
//-------------------------------------------------------
//            指针作为函数参数，操作字符串
//-------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>

// 指针操作字符串：把字符串转大写（原地修改）
void strToUpper(char *str) {
    while(*str != '\0') { // 遍历到字符串结束符
        if(*str >= 'a' && *str <= 'z') {
            *str -= 32; // 小写转大写（ASCII差32）
        }
        str++; // 指针后移，遍历下一个字符
    }
}

int main() {
    char str[] = "hello c pointer!"; // 字符数组存字符串

    printf("转换前：%s\n", str);
    strToUpper(str); // 传递字符串首地址
    printf("转换后：%s\n", str);

    system("pause"); return 0;
}*/


/*
//-------------------------------------------------------
//                 指针数组是：指向数组的指针
//-------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 1. 定义3个一维int数组（模拟3个班级的成绩）
    int class1[] = {85, 92, 78, 90, 88};
    int class2[] = {76, 89, 95, 81};
    int class3[] = {91, 83, 79, 87, 93, 80};

    // 2. 指针数组：数组的每个元素是int*（存上面3个数组的首地址）
    int *scores[] = {class1, class2, class3};
    // 记录每个数组的长度（和指针数组一一对应）
    int len[] = {sizeof(class1)/sizeof(int), sizeof(class2)/sizeof(int), sizeof(class3)/sizeof(int)}; // class1长度5，class2长度4，class3长度6

    // 3. 遍历指针数组，输出每个班级的成绩
    printf("===== 各班成绩 =====\n");
    for(int i=0; i<3; i++) // 3个班级
	{ 
        printf("第%d班成绩：", i+1);
        // 遍历当前班级的成绩（scores[i]指向该班数组首地址）
        for(int j=0; j<len[i]; j++) 
		{
            // scores[i][j] 等价于 *(scores[i]+j)，两种写法都可
            printf("%d ", scores[i][j]); 
        }
        printf("\n");
    }

    // 额外演示：直接通过指针数组访问指定元素（强化理解）
    printf("\n单独访问：\n");
    printf("1班第2个成绩：%d\n", scores[0][1]); // class1[1] = 92
    printf("2班第3个成绩：%d\n", scores[1][2]); // class2[2] = 95
    printf("3班第5个成绩：%d\n", scores[2][4]); // class3[4] = 93

    system("pause"); return 0;
}*/



//-------------------------------------------------------
//             指针数组：指向字符型数组也一样
//-------------------------------------------------------
// #include <stdio.h>
// #include <stdlib.h>

// int main() 
// {
//     // 1. 定义多个字符串（字符常量）
//     char *course1 = "C语言";
//     char *course2 = "高等数学";
//     char *course3 = "大学英语";
//     char *course4 = "计算机基础";

//     // 2. 指针数组：数组的每个元素是char*类型（存字符串的首地址）
//     char *courses[] = {course1, course2, course3, course4};
//     // 指针数组的长度（4个课程）
//     int course_num = sizeof(courses) / sizeof(char*);

//     // 3. 遍历指针数组，输出所有课程
//     printf("===== 大一必修课程 =====\n");
//     for(int i=0; i<course_num; i++) {
//         // courses[i]是第i个字符串的首地址，printf直接输出字符串
//         printf("第%d门课：%s\n", i+1, courses[i]);
//     }

//     // 额外演示：直接访问指定字符串（强化理解）
//     printf("\n单独访问：\n");
//     printf("第2门课：%s\n", courses[1]); // 访问第二个字符串
//     printf("第4门课：%s\n", courses[3]); // 访问第四个字符串

//     system("pause"); return 0;
// }



/*
//-------------------------------------------------------
//             指针数组：带个子函数
//-------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>
// 辅助函数：排序单个班级的成绩（冒泡排序）
void sortScore(int *score, int len) {
    for(int i=0; i<len-1; i++) {
        for(int j=0; j<len-1-i; j++) {
            if(score[j] < score[j+1]) { // 降序排序（从高到低）
                int t = score[j];
                score[j] = score[j+1];
                score[j+1] = t;
            }
        }
    }
}

int main() {
    // 1. 定义3个班级的成绩数组（一维int数组）
    int class1[] = {85, 92, 78, 90, 88};
    int class2[] = {76, 89, 95, 81};
    int class3[] = {91, 83, 79, 87, 93, 80};

    // 2. 指针数组：数组的每个元素都是int*类型，指向各班级成绩数组的首地址
    //    scores[0] = &class1[0], scores[1] = &class2[0], scores[2] = &class3[0]
    int *scores[] = {class1, class2, class3};
    // 记录每个班级的人数（和指针数组一一对应）
    int classLen[] = {sizeof(class1)/sizeof(int), 
                      sizeof(class2)/sizeof(int), 
                      sizeof(class3)/sizeof(int)};
    int classNum = sizeof(scores)/sizeof(int*); // 班级数量

    // 3. 遍历指针数组，排序并输出每个班级的成绩
    printf("===== 各班成绩榜单（降序）=====\n");
    for(int i=0; i<classNum; i++) {
        sortScore(scores[i], classLen[i]); // 指针数组元素作为函数参数（传递数组地址）
        
        printf("第%d班（%d人）：", i+1, classLen[i]);
        // 遍历当前班级的成绩（scores[i]指向该班成绩数组首地址）
        for(int j=0; j<classLen[i]; j++) {
            printf("%d ", *(scores[i] + j)); // 等价于 scores[i][j]
        }
        printf("\n");
    }

    system("pause"); return 0;
}*/


/*
//-------------------------------------------------------
//             加大难度：指针数组作为函数参数
//-------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>

// 函数参数：
// scores：指针数组（int*类型的数组），接收所有班级成绩数组的地址
// classLen：普通int数组，接收每个班级的人数
// classNum：班级总数
void sortAllClass(int *scores[], int classLen[], int classNum) {
    // 遍历每个班级，排序成绩
    for(int i=0; i<classNum; i++) {
        // 对第i个班级的成绩进行冒泡排序（降序）
        int *score = scores[i]; // 取出第i个班级的成绩数组地址
        int len = classLen[i];  // 取出第i个班级的人数
        for(int j=0; j<len-1; j++) {
            for(int k=0; k<len-1-j; k++) {
                if(score[k] < score[k+1]) {
                    int t = score[k];
                    score[k] = score[k+1];
                    score[k+1] = t;
                }
            }
        }
    }
}

// 辅助输出函数（可选，也可合并到main，这里拆分更清晰）
void printAllClass(int *scores[], int classLen[], int classNum) {
    printf("===== 各班成绩榜单（降序）=====\n");
    for(int i=0; i<classNum; i++) {
        printf("第%d班（%d人）：", i+1, classLen[i]);
        for(int j=0; j<classLen[i]; j++) {
            printf("%d ", *(scores[i] + j)); // 等价于 scores[i][j]
        }
        printf("\n");
    }
}

int main() {
    // 1. 定义3个班级的成绩数组（一维int数组）
    int class1[] = {85, 92, 78, 90, 88};
    int class2[] = {76, 89, 95, 81};
    int class3[] = {91, 83, 79, 87, 93, 80};

    // 2. 指针数组：每个元素是int*，指向各班级成绩数组首地址
    int *scores[] = {class1, class2, class3};
    // 每个班级的人数（和指针数组一一对应）
    int classLen[] = {sizeof(class1)/sizeof(int), 
                      sizeof(class2)/sizeof(int), 
                      sizeof(class3)/sizeof(int)};
    int classNum = sizeof(scores)/sizeof(int*); // 班级数量

    3. 把指针数组作为函数参数传递，统一排序所有班级
    sortAllClass(scores, classLen, classNum);
    
    // 4. 把指针数组作为函数参数传递，统一输出所有班级
    printAllClass(scores, classLen, classNum);

    system("pause"); 
    return 0;
// }
/**/
// #include<stdio.h>
// int main()
// {
//     int i,j,r;
//     for(i=20,j=7;r=i%j;i=j,j=r)
//     continue;
//     printf("%3d",j);
// }
