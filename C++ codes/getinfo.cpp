/*
 * @Author: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @Date: 2026-02-11 18:16:45
 * @LastEditors: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @LastEditTime: 2026-02-14 17:35:54
 * @FilePath: \VSCODE_NEW\C++ codes\getinfo.cpp
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
#include <iostream>
#include <cmath>
int main()
{
    using namespace std;
    // double sqrt(double);
    double x;
    // double pow(double,double);
    double answer = pow(5.0, 8.0);
    // x = sqrt(6.25);
    int carrots;
    cout << "How many carrots do you have?" << endl;
    cin >> carrots;
    std::cout << "Here are two more: ";
    carrots += 22;
    cout
        << "Now you have "
        << carrots
        << " carrots."
        << endl;
    // cout << x;
    cout << answer;
    return 0;
}