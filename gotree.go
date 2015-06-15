package main

import (
        "fmt"
)

// BST
type Tree struct {
        v int
        l *Tree
        r *Tree
}

func PrintTree(t Tree) {
        fmt.Print(t.v)
        if t.l != nil {
                fmt.Print(" ( ")
                PrintTree(*t.l)
                fmt.Print(", ")
        } else {
                fmt.Print(" ( nil, ")
        }
        if t.r != nil {
                PrintTree(*t.r)
                fmt.Print(" ) ")
        } else {
                fmt.Print("nil ) ")
        }
}

func Add(t *Tree, v int) {
        if t.v == v {
                return
        }

        if v > t.v {
                if t.r == nil {
                        t.r = &Tree{v, nil, nil}
                } else {
                        Add(t.r, v)
                }
                return
        }

        if t.l == nil {
		t.l = &Tree{v, nil, nil}
        } else {
                Add(t.l, v)
        }
}

func main() {
        flag.Parse()

        t := Tree{0, nil, nil}
        Add(&t, 3)
        Add(&t, 8)
        Add(&t, 1)
        Add(&t, 19)
        Add(&t, 9)
        PrintTree(t)
        fmt.Println()
}
