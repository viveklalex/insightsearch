from insightseaarch.data_clean import *
from insightsearch.dataframe_checking import *
from pathlib import Path

class Analysis(DataframeClean):
    def __init__(
        self, df, column_name , date_column= None, vader=False ):

        self.df = df
        self.column_name = column_name
        self.date_column = date_column
        self.vader=vader
        DFvalid.__init__(self, self.df, self.column_name, self.date_column,self.vader)
        self._clean()
    def review_analyze(self):
        self.showing_aspect()
        self.showing_sentiment()



a = Analysis(
    df=str(Path(__file__).parent.parent) +'/saved/All_Beauty_5.csv',
    column_name="reviewText",date_column='reviewTime',vader=False
    )

a.review_analyze()
