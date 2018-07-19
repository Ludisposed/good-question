import time
import string
from collections import Counter
import json

import requests
import nltk
from bs4 import BeautifulSoup, SoupStrainer


HEADERS = {'User-Agent': 'GoodQuestionBot -- https://github.com/Ludisposed/good-question'}
BASE_URL = 'https://codereview.stackexchange.com'
TRANS = str.maketrans('', '', string.punctuation)
STOPS = nltk.corpus.stopwords.words('english')

def get_new_questions(url):
    """yields new questions from the Code-Review questions page"""
    parsed = set()
    while True:
        data = requests.get(url, headers=HEADERS).text
        strainer = SoupStrainer(id="questions")
        soup = BeautifulSoup(data, "html.parser", parse_only=strainer)
        questions = soup.select(".question-hyperlink")
        for question in questions:
            text = question.text
            if not text in parsed:
                parsed.add(text)
                yield question.get("href")
        time.sleep(600)

def scrape_question(url):
    """Scrapes question, parse it and return"""
    data = requests.get(url, headers=HEADERS).text
    return parse_question(data)

def parse_question(data):
    """Returns the parsed question (votes, code, text, tags)"""
    strainer = SoupStrainer(class_="question")
    soup = BeautifulSoup(data, "html.parser", parse_only=strainer)
    votes = soup.select_one(".vote-count-post").text
    post = soup.select_one(".post-text")
    tags = soup.select_one(".post-taglist").text.split()
    code = None if post.code is None else post.code.text
    text = Counter(i for i in tokenize(post.text.replace(code, "")))
    return votes, code, text, tags

def scrape():
    """For each new question, it will scrape and parse the content"""
    for link in get_new_questions(f"{BASE_URL}/questions"):
        title = Counter(i for i in tokenize(link.split('/')[-1]))
        votes, code, text, tags = scrape_question(f"{BASE_URL}{link}")
        yield votes, code, text, tags, title

def tokenize(text):
    """Tokenizes the text"""
    text = text.translate(TRANS).lower()
    for word in nltk.tokenize.word_tokenize(text):
        if word not in STOPS:
            yield word

def save_database(title, votes, text, code, tags):
    """"Not Yet Implemented"""
    data = {"title": title, "votes": votes, "text": text, "code": code, "tags": tags}
    print(json.dumps(data))

if __name__ == '__main__':
    for votes, code , text, tags, title in scrape():
        save_database(title, votes, text, code, tags)
