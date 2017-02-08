// simulate the probability of the sum of rolling two dices.

package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	n := 1000
	cnt := 0
	for i := 0; i < n; i++ {
		s := rand.Intn(6) + rand.Intn(6) + 2
		if s == 3 {
			cnt += 1
		}
	}

	fmt.Printf("%.4f\n", float64(cnt)/float64(n))
}
