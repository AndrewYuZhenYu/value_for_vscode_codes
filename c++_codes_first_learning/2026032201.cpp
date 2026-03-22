#include <iostream>
#include <cmath>
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
    cout << "The number of x is " << x << endl;
    cout << "x的三次方是" << pow(x, 3) << "\n";
    cout << "x的五次方是" << pow(x, 5) << endl;
}