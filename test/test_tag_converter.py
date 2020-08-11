import unittest
import os
from bss_converter import TagConverter

class TemporaryFile:
    """
    Context manager to create a copy of an html file,
    TagConverter will rewrite this file.
    """
    COPY_EXTENSION = ".tmp"
    def __init__(self, filename):
        self.filename = filename
        self.copy = self.filename + self.COPY_EXTENSION

    def __enter__(self):
        with open(self.filename, "r") as base_stream, \
                open(self.copy, "w") as copy_stream:
            print(base_stream.read(), file=copy_stream)
        return self.copy

    def __exit__(self, *args, **kwargs):
        os.unlink(self.copy)

class TagConverterTest(unittest.TestCase):
    """
    Test suits for bss_converter.TagConverter class.

    Verify if bss attributes for django are well converted
    to their respectiv tags.
    """
    # Get relative and absolute path of the template folder
    TEMPLATE_FOLDER = "html_templates"
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), \
            TEMPLATE_FOLDER)

    #Used extension to diffentiate html from bss and
    #html using django template.
    BSS_EXTENSION = ".html"
    DJANGO_EXTENSION = ".render.html"

    def compare_file(self, folder, filename):
        """
        Select a bss template, create a copy of the template,
        and render the copy with TagConverter.

        Compare this temporary file with a reference file
        created manually.
        """
        #Get absolute path of filename, without any extension
        filename = os.path.join(folder, filename)
        filename = os.path.join(self.TEMPLATE_DIR, filename)

        bss_file = filename + self.BSS_EXTENSION
        django_file = filename + self.DJANGO_EXTENSION 
        with TemporaryFile(bss_file) as copy_file:
            TagConverter(copy_file)
            self.compare_file_content(copy_file, django_file)

    @staticmethod
    def readfile(filename):
        """
        Return content of given filename.
        
        Clean action:
        - Trim/strip each line
        """
        with open(filename) as file_stream:
            file_content = file_stream.readlines()

        for index, line in enumerate(file_content):
            file_content[index] = line.strip()

        return "\n".join(file_content).strip()

    def compare_file_content(self, reference_file, result_file):
        """
        Perform assertion to check if rendered content is equal
        to expected content.
        """
        reference_content = self.readfile(reference_file)
        result_content = self.readfile(result_file)

        self.assertEqual(reference_content, result_content)

    def test_for_loop(self):
        self.compare_file("for_loop", "basic")
        self.compare_file("for_loop", "multiple")
        self.compare_file("for_loop", "nested")
        self.compare_file("for_loop", "manage_attribute")

    def test_if_clause(self):
        self.compare_file("if", "basic")
        self.compare_file("if", "multiple")
        self.compare_file("if", "nested")
        self.compare_file("if", "manage_attribute")

    def test_block_clause(self):
        self.compare_file("block", "basic")
        self.compare_file("block", "multiple")
        self.compare_file("block", "nested")
        self.compare_file("block", "manage_attribute")

    def test_load_tag(self):
        self.compare_file("load", "basic")
        self.compare_file("load", "multiple")
        self.compare_file("load", "nested")
        self.compare_file("load", "manage_attribute")

    def test_static_links(self):
        self.compare_file("static_links", "src")
        self.compare_file("static_links", "href")
