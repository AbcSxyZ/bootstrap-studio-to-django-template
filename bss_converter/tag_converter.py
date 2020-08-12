#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pathlib import PurePath
import sys
import re
import os

def error_exit(msg):
    """
    Called on program error. Print formatted message and leave
    program.
    """
    script_name = os.path.basename(sys.argv[0])
    print(f"{script_name}: {msg}", file=sys.stderr)
    exit(1)

class TagConverter:
    #Define different type of tag behavior
    ENCLOSED_TAG = ["for", "if", "block"]
    OPEN_TAG = ["load"]
    TAG_LINK = ["script", "img", "link"]

    def __init__(self, htmlfile):
        self.htmlfile = htmlfile
        self.tree = self._extract_tree()

        self._remove_for_data()

        for tag in self.ENCLOSED_TAG:
            self._extend_tag(tag, before=True, after=True)

        for tag in self.OPEN_TAG:
            self._extend_tag(tag, before=True)

        for tag in self.TAG_LINK:
            self._replace_static_links(tag)

        self._replace_ref()
        self._save_tree()

    def _extract_tree(self):
        """
        Convert file to an html tree using BeautifulSoup.
        """
        #Control file existence and type
        if not os.path.exists(self.htmlfile) or \
                not os.path.isfile(self.htmlfile):
            err_msg = "file '{}' is invalid or don't exists"
            error_exit(err_msg.format(self.htmlfile))

        with open(self.htmlfile) as htmlstream:
            return BeautifulSoup(htmlstream, "html.parser")

    def _save_tree(self):
        """
        Write html tree in a destination file
        """
        with open(self.htmlfile, 'w') as htmlstream:
            print("{% load static %}", file=htmlstream)
            content = self._replace_background_img(self.tree.prettify())
            print(content, file=htmlstream)
            
    @staticmethod
    def _convert_bss_attribute(attribute):
        return f"dj-{attribute}"

    def _remove_for_data(self):
        """
        Remove extra tag used to simulate for loop content.
        """
        bss_attribute = self._convert_bss_attribute("for-data")
        for element in self.tree.select(f'[{bss_attribute}]'):
            element.extract()

    def _extend_tag(self, django_tag, before=False, after=False):
        """
        Replace html attribute from bss to django template tag.
        Used for tag with opening and closing part : if, for, block, etc.
        """
        bss_attribute = self._convert_bss_attribute(django_tag)
        close_tag = f"{{% end{django_tag} %}}"
        for element in self.tree.select(f'[{bss_attribute}]'):
            #Create content of django template tag
            #with value in html tags attributes
            attribute_value = element.attrs.pop(bss_attribute)
            open_tag = f"{{% {django_tag} {attribute_value} %}}"

            #Insert element in tree
            if before:
                element.insert_before(open_tag)
            if after:
                element.insert_after(close_tag)

    def _convert_bss_link(self, file_link):
        """
        Change link pointed by static tag, file architecture
        of export is different from django.

        In bss : file_type/app_name (ex: js/home)
        In django : app_name/file_type (ex: home/js)
        """
        if file_link.startswith("http"):
            return file_link

        #Remove file root
        if file_link.startswith("/"):
            file_link = file_link[1:]

        path = PurePath(file_link)

        app_name = path.parts[2]
        file_type = path.parts[1]

        #Create link by switching app_name and file_type
        new_path = PurePath(app_name) / file_type / "/".join(path.parts[3:])
        return str(new_path)

    def _replace_static_links(self, tag_name):
        """
        Replace tag who will use django static files.
        
        e.g. img, script etc.
        """
        for element in self.tree.select(tag_name):
            href = element.attrs.get("href")
            src = element.attrs.get("src")

            static_template = '{{% static "{}" %}}'

            if src and not src.startswith("http"):
                src = self._convert_bss_link(src)
                element.attrs["src"] = static_template.format(src)

            if href and not href.startswith("http"):
                href = self._convert_bss_link(href)
                element.attrs["href"] = static_template.format(href)

    def _replace_ref(self):
        """
        Insert variable reference in specified tags.
        """
        bss_attribute = self._convert_bss_attribute("ref")
        for element in self.tree.select(f'[{bss_attribute}]'):
            attribute_value = element.attrs.pop(bss_attribute)
            variable = f"{{ {attribute_value} }}"
            element.insert(0, variable)

    def _replace_background_img(self, raw_file):
        """
        Replace background-image css attribute inside
        an html file. Change it to serve file according
        to django architecture.
        """
        def url_convert(match):
            """
            Use current filename and convert it to
            a static link if needed.
            """
            url = match.group(1)
            if not url.startswith("http"):
                url = self._convert_bss_link(url)
                url = f'{{% static "{url}" %}}'
            return f"url({url})"

        return re.sub("url\((.*?)\)", url_convert, raw_file)
