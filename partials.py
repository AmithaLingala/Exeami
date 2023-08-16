import utils
from pybars import Compiler

from os.path import join

compiler = Compiler()
tags = compiler.compile(utils.read_file(join("templates", "tags.html")))
header = compiler.compile(utils.read_file(join("templates", "header.html")))
footer = compiler.compile(utils.read_file(join("templates", "footer.html")))
nav = compiler.compile(utils.read_file(join("templates", "nav.html")))
blog_item = compiler.compile(
    utils.read_file(join("templates", "blogs-content.html")))
theme_switcher = compiler.compile(
    utils.read_file(join("templates", "theme-switcher.html")))

partials = {
    'tags': tags,
    'header': header,
    'nav': nav,
    'footer': footer,
    'theme-switcher': theme_switcher,
    'blog-item': blog_item
}

special_pages = ["blogs", "projects", "channel"]


def get_partial_for_special_page(page_name, route):
    partial = {}
    partial_name = "templates/{0}-content".format(page_name)
    template = join("templates", "{0}-content.html".format(page_name))
    route["content-item"] = partial_name
    route["content-data"] = utils.get_json_data(page_name)

    partial[route["content-item"]] = compiler.compile(
        utils.read_file(template))

    return partial


def get_content_partial(route, category):
    page_name = utils.get_filename_from_page(route)

    if page_name in special_pages:
        return get_partial_for_special_page(page_name, route)

    route["content"] = utils.get_page_path(page_name, category)
    content_file = join("content", "{0}.html".format(route["content"]))

    partial = {}
    partial[route["content"]] = compiler.compile(utils.read_file(content_file))

    return partial
