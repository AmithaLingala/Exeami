#!/bin/env python

import json
from shutil import copyfile, rmtree, copytree
import os
from os.path import join

from fileinput import FileInput

output_dir = "html"


def get_output_path(path):
    return os.path.join(output_dir, path)


def get_filename_from_page(page):
    file_name = page["url"].replace("/", "")
    return "index" if file_name == "" else file_name


def get_json_data(file_name):
    with open(join("data", "{0}.json".format(file_name)), "r") as data_file:
        return json.loads(data_file.read())

def read_file(file_name):
     with open(file_name, "r") as data_file:
        return data_file.read()

def replace_text(file_name, search_text, replace_text):
    with FileInput(file_name, inplace=True) as file:
        for line in file:
            print(line.replace(search_text, replace_text), end="")


def insert_file_contents(template_file, search_text, input_file_name):
    with open(input_file_name, "r") as input_file:
        replace_text(template_file, search_text, input_file.read())


def generate_navbar_data():
    navbar_template = read_file(join("templates", "nav.html"))
    navbar_string = '<a href="{0}" class="navbar-item">{1}</a>\n'
    navbar_data = ""

    for route in get_json_data("routes"):
        if(route["url"] == '/'):
            continue
        navbar_data += navbar_string.format(route["url"],
                                                    route["title"])
    return navbar_template.replace("###navbar_items###", navbar_data)


def generate_header(page):
    header_data = read_file(join("templates", "header.html"))

    for key in page:
        header_data = header_data.replace("###{0}###".format(key), str(page[key]))

    return header_data

def render_template(template, data):
    for key in data.keys():
        replace_text(template, "###{0}###".format(key), str(data[key]))


def generate_page(page, category, template):
    page_template_file = join("templates", "{0}.html".format(template))
    page_name = get_filename_from_page(page)

    if category == "main":
        page_path = "{0}".format(page_name)
    else:
        page_path = join(category, page_name)

    if page_name == "index":
        page_file = get_output_path("index.html")
        header_file = get_output_path("header.html")
    else:
        os.makedirs(get_output_path(page_path))
        page_file = get_output_path(join(page_path ,"index.html"))
        header_file = get_output_path(join(page_path,"{0}-header.html".format(page_name)))

    copyfile(page_template_file, page_file)

    page["header"] = generate_header(page)
    
    if "content" not in page:
        content_file = join("content", "{0}.html".format(page_path))
        page["content"] = read_file(content_file)

    render_template(page_file, page)



def generate_sub_pages(category):
    sub_pages = get_json_data(category["sub_page_path"])
    category_name = get_filename_from_page(category)

    for sub_page in sub_pages:
        sub_page["navbar"] = category["navbar"]
        sub_page["footer"] = category["footer"]
        generate_page(sub_page, category_name, "page")


def generate_website():
    navbar = generate_navbar_data()
    footer = read_file(join("templates", "footer.html"))

    for route in get_json_data("routes"):
        route["navbar"] = navbar
        route["footer"] = footer

        if "sub_page_path" in route:
            route["content"] = generate_content(route)
            generate_page(route, "main","blogs")
            generate_sub_pages(route)
        else:
            generate_page(route, "main","page")


def generate_content(page):
    if(get_filename_from_page(page) == "blogs"):
        return generate_blog_page()

def generate_blog_page():
    blog_item_string_template = read_file(join("templates","blog-item.html"))
    generate_blog_content = ""

    for blog in get_json_data("blogs"):
        blog_item_string = blog_item_string_template
        for key in blog:
            blog_item_string = blog_item_string.replace("###{0}###".format(key), str(blog[key]))
        generate_blog_content += blog_item_string
    return generate_blog_content

def main():
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    copytree('static', output_dir)

    generate_website()
    full_output_path = os.path.join(os.getcwd(), output_dir)
    print("Generated website can be found in {0}".format(full_output_path))


if __name__ == "__main__":
    main()
