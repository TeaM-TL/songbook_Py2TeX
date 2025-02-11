python main.py
cd tmp
xelatex main.tex
texlua songidx.lua cbtitle.sxd cbtitle.sbx
xelatex main.tex
copy main.pdf ..\
cd ..