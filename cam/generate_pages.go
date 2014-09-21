package main

import (
	"bytes"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"
)

var dataDir = flag.String("data_dir", "", "")

// start with path higher up the tree, say $HOME
func walkDir(dirPath string) {
	err := filepath.Walk(dirPath, walkFn)
	if err != nil {
		log.Printf("Err: %s", err)
	}
	generateIndexPage(*dataDir)
}

func walkFn(srcFile string, fi os.FileInfo, err error) (e error) {
	if !fi.IsDir() {
		// one level dir
		return nil
	}

	if srcFile == *dataDir {
		return nil
	}

	generateSinglePage(srcFile)
	return nil
}

func saveToFile(filename string, content string) (e error) {
	f, err := os.Create(filename)
	if err != nil {
		fmt.Println(err)
	}
	n, err := io.WriteString(f, content)
	if err != nil {
		fmt.Println(n, err)
		return err
	}
	f.Close()
	os.Chmod(filename, 0644)
	if err = os.Chmod(filename, 0644); err != nil {
		log.Println(err)
		return err
	}
	log.Println(filename, "generated!")
	return nil
}

func genLinksInDir(dirPath string) (ret string) {
	const htmlStr = `
  <div>
    <a href="%s">
      <img src="%s" alt="%s"/>
    </a>
  </div>`

	files, _ := ioutil.ReadDir(dirPath)
	var buffer bytes.Buffer
	for _, f := range files {
		segs := strings.Split(dirPath, string(os.PathSeparator))
		imgPath := segs[len(segs)-1] + "/" + f.Name() // for html
		buffer.WriteString(fmt.Sprintf(htmlStr, imgPath, imgPath, f.Name()))

	}
	return buffer.String()
}

func generateSinglePage(workDir string) {
	pagePath := workDir + "_test.html"
	log.Println("Generating", pagePath, "...")
	subHtml := genLinksInDir(workDir)

	const htmlTmp = `
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport"content="target-densitydpi=device-dpi, width=device-width" />

  <style type="text/css">
    .result div { width: 275px; height: 183px; padding-top: 0px; padding-bottom: 1px; display: inline-block; }
    .result div a img { width:275px;height:183px;margin-left:0px;margin-right:0px;margin-top:0px }
  </style>
  <title>View Snapshots</title>
</head>

<body>
  <p>
    <a href="index.html">index</a>
  </p>
<div class="result">
%s
</div>

</body>
</html>`

	saveToFile(pagePath, fmt.Sprintf(htmlTmp, subHtml))
}

func generateIndexPage(workDir string) {

	const liHtml = `<li><a href="%s">%s</a></li>`

	const indexPageHtml = `
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport"content="target-densitydpi=device-dpi, width=device-width" />

  <style type="text/css">
  </style>
  <title>View Snapshots</title>
</head>

<body>
  <ul>
  %s
  </ul>
</body>

</html>`

	files, _ := ioutil.ReadDir(workDir)
	var buffer bytes.Buffer
	for _, f := range files {
		if f.IsDir() {
			continue
		}
		if strings.HasSuffix(f.Name(), "~") {
			continue
		}
		if f.Name() == "index.html" {
			continue
		}

		buffer.WriteString(fmt.Sprintf(liHtml, f.Name(), f.Name()))
	}
	pageContent := fmt.Sprintf(indexPageHtml, buffer.String())
	saveToFile(path.Join(workDir, "index.html"), pageContent)
}

func main() {
	flag.Parse()

	walkDir(*dataDir)
	return
}
