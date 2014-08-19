// Usage:
//   alias g++="g++ -std=c++11"
//   g++ vector_reallocation.cpp
//   ./a.out  (for multiple times)
//
// This code was originally written for showing a bug, later I changed
// it for benchmark among programming languages.
//
// If with bug (see main() function below), the program will end up with:
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

#include <sys/time.h>

#include <iostream>
#include <list>
#include <thread>
#include <vector>

// Don't set too crazy num.
// In 4-CPU Mac
// $ g++ --version
//  Apple LLVM version 5.0 (clang-500.2.79) (based on LLVM 3.3svn)
//  Target: x86_64-apple-darwin13.3.0
//  Thread model: posix
// For RECUR_N=40, num_tasks=9:
//   2118ms * 9 sequentially
//   9733ms in parallel
static const int RECUR_N = 40;
static const int NUM_TASKS = 9;  // The error is related to this number.

class TaskManager {
public:
  TaskManager() { }

  void AddTask(int* task) {
    tasks_.push_back(task);
  }

  void Run() {
    //    RunInParallel();
    RunSequentially();
  }

private:
  void RunSequentially() {
    for (int* latency : tasks_) {
      TaskManager::ReportCost(latency);
    }
  }

  void RunInParallel() {
    std::vector<std::thread> thread_vec;
    for (int* latency : tasks_) {
      thread_vec.push_back(std::thread(TaskManager::ReportCost, latency));
    }

    for (std::thread& t : thread_vec) {
      t.join();
    }
  }

  static void ReportCost(int* latency_ms) {
    const int cost_ms = InsaneCompute();
    std::cout << "cost_ms: " << cost_ms << std::endl;
    *latency_ms = cost_ms;
  }

  static int InsaneCompute() {
    std::cout << "Start InsaneCompute()...\n";
    struct timeval start, end;
    gettimeofday(&start, NULL);
    for (int i = 2; i < RECUR_N; ++i) {
      if (Recur(i) < 1) {
	std::cout << "int overflow...\n";
      }
    }
    std::cout << "Verify the value: " << Recur(RECUR_N) << ", "
	      << (float)Recur(RECUR_N-1)/(float)Recur(RECUR_N) << std::endl;

    gettimeofday(&end, NULL);
    long sec  = end.tv_sec  - start.tv_sec;
    long usec = end.tv_usec - start.tv_usec;
    return (int)(((sec)*1000 + usec/1000.0) + 0.5);  // ms
  }

  static int Recur(int n) {
    if (n <= 2) {
      return n;
    }
    return Recur(n-1) + Recur(n-2);
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

const std::string GetNowString() {
  time_t     now = time(0);
  struct tm  tstruct;
  char       buf[40];
  strftime(buf, sizeof(buf), "%Y/%m/%d %X", localtime(&now));
  return buf;
}

void Test_ScheduleTasks() {
  std::vector<int> data_vec;  // own the memory.
  // Comment the line below will make the job crash due to address
  // change during container's memory reallocation.  See comment on
  // top of this file.
  data_vec.reserve(NUM_TASKS);
  TaskManager task_manager;
  ScheduleTasks(NUM_TASKS, &data_vec, &task_manager);

  std::cout << GetNowString() << " Before:\n";
  for (int i = 0; i < data_vec.size(); ++i) {
    std::cout << i << ", " << data_vec[i] << "\n";  // For debugging
  }
  task_manager.Run();
  std::cout << GetNowString() << " After:\n";
  for (int i = 0; i < data_vec.size(); ++i) {
    std::cout << i << ", " << data_vec[i] << "\n";  // For debugging
  }
}

int main() {
  Test_ScheduleTasks();
}
