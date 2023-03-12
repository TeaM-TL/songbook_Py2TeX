# Songbook Py2TeX

Python generator for songbook, from dict to TeX format

## Idea

### Source of songs

Every song is in separate file, like
```python
title
Umbriaga
authors
lyrics and music: Witold Zamojski

verse
       a7               D7
Kiedy jacht nie wraca z mórz
H7                  e"
i w główkach portu ciągle go brak,
      a7
Przejmujesz się i serce Ci drży,
                      H7
a może już pozostanie tak?
endverse

chorus
Ae
Umbriaga wciąż gna,
a7
silnych wiatrów nie boi się,
                     D7
Szuflady wali raz po raz,
G               H7
bo przebrany ma bras.
         e
Więc nie przejmuj się,
    a7
oni wrócą tu,
          D7
Bo oprócz wiatrów i burz
G            H7
muszą być, i już.
endchorus
```

### Songs after processing
```tex
\beginsong{Umbriaga}[by={tekst i muzyka: Witold Zamojski}]


\verse
Kied\[a7]y jacht nie w\[D7]raca z mórz
\[H7]i w główkac\[e]h portu ciągle go brak,
Prz\[a7]ejmujesz się i serce Ci drży,
a może już po\[H7]zostanie tak?
\endverse

...
\endsong
```

### Output

After song processing XeLaTeX will process full songbook using *songbook* package.
Output format is PDF.

## Requirements
- XeLaTeX installation, TeX Live or MacTeX
- Python3

## How to run

Linux or MacOS
```bash
sh start.sh
```
or if use Windows
```bash
start.bat
```

