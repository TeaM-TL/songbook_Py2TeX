# Songbook Py2TeX

Python generator for songbook in PDF, from plain TXT via TeX format

## Idea

### Source of songs

Every song is in separate file, like
```python
title: Umbriaga
authors: lyrics and music: Witold Zamojski


Kiedy jacht nie wraca z mórz | a7 D7
i w główkach portu ciągle go brak, | H7 e
Przejmujesz się i serce Ci drży, | a7
a może już pozostanie tak? | H7


 Umbriaga wciąż gna, | Ae
 silnych wiatrów nie boi się, | a7
 Szuflady wali raz po raz, | D7
 bo przebrany ma bras. | G H7
 Więc nie przejmuj się, | e
 oni wrócą tu, | a7
 Bo oprócz wiatrów i burz | D7
 muszą być, i już. | G H7

chorus
```

keyword *chorus* repeat chorus instead write again

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

## Configuration

Example of `config.ini`:

```ini
[Settings]
chord_right = 0
chorus_repeat = 1
slide = 0
font_lato = 1
new_page = 1
contents = 1
```

- chord_right - chord is printed on left (0) or right side (1)
- chorus_repeat - repeat (1) chorus or not (0)
- slide - generate as book (0) or as slide (1) eg. for mobile phone
- font_lato - use font lato (1) or default (0)
- new_page - every song start on new page (1) or not (0)
- contents - add (1) table of contents or not (0)
