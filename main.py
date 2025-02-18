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
import os.path
import re
import shutil


TEMPLATE_DIR = os.path.join(os.getcwd(), "tex")
OUT_DIR = os.path.join(os.getcwd(), "tmp")
SONGS_DIR = os.path.join(os.getcwd(), "songs")
MAIN_TEX = os.path.join(OUT_DIR, "main.tex")
LAYOUT_TEX = os.path.join(OUT_DIR, "main_layout.tex")
SONG_REF_TEX = os.path.join(OUT_DIR, "main_song_ref.tex")


def tex_layout(layout, lato, table_of_contents, chorus_left_line):
    """initial layout"""
    if layout:
        layout = "slides"
    else:
        layout = "chorded"

    with open(LAYOUT_TEX, "w", encoding="utf-8") as fh_out:
        fh_out.write("\\usepackage[" + layout + "]{songs}\n")
        if lato:
            fh_out.write("\\setmainfont{Lato}\n\\setsansfont{Lato Light}\n")
        if not chorus_left_line:
            fh_out.write("\\setlength{\cbarwidth}{0pt}")

    with open(SONG_REF_TEX, "w", encoding="utf-8") as fh_out:
        if table_of_contents:
            text = """% hyperlinks for table of contents
\\renewcommand{\\songtarget}[2]
{\\pdfbookmark[#1]{\\thesongnum. \\songtitle}{#2}}
\\renewcommand{\\songlink}[2]{\\hyperlink{#1}{#2}}
"""
        else:
            text = "% empty file\n"
        fh_out.write(text)


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


def generate_begin_section(full_dir, short_dir):
    """generate section if filr 0.dir exists"""
    file_name = short_dir + "_begin"
    print("Processing: " + file_name)
    section_file = os.path.join(full_dir, "0.dir")
    section_data = ""
    if os.path.exists(section_file):
        with open(section_file, "r", encoding="utf-8") as fh_section:
            section_data = fh_section.readline()
    if section_data:
        section_data = "\\songsection{" + section_data + "}\n"
    file_contents = section_data + "\\begin{songs}{titleidx}\n"

    with open(
        os.path.join(OUT_DIR, file_name + ".tex"), "w", encoding="utf-8"
    ) as fh_out:
        fh_out.write(file_contents)
    with open(MAIN_TEX, "a", encoding="utf-8") as fh_out:
        fh_out.write("\\input{" + file_name + "}\n\n")


def generate_end_section(short_dir):
    """generate section if filr 0.dir exists"""
    file_name = short_dir + "_end"
    print("Processing: " + file_name)
    file_contents = "\\end{songs}\n"

    with open(
        os.path.join(OUT_DIR, file_name + ".tex"), "w", encoding="utf-8"
    ) as fh_out:
        fh_out.write(file_contents)
    with open(MAIN_TEX, "a", encoding="utf-8") as fh_out:
        fh_out.write("\\input{" + file_name + "}\n\n")


def generate(songs_txt_dir, song_on_new_page):
    """generate TeX from TXT file"""

    song_files = [
        file_name
        for file_name in os.listdir(songs_txt_dir)
        if file_name.endswith("txt")
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
            os.path.join(songs_txt_dir, song_file), "r", encoding="utf-8"
        ) as fh_data:
            for line in fh_data:
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
        ) as fh_out:
            fh_out.write(file_contents)
        with open(MAIN_TEX, "a", encoding="utf-8") as fh_out:
            fh_out.write("\\input{" + song_name + "}\n\n")


def generate_end_tex_statements(table_of_contents):
    """add end statements in TeX file"""
    with open(MAIN_TEX, "a", encoding="utf-8") as fh_out:
        text = "\n"
        if table_of_contents:
            text += "\\showindex[2]{Spis treści}{titleidx}\n"
        text += "\\end{document}\n"
        fh_out.write(text)


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
        chorus_line = config.getint("Settings", "chorus_line")
    except:
        chord_right = 0
        slide = 0
        font_lato = 0
        new_page = 0
        contents = 0
        chorus_line = 1

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    tex_layout(slide, font_lato, contents, chorus_line)

    # TeX templates
    for filename in ("main.tex", "title.tex", "songs.sty", "songidx.lua"):
        shutil.copyfile(
            os.path.join(TEMPLATE_DIR, filename), os.path.join(OUT_DIR, filename)
        )

    if chord_right == 0:
        with open(MAIN_TEX, "a", encoding="utf-8") as fh_out:
            fh_out.write("\\reversemarginpar\n\n")

    songs_dirs = list(os.listdir(SONGS_DIR))
    songs_dirs.sort()
    print(songs_dirs)
    for songs_dir in songs_dirs:
        songs_full_dir = os.path.join(SONGS_DIR, songs_dir)
        if os.path.isdir(songs_full_dir):
            generate_begin_section(songs_full_dir, songs_dir)
            generate(songs_full_dir, new_page)
            generate_end_section(songs_dir)

    generate_end_tex_statements(contents)


if __name__ == "__main__":
    main()
