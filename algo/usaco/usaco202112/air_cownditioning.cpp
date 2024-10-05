// http://www.usaco.org/index.php?page=viewproblem2&cpid=1156

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void print_vec(vector<int> vec, string label) {
  return;
  cout << label << endl;
  for (int i=0; i<vec.size(); i++) {
    cout << vec[i] << ", ";
  }
  cout << endl;
}

int solution(vector<int> p, vector<int> t) {
  // p.size() == t.size(), not empty
  // [1, 2, 2, 2, -2, -1, 2] ==> [1, 2, 0, 2, 1, 0, 2]
  vector<int> delta;
  int d = p[0] - t[0];
  int prev = d;
  if (d < 0) {
    d = -d;
  }
  delta.push_back(d);
    
  for (int i = 1; i < p.size(); i++) {
    int d = p[i] - t[i];
    if (d == prev) {
      continue;
    }
    if (d * prev < 0) {
      delta.push_back(0);
    }
    prev = d;
    if (d < 0) {
      d = -d;
    }
    delta.push_back(d);
  }

  print_vec(delta, "delta");

  // process
  // 0, 3, 0, 4, 3, 0, 3
  // [0]
  // ret: 3

  int ret = 0;
  int last = delta[0];
  for (int i = 1; i < delta.size(); i++) {
    int d = delta[i];
    if (d < last) {
      // find bottom, handle top
      ret += last - d;
    }
    last = d;
  }
  ret += last;

  return ret;
}


int main() {
  int n;
  vector<int> p, t;
  cin >> n;
  for (int i=0; i<n; i++) {
    int a;
    cin >> a;
    p.push_back(a);
  }
  for (int i=0; i<n; i++) {
    int a;
    cin >> a;
    t.push_back(a);
  }

  print_vec(p, "p:");
  print_vec(t, "t:");

  int ret = solution(p, t);
  cout << "ret: " << ret << endl;
}
