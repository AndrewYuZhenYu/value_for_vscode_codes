/*
 * @Author: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @Date: 2026-02-15 18:01:02
 * @LastEditors: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @LastEditTime: 2026-02-15 18:10:55
 * @FilePath: \VSCODE_NEW\C++ codes\(26021501)sizeof test.cpp
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// limits.cpp -- some integer limits
#include <iostream>
#include <climits> // use limits.h for older systems

int main()
{
    using namespace std;

    int n_int = INT_MAX;      // initialize n_int to max int value
    short n_short = SHRT_MAX; // symbols defined in climits file
    long n_long = LONG_MAX;
    long long n_llong = LLONG_MAX;
    int fun_1(20);
    // sizeof operator yields size of type or of variable
    cout << "int is " << sizeof(int) << " bytes." << endl;
    cout << "short is " << sizeof n_short << " bytes." << endl;
    cout << "long is " << sizeof n_long << " bytes." << endl;
    cout << "long long is " << sizeof n_llong << " bytes." << endl;
    cout << endl;

    cout << "Maximum values:" << endl;
    cout << "int: " << n_int << endl;
    cout << "short: " << n_short << endl;
    cout << "long: " << n_long << endl;
    cout << "long long: " << n_llong << endl
         << endl;

    cout << "Minimum int value = " << INT_MIN << endl;
    cout << "Bits per byte = " << CHAR_BIT << endl;
    cout << fun_1<<endl;
    return 0;
}