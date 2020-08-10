#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import os

def error_exit(msg):
    """
    Called on program error. Print formatted message and leave
    program.
    """
    script_name = os.path.basename(sys.argv[0])
    print(f"{script_name}: {msg}", file=sys.stderr)
    exit(1)

def extract_file(filename):
    """
    Convert file to an html tree using lxml.
    """
    #Control file existence and type
    if not os.path.exists(filename) or not os.path.isfile(filename):
        error_exit(f"file '{filename}' is invalid or don't exists")

    with open(filename) as html_file:
        html_tree = BeautifulSoup(html_file, "html.parser")
    return html_tree

def save_file(destination, htmltree):
    """
    Write html tree in a destination file
    """
    with open(destination, 'w') as File:
        print("{% load static %}", file=File)
        print(htmltree.prettify(), file=File)
        
def convert_bss_attribute(attribute):
    return f"dj-{attribute}"

def extend_tag(htmltree, django_tag, before=False, after=False):
    """
    Replace html attribute from bss to django template tag.
    Used for tag with opening and closing part : if, for, block, etc.
    """
    bss_attribute = convert_bss_attribute(django_tag)
    close_tag = f"{{% end{django_tag} %}}"
    for element in htmltree.select(f'[{bss_attribute}]'):
        #Retrieve value in bss attribute and format django template tag
        attribute_value = element.attrs.pop(bss_attribute)
        open_tag = f"{{% {django_tag} {attribute_value} %}}"

        #Insert element in tree
        if before:
            element.insert_before(open_tag)
        if after:
            element.insert_after(close_tag)

def replace_ref(htmltree):
    """
    Insert variable reference in specified tags.
    """
    bss_attribute = convert_bss_attribute("ref")
    for element in htmltree.select(f'[{bss_attribute}]'):
        attribute_value = element.attrs.pop(bss_attribute)
        variable = f"{{ {attribute_value} }}"
        element.insert(0, variable)

def replace_static_links(htmltree, tag_name):
    """
    Replace tag who will use django static files.
    
    e.g. img, script etc.
    """
    for element in htmltree.select(tag_name):
        href = element.attrs.get("href")
        src = element.attrs.get("src")

        static_template = '{{% static "{}" %}}'

        if src and not src.startswith("http"):
            element.attrs["src"] = static_template.format(src)

        if href and not href.startswith("http"):
            element.attrs["href"] = static_template.format(href)

def remove_for_data(htmltree):
    """
    Remove extra tag used to simulate for loop content.
    """
    for element in htmltree.select('[dj-for-data]'):
        element.extract()

def bss_convert(filename):
    htmltree = extract_file(filename)

    #Define different type of tag behavior
    enclosed_tag = ["for", "if", "block"]
    open_tag = ["load"]
    tag_link = ["script", "img", "link"]

    remove_for_data(htmltree)
    for tag in enclosed_tag:
        extend_tag(htmltree, tag, before=True, after=True)

    for tag in open_tag:
        extend_tag(htmltree, tag, before=True)

    for tag in tag_link:
        replace_static_links(htmltree, tag)

    replace_ref(htmltree)
    save_file("render_" + filename, htmltree)

if __name__ == "__main__":
    #Check program arguments validity
    if len(sys.argv) != 2:
        error_exit("syntax error")
