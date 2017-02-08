package main

import (
	"fmt"
	"math"
	"sort"
)

// Example represents the point and label
type Example struct {
	d1    int
	d2    int
	d3    int
	label int
}

// IndexDist represents the index of the example in the array and the distance of given point
type IndexDist struct {
	index    int
	distance float64
}

// distance calculates the Euclidean distance.
func distance(ex1, ex2 Example) float64 {
	return math.Sqrt(math.Pow(float64(ex1.d1-ex2.d1), 2) + math.Pow(float64(ex1.d2-ex2.d2), 2) + math.Pow(float64(ex1.d3-ex2.d3), 2))
}

// Cmp is used for sorting the array.
type Cmp []IndexDist

func (c Cmp) Len() int {
	return len(c)
}

func (c Cmp) Swap(i, j int) {
	c[i], c[j] = c[j], c[i]
}

func (c Cmp) Less(i, j int) bool {
	return c[i].distance < c[j].distance
}

func knn(x Example, n int) int {
	// known points
	examples := []Example{
		{1, 3, 5, 1},
		{3, 4, 6, -1},
		{-1, 2, 9, 1},
		{-3, 7, 2, 1},
		{-4, 1, 8, 1},
	}

	// calculates all the distances of the elements
	dists := []IndexDist{}
	for i, ex := range examples {
		dists = append(dists, IndexDist{i, distance(ex, x)})
	}
	sort.Sort(Cmp(dists))

	fmt.Printf("examples =\t%v\n", examples)
	fmt.Printf("dists =\t%v\n", dists)

	ret := 0
	for i := 0; i < n; i++ {
		ex := examples[dists[i].index]
		fmt.Printf("i=%d, distance=%f, %v\n", i, dists[i].distance, ex)
		ret += ex.label
	}
	return ret
}

func main() {
	fmt.Printf("label = %d\n", knn(Example{2, 4, -1, 0}, 3))
	fmt.Printf("label = %d\n", knn(Example{-2, 5, 3, 0}, 3))
}
