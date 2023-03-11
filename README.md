# Songbook Py2TeX

Python generator for songbook, from dict to TeX format

## Idea

### Source of songs

Every song is in separate file, like
```python
[
"       a7               D7"
"Kiedy jacht nie wraca z mórz"
"H7                  e"
"i w główkach portu ciągle go brak,"
"      a7"
"Przejmujesz się i serce Ci drży,"
"                      H7"
"a może już pozostanie tak?"
]
```

### Songs after processing
```tex
Kied\[a7]y jacht nie w\[D7]raca z mórz
\[H7]i w główkac\[e]h portu ciągle go brak,
Prz\[a7]ejmujesz się i serce Ci drży,
a może już po\[H7]zostanie tak?
```

### Output

After song processing XeLaTeX will process full songbook using *songbook* package.
Output format is PDF.

## Requirements
- XeLaTeX installation, TeX Live or MacTeX
- Python3
