#!/bin/env python

import json
from shutil import copyfile, rmtree
import os

from fileinput import FileInput

output_dir = "html"


def get_output_path(path):
    return "{0}/{1}".format(output_dir, path)


def get_filename_from_page(page):
    file_name = page["url"].replace("/", "")
    return "index" if file_name == "" else file_name


def get_json_data(file_name):
    with open("data/{0}.json".format(file_name), "r") as data_file:
        return json.loads(data_file.read())


def replace_text(file_name, search_text, replace_text):
    with FileInput(file_name, inplace=True) as file:
        for line in file:
            print(line.replace(search_text, replace_text), end="")


def insert_file_contents(template_file, search_text, input_file_name):
    with open(input_file_name, "r") as input_file:
        replace_text(template_file, search_text, input_file.read())


def generate_navbar_items():
    navbar_string = '<a href="{0}" class="navbar-item">{1}</a>\n'
    generated_nav_items = ""

    for route in get_json_data("routes"):
        generated_nav_items += navbar_string.format(route["url"],
                                                    route["title"])

    output_file = get_output_path("nav.html")
    copyfile("templates/nav.html", output_file)
    replace_text(output_file, "###navbar_items###", generated_nav_items)


def generate_header(page, page_path):
    header_template = "templates/header.html"

    copyfile(header_template, page_path)
    replace_text(page_path, "###Title###", page["title"])
    replace_text(page_path, "###Keywords###", ",".join(page["keywords"]))
    replace_text(page_path, "###Description###", page["description"])


def generate_page(page, category):
    page_template_file = "templates/page.html"
    page_name = get_filename_from_page(page)

    if category == "main":
        page_path = "{0}".format(page_name)
    else:
        page_path = "{0}/{1}".format(category, page_name)

    if page_name == "index":
        page_file = get_output_path("index.html")
        header_file = get_output_path("header.html")
    else:
        os.makedirs(get_output_path(page_path))
        page_file = get_output_path("{0}/index.html".format(page_path))
        header_file = get_output_path("{0}/{1}-header.html".format(
            page_path, page_name))

    copyfile(page_template_file, page_file)

    replace_text(page_file, "###Title###", page["title"])

    generate_header(page, header_file)
    insert_file_contents(page_file, "###Header###", header_file)
    os.remove(header_file)

    insert_file_contents(page_file, "###Navbar###",
                         get_output_path("nav.html"))
    insert_file_contents(page_file, "###Footer###",
                         get_output_path("footer.html"))

    content_file = "content/{0}.html".format(page_path)
    insert_file_contents(page_file, "###Page###", content_file)


def generate_sub_pages(category):
    sub_pages = get_json_data(category["sub_page_path"])
    category_name = get_filename_from_page(category)

    for sub_page in sub_pages:
        generate_page(sub_page, category_name)


def generate_website():
    generate_navbar_items()
    generate_blog_page()
    copyfile("templates/footer.html", get_output_path("footer.html"))

    for route in get_json_data("routes"):
        generate_page(route, "main")
        if "sub_page_path" in route:
            generate_sub_pages(route)

    os.remove(get_output_path("nav.html"))
    os.remove(get_output_path("footer.html"))

def generate_blog_page():
    blog_item_string = '<div><a href="/blogs/{0}" class="blog-item">{1}</a></div>\n'
    generated_blog_items = ""

    for blog in get_json_data("blogs"):
        generated_blog_items += blog_item_string.format(blog["url"],
                                                    blog["title"])

    output_file = "content/blogs.html"
    copyfile("templates/blogs.html", output_file)
    replace_text(output_file, "###BlogItems###", generated_blog_items)

def main():
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    os.mkdir(output_dir)

    generate_website()
    full_output_path = os.path.join(os.getcwd(), output_dir)
    print("Generated website can be found in {0}".format(full_output_path))


if __name__ == "__main__":
    main()
