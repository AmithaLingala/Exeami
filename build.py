#!/bin/env python

import json
from shutil import copyfile, rmtree
import os

from fileinput import FileInput

def get_filename_from_route(route):
    file_name = route["url"].replace("/", "")
    return "index" if file_name == "" else file_name
    
def get_route_data():
    with open("data/routes.json", "r") as routes_file:
        return json.loads(routes_file.read())

def replace_text(file_name, search_text, replace_text):
    with FileInput(file_name, inplace=True) as file:
        for line in file:
            print(line.replace(search_text, replace_text), end="")

def insert_file_contents(template_file, search_text, input_file_name):
    with open(input_file_name, "r") as input_file:
        replace_text(template_file, search_text, input_file.read())

def generate_navbar_items():
    navbar_string='<a href="{0}" class="navbar-item">{1}</a>\n';
    generated_nav_items = ""
    
    for route in get_route_data():
        generated_nav_items += navbar_string.format(route["url"], route["title"])

    copyfile("templates/nav.html","build/nav.html")
    replace_text("build/nav.html", "###navbar_items###", generated_nav_items)

    print("generated navbar file")

def generate_header():
    header_template = "templates/header.html"

    for route in get_route_data():
        generated_header = "build/{0}-header.html".format(get_filename_from_route(route))

        copyfile(header_template, generated_header)
        replace_text(generated_header, "###Title###", route["title"])
        replace_text(generated_header, "###Keywords###", ",".join(route["keywords"]))
        replace_text(generated_header, "###Description###", route["description"])
    print("generated main header files")

def generate_main_pages():
    page_template_file = "templates/page.html"
    copyfile("templates/footer.html", "build/footer.html")

    for route in get_route_data():
        route_name = get_filename_from_route(route)
        page_file="build/{0}.html".format(route_name)
        copyfile(page_template_file, page_file)

        replace_text(page_file, "###Title###", route["title"])
        
        header_file="build/{0}-header.html".format(route_name)
        insert_file_contents(page_file, "###Header###", header_file)
        os.remove(header_file)

        insert_file_contents(page_file, "###Navbar###", "build/nav.html")
        insert_file_contents(page_file, "###Footer###", "build/footer.html")

        content_file = "content/{}.html".format(route_name)
        insert_file_contents(page_file, "###Page###", content_file)

def main():
    if os.path.isdir("build"):
        rmtree("build")
    os.mkdir("build")
    generate_navbar_items()
    generate_header()
    generate_main_pages()

if __name__ == "__main__":
    main()
        

