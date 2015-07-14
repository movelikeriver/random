#include <iostream>
#include <vector>
#include <string>
#include <stack>
using namespace std;

// Parses string into a vector by {} or nested {:{}} {{}{}}.
// Returns false if the input string format is invalid.
bool ParseTemplate(const string& str, vector<string>* vec) {
  stack<int> s;
  bool last_open = false;
  for (int i = 0; i < str.length(); i++) {
    char ch = str[i];
    switch (ch) {
      case '{':
        if (last_open) {
          // insert a hidden ':'.
          s.push(i);
          s.push(-1);
        }
        s.push(i);
        last_open = true;
        break;

      case ':':
        if (last_open) {
          s.push(i);
          s.push(-1);
        }
        last_open = false;
        break;

      case '}': {
        if (s.empty()) {
          // no '{' before this '}'.
          return false;
        }

        // choose "{match}" by default.
        int last_index = s.top();
        s.pop();
        int end_index = i;
        if (last_index == -1) {
          // choose "{match:".
          end_index = s.top();
          s.pop();
          if (s.empty()) {
            // no '{' before this ':'.
            return false;
          }
          last_index = s.top();
          s.pop();
        }
        string item =
            StrCat(str.substr(last_index, end_index - last_index), "}");
        vec->emplace_back(std::move(item));
        last_open = false;
      } break;

      default:
        break;
    }  // switch
  }

  return s.empty();
}

int main() {
  string aa = "asdf{cc:{dd:{ee}}afd{ff}}w{bbb{aa}f{cc}e}fw";
  vector<string> vec;
  cout << ParseLine(aa, &vec) << endl;
  for (const auto& elem : vec) {
    cout << elem << ", ";
  }
  cout << endl;
}
