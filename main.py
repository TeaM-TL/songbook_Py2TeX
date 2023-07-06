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

Python generator for songbook, from txt to TeX format
"""

import configparser
import os
import re
import shutil

SONGS='songs'
OUTDIR='tmp'
TEXTMPL='tex'
SONGEXT='txt'
TEXEXT='.tex'


def line_parse(line, current_line, start):
    """ parse line """
    line = line.strip()
    splitted_line = re.split('\|', line, 1)
    if len(splitted_line) == 2:
        text = '\\marginnote{\\textsf{' + splitted_line[1] + '}} ' + splitted_line[0] + '\n'
    else:
        text = line + '\n'
    if start:
        if current_line == 'verse':
            text = '\\verse\\singlespace\n' + text
        elif current_line == 'chorus':
            text = '\\chorus\\singlespace\n' + text

    return text

def generate(songs_dir, out_dir, chord_right):
    """ generate TeX from TXT file """

    song_files = [file_name for file_name in os.listdir(songs_dir) if file_name.endswith(SONGEXT)]
    song_files.sort()
    for song_file in song_files:
        song_name = os.path.splitext(song_file)[0]
        print('Processing: ' + song_name)

        file_contents = ''
        chorus_contents = ''
        text = ''
        current = ''
        with open(os.path.join(songs_dir,song_file), 'r', encoding='utf-8') as file_data:
            for line in file_data:
                line_strip = line.strip()
                if len(line_strip) == 0:
                    # empty line as separator
                    if current == 'verse':
                        text = '\\endverse\n\n'
                    elif current == 'chorus':
                        text = '\\endchorus\n\n'
                        chorus_contents = chorus_contents + text
                    else:
                        text = ''
                    current = ''
                    start_verse = 1
                    start_chorus = 1
                elif re.search('chorus', line):
                    # print chorus
                    text = chorus_contents
                elif re.search('^title:', line):
                    # title
                    title = re.split('^title:', line)
                    text = '\\beginsong{' + title[1].strip() + '}['
                elif re.search('^authors:', line):
                    # authors
                    authors = re.split('^authors:', line)
                    text =  'by={' + authors[1].strip() + '}]\n\n'
                elif re.search('^[^ ]', line):
                    # verse
                    current = 'verse'
                    text = line_parse(line, current, start_verse)
                    if start_verse:
                        start_verse = 0
                elif re.search('^ ', line):
                    # chorus
                    current = 'chorus'
                    text = line_parse(line, current, start_chorus)
                    if start_chorus:
                        start_chorus = 0
                    chorus_contents = chorus_contents + text

                file_contents = file_contents + str(text)

        file_contents = file_contents + '\n\\endsong\n'
        #print(file_contents)
        with open(os.path.join(out_dir, song_name + TEXEXT), 'w', encoding='utf-8') as file_out:
            file_out.write(file_contents)
        with open(os.path.join(out_dir, 'main.tex'), 'a', encoding='utf-8') as file_out:
            file_out.write('\\input{' + song_name + '}\n\n')


def main():
    """ main function """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding="utf8")

        # read values from a section
        chord_right = config.getint('Settings', 'chord_right')
    except:
        chord_right = 0

    songs_dir = os.path.join(os.getcwd(), SONGS)
    template = os.path.join(os.getcwd(), TEXTMPL)
    out_dir = os.path.join(os.getcwd(), OUTDIR)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # TeX template
    shutil.copyfile(os.path.join(template, 'template.tex'), os.path.join(out_dir, 'main.tex'))
    shutil.copyfile(os.path.join(template, 'title.tex'),    os.path.join(out_dir, 'title.tex'))
    shutil.copyfile(os.path.join(template, 'songs.sty'),    os.path.join(out_dir, 'songs.sty'))
    shutil.copyfile(os.path.join(template, 'songidx.lua'),  os.path.join(out_dir, 'songidx.lua'))
    if chord_right == 0:
        with open(os.path.join(out_dir, 'main.tex'), 'a', encoding='utf-8') as file_out:
            file_out.write('\\reversemarginpar\n')
    generate(songs_dir, out_dir, chord_right)
    # end statements in TeX file
    with open(os.path.join(out_dir, 'main.tex'), 'a', encoding='utf-8') as file_out:
        text = '\n\\end{songs}\n\\showindex[2]{Spis szant}{titleidx}\n\\end{document}\n'
        file_out.write(text)


if __name__=="__main__":
    main()
