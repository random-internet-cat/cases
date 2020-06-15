import os
import shutil

cases_dir_path = "cases"
case_list_path = "out.csv"

def format_index_single_case(case_name):
    return "* CFJ {0}: [html](cases/{0}), [raw](cases/raw/{0})\n".format(case_name)

def generate_index(case_list):
    output_header = "# Test CFJ archive\n"
    output_footer = ""

    output = ""
    output += output_header

    for case_name in case_list:
        output += format_index_single_case(case_name)

    output += output_footer

    return output

def case_text_of(case_name):
    with open(os.path.join(cases_dir_path, case_name), encoding="utf-8",errors="replace") as case_file:
        return case_file.read()

def get_case_name_list():
    with open(case_list_path) as case_list_file:
        return [case for case in [case.strip() for case in case_list_file.read().split('\n')] if case != ""]

def generate_case_raw_text(case_list, case_index):
    case_name = case_list[case_index]
    case_text = case_text_of(case_name)
    
    case_raw_text_header="---\ntitle: CFJ {0} (raw)\npermalink: /raw/{0}\n---\n\n<!DOCTYPE html>\n<html><body><pre>".format(case_name)
    case_raw_text_footer="</pre></body></html>"

    return case_raw_text_header + case_text + case_raw_text_footer
    

def generate_case_html(case_list, case_index):
    case_name = case_list[case_index]
    
    previous_case_index = min(len(case_list) - 1, case_index + 1)
    previous_case_name = case_list[previous_case_index]

    next_case_index = max(0, case_index - 1)
    next_case_name = case_list[next_case_index]

    case_html_header = "---\ntitle: CFJ {0}\npermalink: /{0}\n---\n".format(case_name) + """
<!DOCTYPE html>
<html><head><title>CFJ {0}</title>
        <style>
            body {
              font-family: monospace;
            }
          table{
              font: 1em/1.2 \"Helvetica Neue\", Helvetica, Arial, Geneva, sans-serif;
              border-collapse: collapse;
              width: 550px;
          }         
         a:link     {text-decoration: none;  color: white;}
         a:visited  {text-decoration: none;  color: white;}
         td:hover {background-color: #666;}
 td {
    border: 1px solid #ddd;
    padding: 8px;
    overflow: hidden;
    font-size: 1.2em;
    text-align: center;
    background-color: #444;
    color: white;
}
.indx{text-align:left; vertical-align:bottom; font-size:100%;}
.prev{text-align:right; vertical-align:bottom; font-size:85%;}
.next{text-align:left; vertical-align:bottom; font-size:85%;}
.text{text-align:right; vertical-align:bottom; font-size:100%;}
td a{
  display: block;
  margin: -10cm;
  padding: 10cm;
}
         </style>
         </head>
         <body>
         <table><tr>""" + """
         <td class=\"indx\"><a href=\"./#{2}\">Index</a></td>
         <td class=\"prev\"><a href=\"./{1}\"><b>&larr;&nbsp;{1}</b></a></td>
         <td><a href=\"./?{0}\"><b>CFJ {0}</b></a></td>
         <td class=\"next\"><a href=\"./{2}\"><b>{2}&nbsp;&rarr;</b></a></td>
         <td class=\"text\"><a href=\"./raw/{0}\">text</a></td>
         </tr></table><pre>\n""".format(case_name, previous_case_name, next_case_name)
    
    case_html_footer = "</pre></body></html>"

    return case_html_header + case_text_of(case_name) + case_html_footer

output_dir_path = "generated"
os.makedirs(output_dir_path, exist_ok=True)

header_path = os.path.join(output_dir_path, "index.md")

case_name_list = get_case_name_list()

open(header_path, "w").write(generate_index(case_name_list))

# Copy raw cases to output path

# output_raw_cases_path = os.path.join(output_dir_path, "cases", "raw")
# os.makedirs(output_raw_cases_path, exist_ok=True)
# shutil.copytree(cases_dir_path, output_raw_cases_path, dirs_exist_ok=True)

output_html_cases_path = os.path.join(output_dir_path, "cases")
os.makedirs(output_html_cases_path, exist_ok=True)

output_raw_cases_path = os.path.join(output_dir_path, "cases", "raw")
os.makedirs(output_raw_cases_path, exist_ok=True)

for case_index in range(0, len(case_name_list)):
    case_name = case_name_list[case_index]
    print("Processing case {}".format(case_name))

    case_html = generate_case_html(case_name_list, case_index)
    case_raw = generate_case_raw_text(case_name_list, case_index)
    case_html_out_path = os.path.join(output_html_cases_path, case_name + ".html")
    case_raw_out_path = os.path.join(output_raw_cases_path, case_name + ".html")

    with open(case_html_out_path, "w") as case_html_out_file:
        case_html_out_file.write(case_html)

    with open(case_raw_out_path, "w") as case_raw_out_file:
        case_raw_out_file.write(case_raw)
