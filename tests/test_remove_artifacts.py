import os
import tempfile
import unittest
from pathlib import Path

from rgc.utils.data import remove_artifacts


class TestRemoveArtifacts(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

        # Create test files in the temporary directory
        self.test_files = ["file1.txt", "file2.jpg", "file3.txt", "file4.png", "file5.csv"]
        for file_name in self.test_files:
            Path(os.path.join(self.test_dir.name, file_name)).touch()

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_remove_artifacts(self):
        # Define extensions to keep
        extensions_to_keep = [".txt", ".jpg"]

        # Run the function
        remove_artifacts(self.test_dir.name, extensions_to_keep)

        # List remaining files
        remaining_files = os.listdir(self.test_dir.name)

        # Check that only .txt and .jpg files are kept
        expected_remaining_files = ["file1.txt", "file2.jpg", "file3.txt"]
        self.assertEqual(sorted(remaining_files), sorted(expected_remaining_files))

        # Check that other files are removed
        self.assertNotIn("file4.png", remaining_files)
        self.assertNotIn("file5.csv", remaining_files)


if __name__ == "__main__":
    unittest.main()
