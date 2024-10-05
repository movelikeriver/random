#include <iostream>
#include <string>
#include <vector>
#include <utility>
using namespace std;


void print_roads(const vector<string>& roads) {
  for (int i = 0; i < roads.size(); i++) {
    cout << roads[i] << endl;
  }
}

void print_vec(const vector<int>& vec) {
  cout << "[";
  for (auto elem : vec) {
    cout << elem << ",";
  }
  cout << "]";
}

void print_pairs(const vector<vector<pair<vector<int>, vector<int>>>>& resp) {
  for (int i = 0; i < resp.size(); i++) {
    for (int j = 0; j < resp[i].size(); j++) {
      auto cur = resp[i][j];
      cout << "(";
      print_vec(cur.first);
      cout << ", ";
      print_vec(cur.second);
      cout << ")\t|";
    }
    cout << endl;
  }
}

vector<int> merge(const vector<int>& same, const vector<int>& turn, int k) {
  // [0, 2], [10, 11] ==> [0, 12, 11]
  vector<int> ret;
  for (auto elem : same) {
    ret.push_back(elem);
  }
  for (int i = 0; i < turn.size(); i++) {
    if (i+1 > k) break;

    if (i+1 < same.size()) {
      ret[i+1] += turn[i];
    } else {
      ret.push_back(turn[i]);
    }
  }
  return ret;
}

int route(const vector<string>& roads, int k) {
  // a a         a          ([0], [1])
  // a a         a          ([0], [1])
  // a a  ([0, 1], [0, 1])  ([0], [1])
  // a a  ([1], [0])        ([ ], [ ])
  vector<vector<pair<vector<int>, vector<int>>>> resp;
  for (int i = 0; i < roads.size(); i++) {
    vector<pair<vector<int>, vector<int>>> row;
    for (int j = 0; j < roads[i].size(); j++) {
      row.push_back(make_pair(vector<int>(), vector<int>()));
    }
    resp.push_back(row);
  }
  
  int size = resp.size();
  // last row
  int a = roads[size-1][size-2] == '.' ? 1 : 0;
  resp[size-1][size-2].first.push_back(a);
  resp[size-1][size-2].second.push_back(0);
  
  for (int j = size-3; j >= 0; j--) {
    if (roads[size-1][j] == '.') {
      for (auto elem : resp[size-1][j+1].first) {
	resp[size-1][j].first.push_back(elem);
      }
    } else {
      resp[size-1][j].first.push_back(0);
    }
    resp[size-1][j].second.push_back(0);
  }

  // last col
  a = roads[size-2][size-1] == '.' ? 1 : 0;
  resp[size-2][size-1].second.push_back(a);
  resp[size-2][size-1].first.push_back(0);

  for (int i = size-3; i >= 0; i--) {
    if (roads[i][size-1] == '.') {
      for (auto elem : resp[i+1][size-1].second) {
	resp[i][size-1].second.push_back(elem);
      }
    } else {
      resp[i][size-1].second.push_back(0);
    }
    resp[i][size-1].first.push_back(0);
  }

  for (int i = size-2; i >= 0; i--) {
    for (int j = size-2; j >= 0; j--) {
      if (roads[i][j] == '.') {
	vector<int> y = merge(resp[i+1][j].second, resp[i+1][j].first, k);
	vector<int> x = merge(resp[i][j+1].first, resp[i][j+1].second, k);
	resp[i][j] = make_pair(x, y);
      } else {
	resp[i][j].first.push_back(0);
	resp[i][j].second.push_back(0);
      }
    }
  }
  
  //  print_pairs(resp);

  int ret = 0;
  auto v = resp[0][0];
  for (int i = 0; i < v.first.size(); i++) {
    if (i > k) break;

    ret += v.first[i];
  }
  for (int i = 0; i < v.second.size(); i++) {
    if (i > k) break;

    ret += v.second[i];
  }
  
  return ret;
}

int main() {
  int n_case;
  cin >> n_case;
  for (int i = 0; i < n_case; i++) {
    int n, k;
    cin >> n >> k;
    vector<string> roads;
    for (int j = 0; j < n; j++) {
      string row;
      cin >> row;
      roads.push_back(row);
    }

    // print_roads(roads);
    // cout << endl;

    int ret = route(roads, k);
    cout << ret << endl;
  }

  
}
