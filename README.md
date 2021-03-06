# insightsearch

[![GitHub issues](https://img.shields.io/github/issues/vivekalex61/insightsearch)](https://github.com/vivekalex61/insightsearch/issues) [![GitHub license](https://img.shields.io/github/license/vivekalex61/insightsearch?style=flat-square)](https://github.com/vivekalex61/insightsearch/blob/master/LICENCE.txt) [![GitHub forks](https://img.shields.io/github/forks/vivekalex61/insightsearch)](https://github.com/vivekalex61/insightsearch/network) [![GitHub stars](https://img.shields.io/github/stars/vivekalex61/insightsearch)](https://github.com/vivekalex61/insightsearch/stargazers)


Insightsearch is built for Analyzing customer reviews and texts. It will convert the unorganized text data into useful insights and their opinions. Simply, insightsearch tell you what people are talking about your products and services. Insightsearch pipeline is built on top of popular NLP frameworks include Spacy,Textblob and NLTK. Any one can freely use it for finding sentiments, hidden insights and their opinions.

## Features
- **Aspect and Opinion extraction**: Insight search is a aspect based opinion extraction method. It uses simple rule based algorithm to detect and extract aspects and their opinions

- **Sentiment Analysis**: Insightsearch classifies review data into positive and negative sentiments. It also visualises consumers sentiments changes in both monthly and weekly time frame.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install insightsearch.

```bash
pip install insightsearch
```

## Usage

```python
import insightsearch

#create a insightsearch object
ins = insightsearch.Analysis(
    df='PathtoCSV',
    column_name="Text",date_column='date_column_name',vader=False
    )

# returns html file with insights visualisation
ins.review_analyze()
```
## Output
- **Overall sentiments** 
![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/overall_sentiments.png)
- **Sentiment score over the time period** 
![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/overall_sentiments_weekly.png)
![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/overall_sentiments_monthly.png)
- **Aspects and opinions**
 
   ![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/aspect_opinions_1.png)

   ![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/aspect_opinions_2.png)

   ![alt text](https://raw.githubusercontent.com/vivekalex61/insightsearch/master/test/aspect_opinions_3.png)




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
