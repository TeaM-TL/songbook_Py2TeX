#!/bin/sh

python3 main.py
cd tmp
xelatex main.tex
xelatex main.tex
cd -
