# WHAT DOES IT DO?
1. Extracts Tweets/Hashtags by a filter keyword and saves them into a local CSV file
2. Visualizes the Tweets/Hashtags from the local CSV file
- Plots the Frequency of Hashtags
- Shows the latest Tweet processed
- Allows for searching of Tweet by index with simple Sentiment output & Information Extraction Output
<img width="812" alt="viz" src="https://user-images.githubusercontent.com/31118924/111952455-258acd80-8b20-11eb-81b1-0831f103c5e8.png">
<img width="812" alt="senti_ie_output" src="https://user-images.githubusercontent.com/31118924/111952475-2e7b9f00-8b20-11eb-8a36-bf194f135e65.png">



# HOW TO RUN:  
$ git clone git@github.com:davidygp/twitter_live_stream.git  
$ cd ./twitter_live_stream  
$ pip install -r requirements.txt  
$ bash run.sh  
(If you have no bash, sh works too, else do `python run_collector.py` and `python run_visualization.py`)  
$ (Open "localhost:8050" or "127.0.0.1:8050/"  on your browser)  

NOTE: config.json is kept secret to prevent misuse.
