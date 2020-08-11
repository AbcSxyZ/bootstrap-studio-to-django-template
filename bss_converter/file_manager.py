import glob
from . import TagConverter

class FileManager:
    """
    Convert html file and move site assets according
    to django architecture.
    """
    def __init__(self):
        self._convert_html_file()

    def _convert_html_file(self):
        """
        Retrieve recursively all html files in the export
        folder, and convert bss attributes to django tag
        using TagConverter.
        """
        htmlfiles = glob.glob("**/*.html", recursive=True)

        for filename in htmlfiles:
            TagConverter(filename)
