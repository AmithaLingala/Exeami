#!/bin/env python3

import utils
import itertools
from shutil import copyfile, rmtree, copytree
import os
import copy
from os.path import join
from datetime import date

from fileinput import FileInput
from pybars import Compiler

from partials import partials, get_content_partial

compiler = Compiler()
output_dir = "docs"
default_template = "page"

def get_content_page(this, option):
    return "posts/{0}".format(option["url"])

def is_defined(this, option, attribute):
    return option[attribute] != ""
helpers={
    'is_defined': is_defined,
    'get_content_page': get_content_page
}

def render_template(template, data, partial=None):
    template = compiler.compile(utils.read_file(template))

    if partial is not None:
        template_partials = partials | partial
    else:
        template_partials = partials

    return template({"page": data}, helpers=helpers, partials=template_partials)


def generate_blog_suggestions(route):
    page_file_name = utils.get_filename_from_page(route)
   
    blog_suggestions = []
    for item in itertools.islice(utils.get_json_data("blogs"), 3):
        if(item["url"] != page_file_name):
            blog_suggestions.append(item)
    route["suggestions"] = blog_suggestions

def generate_posts_suggestions(route):
    page_file_name = utils.get_filename_from_page(route)
   
    post_suggestions = []
    for item in itertools.islice(utils.get_json_data("posts"), 3):
        post_suggestions.append(item)
    route["posts"] = post_suggestions

def generate_sub_pages(route):
    sub_pages = utils.get_json_data(route["sub_page_path"])
    category_name = utils.get_filename_from_page(route)

    for sub_page in sub_pages:
        sub_page['routes'] = utils.get_json_data("routes")
        generate_page(sub_page, category_name)


def create_output_path(route, category, page_file_name):
    page_template_file = join("templates", "{0}.html".format(default_template))

    page_file_path = utils.get_page_path(page_file_name, category)

    if page_file_name == "index":
        output_path = utils.get_output_path("index.html")
    else:
        os.makedirs(utils.get_output_path(page_file_path), exist_ok=True)
        output_path = utils.get_output_path(join(page_file_path, "index.html"))

    copyfile(page_template_file, output_path)
    return output_path


def generate_page(route, category="main"):
    page_file_name = utils.get_filename_from_page(route)
    output_path = create_output_path(route, category, page_file_name)

    if (category == "blogs" or page_file_name == "index"):
        generate_blog_suggestions(route)
    if (page_file_name == "index"):
        generate_posts_suggestions(route)

    partial = get_content_partial(route, category)
    rendered_template = render_template(output_path, route, partial)
    utils.write_file(output_path, rendered_template)


def generate_website():
    for route in utils.get_json_data("routes"):
        route['routes'] = utils.get_json_data("routes")
        generate_page(route)
        if "sub_page_path" in route:
            generate_sub_pages(route)

def generate_sitemap():
    data = []
    for route in utils.get_json_data("routes"):
        if(route["url"] == "/"):
            data.append({"url":"", "last_modified":str(date.today()), "priority":"1.00"})
        else:
            data.append({"url":route["url"], "last_modified":str(date.today()), "priority":"0.80"})
    for blog in utils.get_json_data("blogs"):
            data.append({"url":"/blogs/"+blog["url"], "last_modified":blog["last_modified"], "priority":"0.60"})
    for post in utils.get_json_data("posts"):
            data.append({"url": "/posts/"+post["url"], "last_modified":post["last_modified"], "priority":"0.60"})
    for project in utils.get_json_data("projects"):
            data.append({"url": "/projects/"+project["url"], "last_modified":project["last_modified"], "priority":"0.60"})

    template = join("templates", "sitemap.xml")
    rendered_template = render_template(template, data)
    output_path = utils.get_output_path("sitemap.xml")
    
    utils.write_file(output_path, rendered_template)

def generate_atom_feed(cat):
    dates = []
    template = join("templates", "atom.xml")
    output_path = utils.get_output_path("{0}/atom.xml".format(cat))
    cat_items = utils.get_json_data(cat)  
    for cat_item in cat_items:
        dates.append(cat_item["last_modified"])
        page_name = utils.get_filename_from_page(cat_item)
        content_file_name = utils.get_page_path(page_name, cat)
        content_file = join("content", "{0}.html".format(content_file_name))
        cat_item["content"] = compiler.compile(utils.read_file(content_file))
        cat_item["content"] = utils.escape(cat_item["content"]({"page" : cat_item}))
    dates.sort(reverse=True)
    partial = compiler.compile(utils.read_file(template))
    rendered_template = partial({"pages": cat_items, "date" : dates[0], "cat": cat},helpers=helpers)

    utils.write_file(output_path, rendered_template)

def main():
    if os.path.isdir(output_dir):
        rmtree(output_dir)

    copytree('static', output_dir)
    generate_website()
    generate_sitemap()
    generate_atom_feed("blogs")
    generate_atom_feed("posts")
    full_output_path = join(os.getcwd(), output_dir)
    print("Generated website can be found in {0}".format(full_output_path))


if __name__ == "__main__":
    main()
