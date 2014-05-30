// See demo at:  http://readchinesename.appspot.com

package readchinesename

import (
    "html/template"
    "net/http"
)

func init() {
    http.HandleFunc("/", handler)
}

// rootTmpl is the main (and only) HTML template.
var rootTmpl = template.Must(template.ParseFiles("tmpl/read_chinese_name.html"))

func handler(w http.ResponseWriter, r *http.Request) {
     err := rootTmpl.Execute(w, "")
     if err != nil {
     	http.Error(w, err.Error(), http.StatusInternalServerError)
     }
}