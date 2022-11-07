# Natural language processing of customer reviews

This project aims to predict the star rating through text ratings from Thomann customers. A training dataset is generated based on web scraping techniques. The data was used to create a model that can predict an associated star rating for each text rating in the range of 1 to 5. As a result, it was found that prediction of stars by text ratings is well possible.

{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 0. Imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import re\n",
    "import time\n",
    "import random\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Web Scraping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_thomann_review_page(product: str, page=1, rating=0, order=0, reviewlang=1) -> requests.Response:\n",
    "    print(f\"Reading page {page} for product {product}...\")\n",
    "    return requests.get(f'https://www.thomann.de/de/{product}_reviews.htm?page={page}&order={order}&rating={rating}&reviewlang%5B%5D={reviewlang}')\n",
    "\n",
    "def get_thomann_review_page_soup(product: str, page=1, rating=0, order=0, reviewlang=1) -> BeautifulSoup:\n",
    "    web_page = get_thomann_review_page(product, page=page, rating=rating, order=order, reviewlang=reviewlang)\n",
    "    return BeautifulSoup(web_page.text, 'html.parser')\n",
    "\n",
    "def get_thomann_review_page_text(product: str, page=1, rating=0, order=0, reviewlang=1, class_filter=\".rs-prod.review\"):\n",
    "    soup = get_thomann_review_page_soup(product, page=page, rating=rating, order=order, reviewlang=reviewlang)\n",
    "\n",
    "    return soup.select(class_filter)\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_all_pages_for_thomann_review(product: str, start_page=1, rating=0, order=0, reviewlang=1, class_filter=\".rs-prod.review\"):\n",
    "    pages = []\n",
    "\n",
    "    current_page = start_page\n",
    "    texts = get_thomann_review_page_text(product, page=current_page, rating=rating, order=order, reviewlang=reviewlang, class_filter=class_filter)\n",
    "\n",
    "    while len(texts) > 0:\n",
    "        pages.extend(texts)\n",
    "        current_page += 1\n",
    "        sleep_time = random.choice([x * 0.1 for x in range(0, 20)])\n",
    "        print(f'Sleeping for {sleep_time} seconds...')\n",
    "        time.sleep(sleep_time)\n",
    "        texts = get_thomann_review_page_text(product, page=current_page, rating=rating, order=order, reviewlang=reviewlang, class_filter=class_filter)\n",
    "    \n",
    "    return pages\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def strip_reviews(reviews: list):\n",
    "    return [x.text.strip() for x in reviews]\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Add functionality for getting individual ratings\n",
    "def get_stars_from_review(review: str, css_selector=\".total-stars .overlay-wrapper\"):\n",
    "    soup = BeautifulSoup(str(review))\n",
    "    selector = soup.select(css_selector)\n",
    "    style = selector[0].get(\"style\")\n",
    "    percentage = float(re.search(r\"(\\d+(\\.\\d+)?)\", style).group(1))\n",
    "    return int(5 * (percentage / 100))\n",
    "\n",
    "def get_text_from_review(review: str, css_selector=\".inner.js-text-original\"):\n",
    "    soup = BeautifulSoup(str(review))\n",
    "    selector = soup.select(css_selector)\n",
    "    return selector[0].text.strip()\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_review_data(product_name: str) -> list:\n",
    "    raw_reviews = get_all_pages_for_thomann_review(product_name)\n",
    "    stars = [get_stars_from_review(review) for review in raw_reviews]\n",
    "    text = [get_text_from_review(review) for review in raw_reviews]\n",
    "    product_name_list = [product_name for x in raw_reviews]\n",
    "    return list(zip(product_name_list, text, stars))\n",
    "\n",
    "def get_data_for_products(products: list) -> list:\n",
    "    data = []\n",
    "\n",
    "    for product in products:\n",
    "        data.extend(get_review_data(product))\n",
    "\n",
    "    return data\n",
    "\n",
    "def get_dataframe_for_products(products: list, column_names = ['product_name', 'text', 'stars']):\n",
    "    data = get_data_for_products(products)\n",
    "    return pd.DataFrame(data, columns=column_names)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Reading page 1 for product sennheiser_hd_25...\n",
      "Sleeping for 0.9 seconds...\n",
      "Reading page 2 for product sennheiser_hd_25...\n",
      "Sleeping for 0.8 seconds...\n",
      "Reading page 3 for product sennheiser_hd_25...\n",
      "Sleeping for 0.1 seconds...\n",
      "Reading page 4 for product sennheiser_hd_25...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 5 for product sennheiser_hd_25...\n",
      "Sleeping for 0.0 seconds...\n",
      "Reading page 6 for product sennheiser_hd_25...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 7 for product sennheiser_hd_25...\n",
      "Reading page 1 for product thomann_ctg10...\n",
      "Sleeping for 0.0 seconds...\n",
      "Reading page 2 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 3 for product thomann_ctg10...\n",
      "Sleeping for 1.8 seconds...\n",
      "Reading page 4 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 5 for product thomann_ctg10...\n",
      "Sleeping for 1.5 seconds...\n",
      "Reading page 6 for product thomann_ctg10...\n",
      "Sleeping for 0.0 seconds...\n",
      "Reading page 7 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 8 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 9 for product thomann_ctg10...\n",
      "Sleeping for 1.6 seconds...\n",
      "Reading page 10 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 11 for product thomann_ctg10...\n",
      "Sleeping for 0.4 seconds...\n",
      "Reading page 12 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 13 for product thomann_ctg10...\n",
      "Sleeping for 0.0 seconds...\n",
      "Reading page 14 for product thomann_ctg10...\n",
      "Sleeping for 1.9000000000000001 seconds...\n",
      "Reading page 15 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 16 for product thomann_ctg10...\n",
      "Sleeping for 0.7000000000000001 seconds...\n",
      "Reading page 17 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 18 for product thomann_ctg10...\n",
      "Sleeping for 1.7000000000000002 seconds...\n",
      "Reading page 19 for product thomann_ctg10...\n",
      "Sleeping for 0.8 seconds...\n",
      "Reading page 20 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 21 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 22 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 23 for product thomann_ctg10...\n",
      "Sleeping for 1.5 seconds...\n",
      "Reading page 24 for product thomann_ctg10...\n",
      "Sleeping for 1.2000000000000002 seconds...\n",
      "Reading page 25 for product thomann_ctg10...\n",
      "Sleeping for 0.1 seconds...\n",
      "Reading page 26 for product thomann_ctg10...\n",
      "Sleeping for 1.6 seconds...\n",
      "Reading page 27 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 28 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 29 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 30 for product thomann_ctg10...\n",
      "Sleeping for 1.9000000000000001 seconds...\n",
      "Reading page 31 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 32 for product thomann_ctg10...\n",
      "Sleeping for 1.5 seconds...\n",
      "Reading page 33 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 34 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 35 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 36 for product thomann_ctg10...\n",
      "Sleeping for 0.4 seconds...\n",
      "Reading page 37 for product thomann_ctg10...\n",
      "Sleeping for 0.6000000000000001 seconds...\n",
      "Reading page 38 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 39 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 40 for product thomann_ctg10...\n",
      "Sleeping for 1.5 seconds...\n",
      "Reading page 41 for product thomann_ctg10...\n",
      "Sleeping for 1.6 seconds...\n",
      "Reading page 42 for product thomann_ctg10...\n",
      "Sleeping for 1.3 seconds...\n",
      "Reading page 43 for product thomann_ctg10...\n",
      "Sleeping for 1.0 seconds...\n",
      "Reading page 44 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 45 for product thomann_ctg10...\n",
      "Sleeping for 0.9 seconds...\n",
      "Reading page 46 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 47 for product thomann_ctg10...\n",
      "Sleeping for 0.6000000000000001 seconds...\n",
      "Reading page 48 for product thomann_ctg10...\n",
      "Sleeping for 1.9000000000000001 seconds...\n",
      "Reading page 49 for product thomann_ctg10...\n",
      "Sleeping for 0.8 seconds...\n",
      "Reading page 50 for product thomann_ctg10...\n",
      "Sleeping for 0.5 seconds...\n",
      "Reading page 51 for product thomann_ctg10...\n",
      "Sleeping for 1.6 seconds...\n",
      "Reading page 52 for product thomann_ctg10...\n",
      "Sleeping for 1.2000000000000002 seconds...\n",
      "Reading page 53 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 54 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 55 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 56 for product thomann_ctg10...\n",
      "Sleeping for 1.2000000000000002 seconds...\n",
      "Reading page 57 for product thomann_ctg10...\n",
      "Sleeping for 0.4 seconds...\n",
      "Reading page 58 for product thomann_ctg10...\n",
      "Sleeping for 1.5 seconds...\n",
      "Reading page 59 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 60 for product thomann_ctg10...\n",
      "Sleeping for 0.9 seconds...\n",
      "Reading page 61 for product thomann_ctg10...\n",
      "Sleeping for 0.4 seconds...\n",
      "Reading page 62 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 63 for product thomann_ctg10...\n",
      "Sleeping for 0.5 seconds...\n",
      "Reading page 64 for product thomann_ctg10...\n",
      "Sleeping for 1.9000000000000001 seconds...\n",
      "Reading page 65 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 66 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 67 for product thomann_ctg10...\n",
      "Sleeping for 0.6000000000000001 seconds...\n",
      "Reading page 68 for product thomann_ctg10...\n",
      "Sleeping for 1.7000000000000002 seconds...\n",
      "Reading page 69 for product thomann_ctg10...\n",
      "Sleeping for 1.4000000000000001 seconds...\n",
      "Reading page 70 for product thomann_ctg10...\n",
      "Sleeping for 0.9 seconds...\n",
      "Reading page 71 for product thomann_ctg10...\n",
      "Sleeping for 1.0 seconds...\n",
      "Reading page 72 for product thomann_ctg10...\n",
      "Sleeping for 0.2 seconds...\n",
      "Reading page 73 for product thomann_ctg10...\n",
      "Sleeping for 0.0 seconds...\n",
      "Reading page 74 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 75 for product thomann_ctg10...\n",
      "Sleeping for 1.2000000000000002 seconds...\n",
      "Reading page 76 for product thomann_ctg10...\n",
      "Sleeping for 0.7000000000000001 seconds...\n",
      "Reading page 77 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 78 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 79 for product thomann_ctg10...\n",
      "Sleeping for 0.7000000000000001 seconds...\n",
      "Reading page 80 for product thomann_ctg10...\n",
      "Sleeping for 0.6000000000000001 seconds...\n",
      "Reading page 81 for product thomann_ctg10...\n",
      "Sleeping for 1.1 seconds...\n",
      "Reading page 82 for product thomann_ctg10...\n",
      "Sleeping for 0.1 seconds...\n",
      "Reading page 83 for product thomann_ctg10...\n",
      "Sleeping for 0.1 seconds...\n",
      "Reading page 84 for product thomann_ctg10...\n",
      "Sleeping for 1.2000000000000002 seconds...\n",
      "Reading page 85 for product thomann_ctg10...\n",
      "Sleeping for 1.7000000000000002 seconds...\n",
      "Reading page 86 for product thomann_ctg10...\n",
      "Sleeping for 0.30000000000000004 seconds...\n",
      "Reading page 87 for product thomann_ctg10...\n",
      "Sleeping for 0.8 seconds...\n",
      "Reading page 88 for product thomann_ctg10...\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>product_name</th>\n",
       "      <th>text</th>\n",
       "      <th>stars</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>sennheiser_hd_25</td>\n",
       "      <td>Den HD-25 habe ich Anfang der 2000er Jahre ken...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>sennheiser_hd_25</td>\n",
       "      <td>Zum Kopfhörer selbst brauche ich wohl nichts m...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>sennheiser_hd_25</td>\n",
       "      <td>Ich brauchte einen DJ-Kopfhörer, der einen gee...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>sennheiser_hd_25</td>\n",
       "      <td>Einsatz: Ich arbeite als Tonmeister am Filmset...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>sennheiser_hd_25</td>\n",
       "      <td>Der HD-25 ist ein Hörer, den ich für bestimmte...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2297</th>\n",
       "      <td>thomann_ctg10</td>\n",
       "      <td>normalerweise tune ich mit meinem Iphone. Dies...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2298</th>\n",
       "      <td>thomann_ctg10</td>\n",
       "      <td>Für den Preis ein absoluter Ladenmitnehmer ;o)...</td>\n",
       "      <td>4</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2299</th>\n",
       "      <td>thomann_ctg10</td>\n",
       "      <td>tolles Gerät, sehr einfach zu bedienen, auch f...</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2300</th>\n",
       "      <td>thomann_ctg10</td>\n",
       "      <td>Stimmgerät funktioniert prima. Für den Preis i...</td>\n",
       "      <td>4</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2301</th>\n",
       "      <td>thomann_ctg10</td>\n",
       "      <td>Der Clip Tuner funktioniert bei der Gitarre se...</td>\n",
       "      <td>3</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2302 rows × 3 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "          product_name                                               text  \\\n",
       "0     sennheiser_hd_25  Den HD-25 habe ich Anfang der 2000er Jahre ken...   \n",
       "1     sennheiser_hd_25  Zum Kopfhörer selbst brauche ich wohl nichts m...   \n",
       "2     sennheiser_hd_25  Ich brauchte einen DJ-Kopfhörer, der einen gee...   \n",
       "3     sennheiser_hd_25  Einsatz: Ich arbeite als Tonmeister am Filmset...   \n",
       "4     sennheiser_hd_25  Der HD-25 ist ein Hörer, den ich für bestimmte...   \n",
       "...                ...                                                ...   \n",
       "2297     thomann_ctg10  normalerweise tune ich mit meinem Iphone. Dies...   \n",
       "2298     thomann_ctg10  Für den Preis ein absoluter Ladenmitnehmer ;o)...   \n",
       "2299     thomann_ctg10  tolles Gerät, sehr einfach zu bedienen, auch f...   \n",
       "2300     thomann_ctg10  Stimmgerät funktioniert prima. Für den Preis i...   \n",
       "2301     thomann_ctg10  Der Clip Tuner funktioniert bei der Gitarre se...   \n",
       "\n",
       "      stars  \n",
       "0         5  \n",
       "1         5  \n",
       "2         5  \n",
       "3         5  \n",
       "4         5  \n",
       "...     ...  \n",
       "2297      5  \n",
       "2298      4  \n",
       "2299      5  \n",
       "2300      4  \n",
       "2301      3  \n",
       "\n",
       "[2302 rows x 3 columns]"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "products = [\"sennheiser_hd_25\", \"thomann_ctg10\"]\n",
    "\n",
    "data = get_dataframe_for_products(products)\n",
    "data\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Natural Language Processing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from scipy import sparse\n",
    "\n",
    "from sklearn.pipeline import Pipeline, make_pipeline\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.base import BaseEstimator, ClassifierMixin\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.model_selection import cross_val_score\n",
    "from sklearn import metrics\n",
    "from sklearn.metrics import roc_auc_score\n",
    "\n",
    "from keras.preprocessing.text import Tokenizer\n",
    "from keras.preprocessing.sequence import pad_sequences\n",
    "from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, SpatialDropout1D, GRU\n",
    "from keras.layers import Bidirectional, GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate\n",
    "from keras.models import Model\n",
    "from keras import initializers, regularizers, constraints, optimizers, layers\n",
    "from keras.utils import to_categorical\n",
    "from keras.callbacks import EarlyStopping, ModelCheckpoint\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "data['stars'].hist(legend=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "number_of_rows = len(data.index)\n",
    "training_data_percentage = 0.8\n",
    "split_point = int(number_of_rows * training_data_percentage)\n",
    "\n",
    "rev_samp = data.sample(n = number_of_rows, random_state = 42)  # shuffle dataset\n",
    "train = rev_samp[0:split_point]\n",
    "test = rev_samp[split_point:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#train = pd.read_csv('/home/adam/R/Yelp/dataset/model_train.csv', usecols = ['text', 'stars'])\n",
    "train = train[['text', 'stars']]\n",
    "train['stars'].hist();train.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#train = pd.read_csv('/home/adam/R/Yelp/dataset/model_train.csv', usecols = ['text', 'stars'])\n",
    "test = test[['text', 'stars']]\n",
    "test['stars'].hist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "train = pd.get_dummies(train, columns = ['stars'])\n",
    "train.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "test = test[['text', 'stars']]\n",
    "test = pd.get_dummies(test, columns = ['stars'])\n",
    "train.shape, test.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Naive Bayes Linear Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# max_features is an upper bound on the number of words in the vocabulary\n",
    "max_features = 2000\n",
    "tfidf = TfidfVectorizer(max_features = max_features)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class NBFeatures(BaseEstimator):\n",
    "    '''Class implementation of Jeremy Howards NB Linear model'''\n",
    "    def __init__(self, alpha):\n",
    "        # Smoothing Parameter: always going to be one for my use\n",
    "        self.alpha = alpha\n",
    "        \n",
    "    def preprocess_x(self, x, r):\n",
    "        return x.multiply(r)\n",
    "    \n",
    "    # calculate probabilities\n",
    "    def pr(self, x, y_i, y):\n",
    "        p = x[y == y_i].sum(0)\n",
    "        return (p + self.alpha)/((y==y_i).sum()+self.alpha)\n",
    "    \n",
    "    # calculate the log ratio and represent as sparse matrix\n",
    "    # ie fit the nb model\n",
    "    def fit(self, x, y = None):\n",
    "        self._r = sparse.csr_matrix(np.log(self.pr(x, 1, y) /self.pr(x, 0, y)))\n",
    "        return self\n",
    "    \n",
    "    # apply the nb fit to original features x\n",
    "    def transform(self, x):\n",
    "        x_nb = self.preprocess_x(x, self._r)\n",
    "        return x_nb"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create pipeline using sklearn pipeline:\n",
    "    # I basically create my tfidf features which are fed to my NB model \n",
    "    # for probability calculations. Then those are fed as input to my \n",
    "    # logistic regression model.\n",
    "lr = LogisticRegression()\n",
    "nb = NBFeatures(1)\n",
    "p = Pipeline([\n",
    "    ('tfidf', tfidf),\n",
    "    ('nb', nb),\n",
    "    ('lr', lr)\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class_names = ['stars_1', 'stars_2', 'stars_3', 'stars_4', 'stars_5']\n",
    "scores = []\n",
    "preds = np.zeros((len(test), len(class_names)))\n",
    "for i, class_name in enumerate(class_names):\n",
    "    train_target = train[class_name]    \n",
    "    cv_score = np.mean(cross_val_score(estimator = p, X = train['text'].values, \n",
    "                                      y = train_target, cv = 3, scoring = 'accuracy'))\n",
    "    scores.append(cv_score)\n",
    "    print('CV score for class {} is {}'.format(class_name, cv_score))\n",
    "    p.fit(train['text'].values, train_target)\n",
    "    preds[:,i] = p.predict_proba(test['text'].values)[:,1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "t = metrics.classification_report(np.argmax(test[['stars_1', 'stars_2', 'stars_3', 'stars_4', 'stars_5']].values, axis = 1),np.argmax(preds, axis = 1))\n",
    "print(t)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3.9.4 64-bit",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.4"
  },
  "metadata": {
   "interpreter": {
    "hash": "065fbddbbd04e9cc2c204917ee0b59bd10217cd6f1a3c0be0571a3c1dddce48b"
   }
  },
  "orig_nbformat": 2,
  "vscode": {
   "interpreter": {
    "hash": "cdfc92692d6021c2c23fe081779710ba78c65081be41b6edd4e9dc4ff6b5838d"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
