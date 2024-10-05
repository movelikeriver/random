#include <iostream>

using namespace std;

int main() {
  long long n, t;
  cin >> n >> t;
  // 1 10 -> ret, start, len = 0, 1, 10
  // 5 10 -> ret, start, len = 0, 1, 10+10
  //
  // 1 3 -> ret, start, len = 0, 1, 3
  // 5 3 -> ret, start, len = 3, 5, 3
  //
  // 1 1 -> ret, start, len = 0, 1, 1
  // 4 2 -> ret, start, len = 1, 4, 2
  //
  // 1 1 -> ret, start, len = 0, 1, 1
  // 5 2 -> ret, start, len = 1, 5, 2
  // 5 2 -> ret, start, len = 1, 5, 4
  long long len = 0;
  long long ret = 0;
  long long start = 1;
  for (int i = 0; i < n; i++) {
    long long day, h;
    cin >> day >> h;
    if (day > start + len - 1) {
      ret += len;
      start = day;
      len = h;
    } else {
      len += h;
    }
    // cout << "ret = " << ret << ", start = " << start << ", len = " << len << endl;
  }

  if (start + len - 1 > t) {
    ret += (t-start+1);
  } else {
    ret += len;
  }

  cout << ret << endl;
}
