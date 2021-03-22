from allennlp.predictors.predictor import Predictor
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import json
import pandas as pd
import plotly

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div(
        [
            html.I(
                "Welcome to this simple visualization of Tweets from the Twitter API"
            ),
            html.Hr(),

            html.Br()
            html.Div(id="latest_processed_tweet"),
            html.Hr(),

            html.Br()
            dcc.Graph(id="live-update-graph-bar"),
            dcc.Interval(id="interval-component", interval=1 * 1000),
            html.Hr(),

            html.I("Input an index of tweets to select:  "),
            dcc.Input(
                id="tweet_index",
                type="text",
                placeholder="Select Tweet Index of saved database to Analyse",
            ),
            html.Div(id="index_info"),
            html.Div(id="tweet_info"),
            html.Br(),
            html.Div(id="senti_output"),
            html.Br(),
            html.Div(id="ie_output"),
        ]
    )
)


@app.callback(
    Output("latest_processed_tweet", "children"),
    Input("interval-component", "n_intervals"),
)
def update_latest_processed_tweet(n):
    """Extracts the latest processed tweet from tweets_file.
    Input: 
        n, int: A counter to activate callback
    Output:
        latest_processed_tweet, str: The latest processed tweet
    """
    tweets_pdf = pd.read_csv(tweets_file, header=0)
    latest_tweet = tweets_pdf.loc[tweets_pdf.shape[0] - 1]["tweet"]
    return "Latest Processed Tweet:\n{}".format(latest_tweet)


@app.callback(
    Output("live-update-graph-bar", "figure"),
    Input("interval-component", "n_intervals"),
)
def update_graph_bar(n):
    """Extracts the hashtags from hashtags_file for plotting.
    Input:
        n, int: A counter to activate callback
    Output:
        dict, dict: The plotly data(traces) and layout to be rendered by dash.
    """
    hashtags_pdf = pd.read_csv(hashtags_file, header=0)
    sorted_hashtags_pdf = hashtags_pdf.sort_values("count")
    hashtags = sorted_hashtags_pdf["hashtag"].tolist()
    count = sorted_hashtags_pdf["count"].tolist()
    traces = [plotly.graph_objs.Bar(y=hashtags, x=count, orientation="h")]
    layout = plotly.graph_objs.Layout(title="Count of Hashtags from Tweets")
    return {"data": traces, "layout": layout}


@app.callback(
    Output("index_info", "children"),
    Output("tweet_info", "children"),
    Output("senti_output", "children"),
    Output("ie_output", "children"),
    Input("tweet_index", "value"),
)
def update_tweet_info(tweet_index):
    """To update the tweet to show based on the index.
    Input: 
        tweet_index, index of tweet from tweets_file (input by user)
    Output:
        index_info, str: the index chosen by user or the last index
        tweet_info, str: the selected tweet from tweets_file
        senti_output, str: the Sentiment Analysis output (positive/negative)
        ie_output, str: the Information Analysis output
    """
    tweets_pdf = pd.read_csv(tweets_file, header=0)
    max_index = tweets_pdf.shape[0] - 1
    tweet_idx = (
        max_index
        if tweet_index is None or len(tweet_index) == 0
        else int(tweet_index)
    )
    selected_tweet = tweets_pdf.iloc[tweet_idx]["tweet"]

    senti_pred = senti_predictor.predict(selected_tweet)
    ie_pred = ie_predictor.predict(selected_tweet)

    index_info = "Selected Tweet Index: %s of %s" % (tweet_idx, max_index)
    tweet_info = "Selected Tweet is: %s" % (selected_tweet)
    senti_output = "Sentiment is %s" % (
        "negative" if senti_pred["label"] == "0" else "positive"
    )
    ie_output1 = "      ".join(
        [
            "For verb %s, %s" % (v["verb"], v["description"])
            for v in ie_pred["verbs"]
        ]
    )
    ie_output = "Information Extraction Output is: %s" % (ie_output1)

    return index_info, tweet_info, senti_output, ie_output


if __name__ == "__main__":
    """#For easier debugging
    ie_model_file = "./models/openie-model.2020.03.26.tar.gz"
    senti_model_file = "./models/basic_stanford_sentiment_treebank-2020.06.09.tar.gz"
    hashtags_file = "./data/hashtags.csv"
    tweets_file = "./data/tweets.csv"
    """

    # Extract the configuration parameters from the config file
    config_file = "./config.json"
    with open(config_file, "r") as jsonfile:
        cfg = json.load(jsonfile)

    hashtags_file = cfg["hashtags_file"]
    tweets_file = cfg["tweets_file"]

    ie_model_file = cfg["ie_model_file"]
    senti_model_file = cfg["senti_model_file"]

    ie_predictor = Predictor.from_path(ie_model_file)
    senti_predictor = Predictor.from_path(senti_model_file)
    app.run_server(debug=True)
