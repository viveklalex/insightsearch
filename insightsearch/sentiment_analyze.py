import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm

analyser = SentimentIntensityAnalyzer()
class Sentimentanalyze:
    def __init__(self,clean_df, column_name,date_column,vader):
        self.clean_df=clean_df
        self.column_name=column_name
        self.date_column=date_column
        self.vader=vader



    @staticmethod
    def _prediction_textblob(text):
        return 0 if (TextBlob(text).sentiment.polarity <= 0)else 1

    @staticmethod
    def _prediction_vader(text):
        sentiment_score = analyser.polarity_scores(text)

        return 1 if (sentiment_score['compound']  >= 0.05 ) else 0

    def showing_sentiment(self):
        df1 = self.clean_df.copy()
        if self.vader== False:
            tqdm.pandas(desc="Applying sentiment scores using TextBlob classifier")
            df1['sentiment'] = df1['reviewText'].progress_apply(self._prediction_textblob)



        else:
                tqdm.pandas(desc="Applying sentiment scores using Vader classifier")

                df1['sentiment']=df1['reviewText'].progress_apply(self._prediction_vader)

        fig1 = go.Figure(data=[go.Pie(labels=['positive', 'negative'],name="overall sentiments", values=df1['sentiment'].value_counts())],layout=go.Layout(
        title=go.layout.Title(text="Overall Sentiment Analysis")
    ))

        fig1.update_traces(marker=dict(colors=px.colors.sequential.Agsunset , line=dict(color='#000000', width=2)))

        if self.date_column != None:
            try:

                df_week = df1.groupby([pd.Grouper(key=str(self.date_column), freq='W'), 'sentiment']).size().unstack()
                data_week = pd.DataFrame(
                    {'date': (df_week.index), 'negative': (df_week[0].values), 'positive': (df_week[1].values)})

                df_month = df1.groupby([pd.Grouper(key=str(self.date_column), freq='M'), 'sentiment']).size().unstack()
                data_month = pd.DataFrame(
                    {'date': (df_month.index), 'negative': (df_month[0].values), 'positive': (df_month[1].values)})

                weekly_plot_negative=go.Scatter(x=data_week['date'], y=data_week['negative'],
                                         mode='lines+markers',
                                         name='number of Negative reviews per week')
                weekly_plot_positive=go.Scatter(x=data_week['date'], y=data_week['positive'],
                                         mode='lines+markers',
                                         name='number of Positive reviews per week')
                data_week=[weekly_plot_negative,weekly_plot_positive]

                layout_month={

                    'xaxis':dict(
                        tickformat="%Y-%B",
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),
                    ),
                    'yaxis':dict(
                        showgrid=False,
                        zeroline=False,
                        showline=False
                    ),
                    'title':dict(text="Monthly sentiment analysis"),

                    'xaxis_title' : dict(text='Year-Month'),
                    'yaxis_title' :dict(text='Number of reviews'),
                    'autosize':True,
                    'margin':dict(
                        autoexpand=False,
                        l=100,
                        r=20,
                        t=110,
                    )}
                layout_week = {
                    'xaxis': dict(
                        tickformat="%Y-%B-%w",
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),
                    ),
                    'yaxis': dict(
                        showgrid=False,
                        zeroline=False,
                        showline=False
                    ),
                    'autosize': True,
                    'title': dict(text="Monthly sentiment analysis"),

                    'xaxis_title' : dict(text='Year-Month-week'),
                    'yaxis_title' :dict(text='Number of reviews'),
                    'margin': dict(
                        autoexpand=False,
                        l=100,
                        r=20,
                        t=110,
                    )}

                fig2 = go.Figure(data=data_week,layout=layout_week)

                monthly_plot_negative= go.Scatter(x=data_month['date'], y=data_month['negative'],
                                  mode='lines+markers',
                                  name='number of Negative reviews per week')
                monthly_plot_positive = go.Scatter(x=data_month['date'], y=data_month['positive'],
                                   mode='lines+markers',
                                   name='number of Positive reviews per week')
                data_month = [monthly_plot_negative, monthly_plot_positive]
                fig3 = go.Figure(data=data_month, layout=layout_month)
                self.figures_to_html([fig1, fig2, fig3,self.fig_aspect])

            except:
                    print('Date column is invalid')

        else:

                    self.figures_to_html([fig1,self.fig_aspect])

    @staticmethod
    def figures_to_html(figs, filename="dashboard.html"):
            dashboard = open(filename, 'w')
            dashboard.write("<html><head></head><body>" + "\n")
            for fig in figs:

                inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
                dashboard.write(inner_html)
            dashboard.write("</body></html>" + "\n")







