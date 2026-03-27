#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

typedef long long ll;
const int MOD = 998244353;

ll power(ll base, ll exp)
{
    ll res = 1;
    base %= MOD;
    while (exp > 0)
    {
        if (exp % 2 == 1)
            res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

void solve()
{
    int n;
    if (!(cin >> n))
        return;
    vector<ll> a(n);
    for (int i = 0; i < n; ++i)
    {
        cin >> a[i];
    }
    sort(a.begin(), a.end());

    ll total_sum = 0;
    for (int i = 0; i < n; ++i)
    {
        ll val = (a[i] % MOD * power(2, i)) % MOD;
        val = (val * power(2, n - 1 - i)) % MOD;

        ll multiplier = power(2, i);
        ll contribution = (a[i] % MOD * multiplier) % MOD;
        contribution = (contribution * power(2, n - 1 - i)) % MOD;

        total_sum = (total_sum + contribution) % MOD;
    }

    total_sum = 0;
    for (int i = 0; i < n; ++i)
    {
        ll coeff = power(3, i);
        ll term = (a[i] % MOD * coeff) % MOD;
        term = (term * power(2, n - 1 - i)) % MOD;
        total_sum = (total_sum + term) % MOD;
    }

    cout << total_sum << endl;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t))
        return 0;
    while (t--)
    {
        solve();
    }
    return 0;
}