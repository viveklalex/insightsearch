import tensorflow as tf
from transformers import InputExample, InputFeatures, BertConfig,BertTokenizer, TFBertForSequenceClassification
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from textblob import TextBlob

class Sentimentanalyze:
    def __init__(self,clean_df, column_name,date_column,bert):
        self.clean_df=clean_df
        self.column_name=column_name
        self.date_column=date_column
        self.bert=bert


    def _model_init(self):
        # bert_tokenizer

        # model configuration for bert-base-cased

        if not os.path.exists(str(Path(__file__).parent)+'/saved/config.json'):
            model_config = BertConfig.from_pretrained('bert-base-uncased')
            model_config.output_hidden_states = True
            model_config.save_pretrained(str(Path(__file__).parent)+'/saved')

        else:
            print('loading the saved model_config')
            model_config = BertConfig.from_pretrained(str(Path(__file__).parent)+'/saved')
            model_config.output_hidden_states = True

        if not os.path.exists(str(Path(__file__).parent)+'/saved/tf_model.h5'):
            # Path('./trained-weights').mkdir(parents=True, exist_ok=True)
            bert_model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
            bert_model.save_pretrained(str(Path(__file__).parent)+'/saved')
        else:
            print('loading the saved pretrained model')
            bert_model = TFBertForSequenceClassification.from_pretrained(str(Path(__file__).parent)+'/saved')


        bert_model.load_weights(str(Path(__file__).parent)+'/saved/sentiment.h5')

        return bert_model

    def _tokenizer_bert(self):
        if not os.path.exists(str(Path(__file__).parent)+'/saved/vocab.txt'):

            tz = BertTokenizer.from_pretrained("bert-base-uncased")
            tz.save_pretrained(str(Path(__file__).parent)+'/saved')


        else:
            print('loading the saved pretrained tokenizer')
            tz = BertTokenizer.from_pretrained(str(Path(__file__).parent)+'/saved')

        return tz

    def _tokenize_text(self, text, tz):

        encoded = tz.encode_plus(
            text=text,  # the sentence to be encoded
            add_special_tokens=True,  # Add [CLS] and [SEP]
            max_length=256,  # maximum length of a sentence
            pad_to_max_length=True,  # Add [PAD]s
            return_attention_mask=True,  # Generate the attention mask
            truncation=True,
            return_tensors='tf')

        return encoded

    # loading and saving tfbert
    @staticmethod
    def _prediction_textblob(text):
        return 0 if (TextBlob(text).sentiment.polarity < 0)else 1


    def _prediction_bert(self, input_sentences, model, tk):



        tf_outputs = model(tk)

        tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
        labels = ['Negative', 'Positive']
        label = tf.argmax(tf_predictions, axis=1)
        label = label.numpy()
        return int(label)

    def showing_sentiment(self):
        df1 = self.clean_df.copy()
        if self.bert == True:

                model = self._model_init()
                tz = self._tokenizer_bert()

                df1['sent_bert'] = df1['reviewText'].apply(lambda x: self._prediction_bert(x, model, self._tokenize_text(x, tz)))

        else:

                df1['sentiment']=df1['reviewText'].apply(self._prediction_textblob)

        fig1 = go.Figure(data=[go.Pie(labels=['positive', 'negative'],name="overall sentiments", values=df1['sentiment'].value_counts())],layout=go.Layout(
        title=go.layout.Title(text="Overall Sentiment Analysis")
    ))

        fig1.update_traces(marker=dict(colors=px.colors.sequential.Agsunset , line=dict(color='#000000', width=2)))

        if self.date_column is not None:
            try:
                df_week = df1.groupby([pd.Grouper(key='reviewTime', freq='W'), 'sentiment']).size().unstack()
                data_week = pd.DataFrame(
                    {'date': (df_week.index), 'negative': (df_week[0].values), 'positive': (df_week[1].values)})

                df_month = df1.groupby([pd.Grouper(key='reviewTime', freq='M'), 'sentiment']).size().unstack()
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
                fig3.show()
                self.figures_to_html([fig1, fig2, fig3,self.fig_aspect])

            except:
                    self.figures_to_html([fig1,self.fig_aspect])

    @staticmethod
    def figures_to_html(figs, filename="dashboard.html"):
            dashboard = open(filename, 'w')
            dashboard.write("<html><head></head><body>" + "\n")
            for fig in figs:

                inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
                dashboard.write(inner_html)
            dashboard.write("</body></html>" + "\n")







