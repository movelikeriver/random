// Compare two csv files.
//
// Sample csv file looks like:
//
// backend,avg_latency_ms
// NULL,NULL
// 42,4.547616803899721
// 12,11.509030513148076
// 294,24.52723366523726
// 257,1.0702006368320145
// 281,169.880712938734
// 14,86.78706868531333
// 20,2.1839169421118565
// 30,12.29896337549137
// 29,10.84948654459931
//
// Usage:
//    ./csv-sxs --input_files="fn1.csv,fn2.csv" --threshold=11.0 whitelist_keys="1=servera,12=serverb,23=serverc"

package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

var inputFilesFlag = flag.String("input_files", "", "The input array of files splited by \",\", e.g. \"fn1.csv,fn2.csv,fn3.csv\".")
var whitelistKeysFlag = flag.String("whitelist_keys", "", "The input array of keys splitted by \",\", e.g. \"2=aa,12=bb,3=cc,283=dd\".")
var thresholdFlag = flag.Float64("threshold", 0.0, "The threshold of the float value.")

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

func ReadFileToMap(filename string, item_map *map[int]string) {
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
	for i, line := range lines {
		backend_v, err := strconv.Atoi(line[0])
		if err != nil {
			log.Println(i, err)
			continue
		}
		latency_v, err := strconv.ParseFloat(line[1], 32)
		if err != nil {
			log.Println(i, err)
			continue
		}
		if latency_v > *thresholdFlag {
			(*item_map)[backend_v] = line[1] // save as string
		}
	}
}

func CompareValue(v1_str string, v2_str string) string {
	v1, err := strconv.ParseFloat(v1_str, 32)
	if err != nil {
		log.Println("Parsing ", v1_str, " error, should never happen")
		return " x "
	}

	v2, err := strconv.ParseFloat(v2_str, 32)
	if err != nil {
		log.Println("Parsing ", v2_str, " error, should never happen")
		return " x "
	}

	if v1 == v2 {
		return " = "
	}

	if v1 != 0 && v2 != 0 {
		delta := math.Abs(v2 - v1)
		if (delta/v1) < 0.003 || delta < 0.4 {
			return " = "
		}
	}

	if v1 > v2 {
		return " > "
	} else {
		return " < "
	}
}

func main() {
	flag.Parse()
	log.Println(*inputFilesFlag)

	whitelist_key_map := make(map[int]string)
	result_map := make(map[int]map[int]string)

	if whitelistKeysFlag != nil {
		whitelist_keys := strings.Split(*whitelistKeysFlag, ",")
		for i, whitelist_key := range whitelist_keys {
			segs := strings.Split(whitelist_key, "=")
			key_int, err := strconv.Atoi(segs[0])
			if err != nil {
				log.Println(i, ":", segs[0], "is not int")
				continue
			}
			whitelist_key_map[key_int] = segs[1]
		}
	}

	filename_list := strings.Split(*inputFilesFlag, ",")
	for i, filename := range filename_list {
		log.Println(filename)
		item_map := make(map[int]string)
		ReadFileToMap(filename, &item_map)
		result_map[i] = item_map
	}

	output_map := make(map[int]string)
	for _, item_map := range result_map {
		for key, value := range item_map {
			if second, ok := output_map[key]; ok {
				cmp_str := CompareValue(second, value)
				output_map[key] = (second + cmp_str + value)
			} else {
				output_map[key] = value
			}
		}
	}

	for key, value := range output_map {
		if second, ok := whitelist_key_map[key]; ok {
			fmt.Println(second, ":\t", value)
		} else {
			fmt.Println(key, ":      \t", value)
		}
	}

}
