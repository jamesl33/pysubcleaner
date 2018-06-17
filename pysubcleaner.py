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
    def __init__(self, input_file):
        self.input_file = input_file

        if os.path.isfile(input_file) and os.path.splitext(input_file)[-1] == '.srt':
            universal_detector = UniversalDetector()

            for line in open(input_file, 'rb'):
                line = bytearray(line)
                universal_detector.feed(line)

                if universal_detector.done:
                    break

            universal_detector.close()

            try:
                self.subtitles = pysrt.open(input_file, universal_detector.result['encoding'])
            except UnicodeDecodeError:
                print('Error: Unable to open subtitle file')
                exit(1)

        else:
            print('Error: File doesn\'t exist or isn\'t a subtitle file')
            exit(1)

    def clean_subtitles(self):
        marked = []
        adverts = self._get_regex('cleaner.regex')

        for index, subtitle in enumerate(self.subtitles):
            for advert in adverts:
                result = re.search(re.compile(advert, flags=re.IGNORECASE), subtitle.text)

                if result:
                    marked.append(index)

        for index in sorted(list(set(marked)), reverse=True):
            del self.subtitles[index]

        self.subtitles.clean_indexes()
        self.subtitles.save(self.input_file)

    @classmethod
    def _get_regex(cls, file_name):
        with open(file_name) as file:
            return [regex.rstrip() for regex in file.readlines()]


def main():
    parser = argparse.ArgumentParser(
        description='remove unwanted subtitles from subtitle files'
    )

    parser.add_argument(
        'file',
        action='store',
        help='the subtitle file that you want to clean',
        type=str
    )

    arguments = parser.parse_args()

    subtile_cleaner = SubtitleCleaner(arguments.file)
    subtile_cleaner.clean_subtitles()


if __name__ == '__main__':
    import argparse
    main()
