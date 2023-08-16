#!/bin/env python3
import os
from os.path import join
import json

output_dir = "docs"
def get_filename_from_page(page):
    file_name = page["url"].replace("/", "")
    return "index" if file_name == "" else file_name


def get_page_path(page_name, category="main"):
    return "{0}".format(page_name) if category == "main" else join(
        category, page_name)


def get_output_path(path):
    return os.path.join(output_dir, path)


def get_json_data(file_name):
    with open(join("data", "{0}.json".format(file_name)), "r") as data_file:
        return json.loads(data_file.read())


def read_file(file_name):
    with open(file_name, "r") as data_file:
        return data_file.read()


def write_file(file_name, content):
    with open(file_name, "w") as data_file:
        data_file.writelines(content)

