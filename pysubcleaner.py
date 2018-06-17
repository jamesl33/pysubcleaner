#!/usr/bin/python3
"""
Author: James Lee
Email: jamesl33info@gmail.com
Supported Python version: 3.5.2+
"""


import os
import re
import pysrt
from chardet.universaldetector import UniversalDetector


class SubtitleCleaner():
    """Clean subtitle files by removing adverts and unwanted notifications"""
    def clean_subtitles(self, full_path):
        """Clean adverts/unwanted subtitles from subtitle files or a folder
        containing several subtitle files.

        Args:
            full_path (str): The path to a file/folder to clean.
        """
        if os.path.isdir(full_path):
            for subtitle_file in self._get_subtitle_files(full_path):
                self._clean_subtitle_file(subtitle_file)
        elif os.path.splitext(full_path)[-1] == '.srt':
            self._clean_subtitle_file(full_path)
        else:
            print('Error: File doesn\'t exist or isn\'t a subtitle file')
            exit(1)

    def _clean_subtitle_file(self, full_path):
        """Clean adverts/unwanted subtitles from a subtitle file.

        Args:
            full_path (str): The path to the subtitle file.
        """
        marked = []
        adverts = self._get_regex('cleaner.regex')
        subtitles = self._open_sub_file(full_path)

        for index, subtitle in enumerate(subtitles):
            for advert in adverts:
                result = re.search(re.compile(advert, flags=re.IGNORECASE), subtitle.text)

                if result:
                    marked.append(index)

        if marked:
            for index in sorted(list(set(marked)), reverse=True):
                del subtitles[index]

            subtitles.clean_indexes()
            subtitles.save(full_path)

    @classmethod
    def _open_sub_file(cls, full_path):
        """Automatically detect the encoding for a subtitle file and load it.

        Args:
            full_path (str): The path to the subtitle file.
        """

        universal_detector = UniversalDetector()

        for line in open(full_path, 'rb'):
            line = bytearray(line)
            universal_detector.feed(line)

            if universal_detector.done:
                break

        universal_detector.close()

        try:
            return pysrt.open(full_path, universal_detector.result['encoding'])
        except UnicodeDecodeError:
            print('Error: Unable to open subtitle file')
            exit(1)

    @classmethod
    def _get_subtitle_files(cls, full_path):
        """Recursively search through a folder for subtitle files.

        Args:
            full_path (str): The path to a folder containing subtitle files.

        Returns:
            (list): A list of paths to subtitle files.
        """
        subtitles = []
        for dirpath, _, filenames in os.walk(full_path):
            for file_name in filenames:
                if os.path.splitext(file_name)[-1] == '.srt':
                    subtitles.append(os.path.join(dirpath, file_name))
        return subtitles

    @classmethod
    def _get_regex(cls, full_path):
        """Load all of the regex definitions from 'cleaner.regex' which will be used to
        search for adverts/unwanted subtitles.

        Args:
            full_path (str): The path to the file containing regex definitions.

        Returns:
            (list): List containing all the regex definitions found.
        """
        with open(full_path) as file:
            return [regex.rstrip() for regex in file.readlines()]


def main():
    """Main driver code containing the command line user interface"""
    parser = argparse.ArgumentParser(
        description='remove unwanted subtitles from subtitle files'
    )

    parser.add_argument(
        'folder',
        action='store',
        help='input folder/file which you want to clean',
        type=str
    )

    arguments = parser.parse_args()

    subtile_cleaner = SubtitleCleaner()
    subtile_cleaner.clean_subtitles(arguments.folder)


if __name__ == '__main__':
    import argparse
    main()
