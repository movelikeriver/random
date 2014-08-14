// Usage:
//   g++ vector_reallocation.cpp
//   ./a.out
//
// The program will be "Segmentation fault: 11" due to updating dangling pointer in &vector[i].

#include <time.h>  // clock_t, clock, CLOCKS_PER_SEC

#include <iostream>
#include <list>
#include <vector>

class TaskManager {
public:
  TaskManager() { }

  void AddTask(int* task) {
    tasks_.push_back(task);
  }

  void Run() {
    // In real life production, these tasks can be run in parallel.
    for (std::list<int*>::iterator it = tasks_.begin();
         it != tasks_.end(); ++it) {
      ReportCost(*it);
    }
  }

private:
  void ReportCost(int* latency_ms) {
    const int cost_ms = InsaneCompute();
    std::cout << "cost_ms: " << cost_ms << std::endl;
    *latency_ms = cost_ms;
  }

  int InsaneCompute() {
    std::cout << "executing InsaneCompute()..." << std::endl;
    const clock_t start = clock();
    for (int i = 2; i < 25; ++i) {   // don't set too crazy num  :)
      if (double(Recur(i+1)) / double(Recur(i)) < 0.0) {
	std::cout << "hmmm... that's impossible...";
      }
    }
    return int(double(clock() - start) / CLOCKS_PER_SEC * 1000.0);  // ms
  }

  int Recur(int n) {
    if (n <= 2) {
      return n;
    }
    int sum = 0;
    for (int i = 0; i < n; ++i) {
      sum += Recur(i);
    }
    return sum;
  }

  std::list<int*> tasks_;  // not own the memory.
};


void ScheduleTasks(const int n, std::vector<int>* data_vec,
                   TaskManager* task_manager) {
  for (int i = 0; i < n; ++i) {
    data_vec->push_back(i);  // dynamically add a new element.
    task_manager->AddTask(&(*data_vec)[data_vec->size() - 1]);
  }
}

void Test_ScheduleTasks() {
  std::vector<int> data_vec;  // own the memory.
  //  data_vec.reserve(9);
  //  Uncomment the line above can make the code pass, but in real life application, the num of tasks may not be determined beforehand, it could be more difficult to trace the problem because of reallocation after exceeding reserved size.
  const int num_tasks = 9;  // The 'Segmentation fault' is related to this number.
  TaskManager task_manager;
  ScheduleTasks(num_tasks, &data_vec, &task_manager);
  task_manager.Run();
  for (int i = 0; i < data_vec.size(); ++i) {
    std::cout << i << ", " << data_vec[i] << "\n";  // For debugging
  }
}

int main() {
  Test_ScheduleTasks();
}
