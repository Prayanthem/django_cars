# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import datasets
import json
from sqlalchemy import create_engine
from index_prices_prohibitorum.settings import DATABASES
from .models import Car, Price
import statsmodels.api as sm
import plotly.graph_objects as go
from plotly.offline import plot
import re

''' TODO:
1. Use Dash to chart data
2. logtransform price (so it cannot go below 0)
3. Other stuff
'''

class MyAnalysis():
        def get_engine(self):
                db_creds = DATABASES['default']
                conn_url = 'postgresql://{}:{}@{}:{}/{}'.format(db_creds['USER'], db_creds['PASSWORD'], db_creds['HOST'], db_creds['PORT'], db_creds['NAME'])
                print(conn_url)
                return create_engine(conn_url)

        def get_dataframe(self, name):

                dicts = {}
                for i,car in enumerate(Car.objects.filter(name=name)):
                        print(i,car)
                        price = Price.objects.filter(car=car).latest('date')
                        car_dict = car.__dict__
                        car_dict['pris'] = price.price
                        dicts[i] = car_dict
                df = pd.DataFrame(dicts).T
                return df

        def get_dataframe_django(self, name):
                dicts = Car.objects.filter(name=name).values()
                price_l = []
                for car in Car.objects.filter(name=name):
                        prices = Price.objects.filter(car=car).latest('date')
                        price_l.append(prices.price)
                df = pd.DataFrame(dicts)
                df_prices = pd.DataFrame({'pris' : price_l})
                return pd.concat([df,df_prices], axis=1)

        def get_model(self, name):
                self.name = name
                self.df = self.get_dataframe_django(name)

                #if len(self.df.index) >= 30:
                f = "pris ~ Kmstand + Årsmodell + Effekt"
                model = sm.formula.ols(f, data=self.df, missing='drop').fit()
                return model

        def get_summary(self, model):
                summ = model.summary()
                return [summ.tables[0].as_html(), summ.tables[1].as_html(), summ.tables[2].as_html()]

        def get_equation(self, model):
                summ = model.summary()
                dicts = {}
                dicts["intercept"] = model.params[0]
                dicts["km"] = model.params[1]
                return dicts


        def find_underperformers(self, model):
                pass

        def graph_model(self, df, model):
                y = df['pris']
                x = df['Kmstand']

                raw_data = go.Scatter(x=x,
                                y=y,
                                mode='markers',
                                text='<a href="{}"></a>'.format(df['Finn_kode']),
                                name="Observations",
                                )
                prediction = go.Scatter(x=x,
                                y=model.predict(),
                                mode='lines',
                                name='Prediction',
                                )

                fig = go.Figure(data=[raw_data, prediction])
                
                fig.update_layout(
                        title='Cars',

                        )
                plot_div = plot(fig, output_type='div', include_plotlyjs=False) #https://github.com/ricleal/DjangoPlotLy
                return plot_div

        def graph_model_interactive(self, df, model): #https://community.plot.ly/t/hyperlink-to-markers-on-map/17858/6
                y = df['pris']
                x = df['Kmstand']
                links = df['Finn_kode']

                y_prediction = model.predict()
                predictions = model.get_prediction(df)
                alpha = 0.1
                frame = predictions.summary_frame(alpha=alpha) #https://stackoverflow.com/questions/17559408/confidence-and-prediction-intervals-with-statsmodels

                raw_data = go.Scatter(x=x,
                                y=y,
                                mode='markers',
                                text=df['header'],
                                name="Observations",
                                customdata=links,
                                )
                prediction = go.Scatter(x=x,
                                y=y_prediction,
                                mode='lines',
                                name='Prediction',
                                hoverinfo='skip', #doesn't display anything on hover
                                )
                ci_lower = go.Scatter(x=x,
                                y=frame.obs_ci_lower,
                                mode='lines',
                                name='CI Lower',
                                hoverinfo='skip',
                                opacity=0.4,
                                )
                ci_upper = go.Scatter(x=x,
                                y=frame.obs_ci_upper,
                                mode='lines',
                                name='CI Upper',
                                hoverinfo='skip',
                                opacity=0.4,
                                )
                pi_lower = go.Scatter(x=x,
                                y=frame.mean_ci_lower,
                                mode='lines',
                                name='Prediction Lower Interval',
                                hoverinfo='skip',
                                opacity=0.2,
                                )
                pi_upper = go.Scatter(x=x,
                                y=frame.mean_ci_upper,
                                mode='lines',
                                name='Prediction Upper Interval',
                                hoverinfo='skip',
                                opacity=0.2,
                                )

                # Build layout
                layout = go.Layout(
                hovermode='closest',
                height=800,
                title="Alpha {}".format(alpha),
                )

                # Build Figure
                fig = go.Figure(
                data=[raw_data, prediction, ci_lower, ci_upper, pi_lower, pi_upper],
                layout=layout,
                )
                
                # Get HTML representation of plotly.js and this figure
                plot_div = plot(fig, output_type='div', include_plotlyjs=True)

                # Get id of html div element that looks like
                # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
                res = re.search('<div id="([^"]*)"', plot_div)
                div_id = res.groups()[0]

                # Build JavaScript callback for handling clicks
                # and opening the URL in the trace's customdata 
                js_callback = """
                <script>
                var plot_element = document.getElementById("{div_id}");
                plot_element.on('plotly_click', function(data){{
                console.log(data);
                let point = data.points[0];
                if (point) {{
                        var link = `https://www.finn.no/car/used/ad.html?finnkode=${{point.customdata}}`;
                        window.open(link);
                }}
                }})
                </script>
                """.format(div_id=div_id)

                # Build HTML string
                html_str = """
                {plot_div}
                {js_callback}
                """.format(plot_div=plot_div, js_callback=js_callback)

                return html_str