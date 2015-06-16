// Find the shortest word in a dictionary containing all the letters
// present in a given word.
// E.g. "ac" --> "car", "tarw" --> "water".
//
// The approach is like a search engine, indexed by each letter to
// post list of words. The intersection of all the results for each
// letter are the final result. The shortest word in the intersection is
// the final result. The trick is for the repeated letters in the word,
// we can use count as the value of the map of letter and word.

package main

import (
        "fmt"
)

func arrToIndex(arr []string) map[rune]map[string]int {
        index := make(map[rune]map[string]int)
        for _, word := range arr {
                for _, ch := range word {
                        if _, ok := index[ch]; !ok {
                                index[ch] = make(map[string]int)
                        }
                        if _, ok := index[ch][word]; !ok {
                                index[ch][word] = 0
                        }
                        index[ch][word] += 1
                }
        }
        return index
}

func find(ch rune, cnt int, index map[rune]map[string]int) map[string]bool {
        ret := make(map[string]bool)
        if res, ok := index[ch]; ok {
                for k, v := range res {
                        if v >= cnt {
                                ret[k] = true
                        }
                }
        }
        return ret
}

func join(m1 map[string]bool, m2 map[string]bool) map[string]bool {
        ret := make(map[string]bool)
        for k, _ := range m1 {
                if _, ok := m2[k]; ok {
                        ret[k] = true
                }
        }
        return ret
}

func lookup(letters string, index map[rune]map[string]int) map[string]bool {
        chCnt := make(map[rune]int)
        for _, ch := range letters {
                if _, ok := chCnt[ch]; !ok {
                        chCnt[ch] = 1
                } else {
                        chCnt[ch] += 1
                }
        }
        first := true
        empty := false
        ret := make(map[string]bool)
        for k, v := range chCnt {
                m := find(k, v, index)
                if len(m) == 0 {
                        empty = true
                        break
                }
                if first {
                        first = false
                        ret = m
                } else {
                        ret = join(ret, m)
                }
        }
        if empty {
                // clear
                ret = make(map[string]bool)
        }
        return ret
}

func printIndex(index map[rune]map[string]int) {
        for ch, m := range index {
                fmt.Print(string(ch), ": ")
                for word, cnt := range m {
                        fmt.Print("(", word, ", ", cnt, "), ")
                }
                fmt.Println()
        }
}

func printMap(m map[string]bool) {
        for word, _ := range m {
                fmt.Print(word, ", ")
        }
        fmt.Println()
}

func main() {
        // dict
        arr := []string{"car", "you", "meet", "apple", "see", "banana", "baba", "se"}
        // input word
        word := "ee"

        index := arrToIndex(arr)
        fmt.Println("index:")
        printIndex(index)

        res := lookup(word, index)

        fmt.Println("\nfinal result for [", word, "]:")
        printMap(res)
}
