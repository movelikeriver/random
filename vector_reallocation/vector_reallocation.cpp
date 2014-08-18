// Usage:
//   alias g++="g++ -std=c++11"
//   g++ vector_reallocation.cpp
//   ./a.out  (for multiple times)
//
// The program will end up with:
//
//   Before:
//   0, 0
//   1, 1
//   2, 2
//   3, 3
//   4, 4
//   5, 5
//   6, 6
//   7, 7
//   8, 8
//   cost_ms: 13403
//   cost_ms: 13426
//   cost_ms: 13517
//   cost_ms: 13529
//   cost_ms: 13528
//   cost_ms: 13499
//   cost_ms: 13501
//   cost_ms: 13524
//   cost_ms: 13527
//   After:
//   0, 0
//   1, 1
//   2, 2
//   3, 3
//   4, 4
//   5, 5
//   6, 6
//   7, 7
//   8, 13501
//   a.out(28325,0x7fff78223310) malloc: *** error for object 0x7fdddb403968: incorrect checksum for freed object - object was probably modified after being freed.
//   *** set a breakpoint in malloc_error_break to debug
//   Abort trap: 6
//
// or "Segment fault: 11" (mostly if running in single thread mode).
//
// It's due to updating dangling pointer in &vector[i].

#include <time.h>  // clock_t, clock, CLOCKS_PER_SEC

#include <iostream>
#include <list>
#include <thread>
#include <vector>

class TaskManager {
public:
  TaskManager() { }

  void AddTask(int* task) {
    tasks_.push_back(task);
  }

  void Run() {
    std::vector<std::thread> thread_vec;
    // Run in parallel.
    for (int* latency : tasks_) {
      thread_vec.push_back(std::thread(TaskManager::ReportCost, latency));
    }

    for (std::thread& t : thread_vec) {
      t.join();
    }
  }

private:
  static void ReportCost(int* latency_ms) {
    const int cost_ms = InsaneCompute();
    std::cout << "cost_ms: " << cost_ms << std::endl;
    *latency_ms = cost_ms;
  }

  static int InsaneCompute() {
    const clock_t start = clock();
    for (int i = 2; i < 27; ++i) {   // don't set too crazy num  :)
      if (double(Recur(i+1)) / double(Recur(i)) < 0.0) {
	std::cout << "hmmm... that's impossible...";
      }
    }
    return int(double(clock() - start) / CLOCKS_PER_SEC * 1000.0);  // ms
  }

  static int Recur(int n) {
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
    // Pointer to the address of container's index, but not element directly.
    task_manager->AddTask(&(*data_vec)[data_vec->size() - 1]);
  }
}

void Test_ScheduleTasks() {
  std::vector<int> data_vec;  // own the memory.
  //  data_vec.reserve(9);
  //  Uncomment the line above can make the code pass, but in real life application, the num of tasks may not be determined beforehand, it could be more difficult to trace the problem because of reallocation after exceeding reserved size.
  const int num_tasks = 9;  // The error is related to this number.
  TaskManager task_manager;
  ScheduleTasks(num_tasks, &data_vec, &task_manager);

  std::cout << "Before:\n";
  for (int i = 0; i < data_vec.size(); ++i) {
    std::cout << i << ", " << data_vec[i] << "\n";  // For debugging
  }
  task_manager.Run();
  std::cout << "After:\n";
  for (int i = 0; i < data_vec.size(); ++i) {
    std::cout << i << ", " << data_vec[i] << "\n";  // For debugging
  }
}

int main() {
  Test_ScheduleTasks();
}
