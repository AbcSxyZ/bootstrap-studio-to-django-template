import unittest
from tree_generator import TreeScript

class FileManagerTest(unittest.TestCase):
    maxDiff = None

    def run_script(self, script_file):
        """
        Perform test from a single tree script.
        """
        script_manager = TreeScript(script_file)
        try:
            result_tree, expected_tree = script_manager.launch()
        finally:
            script_manager.clean()
        self.assertEqual(str(result_tree), str(expected_tree))

    def test_first(self):
        self.run_script("test/tree_script/test.txt")
