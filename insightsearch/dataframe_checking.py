import pandas as pd
from insightsearch.data_clean import  DataframeClean


class DFvalid:
    def __init__(self, df, column_name, date_column,vader):
        self.df = pd.read_csv(df)
        self.column_name = str(column_name)
        self.date_column = date_column
        self.vader=vader
        """
        parm df :df is the dataframe that contains review column , df doenot need all rows should be string. Datatypes other than str will be removed
        param column_name = Name of the column that contains review text 

        """
        DataframeClean.__init__(self, self.df, self.column_name, self.date_column,self.vader)
        # chechking df is a pd.DataFrame
        if self.df is not None:
            if isinstance(self.df, pd.DataFrame) != True:
                raise AttributeError("Data you were uploded is not a dataframe")

            if self.column_name is not None:
                if isinstance(self.column_name, str) != True:
                    raise AttributeError("The dataframe name is not string ")
                if self.column_name not in self.df.columns:
                    raise AttributeError(
                        "Your mentioned name in column_name doesnot exists in your uploaded dataframe"
                    )
            else:
                print("Try to mention a column name where your reviews stored")

            if self.date_column != None:
                if isinstance(self.date_column, str) != True:
                    raise AttributeError("The dataframe name is not string ")
                if self.date_column not in self.df.columns:
                    raise AttributeError(
                        "Your mentioned name in date column does not exists in your uploaded dataframe"
                    )
            else:
                pass
        else:
            print("There is no data frame")
