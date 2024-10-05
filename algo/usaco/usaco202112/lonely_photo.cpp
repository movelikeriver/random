// http://www.usaco.org/index.php?page=viewproblem2&cpid=1155

#include <string>
#include <iostream>

using namespace std;

int main() {
  int n;
  string input;
  cin >> n;
  cin >> input;

  // cout << n << " " << input << endl;

  int ret = 0;
  // HHGHHHHG
  for (int i = 0; i < input.length(); i++) {
    char ch = input[i];

    int left = i-1;
    for (; left >= 0; left--) {
      if (input[left] == ch) {
	// find a same type
	break;
      }
    }
    int right = i+1;
    for (; right < input.length(); right++) {
      if (input[right] == ch) {
	// find a same type
	break;
      }
    }
    ret += (i - left - 1) * (right - i - 1);

    if (i - left - 2 > 0) {
      ret += i - left - 2;
    }
    if (right - i - 2 > 0) {
      ret += right - i - 2;
    }
  }

  cout << ret << endl;
}
