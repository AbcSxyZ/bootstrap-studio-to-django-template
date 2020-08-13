import unittest
from pathlib import Path
from tree_generator import TreeScript
import os

class FileManagerTest(unittest.TestCase):
    TEST_FOLDER = "test/tree_script"
    LOG_DIR = os.path.realpath("test_log")
    maxDiff = None

    #For the test fixture, move to specified TEST_FOLDER
    def setUp(self):
        self._oldpwd = os.getcwd()
        os.chdir(self.TEST_FOLDER)

    def tearDown(self):
        result = self.defaultTestResult()
        self._feedErrorsToResult(result, self._outcome.errors)
        os.chdir(self._oldpwd)

    def log_error(self, script_file, result_tree, reference_tree):
        if not os.path.exists(self.LOG_DIR):
            Path(self.LOG_DIR).mkdir()
        logfile = os.path.join(self.LOG_DIR, script_file)
        with open(logfile, "w") as logfile_stream:
            print(result_tree.diff(reference_tree), file=logfile_stream)

    def run_script(self, folder, script_file):
        """
        Perform test from a single tree script.
        """
        script_manager = TreeScript(os.path.join(folder, script_file))
        try:
            result_tree, expected_tree = script_manager.launch()
        finally:
            script_manager.clean()

        #On test error, log diff output in a logfile
        try:
            self.assertEqual(str(result_tree), str(expected_tree))
        except AssertionError as error:
            self.log_error(script_file, result_tree, expected_tree)
            raise error


    def test_html_move(self):
        self.run_script("html", "single_app_single_file")
        self.run_script("html", "single_app_multiple_file")
        self.run_script("html", "multiple_app_single_file")
        self.run_script("html", "multiple_app_multiple_file")
        self.run_script("html", "subfolders")
        self.run_script("html", "file_outside_apps")
        self.run_script("html", "file_outside_and_file_correct")
        self.run_script("html", "created_and_uncreated_app")

    def test_assets(self):
        self.run_script("assets", "img_single_app_single_file")
        self.run_script("assets", "img_single_app_multiple_file")
        self.run_script("assets", "img_multiple_app_single_file")
        self.run_script("assets", "img_multiple_app_multiple_file")
        self.run_script("assets", "subfolders")
        self.run_script("assets", "img_multiple_app_multiple_file")
        self.run_script("assets", "uncreated_app")
        self.run_script("assets", "file_outside_apps")
        self.run_script("assets", "file_outside_and_file_correct")
