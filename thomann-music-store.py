import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

# analyze thomann music store customer reviews
# 1. web scraping


def get_thomann_review_page(product: str, page=1, rating=0, order=0, reviewlang=1) -> requests.Response:
    return requests.get(f'https://www.thomann.de/de/{product}_reviews.htm?page={page}&order={order}&rating={rating}&reviewlang%5B%5D={reviewlang}')


def get_thomann_review_page_soup(product: str, page=1, rating=0, order=0, reviewlang=1) -> BeautifulSoup:
    web_page = get_thomann_review_page(
        product, page=page, rating=rating, order=order, reviewlang=reviewlang)
    return BeautifulSoup(web_page.text, 'html.parser')


def get_thomann_review_page_text(product: str, page=1, rating=0, order=0, reviewlang=1, class_filter=".rs-prod.review"):
    soup = get_thomann_review_page_soup(
        product, page=page, rating=rating, order=order, reviewlang=reviewlang)

    return soup.select(class_filter)


def get_all_pages_for_thomann_review(product: str, start_page=1, rating=0, order=0, reviewlang=1, class_filter=".rs-prod.review"):
    pages = []

    current_page = start_page
    texts = get_thomann_review_page_text(
        product, page=current_page, rating=rating, order=order, reviewlang=reviewlang, class_filter=class_filter)

    while len(texts) > 0:
        pages.extend(texts)
        current_page += 1
        texts = get_thomann_review_page_text(
            product, page=current_page, rating=rating, order=order, reviewlang=reviewlang, class_filter=class_filter)

    return pages


def strip_reviews(reviews: list):
    return [x.text.strip() for x in reviews]


def get_stars_from_review(review: str, css_selector=".total-stars .overlay-wrapper"):
    # TODO: Add functionality for getting individual ratings
    soup = BeautifulSoup(str(review))
    selector = soup.select(css_selector)
    style = selector[0].get("style")
    percentage = float(re.search(r"(\d+(\.\d+)?)", style).group(1))
    return 5 * (percentage / 100)


def get_text_from_review(review: str, css_selector=".inner.js-replace-text"):
    soup = BeautifulSoup(str(review))
    selector = soup.select(css_selector)
    return selector[0].text.strip()


def get_review_data(product_name: str) -> list:
    raw_reviews = get_all_pages_for_thomann_review(product_name)
    stars = [get_stars_from_review(review) for review in raw_reviews]
    text = [get_text_from_review(review) for review in raw_reviews]
    product_name_list = [product_name for x in raw_reviews]
    return list(zip(product_name_list, text, stars))


def get_data_for_products(products: list) -> list:
    data = []

    for product in products:
        data.extend(get_review_data(product))

    return data


def get_dataframe_for_products(products: list, column_names=['product_name', 'review_text', 'stars']):
    data = get_data_for_products(products)
    return pd.DataFrame(data, columns=column_names)


products = ["sennheiser_hd_25", "gravity_ksx_2_rd",
            "istanbul_agop_13_xist_dry_dark_crash"]

get_dataframe_for_products(products)


# 2. text analysis (NLP)
