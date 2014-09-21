package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"
)

var dataDir = flag.String("data_dir", "", "")
var destDir = flag.String("dest_dir", "", "")

func getRangeByHour(hh string) (rangeName string) {
	h, _ := strconv.Atoi(hh)
	h = h / 6
	switch h {
	case 0:
		return "00_06"
	case 1:
		return "06_12"
	case 2:
		return "12_18"
	case 3:
		return "18_24"
	}
	return "NA_NA"
}

// For Foscam, the file is like: Schedule_20140921-103158.jpg
func getDestFullName(fn string) (destFullName string) {
	pairs := strings.Split(fn, "_")
	tp, ts := pairs[0], pairs[1]
	ymd := ts[0:8]
	hh := ts[9:11]

	dirName := path.Join(*destDir,
		fmt.Sprintf("%s_%s_%s", tp, ymd, getRangeByHour(hh)),
		fn)
	return dirName
}

// CopyFile copies a file from src to dst. If src and dst files exist, and are
// the same, then return success. Otherise, attempt to create a hard link
// between the two files. If that fail, copy the file contents from src to dst.
func copyFile(src, dst string) (err error) {
	sfi, err := os.Stat(src)
	if err != nil {
		log.Println(err)
		return err
	}
	if !sfi.Mode().IsRegular() {
		log.Println("!IsRegular()")
		// cannot copy non-regular files (e.g., directories,
		// symlinks, devices, etc.)
		return fmt.Errorf("CopyFile: non-regular source file %s (%q)", sfi.Name(), sfi.Mode().String())
	}

	dfi, err := os.Stat(dst)
	if err != nil {
		if !os.IsNotExist(err) {
			log.Println(dst, " exists.")
			return nil
		}
	} else {
		if !(dfi.Mode().IsRegular()) {
			log.Println("!IsRegular()")
			return fmt.Errorf("CopyFile: non-regular destination file %s (%q)", dfi.Name(), dfi.Mode().String())
		}
		if os.SameFile(sfi, dfi) {
			log.Println("same file")
			return nil
		}
	}
	if err = os.Link(src, dst); err == nil {
		log.Println("link")
		return nil
	}

	dirPath := path.Dir(dst)
	os.Mkdir(dirPath, 0755)

	if err = copyFileContents(src, dst); err != nil {
		log.Println("copy failed....")
		log.Println(err)
		return err
	}
	return nil
}

// copyFileContents copies the contents of the file named src to the file named
// by dst. The file will be created if it does not already exist. If the
// destination file exists, all it's contents will be replaced by the contents
// of the source file.
func copyFileContents(src, dst string) (err error) {
	in, err := os.Open(src)
	if err != nil {
		return
	}
	defer in.Close()
	out, err := os.OpenFile(dst, os.O_RDWR, 0644)
	if err != nil {
		return
	}

	defer func() {
		cerr := out.Close()
		if err == nil {
			err = cerr
		}
	}()
	if _, err = io.Copy(out, in); err != nil {
		return
	}
	err = out.Sync()
	return err
}

func moveFile(srcFn string, desFn string) (e error) {
	_, err := os.Stat(desFn)
	if err != nil {
		if !os.IsNotExist(err) {
			return nil
		}
	}

	dirPath := path.Dir(desFn)
	os.Mkdir(dirPath, 0755)
	err = os.Rename(srcFn, desFn)
	if err != nil {
		log.Println(err)
		return err
	}

	os.Chmod(desFn, 0644)
	return nil
}

// start with path higher up the tree, say $HOME
func walkDir(dirPath string) {
	err := filepath.Walk(dirPath, walkFn)
	if err != nil {
		log.Printf("Err: %s", err)
	}
}

func walkFn(srcFile string, fi os.FileInfo, err error) (e error) {
	if fi.IsDir() {
		// one level dir
		return nil
	}

	// if the first character is a ".", then skip it as it's a hidden file
	if strings.HasPrefix(fi.Name(), ".") {
		return nil
	}

	destFullName := getDestFullName(fi.Name())
	log.Printf("Filename: %s -> %s", srcFile, destFullName)

	copyFile(srcFile, destFullName)

	log.Println("chmod: ", destFullName)
	if err = os.Chmod(destFullName, 0644); err != nil {
		log.Println(err)
		return err
	}

	return nil
}

func main() {
	flag.Parse()

	walkDir(*dataDir)
	return
}
