# munimgen
MUN Placard Image Generator

### Installation Instructions:
1. Download flags images from Flagpedia [here](http://flags.fmcdn.net/data/flags-ultra.zip) and extract it into folder `flags/` in the root directory.
2. Download countries file from `lukes/ISO-3166-Countries-with-Regional-Codes` [here](https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-2/slim-2.csv) and extract it as `countries.csv` in the root directory.
3. Download Helvetica Now from Monotype's website [here](https://hello.monotype.com/Helvetica-Now-Download.html), and extract the font in the archive (`HelveticaNowDisplayXBlk.otf`) to the root directory.
4. Install required modules from the root directory:
```pip install -r requirements.txt```
5. Modify `countries_erratum.csv` as required (see below).
6. Modify `data.csv` to add countries for each committee (see below).
7. Run `main.py` with the following command (where `py` is your Python 3.x interpreter)
```py main.py```
8. Copy output placard images from output folder (`output/`).

#### Modifying `countries_erratum.csv`
For each line, the countries must be written in the following format:
```Name,Code```

|  | Format | Sample |
| - | - | - |
| Name | Country Name | `Taiwan` or `"Taiwan, Republic of China"`|
| Code | Country Code (ISO-3166 Alpha 2)| `TW` or `tw` |

The erratum file is loaded after the countries file and can be used to modify country names and add new countries.

#### Modifying `data.csv`
For each line, the data must be in the following format, where multiple country codes can be entered at once:
```Committee,Code[,Code]```

| | Format | Sample |
| - | - | - |
| Committee | Committee Background Name | `unsc`, `ecofin`, `au`, `interpol` |
| Code | Country Code (ISO-3166 Alpha 2)| `TW` or `tw` |

### Copyright
All assets used in the software belong to their respective owners, and are used under non-commercial fair use. The software is not licensed for use without prior permission.
