#include <iostream>
#include <vector>
#include <cmath>
#include <print>  // C++23: 现代化的格式化输出
#include <ranges> // C++20/23: 视图与转接器
#include <algorithm>

// 计算矩阵的行列式与秩
struct MatrixAnalysis
{
    double det;
    int rank;
};

MatrixAnalysis analyze_matrix(std::vector<double> &flat_data, int rows, int cols)
{
    // 使用二维索引映射 (模拟 C++23 mdspan 行为)
    auto at = [&](int r, int c) -> double &
    {
        return flat_data[r * cols + c];
    };

    double det = 1.0;
    int rank = 0;
    const double EPS = 1e-12; // 浮点数精度控制

    int pivot_row = 0;
    for (int j = 0; j < cols && pivot_row < rows; ++j)
    {
        // 1. 寻找当前列绝对值最大的行（选主元，提高稳定性）
        int sel = pivot_row;
        for (int i = pivot_row + 1; i < rows; ++i)
        {
            if (std::abs(at(i, j)) > std::abs(at(sel, j)))
                sel = i;
        }

        // 2. 如果主元太小，说明这一列是“空”的，跳过
        if (std::abs(at(sel, j)) < EPS)
        {
            det = 0;
            continue;
        }

        // 3. 交换行，符号取反
        if (sel != pivot_row)
        {
            for (int k = j; k < cols; ++k)
                std::swap(at(sel, k), at(pivot_row, k));
            det = -det;
        }

        det *= at(pivot_row, j);

        // 4. 消元：将下方所有行在该列变为 0
        for (int i = pivot_row + 1; i < rows; ++i)
        {
            double factor = at(i, j) / at(pivot_row, j);
            for (int k = j; k < cols; ++k)
            {
                at(i, k) -= factor * at(pivot_row, k);
            }
        }

        pivot_row++;
        rank++;
    }

    // 对于方阵，如果秩不足，行列式必为 0
    if (rows == cols && rank < rows)
        det = 0.0;

    return {det, rank};
}

int main()
{
    int n, m;
    std::print("请输入矩阵行数(N)和列数(M): ");
    if (!(std::cin >> n >> m))
        return 1;

    // 使用一维向量存储，性能更好
    std::vector<double> data(n * m);
    std::print("请按行输入 {} 个元素:\n", n * m);
    for (auto &x : data)
        std::cin >> x;

    // 结构化绑定：一次获取两个结果
    auto [determinant, rank] = analyze_matrix(data, n, m);

    // C++23 std::print 支持直接格式化
    std::print("\n{:=>25}\n", " 分析结果 ");
    if (n == m)
    {
        std::print("行列式 (Det):  {:.4f}\n", determinant);
    }
    else
    {
        std::print("行列式 (Det):  (非方阵无行列式)\n");
    }
    std::print("矩阵的秩 (Rank): {}\n", rank);
    std::print("是否满秩:        {}\n", (rank == std::min(n, m) ? "是" : "否"));
    std::print("{:=>25}\n", "");

    return 0;
}