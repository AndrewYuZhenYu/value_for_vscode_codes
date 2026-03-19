#include <stdio.h>
// setlocale(LC_ALL, "chs"); // 设置区域为简体中文（GBK）
void inverse(int array[], int nStart, int nInverseNumber);
int main()
{
    int arr[10];
    int nStart, nInverseNumber;

    printf("请输入10个整数：\n");
    for (int i = 0; i < 10; i++)
    {
        scanf("%d", &arr[i]);
    }
    printf("请输入起始位置nStart（从1开始计数）：");
    scanf("%d", &nStart);
    printf("请输入要逆序的元素个数nInverseNumber：");
    scanf("%d", &nInverseNumber);

    if (nStart < 1 || nStart > 10)
    {
        printf("错误：起始位置必须在1到10之间\n");
        return 1;
    }
    if (nInverseNumber < 0 || nStart + nInverseNumber - 1 > 10)
    {
        printf("错误：逆序范围超出数组边界\n");
        return 1;
    }
    if (nInverseNumber <= 1)
    {
        printf("注意：逆序元素个数小于等于1，数组保持不变\n");
    }

    printf("\n原数组为：");
    for (int i = 0; i < 10; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    inverse(arr, nStart, nInverseNumber);

    printf("新数组为：");
    for (int i = 0; i < 10; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
void inverse(int array[], int nStart, int nInverseNumber)
{
    int startIndex = nStart - 1;
    int endIndex = startIndex + nInverseNumber - 1;
    for (int i = 0; i < nInverseNumber / 2; i++)
    {
        int temp = array[startIndex + i];
        array[startIndex + i] = array[endIndex - i];
        array[endIndex - i] = temp;
    }
}