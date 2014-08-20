// Usage:
//   gofmt -w vector_reallocation.go
//   go run vector_reallocation.go

package main

import (
	"flag"
	"fmt"
	"log"
	"runtime"
	"sync"
	"time"
)

// Don't set too crazy num.
// In 4-CPU Mac
// $ go version
// go version go1.2.1 darwin/amd64
//
// For FIBONACCI_RECUR, RECUR_N=40, num_tasks=9:
//   5416 ms * 9 sequentially, 2.3495 x
//   20746 ms in parallel
//
// For FIBONACCI_FAST, RECUR_N=90, num_tasks=9:
//   10680 ms * 9 sequentially, 4.7191 x
//   20368 ms in parallel
//
// For PRIME_NUM:
//   48082 ms * 9 sequentially, 2.4753 x
//  174820 ms in parallel

var flagRunInParallel = flag.Bool("run_in_parallel", true,
	"running in parallel if true.")

const (
	FIBONACCI_RECUR int = 0
	FIBONACCI_FAST  int = 1
	PRIME_NUM       int = 2
)

const TEST_MODE int = PRIME_NUM

// for Fibonacci
const RECUR_N int = 90
const NUM_TASKS int = 9

// for prime
const MIN_PRIME_N int64 = 100 * 1000
const MAX_PRIME_N int64 = 300 * 1000

type TaskManager struct {
	taskArr [](*int)
}

func (this *TaskManager) addTask(cost *int) {
	this.taskArr = append(this.taskArr, cost)
}

func (this *TaskManager) run() {
	if *flagRunInParallel {
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
	costMs := this.insaneCompute()
	*latencyMs = costMs
	log.Println("cost in ms:", costMs)
	if wg != nil {
		wg.Done()
	}
}

func (this TaskManager) insaneCompute() int {
	tsStart := time.Now()
	switch TEST_MODE {
	case FIBONACCI_RECUR:
		this.fibonacciRecur(RECUR_N)
		break
	case FIBONACCI_FAST:
		this.fibonacciFast(RECUR_N)
		break
	case PRIME_NUM:
		this.primeNumTestDummy()
		break
	default:
		break
	}
	tsEnd := time.Now()
	return int(tsEnd.Sub(tsStart).Nanoseconds() / 1e6)
}

func (this TaskManager) primeNumTestDummy() {
	log.Println("Starting primeNumTestDummy()...")
	for i := MIN_PRIME_N; i < MAX_PRIME_N; i++ {
		// Whether this number is equal to prime1 * prime2
		this.isTwoPrimeMultipleDummy(i)
	}
}

func (this TaskManager) isTwoPrimeMultipleDummy(num int64) bool {
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
		if !this.isPrimeNumDummy(part1) {
			continue
		}
		if !this.isPrimeNumDummy(part2) {
			continue
		}
		if part1 > 500 && part2 > 500 {
			log.Println("within ", MAX_PRIME_N, ", ", num, " = ",
				part1, " * ", part2, "\n")
		}
		found = true
	}
	return found
}

func (this TaskManager) isPrimeNumDummy(num int64) bool {
	var n int64 = num / 2
	for i := int64(2); i <= n; i++ {
		if num%i == 0 {
			return false
		}
	}
	return true
}

func (this TaskManager) fibonacciFast(n int) {
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

func (this TaskManager) fibonacciRecur(n int) {
	log.Println("Starting fibonacciRecur(", n, ")...")
	for i := 2; i < n; i++ {
		if this.recur(i) < 1 {
			log.Println("WARNING  int overflow...")
		}
	}
	fmt.Printf("Verify the value: %d, %.6f\n",
		this.recur(n),
		float32(this.recur(n-1))/float32(this.recur(n)))
}

func (this TaskManager) recur(n int) int {
	if n <= 2 {
		return n
	}
	return this.recur(n-1) + this.recur(n-2)
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

func main() {
	flag.Parse()
	log.Println("Num of CPUs: ", runtime.NumCPU())
	runtime.GOMAXPROCS(runtime.NumCPU())
	tasks := []int(nil)
	tm := TaskManager{}
	scheduleTasks(NUM_TASKS, &tasks, &tm)
	log.Println("Before:", tasks)
	tm.run()
	log.Println("After:", tasks)
}
