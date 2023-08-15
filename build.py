#!/bin/env python

import json
import itertools
from shutil import copyfile, rmtree, copytree
import os
from os.path import join

from fileinput import FileInput

output_dir = "html"
default_template = "page"


def get_output_path(path):
    return os.path.join(output_dir, path)


def get_filename_from_page(page):
    file_name = page["url"].replace("/", "")
    return "index" if file_name == "" else file_name

def get_page_path(page_name, category="main"):
    return  "{0}".format(page_name) if category == "main" else join(category, page_name)

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

def get_list_items(list_data, list_name):
    generated_content = "<div class='{0}'>".format(list_name)
    list_item_name = list_name[:-1]
    for list_item in list_data:
        item_string = "<span class='{0}'>{1}</span>".format(list_item_name, list_item)
        generated_content += item_string
    generated_content += "</div>"
    return generated_content

def render_template(template, data):
    for key in data.keys():
        value = get_list_items(data[key], key) if type(data[key]) is list  else data[key]       
        replace_text(template, "###{0}###".format(key), str(value))


def generate_page(page, template, category="main"):
    page_template_file = join("templates", "{0}.html".format(template))
    page_name = get_filename_from_page(page)

    page_path = get_page_path(page_name, category)

    if page_name == "index":
        page_file = get_output_path("index.html")
        header_file = get_output_path("header.html")
    else:
        os.makedirs(get_output_path(page_path))
        page_file = get_output_path(join(page_path ,"index.html"))
        header_file = get_output_path(join(page_path,"{0}-header.html".format(page_name)))

    copyfile(page_template_file, page_file)

    page["header"] = generate_header(page)
    page["content"] = generate_content(page, category)

    render_template(page_file, page)

def generate_sub_pages(category):
    sub_pages = get_json_data(category["sub_page_path"])
    category_name = get_filename_from_page(category)

    for sub_page in sub_pages:
        sub_page["navbar"] = category["navbar"]
        sub_page["footer"] = category["footer"]
        sub_page["theme-switcher"] = category["theme-switcher"]
        template = category["sub_page_template"] if "sub_page_template" in category else default_template
        generate_page(sub_page, template, category_name)

def generate_content(page, category):
    page_name = get_filename_from_page(page)
    if(category == "blogs" or page_name == "index"):
        generate_blog_suggestions(page)
    if(page_name == "blogs" or page_name == "projects" or page_name == "comics"):
        return generate_content_page_from_template(page_name)
    
    page_path = get_page_path(get_filename_from_page(page), category)
    content_file = join("content", "{0}.html".format(page_path))
    return read_file(content_file)

def generate_blog_suggestions(page):
    page_name = get_filename_from_page(page)
    item_string_template = read_file(join("templates","blog-item.html"))
    generated_content = ""
    for item in itertools.islice(get_json_data("blogs"), 3):
        if(item["url"] != page_name):
            item_string = item_string_template
            for key in item:
                value = get_list_items(item[key], key) if type(item[key]) is list  else item[key]       
                item_string = item_string.replace("###{0}###".format(key), str(value))
            generated_content += item_string
    page["suggestions"] = generated_content

def generate_content_page_from_template(category):
    item_string_template = read_file(join("templates","{0}-item.html".format(category[:-1])))
    generated_content = ""

    for item in get_json_data(category):
        item_string = item_string_template
        for key in item:
            value = get_list_items(item[key], key) if type(item[key]) is list  else item[key]       
            item_string = item_string.replace("###{0}###".format(key), str(value))
        generated_content += item_string
    return generated_content

def generate_website():
    navbar = generate_navbar_data()
    footer = read_file(join("templates", "footer.html"))
    theme_switcher = read_file(join("templates", "theme-switcher.html"))

    for route in get_json_data("routes"):
        route["navbar"] = navbar
        route["footer"] = footer
        route["theme-switcher"] = theme_switcher

        template = route["template"] if "template" in route else default_template
        generate_page(route, template)

        if "sub_page_path" in route:
            generate_sub_pages(route)
        
def main():
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    copytree('static', output_dir)

    generate_website()
    full_output_path = os.path.join(os.getcwd(), output_dir)
    print("Generated website can be found in {0}".format(full_output_path))


if __name__ == "__main__":
    main()
