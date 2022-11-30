# Rule-analyzer

Analyzer for rules extracted from US states and other territories with English driving manuals 

## Installation

The project uses:

```bash
pip install sklearn
pip install pandas
pip install numpy
pip install matplotlib
pip install pyfiglet
```

## Usage

```bash
 python RuleAnalyzer.py --source "natLangRules.txt" --m "kmeans"
```
Source is taken from the ./data folder.
Right now it provides two model options, bag of words (bow) and K-Means (kmeans)


## License

[MIT](https://choosealicense.com/licenses/mit/)