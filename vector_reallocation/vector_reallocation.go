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

var flagRunInParallel = flag.Bool("run_in_parallel", true,
	"running in parallel if true.")

// Don't set too crazy num.
// In 4-CPU Mac
// $ go version
// go version go1.2.1 darwin/amd64
// For RECUR_N=40, num_tasks=9:
//   5416ms * 9 sequentially
//   20746ms in parallel
const RECUR_N int = 40
const NUM_TASKS int = 9

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
	costMs := this.InsaneCompute()
	*latencyMs = costMs
	log.Println("cost in ms:", costMs)
	if wg != nil {
		wg.Done()
	}
}

func (this TaskManager) InsaneCompute() int {
	log.Println("Start insaneCompute()...")
	tsStart := time.Now()
	for i := 2; i < RECUR_N; i++ {
		if this.Recur(i) < 1 {
			log.Println("int overflow...")
		}
	}
	fmt.Printf("Verify the value: %d, %.6f\n",
		this.Recur(RECUR_N),
		float32(this.Recur(RECUR_N-1))/float32(this.Recur(RECUR_N)))
	tsEnd := time.Now()
	return int(tsEnd.Sub(tsStart).Nanoseconds() / 1e6)
}

func (this TaskManager) Recur(n int) int {
	if n <= 2 {
		return n
	}
	return this.Recur(n-1) + this.Recur(n-2)
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
