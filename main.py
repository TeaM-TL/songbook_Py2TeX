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

import configparser
import os
import shutil

SONGS='songs'
OUTDIR='tmp'
TEXTMPL='tex'
SONGEXT='txt'
TEXEXT='.tex'


def generate(songs_dir, out_dir, chord_above):
    """ generate TeX from TXT file """

    song_files = [file_name for file_name in os.listdir(songs_dir) if file_name.endswith(SONGEXT)]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for song_file in song_files:
        song_name = os.path.splitext(song_file)[0]
        print('Processing: ' + song_name)

        file_contents = '\\beginsong{'
        doit = 0
        text = ''
        with open(os.path.join(songs_dir,song_file), 'r', encoding='utf-8') as file_data:
            for line in file_data:
                line = line.strip()
                if line == 'title':
                    doit = 4
                elif line == 'authors':
                    text = ''
                    doit = 3
                elif line in ('verse', 'chorus'):
                    if chord_above:
                        text = '\\' + line + '\n'
                    else:
                        text = '\\' + line + '\\singlespace\n'
                    doit = 1
                elif line in ('endverse', 'endchorus'):
                    text = '\\' + line + '\n'
                    doit = 0
                elif line == '':
                    text = '\n'
                else:
                    if doit == 4:
                        # title
                        text = line + '}['
                        doit = 0
                    elif doit == 3:
                        # authors
                        text = 'by={' + line + '}]\n'
                        doit = 0
                    elif doit == 1:
                        # acords
                        text = ''
                        doit = 0
                    else:
                        # verse
                        text = line + '\n'
                        doit = 1
                file_contents = file_contents + str(text)

        file_contents = file_contents + '\\endsong\n'
        #print(file_contents)
        with open(os.path.join(out_dir, song_name + TEXEXT), 'w', encoding='utf-8') as file_out:
            file_out.write(file_contents)
        with open(os.path.join(out_dir, 'main.tex'), 'a', encoding='utf-8') as file_out:
            file_out.write('\\input{' + song_name + '}\n')


def main():
    """ main function """
    config = configparser.ConfigParser()
    config.read('config.ini', encoding="utf8")

    # read values from a section
    try:
        chord_above = config.getint('Settings', 'chord_above')
    except:
        chord_above = 0

    songs_dir = os.path.join(os.getcwd(), SONGS)
    template = os.path.join(os.getcwd(), TEXTMPL)
    out_dir = os.path.join(os.getcwd(), OUTDIR)
    # TeX template
    shutil.copyfile(os.path.join(template, 'template.tex'), os.path.join(out_dir, 'main.tex'))
    shutil.copyfile(os.path.join(template, 'songs.sty'),    os.path.join(out_dir, 'songs.sty'))
    generate(songs_dir, out_dir, chord_above)
    # end statements in TeX file
    with open(os.path.join(out_dir, 'main.tex'), 'a', encoding='utf-8') as file_out:
        file_out.write('\\end{songs}\n\\end{document}\n')


if __name__=="__main__":
    main()
