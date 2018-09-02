# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6
import requests
from time import sleep
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin

from general import file_to_set, set_to_file, append_to_file



BASE_URL = "https://someweb.com/"

URL = "https://someweb.com/users/someone?tab=answers"

ANSWER_FILE="answer_path.txt"
QUESTION_FILE="questions.md"

def parse_path(path):
    return requests.get(urljoin(BASE_URL, path)).text 

def answer_links(path):
    strainer = SoupStrainer(class_="answer-link")
    soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=strainer)
    answers = soup.select(".answer-hyperlink")
    for answer in answers:
        yield answer["href"]

def next_page_link(path):
    strainer = SoupStrainer(class_="pager fr")
    soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=strainer)
    next_page=soup.find('a', rel="next")
    if next_page is not None:
        return next_page["href"]
    return None

def parse_answer(path):
    question_header_strainer = SoupStrainer(id="question-header")
    question_header_soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=question_header_strainer)
    question_header_text = question_header_soup.text.replace("\n","")

    question_strainer = SoupStrainer(class_="question")
    question_soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=question_strainer)
    question_text = question_soup.find(class_="post-text").prettify()

    answer_strainer = SoupStrainer(id=f"answer-{path.split('#')[-1]}")
    answer_soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=answer_strainer)
    answer_text = answer_soup.find(class_="post-text").prettify()
    append_to_file("<h3>" + question_header_text + "</h3>\n", QUESTION_FILE)
    append_to_file(question_text, QUESTION_FILE)
    append_to_file("\nANSWER:\n", QUESTION_FILE)
    append_to_file(answer_text, QUESTION_FILE)
    

def crawl_answer_link(url):
    while url is not None:
        answers = set()
        for path in answer_links(url):
            answers.add(path)
        set_to_file(answers, ANSWER_FILE)
        url = next_page_link(url)
        print(url)

def gather_answes():
    links = file_to_set(ANSWER_FILE)
    links = list(links)
    for i in range(len(links)):
        print(f"{i}...")
        sleep(5)
        parse_answer(links[i])


if __name__ == "__main__":
    # crawl_answer_link(URL)
    gather_answes()