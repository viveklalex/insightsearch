from insightsearch.data_clean import *
from insightsearch.dataframe_checking import *
from pathlib import Path

class Analysis(DataframeClean):
    def __init__(
        self, df: pd.DataFrame = None, column_name: str = None, date_column: str = None, bert: bool = False
    ):
        self.df = df
        self.column_name = column_name
        self.date_column = date_column
        self.bert=bert
        DFvalid.__init__(self, self.df, self.column_name, self.date_column,self.bert)
        self._clean()
    def review_analyze(self):
        self.showing_aspect()
        self.showing_sentiment()


a = Analysis(
    str(Path(__file__).parent.parent) +'/saved/All_Beauty_5.csv',
    "reviewText",
    "reviewTime",False
)

a.review_analyze()
