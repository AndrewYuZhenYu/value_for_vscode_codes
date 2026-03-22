#include <iostream>
double square(double x)
{
    return x * x;
}
int main()
{
    using namespace std;
    double x{0};
    auto test_1 = 3.1415926;
    // cout << "the number of test_1 is " << test_1 << "\n";
    cin >> x;
    cout << "The number of x is " << x;
}