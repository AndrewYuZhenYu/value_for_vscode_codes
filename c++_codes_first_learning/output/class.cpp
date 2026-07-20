// ===== 头文件与命名空间 =====
#include <iostream>  // 包含C++标准输入输出流库
using namespace std; // 引入std命名空间

// ===== 插入排序函数（带过程可视化输出） =====
void isort(int a[], int size)
{
    // 对数组a的前size个元素进行插入排序（升序）
    for (int i = 1; i < size; i++)
    {
        // 从第1个元素开始，共执行size-1轮
        int key = a[i]; // 保存当前待插入的元素值
        int j = i - 1;  // j指向已排序区间的最后一个元素

        while (j >= 0 && a[j] > key)
        {
            // 在已排序区间中从后向前扫描，找到key的插入位置
            a[j + 1] = a[j]; // 比key大的元素向后挪一位，腾出空间
            j--;             // 继续向前比较
        }
        a[j + 1] = key; // 将key插入到正确位置

        // ---------- 每轮结束后输出当前数组状态 ----------
        for (int k = 0; k < size; k++)
        {
            // 遍历数组所有元素
            cout << a[k];      // 输出当前元素值
            if (k == i)        // k==i的位置是已排序/未排序的分界线
                cout << " | "; // 竖线左边为已排序，右边为待排序
            else
                cout << "  "; // 普通元素用两个空格分隔
        }
        cout << endl; // 每轮输出后换行
    }
}

// ===== 主函数 =====
int main()
{
    int array[] = {55, 2, 6, 4, 32, 12, 9, 73, 26, 37}; // 待排序数组
    int len = sizeof(array) / sizeof(array[0]);         // 计算数组元素个数（总字节数 / 单个元素字节数）

    cout << "原始数组: "; // 输出原始数组标题
    for (int i = 0; i < len; i++)
    {
        // 遍历数组
        cout << array[i] << "  "; // 输出每个元素，用两个空格分隔
    }
    cout << "\n"
         << endl; // 换行并空一行，与排序过程隔开

    isort(array, len); // 调用插入排序函数（同时在每轮输出过程）

    cout << "\n排序结果: "; // 输出最终排序结果标题
    for (int i = 0; i < len; i++)
    {
        // 遍历已排序数组
        cout << array[i] << "  "; // 输出每个元素
    }
    cout << endl; // 最后的换行

    return 0; // 程序正常结束
}
