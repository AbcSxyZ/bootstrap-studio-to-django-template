import glob
from . import TagConverter
import os
from distutils.dir_util import copy_tree

class FileManager:
    """
    Convert html file and move site assets according
    to django architecture.

    File organisation is bss should be done
    according to django application.

    Use convention of 'static' and 'templates' folders
    to store asset and html templates respectively.
    """
    DJANGO_PROJECT = os.environ['DJANGO_PROJECT']

    def __init__(self):
        self._convert_html_file()
        self.apps = self._retrieve_django_apps()
        self._move_to_django()

    def _convert_html_file(self):
        """
        Retrieve recursively all html files in the export
        folder, and convert bss attributes to django tag
        using TagConverter.
        """
        htmlfiles = glob.glob("**/*.html", recursive=True)

        for filename in htmlfiles:
            TagConverter(filename)

    def _retrieve_folders(self, directory, black_listed=[]):
        """
        Retrieve all folders of a given directory, remove
        some black listed folders.
        """
        ls_result = os.listdir(directory)

        #Remove specifed folder
        for unwanted_dir in black_listed:
            if unwanted_dir in ls_result:
                ls_result.remove(unwanted_dir)

        #Convert path to be absolute
        absolute_ls = [os.path.join(directory, filename) for \
                filename in ls_result]
        return list(filter(os.path.isdir, absolute_ls))

    def _retrieve_django_apps(self):
        """
        Find all available django app/modules in the
        project directory.

        Remove settings folder of the project.
        """
        project_dirs = self._retrieve_folders(self.DJANGO_PROJECT)

        #Find and remove configuration folder
        setting_folder = None
        for directory in project_dirs:
            directory_files = os.listdir(directory)
            if "settings.py" in directory_files:
                setting_folder = directory
                break
        project_dirs.remove(setting_folder)

        #Remove folder path of django project to keep only app names
        return list(map(os.path.basename, project_dirs))

    def _diff_applications(self, folders):
        """
        Compare a list of folder with application of the
        django project.

        Store applications folder in a specific list.
        """
        diff_res = {
                "applications" : [],
                "common" : [],
                }

        #Retrieve possible app name for given folders
        #Map app name to a folder
        app_to_folder = {}
        for folder in folders:
            app = os.path.basename(folder)
            app_to_folder[app] = folder

        #Find folder who are matchin existing apps
        for application in self.apps:
            bss_folder = app_to_folder.pop(application, None)
            if bss_folder:
                diff_res["applications"].append(bss_folder)

        #Store folder who don't match any application
        diff_res["common"] = list(app_to_folder.values())

        return diff_res

    def _move_html(self):
        """
        Move html files from bss export folder to django project
        folder.

        Move them in template directory within the corresponding
        application.
        """
        bss_folders = self._retrieve_folders(".", ["assets"])
        organized_folder = self._diff_applications(bss_folders)

        for bss_app_folder in organized_folder['applications']:
            app_name = os.path.basename(bss_app_folder)

            #Find app folder in django project
            django_app_folder = os.path.join(self.DJANGO_PROJECT, \
                    app_name)
            django_app_folder = os.path.join(django_app_folder, \
                    f"templates/{app_name}")

            copy_tree(bss_app_folder, django_app_folder)

    def _move_to_django(self):
        """
        """
        self._move_html()

