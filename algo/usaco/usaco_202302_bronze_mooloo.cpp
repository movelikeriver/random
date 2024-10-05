#include <iostream>
#include <vector>

using namespace std;

int main() {
  // 2 4
  // 1 7 9 21 25
  //
  // 21 25 -> k+5 vs k+1+k+1 -> k+9
  // 9 [21 25] -> 21-9 vs k+1 -> += k+1
  // 7 [9 21 25] -> 9-7 vs k+1 -> += 2
  // 1 [7 9 21 25] -> 7-1 vs k+1 -> += k+1

  long long n, k;
  cin >> n >> k;
  vector<long long> vec;
  for (long long i = 0; i < n; i++) {
    long long d;
    cin >> d;
    vec.push_back(d);
  }

  if (n == 1) {
    return k+1;
  }

  long long ret = 0;
  long long last1 = vec[vec.size()-1];
  long long last2 = vec[vec.size()-2];
  if (k+1+last1-last2 > k+1+k+1) {
    ret = k+1+k+1;
  } else {
    ret = k+1 + last1-last2;
  }

  // cout << ret << endl;
  for (long long i = vec.size()-3; i >= 0; i--) {
    long long last = vec[i+1];
    long long curr = vec[i];
    if (last - curr > k + 1) {
      ret += 1 + k;
    } else {
      ret += last - curr;
    }
    // cout << i << ": " << vec[i] << ", " << ret << endl;
  }

  cout << ret << endl;
}
