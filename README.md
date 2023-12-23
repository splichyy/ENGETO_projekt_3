## Ukázka projektu

Výsledky hlasovaní pro okres Kutná hora.

1.  argument - 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105'
2.   argument -  vysledky\_kutna\_hora.csv

Spuštění programu:

```css
python main.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105' vysledky_kutna_hora.csv
```

Průběh stahování:

```css
Stahuji data z vybraného URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105
Ukládám do souboru: vysledky_kutna_hora.csv
Ukončuji election-scraper
```

Částečný výstup:

```css
Číslo obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana...
531367,Adamov,102,74,72,5,0,0,9,0,8,14,0,2,0,0,0,7,0,0,0,21,0,0,2,0,0,0,0,4,0
531111,Bernardov,157,89,89,5,0,0,1,0,7,14,0,1,1,0,0,11,1,0,0,30,0,2,1,0,1,0,1,11,2
533971,Bílé Podolí,502,299,299,18,1,0,30,0,30,24,1,5,2,0,0,11,0,0,4,136,0,1,3
...
```
