# trendba

![image](https://github.com/garrethlee/trendba/assets/65230912/a28b3e82-215c-4093-a877-e0613cb65328)

trendba is a project that collects the data from NBA subreddits and visualizes it in a web app. 

**Check it out here:** 
➡️ http://trendba.us-west-2.elasticbeanstalk.com/ 

## Inspiration

I like the NBA. I like browsing Reddit. I like data.

## Overview

The goal of this project is to answer some interesting questions about the NBA subreddits, while employing recently learned knowledge on data engineering tools, such as Airflow and DBT (which I sadly didn't get to use in this project). I wanted to specifically focus on visualizing the sentiment and topics of discussion in various NBA-related subreddits, and I found some pretty interesting stuff in the process. The visualization attempts to answer these questions:

- Which subreddits are the most active and popular?
- How do the subreddits compare in terms of sentiment (positive or negative)?
- What are the most common words and topics discussed in each subreddit?

## Data

The data consists of posts and comments from 31 NBA subreddits (one for each team and one for r/nba). The data is collected hourly and the visualizations in the web app resets every day.

I used Airflow (hosted on a Google Compute instance) to orchestrate a data workflow that collected subrredit data from the Reddit API (using PRAW) and pushed the data to a data lake (Google Cloud Storage). From this, the data is transferred to a data warehouse (Google BigQuery). Because most of the data was already in the form that I wanted, I didn't need to transform it further. Lastly, a plotly Dash webapp (configured as an Amazon Elastic Beanstalk application) collects the data from the data warehouse and visualizes it.

In the visualizations, specifically, for the topic modelling portion, I utilized Latent Dirichlet Allocation to find the top 5 topics in each subreddit. Using t-distributed stochastic neighbor embedding (t-SNE), I reduced the dimensionality of the data to 2 components, which makes visualizing it as a scatter plot easier (both methods have its sklearn wrappers, which was nice).

## Guess the subreddit!

Based on the wordclouds, can you guess which team this subreddit belongs to?

### Easy
![image](https://github.com/garrethlee/trendba/assets/65230912/1a4ef84a-ac4b-40b9-8e00-6734cefb0d3f)
## Hard
![image](https://github.com/garrethlee/trendba/assets/65230912/941e69a9-e515-4928-884a-53b7505d03f5)

## Conclusion

trendba is a project that demonstrates how data science can be used to gain insights into online communities and their behaviors. The project shows that NBA subreddits are diverse and dynamic platforms that reflect the fans' opinions and emotions about their favorite teams and players. The project also shows that there are many interesting questions that can be answered using data analysis and visualization techniques.

## Future Work

Some possible directions for future work are:

- Expand the data set to include more subreddits (such as r/nbadiscussion), more time periods (such as previous seasons), or more features (such as awards or upvotes).
- Apply more advanced natural language processing techniques to extract more information from the text.
- Create interactive dashboards or web applications to display the results in a more user-friendly way.

