// Usage:
//   gofmt -w vector_reallocation.go
//   go run vector_reallocation.go
//
//   2014/08/18 15:24:10 Before: [0 1 2 3]
//   2014/08/18 15:24:16 cost in ms: 6274
//   2014/08/18 15:24:17 cost in ms: 6452
//   2014/08/18 15:24:17 cost in ms: 6448
//   2014/08/18 15:24:17 cost in ms: 6462
//   2014/08/18 15:24:17 After: [0 1 6448 6462]
//
// Oops.. only last 2 elements got updated.

package main

import (
	"log"
	"sync"
	"time"
)

const RECUR_N int = 27 // don't set too crazy num

type TaskManager struct {
	taskArr [](*int)
}

func (this *TaskManager) addTask(cost *int) {
	this.taskArr = append(this.taskArr, cost)
}

func (this *TaskManager) run() {
	var wg sync.WaitGroup
	for i, n := 0, len(this.taskArr); i < n; i++ {
		wg.Add(1)
		// run in parallel
		go this.reportCost(this.taskArr[i], &wg)
	}
	wg.Wait()
}

func (this TaskManager) reportCost(latencyMs *int, wg *sync.WaitGroup) {
	costMs := this.InsaneCompute()
	*latencyMs = costMs
	log.Println("cost in ms:", costMs)
	wg.Done()
}

func (this TaskManager) InsaneCompute() int {
	tsStart := time.Now()
	for i := 2; i < RECUR_N; i++ {
		this.Recur(i)
	}
	tsEnd := time.Now()
	return int(tsEnd.Sub(tsStart).Nanoseconds() / 1e6)
}

func (this TaskManager) Recur(n int) int {
	if n <= 2 {
		return n
	}
	sum := 0
	for i := 0; i < n; i++ {
		sum += this.Recur(i)
	}
	return sum
}

func scheduleTasks(n int, tasks *[]int, tm *TaskManager) {
	for i := 0; i < n; i++ {
		*tasks = append(*tasks, i)
		// the address could be changed after reallocation.
		tm.addTask(&((*tasks)[len(*tasks)-1]))
	}
}

func main() {
	tasks := []int(nil)
	n := 9
	tm := TaskManager{}
	scheduleTasks(n, &tasks, &tm)
	log.Println("Before:", tasks)
	tm.run()
	log.Println("After:", tasks)
}
