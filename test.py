# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6
import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin

BASE_URL = "https://codereview.stackexchange.com/"

URL = "https://codereview.stackexchange.com/users/98493/graipher?tab=answers"

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
    next_page=page_soup.find('a', rel="next")
    if next_page is not None:
        return next_page["href"]
    return None

def parse_answer(path):
    strainer = SoupStrainer(id=f"answer-{path.split('#')[-1]}")
    print(f"answer-{path.split('#')[-1]}")
    soup = BeautifulSoup(parse_path(path), "html.parser", parse_only=strainer)
    print(soup.find(class_="post-text"))


if __name__ == "__main__":
    #print(next_page_link("/users/98493/graipher?tab=answers&sort=votes&page=14"))
    parse_answer("/questions/150378/get-array-slices-from-list-of-lengths/150380#150380")
    