package main

import (
	"log"
	"math/rand"
	"runtime"
	"sync"
	"time"
)

var offset int = 100

type Result struct {
	taskId    int
	taskValue int
}

func produce(num int) <-chan int {
	out := make(chan int)
	go func() {
		for i := 0; i < num; i++ {
			log.Println("produce:", i)
			time.Sleep(1 * time.Millisecond)
			out <- i
		}
		close(out)
	}()
	return out
}

func consumeOne(done <-chan struct{}, in <-chan int, out chan<- Result) {
	for i := range in {
		select {
		case <-done:
			return
		default:
			val := Result{i, i + offset}
			log.Println("consume:", i, "==>", val.taskValue)
			time.Sleep(1 * time.Millisecond)
			out <- val
		}
	}
}

func consume(done <-chan struct{}, in <-chan int) <-chan Result {
	out := make(chan Result)
	var wg sync.WaitGroup

	const num int = 20
	wg.Add(num)
	for i := 0; i < num; i++ {
		go func() {
			consumeOne(done, in, out)
			wg.Done()
		}()
	}
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func updateOffset(id int, num int) {
	for i := 0; i < num; i++ {
		offset = rand.Intn(5) * 100
		log.Println(id, "updateOffset:", offset)
		time.Sleep(100 * time.Millisecond)
	}
}

func test() map[int]Result {
	done := make(chan struct{})
	defer close(done)

	c := produce(1000)
	out := consume(done, c)

	// crazily update global var, but there's no mutex lock issue...
	for i := 0; i < 1000; i++ {
		go updateOffset(i, 100)
	}

	m := make(map[int]Result)
	for r := range out {
		m[r.taskId] = r
	}
	return m
}

func main() {
	log.Println("Num of CPUs: ", runtime.NumCPU())
	runtime.GOMAXPROCS(runtime.NumCPU())

	rand.Seed(time.Now().UTC().UnixNano())
	m := test()

	// output result
	for i := 0; i < len(m); i++ {
		r := m[i]
		if r.taskId%100 == 0 {
			log.Println(r.taskId, ":", r.taskValue)
		}
	}
}
