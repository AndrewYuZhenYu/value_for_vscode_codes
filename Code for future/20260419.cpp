#include <iostream>
#include <tuple>
#include <iomanip>

using namespace std;

// ============================================================
// 1. 辗转相除法（欧几里得算法）— 递归版
//    GCD(a, b) = GCD(b, a mod b), 直到 b = 0
// ============================================================
int gcdEuclideanRecursive(int a, int b) {
    if (b == 0) return a;
    return gcdEuclideanRecursive(b, a % b);
}

// ============================================================
// 2. 辗转相除法（欧几里得算法）— 迭代版
// ============================================================
int gcdEuclideanIterative(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// ============================================================
// 3. 扩展欧几里得算法 (Extended Euclidean Algorithm)
//    求 GCD(a, b) 以及 Bézout 系数 x, y 使得 ax + by = gcd(a, b)
// ============================================================
tuple<int, int, int> gcdExtended(int a, int b) {
    if (b == 0) {
        return {a, 1, 0};
    }
    auto [gcd, x1, y1] = gcdExtended(b, a % b);
    // x = y1, y = x1 - (a / b) * y1
    int x = y1;
    int y = x1 - (a / b) * y1;
    return {gcd, x, y};
}

// ============================================================
// 4. 扩展欧几里得算法（迭代版）
// ============================================================
tuple<int, int, int> gcdExtendedIterative(int a, int b) {
    int x0 = 1, y0 = 0, x1 = 0, y1 = 1;
    int origA = a, origB = b;

    while (b != 0) {
        int q = a / b;
        int r = a % b;
        a = b;
        b = r;

        int tmpX = x0 - q * x1;
        int tmpY = y0 - q * y1;
        x0 = x1; y0 = y1;
        x1 = tmpX; y1 = tmpY;
    }
    return {a, x0, y0};
}

// ============================================================
// 5. 更相减损术（减法版欧几里得算法）
//    中国古代《九章算术》中的方法：
//    若两数相等则返回；若为偶数则不断除以2；
//    否则大数减小数，直到相等
// ============================================================
int gcdSubtraction(int a, int b) {
    // 处理负数
    a = abs(a);
    b = abs(b);
    if (a == 0) return b;
    if (b == 0) return a;

    // 记录公有的因子2的个数
    int shift = 0;
    while (((a | b) & 1) == 0) {
        a >>= 1;
        b >>= 1;
        shift++;
    }

    // 使 a 为奇数
    while ((a & 1) == 0) a >>= 1;

    do {
        while ((b & 1) == 0) b >>= 1;
        if (a > b) swap(a, b);
        b = b - a;
    } while (b != 0);

    return a << shift;
}

// ============================================================
// 6. Stein 算法（二进制 GCD 算法）
//    仅使用移位、比较和减法，无需除法/取模
//    - 若 a, b 均为偶数: gcd(a, b) = 2 * gcd(a/2, b/2)
//    - 若 a 偶 b 奇:     gcd(a, b) = gcd(a/2, b)
//    - 若 a 奇 b 偶:     gcd(a, b) = gcd(a, b/2)
//    - 若 a, b 均为奇数:  gcd(a, b) = gcd(|a-b|, min(a,b))
// ============================================================
int gcdStein(int a, int b) {
    a = abs(a);
    b = abs(b);
    if (a == 0) return b;
    if (b == 0) return a;

    // 提取公因子 2
    int k = 0;
    while (((a | b) & 1) == 0) {
        a >>= 1;
        b >>= 1;
        k++;
    }

    // 使 a 为奇数
    while ((a & 1) == 0) a >>= 1;

    while (b != 0) {
        while ((b & 1) == 0) b >>= 1;
        if (a > b) swap(a, b);
        b = b - a;
    }

    return a << k;
}

// ============================================================
// 7. 暴力枚举法（穷举公约数）
//    从 1 到 min(a,b) 逐个检查
// ============================================================
int gcdBruteForce(int a, int b) {
    a = abs(a);
    b = abs(b);
    int gcd = 1;
    int limit = min(a, b);
    for (int i = 2; i <= limit; i++) {
        if (a % i == 0 && b % i == 0) {
            gcd = i;
        }
    }
    return gcd;
}

// ============================================================
// 8. 多个数的 GCD（使用欧几里得算法逐对计算）
// ============================================================
int gcdMultiple(const vector<int>& nums) {
    if (nums.empty()) return 0;
    int result = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        result = gcdEuclideanIterative(result, nums[i]);
        if (result == 1) break;  // 提前终止：互质时 GCD = 1
    }
    return result;
}

// ============================================================
// 主程序 — 演示所有 GCD 算法
// ============================================================
int main() {
    cout << fixed << setprecision(10);
    cout << "========== 不同方法求最大公约数 (GCD) ==========\n\n";

    // 测试数据
    int testCases[][2] = {
        {48, 18},
        {56, 98},
        {1071, 462},
        {0, 42},
        {1, 999},
        {1024, 256}
    };

    cout << "测试各算法:\n";
    cout << string(70, '-') << endl;

    for (auto& tc : testCases) {
        int a = tc[0], b = tc[1];

        cout << "\ngcd(" << a << ", " << b << "):\n";
        cout << "  1. 欧几里得(递归):       " << gcdEuclideanRecursive(a, b) << endl;
        cout << "  2. 欧几里得(迭代):       " << gcdEuclideanIterative(a, b) << endl;

        auto [g, x, y] = gcdExtended(a, b);
        cout << "  3. 扩展欧几里得(递归):   " << g
             << "  (Bézout: " << x << "*" << a << " + " << y << "*" << b << " = " << g << ")" << endl;

        auto [gi, xi, yi] = gcdExtendedIterative(a, b);
        cout << "  4. 扩展欧几里得(迭代):   " << gi
             << "  (Bézout: " << xi << "*" << a << " + " << yi << "*" << b << " = " << gi << ")" << endl;
        cout << "  5. 更相减损术:           " << gcdSubtraction(a, b) << endl;
        cout << "  6. Stein (二进制GCD):    " << gcdStein(a, b) << endl;
        cout << "  7. 暴力枚举:             " << gcdBruteForce(a, b) << endl;
    }

    // --- 多数的 GCD ---
    cout << "\n" << string(70, '-') << endl;
    cout << "\n8. 多个数的 GCD:\n";
    vector<int> nums = {36, 48, 60, 72};
    cout << "   gcd(";
    for (size_t i = 0; i < nums.size(); i++) {
        cout << nums[i];
        if (i < nums.size() - 1) cout << ", ";
    }
    cout << ") = " << gcdMultiple(nums) << endl;

    // --- 保留交互 ---
    cout << "\n" << string(70, '-') << endl;
    cout << "\n========== 交互测试 ==========\n";
    cout << "请输入两个整数求 GCD (空格分隔): ";
    int userA, userB;
    cin >> userA >> userB;
    cout << "gcd(" << userA << ", " << userB << ") = "
         << gcdEuclideanIterative(userA, userB) << endl;

    auto [ug, ux, uy] = gcdExtended(userA, userB);
    cout << "Bézout 恒等式: " << ux << "*" << userA << " + "
         << uy << "*" << userB << " = " << ug << endl;

    cout << "\n程序结束。\n";
    return 0;
}
