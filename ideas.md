# Trending Basketball Players Dashboard

### What is it?

- Take data from reddit on ~~NBA players or teams~~ premier league teams, updates every 5 minutes.
    - ~~Look for keywords in basketball or NBA related tweets~~ Keywords are the team names
    - Possibly integrate streaming? Build up data up to 5 mins then conduct the preprocessing?
- Keep track of daily data, store daily data in an S3 / GCS bucket. Animate throughout the day.


Links:
- https://www.youtube.com/watch?v=VZ_tS4F6P2A&ab_channel=M%C4%B1sraTurp (streamlit project circle visualization)
- https://plotly.com/python/animations/ (animation plotly express)
- https://betterdatascience.com/apache-airflow-run-tasks-in-parallel/

![image.png](https://preview.redd.it/se4waupjbv091.png?width=1280&format=png&auto=webp&s=82b6210b45e50c48b56e7c9233decd4f2b8aa812)


- airflow (upload to gcs, gcs to bigquery)
- dbt process bigquery table and get final format
- final script takes data from bigquery and produces visualization

- Visualization:

1. Heatmap of the most active times of day for NBA-related posts on Reddit. This could show the days of the week on one axis and the time of day on the other, with darker colors indicating higher activity levels. To make it interactive, users could hover over specific squares to see the number of posts during that time period.
Features needed: 'created_utc', 'subreddit'

Bar chart of the top NBA teams or players mentioned on Reddit over a given time period. This could be a stacked bar chart showing the number of mentions for each team or player. Users could click on each bar to see specific posts related to that team or player.
Features needed: 'title', 'subreddit', 'created_utc'

Word cloud of the most frequently used words in NBA-related posts on Reddit. This could be an animated word cloud that updates in real-time as new posts are added. Users could hover over specific words to see the number of times they have been used.
Features needed: 'title', 'subreddit'

Map of the locations of NBA-related posts on Reddit. This could be a world map showing the number of posts from different countries or cities. Users could zoom in on specific regions to see more detailed information about the posts from that area.
Features needed: 'title', 'subreddit', 'author_flair_text'

Time series line chart of the number of NBA-related posts on Reddit over a given time period. This could show the daily or hourly frequency of posts, with the ability to toggle between different time periods (e.g., week, month, year).
Features needed: 'created_utc', 'subreddit'

Bubble chart of the most popular NBA-related topics on Reddit. This could show the number of posts related to each topic as well as the sentiment (positive, neutral, or negative) associated with those posts. Users could hover over specific bubbles to see the specific posts related to that topic.
Features needed: 'title', 'subreddit', 'selftext'

7. Sankey diagram of the most common paths of user engagement within NBA-related posts on Reddit. This could show the flow of users from one post to another, with the thickness of the lines indicating the number of users. Users could click on specific nodes to see more detailed information about that post. 

Features needed: 'id', 'title', 'subreddit', 'permalink'

8. Scatter plot of the relationship between the sentiment of NBA-related posts on Reddit and the number of comments. This could show the sentiment of each post on one axis and the number of comments on the other, with the ability to filter by specific teams or players. Users could hover over specific points to see the title and subreddit of the associated post. 

Features needed: 'title', 'subreddit', 'selftext', 'num_comments'

9. Network graph of the most commonly co-occurring words in NBA-related posts on Reddit. This could show the words as nodes with the edges indicating co-occurrence. Users could hover over specific nodes to see the number of times that word has been used. 

Features needed: 'title', 'subreddit'

10. Streamgraph of the most active NBA-related subreddits over a given time period. This could show the daily or hourly activity levels of each subreddit, with the ability to toggle between different time periods. Users could hover over specific subreddits to see more detailed information about their activity levels. 

Features needed: 'created_utc', 'subreddit', 'subreddit_name_prefixed'



Processing textual data and creating meaningful visualizations can be a challenging task, but here are 10 ideas and their possible implementations that can help you get started:

1. Word Clouds: A word cloud is a visual representation of the most frequent words in your data. You can create a word cloud for each NBA team subreddit to see which words are most commonly used. Python libraries like WordCloud and matplotlib can be used to create word clouds.

2. Sentiment Analysis: You can use sentiment analysis to identify the sentiment of each comment and see if it's positive, negative, or neutral. This can help you understand the overall sentiment of the NBA fans towards each team. Python libraries like TextBlob and NLTK can be used for sentiment analysis.

3. Topic Modeling: Topic modeling is a technique that can be used to identify the most common topics in your data. You can use topic modeling to identify the most common topics discussed in each NBA team subreddit. Python libraries like gensim and pyLDAvis can be used for topic modeling.

4. Word Frequencies: You can create bar graphs to show the frequency of the most common words used in each NBA team subreddit. Python libraries like pandas and matplotlib can be used to create bar graphs.

5. Named Entity Recognition: Named Entity Recognition is a technique that can be used to identify the named entities in your data, such as the names of NBA players, coaches, and teams. Python libraries like spaCy and NLTK can be used for Named Entity Recognition.

6. Emotion Analysis: Emotion analysis is a technique that can be used to identify the emotions expressed in each comment, such as joy, anger, and sadness. You can use emotion analysis to see which emotions are most commonly expressed in each NBA team subreddit. Python libraries like TextBlob and NLTK can be used for emotion analysis.

7. Word Associations: You can create a network graph to show the relationships between the most common words used in each NBA team subreddit. Python libraries like NetworkX and matplotlib can be used to create network graphs.

8. Word2Vec: Word2Vec is a technique that can be used to identify the most similar words to a given word. You can use Word2Vec to identify the most similar words to the names of NBA players, coaches, and teams. Python libraries like gensim can be used for Word2Vec.

9. Bigrams and Trigrams: Bigrams and Trigrams are pairs and triplets of words that frequently occur together in your data. You can use Bigrams and Trigrams to identify the most common phrases used in each NBA team subreddit. Python libraries like NLTK can be used for Bigrams and Trigrams.

10. Word Embeddings: Word Embeddings are a technique that can be used to represent words as vectors in a high-dimensional space. You can use Word Embeddings to identify the similarities and differences between the most common words used in each NBA team subreddit. Python libraries like gensim can be used for Word Embeddings.

These are just a few ideas to get you started, but there are many other techniques and visualizations that can be used to analyze and visualize textual data. The specific techniques and visualizations that you choose will depend on your research questions and the specific characteristics of your data.