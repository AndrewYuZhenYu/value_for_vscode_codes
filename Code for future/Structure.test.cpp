#include<stdio.h>
#include<string.h>
// struct dog
// {
//     int sex;
//     int age;
// };



// struct dog aaa[3];
// struct student
// {
// char name[30];
// long num;
// double score;
// char add[30];
// double height;
// };



// struct student std1,std2;
// int main(){
// strcpy(std1.name,"Yuzhenyu");
// std1.num=25531089;
// std1.score=100.0;
// strcpy(std1.add,"Tangchenyipin");
// std1.height=183.0;
// printf("Name=%s\nNum=%0ld\nScore=%lf\nAdd:%s\nheight:%lf\n",std1.name,std1.num,std1.score,std1.add,std1.height);



// }
// int main()
// {
//     printf("请依次输入狗狗的性别和年龄（性别1代表公狗，0代表母狗）\n");
//     for (int i=0;i<3;i++)
//     {
        
//         scanf("%d%d",aaa[i].sex,aaa[i].age);
//         printf("\n");
//     }
//     for(int i=0;i<3;i++)
//     {
//         printf("%d  %d\n",aaa[i].sex,aaa[i].age);

//     }
// }


struct student
{
    char name[20];
    int num;
    int score;
};
int main()
{
struct student ass[3]={{"ChenningYang",19221001,100},{"Yuzhenyu",25531089,98},{"fourier",18180505,99}};
for (int i=0;i<3;i++)
{
    printf("%-s  %-d  %-d\n",ass[i].name,ass[i].num,ass[i].score);
}
}