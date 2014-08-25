// Usage:
//   alias g++="g++ -std=c++11"
//   g++ -Ofast -march=native vector_reallocation.cpp
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
#include <string>
#include <thread>
#include <vector>

// Don't set too crazy num.
// In 4-CPU Mac
// $ g++ --version
//  Apple LLVM version 5.0 (clang-500.2.79) (based on LLVM 3.3svn)
//  Target: x86_64-apple-darwin13.3.0
//  Thread model: posix
//
// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
// RUN_IN_PARALLEL=0, total in ms: 13317
//
// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
// RUN_IN_PARALLEL=1, total in ms: 6394
// 2.0827 x
//
// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=0, total in ms: 75175
//
// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=1, total in ms: 33619
// 2.2361 x
//
// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=0, total in ms: 503682
//
// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=1, total in ms: 175475
// 2.8704 x

typedef long long int64;

static bool RUN_IN_PARALLEL = false;
static int RECUR_N = 40;
static const int NUM_TASKS = 9;  // The error is related to this number.

static const int64 MIN_PRIME_N = 100 * 1000;
static const int64 MAX_PRIME_N = 300 * 1000;

enum TestMode {
  FIBONACCI_RECUR = 0,
  FIBONACCI_FAST = 1,
  PRIME_NUM = 2,
};
static TestMode TEST_MODE = FIBONACCI_RECUR;

std::string GetTestModeString(TestMode test_mode) {
  switch (test_mode) {
  case FIBONACCI_RECUR:
    return "FIBONACCI_RECUR";
  case FIBONACCI_FAST:
    return "FIBONACCI_FAST";
  case PRIME_NUM:
    return "PRIME_NUM";
  default:
    break;
  }
  return "INVALID_TestMode";
}


class CpuTimer {
public:
  CpuTimer() {}

  void Start() {
    gettimeofday(&start_, NULL);
  }
  void Stop() {
    gettimeofday(&end_, NULL);
  }
  int GetInMs() {
    long sec  = end_.tv_sec  - start_.tv_sec;
    long usec = end_.tv_usec - start_.tv_usec;
    return (int)(((sec)*1000 + usec/1000.0) + 0.5);  // ms
  }

private:
  struct timeval start_;
  struct timeval end_;
};

struct TestResult {
  std::string overall;
  std::string details;
  int64 cost_in_ms;
};

class TaskManager {
public:
  TaskManager() { }

  void AddTask(int* task) {
    tasks_.push_back(task);
  }

  void Run() {
    if (RUN_IN_PARALLEL) {
      RunInParallel();
    } else {
      RunSequentially();
    }
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
    CpuTimer timer;
    timer.Start();

    switch (TEST_MODE) {
    case FIBONACCI_RECUR:
      FibonacciRecur(RECUR_N);
      break;
    case FIBONACCI_FAST:
      FibonacciFast(RECUR_N);
      break;
    case PRIME_NUM:
      PrimeNumTest();
      break;
    default:
      break;
    }

    timer.Stop();
    return timer.GetInMs();
  }

  static void PrimeNumTest() {
    std::cout << "Starting PrimeNumTest()...\n";
    for (int i = MIN_PRIME_N; i < MAX_PRIME_N; i++) {
      IsTwoPrimeMultipleDummy(i);
    }
  }

  static bool IsTwoPrimeMultipleDummy(const int64 num) {
    const int64 n = num / 2;
    bool found = false;
    for (int64 part1 = 2; part1 <= n; part1++) {
      if (num % part1 != 0) {
	continue;
      }
      const int64 part2 = num / part1;
      if (part1 > part2) {
	break;
      }
      if (!IsPrimeNumDummy(part1)) {
	continue;
      }
      if (!IsPrimeNumDummy(part2)) {
	continue;
      }
      if (part1 > 500 && part2 > 500) {
	std::cout << "within " << MAX_PRIME_N << ", " << num << " = "
		  << part1 << " * " << part2 << "\n";
      }
      found = true;
    }
    return found;
  }

  static bool IsPrimeNumDummy(const int64 num) {
    const int64 n = num / 2;
    for (int64 i = 2; i <= n; i++) {
      if (num % i == 0) {
	return false;
      }
    }
    return true;
  }

  static void FibonacciFast(int n) {
    std::cout << "Starting FibonacciFast(" << n << ")...\n";
    bool verified = false;
    for (int round1 = 0; round1 < 10000; round1++) {
      for (int round2 = 0; round2 < 10000; round2++) {
	if (n <= 2) {
	  return;
	}
	int64 a = 1;
	int64 b = 2;
	for (int i = 2; i < n; i++) {
	  int64 c = a + b;
	  a = b;
	  b = c;
	  if (b < 1) {
	    std::cout << "WARNING  int64 overflow..\n";
	  }
	}
	if (!verified) {
	  std::cout << "Verify the value: " << b << ", "
		    << (double)a / (double)b << "\n";
	  verified = true;
	}
      }
    }
  }

  static void FibonacciRecur(int n) {
    std::cout << "Starting FibonacciRecur(" << n << ")...\n";
    for (int i = 2; i < n; ++i) {
      if (Recur(i) < 1) {
	std::cout << "int overflow...\n";
      }
    }
    std::cout << "Verify the value: " << Recur(n) << ", "
	      << (float)Recur(n-1)/(float)Recur(n) << std::endl;

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

std::string PrintVector(const std::vector<int>& data_vec) {
  std::string ret;
  for (int i = 0; i < data_vec.size(); ++i) {
    char buffer[20];
    sprintf(buffer, "%d, ", data_vec[i]);
    ret += std::string(buffer);
  }
  return ret;
}

void Test_ScheduleTasks(TestResult *result) {
  char buffer[80];
  sprintf(buffer,
	  "For %s, RECUR_N=%d and NUM_TASKS=%d\n"
	  "RUN_IN_PARALLEL=%d, ",
	  GetTestModeString(TEST_MODE).c_str(), RECUR_N, NUM_TASKS,
	  RUN_IN_PARALLEL);
  result->overall += std::string(buffer);

  std::vector<int> data_vec;  // own the memory.
  // Comment the line below will make the job crash due to address
  // change during container's memory reallocation.  See comment on
  // top of this file.
  data_vec.reserve(NUM_TASKS);
  TaskManager task_manager;
  ScheduleTasks(NUM_TASKS, &data_vec, &task_manager);

  result->details += (GetNowString() + " Before: " +
		      PrintVector(data_vec) + "\n");

  CpuTimer timer;
  timer.Start();
  task_manager.Run();
  timer.Stop();
 
  result->details += (GetNowString() + " After: " +
		      PrintVector(data_vec) + "\n");

  sprintf(buffer, "total in ms: %d\n", timer.GetInMs());
  result->overall += std::string(buffer);
  result->cost_in_ms = timer.GetInMs();
}

int main() {
  std::vector<TestResult*> result_vec;
  {
    TEST_MODE = FIBONACCI_RECUR;
    RECUR_N = 40;
    {
      RUN_IN_PARALLEL = false;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
    {
      RUN_IN_PARALLEL = true;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
  }
  {
    TEST_MODE = FIBONACCI_FAST;
    RECUR_N = 90;
    {
      RUN_IN_PARALLEL = false;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
    {
      RUN_IN_PARALLEL = true;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
  }
  {
    TEST_MODE = PRIME_NUM;
    {
      RUN_IN_PARALLEL = false;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
    {
      RUN_IN_PARALLEL = true;
      TestResult* result = new TestResult;
      result_vec.push_back(result);
      Test_ScheduleTasks(result);
      std::cout << result->details << std::endl;
    }
  }

  int64 cost_sequentially = 0;
  for (int i = 0; i < result_vec.size(); ++i) {
    TestResult* result = result_vec[i];

    if (i % 2 == 0) {
      // sequentially
      cost_sequentially = result->cost_in_ms;
    } else {
      char buffer[80];
      sprintf(buffer, "%.4f x\n",
	      (double)cost_sequentially / (double)result->cost_in_ms);
      result->overall += std::string(buffer);
    }
    std::cout << result->details << std::endl;
  }

  for (TestResult* result : result_vec) {
    std::cout << result->overall << std::endl;
    delete result;
  }
}
