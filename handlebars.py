#!/bin/env python3

import utils
import itertools
from shutil import copyfile, rmtree, copytree
import os
import copy
from os.path import join

from fileinput import FileInput
from pybars import Compiler

from partials import partials, get_content_partial

compiler = Compiler()
output_dir = "docs"
default_template = "page"

def get_content_page(this, option):
    return "channel/{0}".format(option["url"])

helpers={
    'get_content_page': get_content_page
}

def render_template(template, data, partial):
    template = compiler.compile(utils.read_file(template))

    if partial is not None:
        template_partials = partials | partial
    else:
        template_partials = partials

    return template({"page": data}, helpers=helpers, partials=template_partials)


def generate_blog_suggestions(route):
    route["suggestions"] = utils.get_json_data("blogs")


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

    partial = get_content_partial(route, category)
    rendered_template = render_template(output_path, route, partial)
    utils.write_file(output_path, rendered_template)


def generate_website():
    for route in utils.get_json_data("routes"):
        route['routes'] = utils.get_json_data("routes")
        generate_page(route)
        if "sub_page_path" in route:
            generate_sub_pages(route)


def main():
    if os.path.isdir(output_dir):
        rmtree(output_dir)

    copytree('static', output_dir)
    generate_website()
    full_output_path = join(os.getcwd(), output_dir)
    print("Generated website can be found in {0}".format(full_output_path))


if __name__ == "__main__":
    main()