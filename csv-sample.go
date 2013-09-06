package main

import (
	"encoding/csv"
	"log"
	"os"
	"strconv"
)

type Item struct {
	backend int
	latency float64
}

func WriteFile(filename string) {
	file, error := os.OpenFile(filename, os.O_RDWR|os.O_CREATE, 0666)
	if error != nil {
		panic(error)
	}
	defer file.Close()

	log.Println("writing to:", filename)
	writer := csv.NewWriter(file)
	writer.Write([]string{"12", "23.423"})
	writer.Write([]string{"15", "24.423"})
	writer.Write([]string{"17", "25.423"})
	writer.Write([]string{"18", "26.423"})
	writer.Flush()
}

func ReadFile(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		log.Println("Error:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	lines, err := reader.ReadAll()
	if err != nil {
		log.Println(err)
		return
	}

	log.Println("reading from:", filename)
	items := make([]Item, len(lines))
	for i, line := range lines {
		backend_v, err := strconv.ParseInt(line[0], 10, 32)
		if err != nil {
			log.Println(err)
			continue
		}
		latency_v, err := strconv.ParseFloat(line[1], 32)
		if err != nil {
			log.Println(err)
			continue
		}
		items[i] = Item{
			backend: int(backend_v),
			latency: latency_v,
		}
	}

	for i, item := range items {
		log.Println(i, ":", item.backend, ": ", item.latency)
	}
}

func main() {
	filename := "tt.csv"
	log.Println(filename)
	WriteFile(filename)
	ReadFile(filename)
}
