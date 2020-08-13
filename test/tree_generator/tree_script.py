#!/usr/bin/env python3

from pathlib import Path
from bss_converter.file_manager import FileManager
from .file_utils import TaggedFile, Directory, Workdir
import shutil
import difflib
import os
import re


class ScriptFormatError(Exception):
    pass

class TreeScript:
    """
    Parse template of tree, generate file
    and folders of the template, to compare moved files moved by
    FileManager class.
    """
    DJANGO_DIR = os.path.realpath("tmp_django")
    BSS_DIR = "tmp_bss"
    def __init__(self, script_file):
        # Fix folder name at the top of template
        # represent Boostrap Studio export folder or
        # a django project folder.
        script, reference = self.from_script(script_file)
        self.script = Directory(self.BSS_DIR, script)
        self.reference = Directory('django', reference)

    def launch(self):
        #Create fake bss and django project
        self.script.generate()
        self.emulate_django_project()

        os.environ["DJANGO_PROJECT"] = self.DJANGO_DIR

        with Workdir(self.BSS_DIR):
            FileManager()
            result_folders = self.from_directory(self.DJANGO_DIR)
            result_tree = Directory("django_result", result_folders)

        return self.reference, result_tree

    def clean(self):
        shutil.rmtree(self.BSS_DIR, ignore_errors=True)
        shutil.rmtree(self.DJANGO_DIR, ignore_errors=True)

    @staticmethod
    def file_indent(filename):
        """
        Find space size of left indentation.
        """
        return len(filename) - len(filename.lstrip())

    def tag_folder_lvl(self, list_file):
        """
        Tag to each line a folder lvl, to understand subfolders
        are organized.

        Return list of line with tag number:
        ex:
        [ 
            (0, "assets/"),
            (1, "img/"),
            (2, "logo.png"),
            (1, "js/"),
            ...
        ]

        Is equivalent to:

        assets/
            |- img/
                |- logo.png
            |- js/
        """
        tagged_lines = []
        real_folder_lvl = 0

        #Match a specific spacing with a folder level.
        #Expect having file from a same level to have
        #exact same number of spaces/tabulations
        available_levels = {
                0:real_folder_lvl,
                }

        # Go through each line, find left space in the line,
        # and use this spaces to tag a folder level
        # using `available_levels`
        for filename in list_file:
            file_indent = self.file_indent(filename)
            if file_indent not in available_levels:
                real_folder_lvl += 1
                available_levels[file_indent] = real_folder_lvl

            current_folder_lvl = available_levels[file_indent]

            file_info = TaggedFile(filename, current_folder_lvl)
            tagged_lines.append(file_info)
        
        return tagged_lines

    def from_script(self, script_file):
        """
        Read strip and clean unexpected content.

        Clean apply:
        - split test and result tree
        - right strip every line
        """
        with open(script_file) as script_stream:
            self.apps = self.find_apps(script_stream.readline())
            script_content = script_stream.read()

        # Split test tree from a reference tree
        # Delimited by EQUAL, delimited with some equal sign.
        # 
        # Example (see tests):
        # =================== EQUAL ====================
        test_script, result_script = re.split("=+\s*EQUAL\s*=+",
                script_content, 
                flags=re.IGNORECASE)

        def clean_script(self, script):
            line_split_script = script.strip().split("\n")
            rstripped_lines = map(str.rstrip, line_split_script)
            return self.tag_folder_lvl(rstripped_lines)

        test_script = clean_script(self, test_script)
        result_script = clean_script(self, result_script)

        return test_script, result_script

    def find_apps(self, app_config):
        """
        Retrieve list of django application, in the fist
        line of a script.
        """
        if not app_config.startswith("apps="):
            raise ScriptFormatError("Please specify script applications,"
            " using 'apps=' at the first line.")
        apps_string = app_config.split("=")[1].strip()
        apps = apps_string.split(",")
        return list(filter("".__ne__, apps))

    def emulate_django_project(self):
        """
        Create folder structure of a django project, to
        emulate file migration.

        Create single folder for each specified apps.

        App configuration is given in the first line of a test
        script, with a format like:

        apps=django-app[settings],app1,app2[,...]

        - [settings] is used to generates a settings.py file in app.
        """
        with Workdir(self.DJANGO_DIR):
            for application in self.apps:

                #Check which app represent the settings module
                is_setting = False
                if "[settings]" in application:
                    application = application.replace(
                            "[settings]", ""
                            )
                    is_setting = True
                
                #Create application folder in any case
                Path(application).mkdir()

                # Add settings.py in expected application
                if is_setting:
                    settings_file = os.path.join(
                            application, "settings.py")
                    Path(settings_file).touch()

    def from_directory(self, directory_name, level=0):
        """
        Create a template from an existing directory.
        Generate tagged list with subfolder level,
        equivalent to `TreeScript.tag_folder_lvl`
        """
        list_files = []
        for filename in os.listdir(directory_name):
            relativ_file = os.path.join(directory_name, filename)
            is_dir = os.path.isdir(relativ_file)

            list_files.append(TaggedFile(filename, level, is_dir))

            if is_dir:
                sub_files = self.from_directory(relativ_file,
                        level + 1)
                list_files.extend(sub_files)
        return list_files
