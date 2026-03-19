/*
 * @Author: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @Date: 2026-03-18 22:42:02
 * @LastEditors: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @LastEditTime: 2026-03-18 22:42:27
 * @FilePath: \value_for_vscode_codes\C++ codes\(26021401)convert.cpp
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
#include <iostream>
using namespace std;
int stonetolb(int);
int main()
{
    // short int fuck=10;
    int stone;
    long long ll;
    cout << "Enter the weight in stone: ";
    cin >> stone;
    int pounds = stonetolb(stone);
    cout << stone << " stone= ";
    cout << sizeof(ll);
    std::cout << pounds << " pounds." << endl;
    // std::cout<<fuck;
    return 0;
}
int stonetolb(int sts)
{
    return 14 * sts;
}