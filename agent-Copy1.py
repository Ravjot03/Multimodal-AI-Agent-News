import requests
from newsapi import NewsApiClient
import openai
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize NewsAPI
news_api_key = 'my_news_api'
newsapi = NewsApiClient(api_key=news_api_key)

# Initialize OpenAI API for summarization (if needed)
openai.api_key = 'my_openai_api'

# Initialize Sentiment Analysis model
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


# Function to fetch news based on user interest
def fetch_news(query):
    api_key = news_api_key
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    articles = news_data['articles']
    return articles



# Function to summarize articles using OpenAI
def summarize_article(article_text):
    """
    Summarizes the content using OpenAI GPT-3 (with updated API).
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can replace this with the desired model version
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Summarize the following article:\n{article_text}"}],
        max_tokens=100  # You can adjust this based on your needs
    )
    return response['choices'][0]['message']['content'].strip()

# Function to perform sentiment analysis on an article
def analyze_sentiment(article_text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(article_text)
    return sentiment_score

# Function to curate news based on user interests
def generate_personalized_news(user_interests):
    all_curated_content = []
    
    for interest in user_interests:
        print(f"Fetching news for: {interest}")
        articles = fetch_news(interest)
        
        for article in articles:
            article_text = article['description'] if article['description'] else article['content']
            if article_text:
                summary = summarize_article(article_text)
                sentiment = analyze_sentiment(article_text)
                
                curated_content = {
                    'title': article['title'],
                    'summary': summary,
                    'sentiment': sentiment,
                    'source': article['source']['name'],
                    'url': article['url']
                }
                all_curated_content.append(curated_content)
    
    return all_curated_content

# Function to display the curated personalized content
def display_personalized_content(user_interests):
    curated_content = generate_personalized_news(user_interests)
    
    for content in curated_content:
        print(f"Title: {content['title']}")
        print(f"Summary: {content['summary']}")
        print(f"Sentiment: {content['sentiment']}")
        print(f"Source: {content['source']}")
        print(f"URL: {content['url']}")
        print("-" * 80)

# Example usage
if __name__ == "__main__":
    user_interests = ['Machine Learning', 'Artificial Intelligence', 'Data Science']
    display_personalized_content(user_interests)