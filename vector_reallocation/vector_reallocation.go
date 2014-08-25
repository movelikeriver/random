// Usage:
//   gofmt -w vector_reallocation.go
//   go run vector_reallocation.go

package main

import (
	"fmt"
	"log"
	"runtime"
	"strings"
	"sync"
	"time"
)

// Don't set too crazy num.
// In 4-CPU Mac
// $ go version
// go version go1.2.1 darwin/amd64
//
// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
// RUN_IN_PARALLEL=false, total in ms: 24319
//
// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
// RUN_IN_PARALLEL=true, total in ms: 8068
// 3.0143 x
//
// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=false, total in ms: 106144
//
// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=true, total in ms: 52843
// 2.0087 x
//
// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=false, total in ms: 482560
//
// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
// RUN_IN_PARALLEL=true, total in ms: 177735
// 2.7151 x


const (
	FIBONACCI_RECUR int = 0
	FIBONACCI_FAST  int = 1
	PRIME_NUM       int = 2
)

var TEST_MODE int = FIBONACCI_RECUR

func getTestModeString(test_mode int) string {
	switch test_mode {
	case FIBONACCI_RECUR:
		return "FIBONACCI_RECUR"
	case FIBONACCI_FAST:
		return "FIBONACCI_FAST"
	case PRIME_NUM:
		return "PRIME_NUM"
	default:
		break
	}
	return "INVALID_TEST_MODE"
}

var RUN_IN_PARALLEL bool = true

// for Fibonacci
var RECUR_N int = 40

const NUM_TASKS int = 9

// for prime
const MIN_PRIME_N int64 = 100 * 1000
const MAX_PRIME_N int64 = 300 * 1000

/////////////
// CpuTimer
/////////////
type CpuTimer struct {
	tsStart time.Time
	tsEnd   time.Time
}

func (this *CpuTimer) start() {
	this.tsStart = time.Now()
}

func (this *CpuTimer) stop() {
	this.tsEnd = time.Now()
}

func (this CpuTimer) getInMs() int {
	return int(this.tsEnd.Sub(this.tsStart).Nanoseconds() / 1e6)
}

///////////////
// TestResult
///////////////
type TestResult struct {
	overall  string
	details  string
	costInMs int
}

///////////////
// TaskManager
///////////////
type TaskManager struct {
	taskArr [](*int)
}

func (this *TaskManager) addTask(cost *int) {
	this.taskArr = append(this.taskArr, cost)
}

func (this *TaskManager) run() {
	if RUN_IN_PARALLEL {
		this.runInParallel()
	} else {
		this.runSequentially()
	}
}

func (this *TaskManager) runInParallel() {
	var wg sync.WaitGroup
	for i, n := 0, len(this.taskArr); i < n; i++ {
		wg.Add(1)
		// run in parallel
		go this.reportCost(this.taskArr[i], &wg)
	}
	wg.Wait()
}

func (this *TaskManager) runSequentially() {
	for i, n := 0, len(this.taskArr); i < n; i++ {
		// run sequentially
		this.reportCost(this.taskArr[i], nil)
	}
}

func (this TaskManager) reportCost(latencyMs *int, wg *sync.WaitGroup) {
	costMs := insaneCompute()
	*latencyMs = costMs
	log.Println("cost in ms:", costMs)
	if wg != nil {
		wg.Done()
	}
}

func insaneCompute() int {
	timer := CpuTimer{}
	timer.start()
	switch TEST_MODE {
	case FIBONACCI_RECUR:
		fibonacciRecurNTimes(RECUR_N)
		break
	case FIBONACCI_FAST:
		fibonacciFast(RECUR_N)
		break
	case PRIME_NUM:
		primeNumTestDummy()
		break
	default:
		break
	}
	timer.stop()
	return timer.getInMs()
}

func primeNumTestDummy() {
	log.Println("Starting primeNumTestDummy()...")
	for i := MIN_PRIME_N; i < MAX_PRIME_N; i++ {
		// Whether this number is equal to prime1 * prime2
		isTwoPrimeMultipleDummy(i)
	}
}

func isTwoPrimeMultipleDummy(num int64) bool {
	var n int64 = num / 2
	found := false
	for part1 := int64(2); part1 <= n; part1++ {
		if num%part1 != 0 {
			continue
		}
		var part2 int64 = num / part1
		if part1 > part2 {
			break
		}
		if !isPrimeNumDummy(part1) {
			continue
		}
		if !isPrimeNumDummy(part2) {
			continue
		}
		if part1 > 500 && part2 > 500 {
			log.Println("within ", MAX_PRIME_N, ", ", num, " = ",
				part1, " * ", part2)
		}
		found = true
	}
	return found
}

func isPrimeNumDummy(num int64) bool {
	var n int64 = num / 2
	for i := int64(2); i <= n; i++ {
		if num%i == 0 {
			return false
		}
	}
	return true
}

func fibonacciFast(n int) {
	log.Println("Starting fibonacciFast(", n, ")...")
	verified := false
	for round1 := 0; round1 < 10000; round1++ {
		for round2 := 0; round2 < 10000; round2++ {
			if n <= 2 {
				return
			}
			a, b := 1, 2
			for i := 2; i < n; i++ {
				b, a = a+b, b
				if b < 1 {
					log.Println("WARNING  int64 overflow...")
				}
			}
			if !verified {
				fmt.Printf("Verify the value: %d, %.6f\n",
					b, float64(a)/float64(b))
				verified = true
			}
		}
	}
}

func fibonacciRecurNTimes(n int) {
	log.Println("Starting fibonacciRecurNTimes(", n, ")...")
	for i := 2; i < n; i++ {
		if fibonacciRecur(i) < 1 {
			log.Println("WARNING  int overflow...")
		}
	}
	fmt.Printf("Verify the value: %d, %.6f\n",
		fibonacciRecur(n),
		float32(fibonacciRecur(n-1))/float32(fibonacciRecur(n)))
}

func fibonacciRecur(n int) int {
	if n <= 2 {
		return n
	}
	return fibonacciRecur(n-1) + fibonacciRecur(n-2)
}

func scheduleTasks(n int, tasks *[]int, tm *TaskManager) {
	for i := 0; i < n; i++ {
		*tasks = append(*tasks, i)
	}
	for i := 0; i < n; i++ {
		tm.addTask(&((*tasks)[i]))
	}
}

// This function has a bug.
//   2014/08/18 15:24:10 Before: [0 1 2 3]
//   2014/08/18 15:24:16 cost in ms: 6274
//   2014/08/18 15:24:17 cost in ms: 6452
//   2014/08/18 15:24:17 cost in ms: 6448
//   2014/08/18 15:24:17 cost in ms: 6462
//   2014/08/18 15:24:17 After: [0 1 6448 6462]
//
// Oops.. only last 2 elements got updated.
//func scheduleTasks(n int, tasks *[]int, tm *TaskManager) {
//	for i := 0; i < n; i++ {
//		*tasks = append(*tasks, i)
//		// the address could be changed after reallocation.
//		tm.addTask(&((*tasks)[len(*tasks)-1]))
//	}
//}

func printArr(arr []int) string {
	var parts []string
	for i := 0; i < len(arr); i++ {
		parts = append(parts, fmt.Sprintf("%d, ", arr[i]))
	}
	return strings.Join(parts, "")
}

func testScheduleTasks() TestResult {
	result := TestResult{}

	result.overall = fmt.Sprintf("For %s, RECUR_N=%d and NUM_TASKS=%d\n"+
		"RUN_IN_PARALLEL=%t, ", getTestModeString(TEST_MODE), RECUR_N,
		NUM_TASKS, RUN_IN_PARALLEL)
	tasks := []int(nil)
	tm := TaskManager{}
	scheduleTasks(NUM_TASKS, &tasks, &tm)

	result.details += (time.Now().Format(time.UnixDate) +
		"  Before: " + printArr(tasks) + "\n")

	timer := CpuTimer{}
	timer.start()
	tm.run()
	timer.stop()

	result.details += (time.Now().Format(time.UnixDate) +
		"  After: " + printArr(tasks) + "\n")

	result.overall += fmt.Sprintf("total in ms: %d\n", timer.getInMs())
	result.costInMs = timer.getInMs()

	return result
}

func main() {
	log.Println("Num of CPUs: ", runtime.NumCPU())
	runtime.GOMAXPROCS(runtime.NumCPU())

	results := []TestResult(nil)
	{
		TEST_MODE = FIBONACCI_RECUR
		RECUR_N = 40
		{
			RUN_IN_PARALLEL = false
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)

		}
		{
			RUN_IN_PARALLEL = true
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)
		}
	}
	{
		TEST_MODE = FIBONACCI_FAST
		RECUR_N = 90
		{
			RUN_IN_PARALLEL = false
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)

		}
		{
			RUN_IN_PARALLEL = true
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)
		}
	}
	{
		TEST_MODE = PRIME_NUM
		{
			RUN_IN_PARALLEL = false
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)

		}
		{
			RUN_IN_PARALLEL = true
			result := testScheduleTasks()
			log.Println(result.details)
			results = append(results, result)
		}
	}

	costSequentially := 0
	for i := range results {
		if i%2 == 0 {
			// sequentially
			costSequentially = results[i].costInMs
		} else {
			results[i].overall += fmt.Sprintf("%.4f x\n",
				float64(costSequentially)/float64(results[i].costInMs))
		}
		fmt.Println(results[i].details)
	}

	for i := range results {
		fmt.Println(results[i].overall)
	}
}
