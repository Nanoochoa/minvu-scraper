`minvu-scraper`
=======

# Description

Scrape [MINVU D.S.01 beneficiaries](http://transparencia.minvu.cl/IRIS_FILES/Transparencia/beneficio_regiones_buscador.html).

# Usage

```bash
python main.py [-h] -y YEAR -f FILENAME
```
## Arguments

|short|long|default|help|
| :--- | :--- | :--- | :--- |
|`-h`|`--help`||show this help message and exit|
|`-y`|`--year`|`None`|year to scrape|
|`-f`|`--filename`|`None`|filename of CSV output|
|`-t`|`--timeout`|`3`|request timeout|