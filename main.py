# -*- coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint disable=invalid-name

"""
Copyright (c) 2023 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Python generator for songbook, from dict to TeX format
"""

import os

SONGS='songs'
OUTDIR='tmp'
SONGEXT='txt'
TEXEXT='.tex'


def generate():
    """ generate TeX from TXT file """
    songs_dir = os.path.join(os.getcwd(), SONGS)
    out_dir = os.path.join(os.getcwd(), OUTDIR)
    song_files = [file_name for file_name in os.listdir(songs_dir) if file_name.endswith(SONGEXT)]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    songs = {}

    for song_file in song_files:
        song_name = os.path.splitext(song_file)[0]
        print('Processing: ' + song_name)

        file_contents = '\\beginsong{'
        doit = 0
        text = ''
        with open(os.path.join(songs_dir,song_file), 'r', encoding='utf-8') as file_data:
            for line in file_data:
                if line == 'title\n':
                    doit = 4
                elif line == 'authors\n':
                    text = ''
                    doit = 3
                elif line == 'verse\n' or line == 'chorus\n':
                    text = '\\' + line
                    doit = 1
                elif line == 'endverse\n' or line == 'endchorus\n':
                    text = '\\' + line
                    doit = 0
                elif line == '':
                    text = '\n'
                else:
                    if doit == 4:
                        # title
                        text = line[0:-1] + '}['
                        doit = 0
                    elif doit == 3:
                        # authors
                        text = 'by={' + line[0:-1] + '}]\n\n'
                        doit = 0
                    elif doit == 1:
                        # acords
                        text = ''
                        doit = 0
                    else:
                        # verse
                        text = line
                        doit = 1
                file_contents = file_contents + text

        file_contents = file_contents + '\\endsong\n'
        #print(file_contents)
        with open(os.path.join(out_dir,song_name + TEXEXT), 'w', encoding='utf-8') as file_out:
            file_out.write(file_contents)


def main():
    """ main function """
    generate()

if __name__=="__main__":
    main()