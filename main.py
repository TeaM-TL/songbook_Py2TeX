# -*- coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=line-too-long

"""
Copyright (c) 2023-2025 Tomasz Łuczak

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


TEMPLATE_DIR = os.path.join(os.getcwd(), "tex")
OUT_DIR = os.path.join(os.getcwd(), "tmp")
SONGS_DIR = os.path.join(os.getcwd(), "songs")
MAIN_TEX = os.path.join(OUT_DIR, "main.tex")
LAYOUT_TEX = os.path.join(OUT_DIR, "main_layout.tex")
SONG_REF_TEX = os.path.join(OUT_DIR, "main_song_ref.tex")


def line_parse(line, current_line, start):
    """parse line"""
    line = line.strip()
    splitted_line = re.split(r"\|", line, 1)
    if len(splitted_line) == 2:
        text = (
            "\\marginnote{\\textsf{"
            + splitted_line[1].strip()
            + "}} "
            + splitted_line[0].strip()
            + "\n"
        )
    else:
        text = line.strip() + "\n"
    if start:
        if current_line == "verse":
            text = "\\verse\\singlespace\n" + text
        elif current_line == "chorus":
            text = "\\chorus\\singlespace\n" + text

    return text


def generate(song_on_new_page):
    """generate TeX from TXT file"""

    song_files = [
        file_name for file_name in os.listdir(SONGS_DIR) if file_name.endswith("txt")
    ]
    song_files.sort()
    for song_file in song_files:
        song_name = os.path.splitext(song_file)[0]
        print("Processing: " + song_name)

        file_contents = ""
        chorus_contents = ""
        text = ""
        current = ""
        with open(
            os.path.join(SONGS_DIR, song_file), "r", encoding="utf-8"
        ) as file_data:
            for line in file_data:
                line_strip = line.strip()
                if len(line_strip) == 0:
                    # empty line as separator
                    if current == "verse":
                        text = "\\endverse\n\n"
                    elif current == "chorus":
                        text = "\\endchorus\n\n"
                        chorus_contents += text
                    else:
                        text = ""
                    current = ""
                    start_verse = 1
                    start_chorus = 1
                elif re.search("chorus", line):
                    # print chorus
                    text = chorus_contents
                elif re.search("^title:", line):
                    # title
                    title = re.split("^title:", line)
                    text = "\\beginsong{" + title[1].strip() + "}["
                elif re.search("^authors:", line):
                    # authors
                    authors = re.split("^authors:", line)
                    text = "by={" + authors[1].strip() + "}]\n\n"
                elif re.search("^[^ ]", line):
                    # verse
                    current = "verse"
                    text = line_parse(line, current, start_verse)
                    if start_verse:
                        start_verse = 0
                elif re.search("^ ", line):
                    # chorus
                    current = "chorus"
                    text = line_parse(line, current, start_chorus)
                    if start_chorus:
                        start_chorus = 0
                    chorus_contents += text

                file_contents += str(text)

        file_contents += "\n\\endsong\n"
        if song_on_new_page:
            # file_contents += "\n\\nextcol\n\n"
            file_contents += "\n\\brk\n"

        with open(
            os.path.join(OUT_DIR, song_name + ".tex"), "w", encoding="utf-8"
        ) as file_out:
            file_out.write(file_contents)
        with open(MAIN_TEX, "a", encoding="utf-8") as file_out:
            file_out.write("\\input{" + song_name + "}\n\n")


def main():
    """main function"""
    try:
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf8")

        # read values from a section
        chord_right = config.getint("Settings", "chord_right")
        slide = config.getint("Settings", "slide")
        font_lato = config.getint("Settings", "font_lato")
        new_page = config.getint("Settings", "new_page")
        contents = config.getint("Settings", "contents")
    except:
        chord_right = 0
        slide = 0
        font_lato = 0
        new_page = 0
        contents = 0

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    if slide:
        layout = "slides"
    else:
        layout = "chorded"

    with open(LAYOUT_TEX, "w", encoding="utf-8") as file_out:
        file_out.write("\\usepackage[" + layout + "]{songs}\n")
        if font_lato:
            file_out.write("\\setmainfont{Lato}\n\\setsansfont{Lato Light}\n")

    with open(SONG_REF_TEX, "w", encoding="utf-8") as file_out:
        if contents:
            text = """% hyperlinks for table of contents
\\renewcommand{\\songtarget}[2]
{\\pdfbookmark[#1]{\\thesongnum. \\songtitle}{#2}}
\\renewcommand{\\songlink}[2]{\\hyperlink{#1}{#2}}
"""

        else:
            text = "% empty file\n"
        file_out.write(text)
    # TeX templates
    for filename in ("main.tex", "title.tex", "songs.sty", "songidx.lua"):
        shutil.copyfile(
            os.path.join(TEMPLATE_DIR, filename), os.path.join(OUT_DIR, filename)
        )

    if chord_right == 0:
        with open(MAIN_TEX, "a", encoding="utf-8") as file_out:
            file_out.write("\\reversemarginpar\n\n")
    generate(new_page)
    # end statements in TeX file
    with open(MAIN_TEX, "a", encoding="utf-8") as file_out:
        text = "\\end{songs}\n"
        if contents:
            text += "\\showindex[2]{Spis szant}{titleidx}\n"
        text += "\\end{document}\n"
        file_out.write(text)


if __name__ == "__main__":
    main()
