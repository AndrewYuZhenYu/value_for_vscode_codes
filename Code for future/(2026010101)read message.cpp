/*
 * @Author: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @Date: 2026-02-09 19:42:06
 * @LastEditors: AndrewYuZhenYu zhenyu_yu@outlook.com
 * @LastEditTime: 2026-02-09 22:09:50
 * @FilePath: \VSCODE_NEW\Code for future\(2026010101)read message.cpp
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
#include <stdio.h>

int main()
{
    long long n, k; // 用 long long 避免溢出
    scanf("%lld%lld", &n, &k);
    long long total = n; // 先算上初始的 n 根
    long long butts = n; // 初始烟蒂数 = 初始烟数

    while (butts >= k)
    {
        long long new_cig = butts / k; // 这次能换的新烟
        total += new_cig;              // 加到总数里
        butts = (butts % k) + new_cig; // 新的烟蒂 = 剩余烟蒂 + 新烟产生的烟蒂
    }

    printf("%lld\n", total);
    return 0;
}