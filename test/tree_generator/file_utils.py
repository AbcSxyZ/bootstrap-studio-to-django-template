import os
import shutil
import difflib
from pathlib import Path

class Workdir:
    """
    Context manager to switch working directory safely.
    """
    def __init__(self, directory):
        self.destination_dir = directory

        if not os.path.exists(directory):
            Path(directory).mkdir()

    def __enter__(self):
        self._old_pwd = os.getcwd()
        os.chdir(self.destination_dir)
    
    def __exit__(self, *args, **kwargs):
        os.chdir(self._old_pwd)

class TaggedFile:
    """
    Represent a single file with his corresponding
    subfolder level.

    Used to facitilate tagging of tree/folder exploration.
    """
    def __init__(self, filename, level, isdir=None):
        if isdir is None:
            isdir = filename.endswith("/")

        self.isdir = isdir
        self.level = level
        self.filename = self.clean_filename(filename)

    @staticmethod
    def clean_filename(filename):
        if filename.endswith("/"):
            filename = filename[:-1]
        return filename.replace('|-', "").strip()

class Directory:
    """
    Represent a single directory, with all availables files
    and directories inside the given folder.

    Understand which folder is a directory, and will store
    directory childrens, subfolder also use Directory.
    """
    def __init__(self, name, potential_files, level=-1):
        self.name = name
        self.level = level
        self.potential_files = potential_files

        self.files = []
        self.directories = []

        self._retrieve_directory_files()
        self._sort()


    def generate(self):
        """
        Create each file and directory expected by
        the given template.
        """
        with Workdir(self.name):
            for directory in self.directories:
                directory.generate()

            for filename in self.files:
                Path(filename).touch()

    def delete(self):
        """
        Delete Directory folder
        """
        shutil.rmtree(self.name)

    def diff(self, other):
        """
        Compare two different document, an return diff output.

        Use the string representation of Directory to perform
        comparaison.
        With alphabetical sort and identical files/folder,
        it must be the same.
        """
        self_repr = str(self).split("\n")
        other_repr = str(other).split("\n")
        res_diff = difflib.ndiff(self_repr, other_repr)
        diff_ouput = "+ : Program output\n- : Reference output\n\n"
        return diff_ouput + "\n".join(res_diff)


    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        """
        Print directory as a tree. Create back equivalent
        of the template script file.

        To be ordered, display sub folder, followed by regular files.
        All directory and files are sorted in alphabetical order.
        """
        # Convert back Directory object to his string representation
        directory_repr = ""

        #Format Directory name
        if self.name and self.level >= 0:
            #add indentation and '|-' on left side
            directory_repr = "    " * self.level
            directory_repr += "|- " if self.level else ""

            directory_repr += self.name + "/\n"

        #Recursive formatting of sub folders
        for sub_directory in self.directories:
            directory_repr += repr(sub_directory)

        #Format all regular files
        for filename in self.files:
            #add indentation and '|-' on left side
            directory_repr += "    " * (self.level + 1)
            directory_repr += "|- " if self.level > 0 else ""

            directory_repr += filename + "\n"

        return directory_repr

    def _sort(self):
        """
        Order alphabetically files and directories.
        """
        self.directories.sort(key=lambda directory : directory.name)
        self.files.sort()
        
        (directory._sort() for directory in self.directories)

    def _retrieve_directory_files(self):
        """
        Indentify files and directories inside the current
        directory.
        """
        for index, tagged_file in enumerate(self.potential_files):
            #Element contained by the directory
            if tagged_file.level == self.level + 1:
                if tagged_file.isdir:
                    new_dir = Directory(
                            tagged_file.filename,
                            self.potential_files[index + 1:],
                            self.level + 1, 
                                )
                    self.directories.append(new_dir)

                else:
                    self.files.append(tagged_file.filename)

            ## Stop iteration if actual file in template list
            ## is a parent folder
            elif tagged_file.level == self.level:
                break
