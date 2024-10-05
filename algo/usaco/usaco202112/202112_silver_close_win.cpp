#include <algorithm>
#include <iostream>
#include <map>
#include <vector>

using namespace std;

void cal_value_in_interval(const vector<long long>& idx_vec, const map<long long, long long>& values,
			   long long start, long long end, double len,
			   long long *first_v, long long* second_v) {
  // [0:4, 4:6, 8:10, 10:8], 12:12, 13:14
  long long p1=start, p2=start;
  long long sub_sum = 0, max_sum = 0;
  for (; p1 <= end; p1++) {
    for (; p2 <= end; p2++) {
      if (idx_vec[p2] - idx_vec[p1] < len) {
	sub_sum += values.find(idx_vec[p2])->second;
	if (sub_sum > max_sum) {
	  // cout << "p1: " << p1 << ", " << "p2: " << p2 << endl;
	  max_sum = sub_sum;
	}
      }
    }
    sub_sum -= values.find(idx_vec[p1])->second;
  }
  *first_v = max_sum;

  long long total_sum = 0;
  for (long long i = start; i <= end; i++) {
    total_sum += values.find(idx_vec[i])->second;
  }
  *second_v = total_sum - *first_v;
}

void print_vec(const vector<long long>& vec, long long start, long long end) {
  cout << "[";
  for (long long i = start; i <= end; i++) {
    cout << vec[i] << ",";
  }
  cout << "]" << endl;
}

int main() {
  int k, m, n;
  cin >> k >> m >> n;
  //  cout << k << ", " << m << ", " << n << endl;
  vector<long long> vec_p, vec_f;
  map<long long, long long> map_t;
  for (int i = 0; i < k; i++) {
    int p, t;
    cin >> p >> t;
    vec_p.push_back(p);
    map_t[p] = t;
  }
  sort(vec_p.begin(), vec_p.end());

  for (int i = 0; i < m; i++) {
    int f;
    cin >> f;
    vec_f.push_back(f);
  }
  sort(vec_f.begin(), vec_f.end());

  //  print_vec(vec_p, 0, vec_p.size()-1);
  //  print_vec(vec_f, 0, vec_f.size()-1);

  vector<long long> processed;
  
  // merge sort
  long long idx_p=0, idx_f=0;
  long long p1=0, p2=0;
  bool in_p = false;
  for (; idx_p < vec_p.size() && idx_f < vec_f.size();) {
    if (vec_p[idx_p] < vec_f[idx_f]) {
      if (!in_p) {
	// switch to vec_p
	in_p = true;
	p1 = idx_p;
      }
      p2 = idx_p;
      idx_p++;
    } else {
      if (in_p) {
	// switch to vec_f
	//  [ f, | p, ..., p, | f ]
	//                      ^
	double len = 0;
	if (idx_f == 0) {
	  len = vec_f[idx_f] * 2;
	} else {
	  len = (vec_f[idx_f] - vec_f[idx_f-1]) * 0.5;
	}
	//	print_vec(vec_p, p1, p2);

	long long first_v, second_v;
	cal_value_in_interval(vec_p, map_t, p1, p2, len, &first_v, &second_v);

	//	cout << "f(" << idx_f-1 << ", " << idx_f << ") "
	//	     << vec_f[idx_f-1] << "~" << vec_f[idx_f] << " len=" << len << " | " << first_v << " ~ " << second_v << endl;

	processed.push_back(first_v);
	if (second_v > 0) {
	  processed.push_back(second_v);
	}
	in_p = false;
      }
      idx_f++;
    }
  }

  if (idx_p < vec_p.size()) {
    p1 = idx_p;
    p2 = vec_p.size() - 1;
  }
  //  print_vec(vec_p, p1, p2);
  double len = 0;
  if (idx_f >= vec_f.size()) {
    len = vec_p[p2] - vec_p[p1] + 1;
    //    cout << "p2=" << p2 << ", p1=" << p1 << "====" << vec_p[p2] << ", " << vec_p[p1] << endl;
  } else {
    len = vec_f[idx_f] - vec_f[idx_f-1];
  }

  long long first_v, second_v;
  cal_value_in_interval(vec_p, map_t, p1, p2, len, &first_v, &second_v);

  //  cout << "f(" << idx_f-1 << ", " << idx_f << ") " << len << " | " << first_v << " ~ " << second_v << endl;

  processed.push_back(first_v);
  if (second_v > 0) {
    processed.push_back(second_v);
  }

  //  for (long long elem : processed) {
  //    cout << elem << ", ";
  //  }
  //  cout << endl;
  long long ret = 0;
  sort(processed.begin(), processed.end());

  //print_vec(processed, 0, processed.size()-1);

  
  if (n > processed.size()) {
    n = processed.size();
  }
  int start = processed.size()-1;
  int end = processed.size()-n;
  //  cout << start << ", " << end << endl;
  for (int i = start; i >= end; i--) {
    //    cout << "i=" << i << ": " << processed[i] << ", ";
    ret += processed[i];
  }

  cout << ret << endl;
}
