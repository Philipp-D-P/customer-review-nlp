# analyze thomann music store customer reviews


# 1. web scraping

import requests
from bs4 import BeautifulSoup

# get html source code 
# multiple url (in total 5) of a specific product (in this example headphones)
web_page_1 = requests.get('https://www.thomann.de/de/sennheiser_hd_25_reviews.htm?ar=379291&page=1&order=0&rating=0&reviewlang%5B%5D=1')
web_page_2 = requests.get('https://www.thomann.de/de/sennheiser_hd_25_reviews.htm?ar=379291&page=2&order=0&rating=0&reviewlang%5B%5D=1')
web_page_3 = requests.get('https://www.thomann.de/de/sennheiser_hd_25_reviews.htm?ar=379291&page=3&order=0&rating=0&reviewlang%5B%5D=1')
web_page_4 = requests.get('https://www.thomann.de/de/sennheiser_hd_25_reviews.htm?ar=379291&page=4&order=0&rating=0&reviewlang%5B%5D=1')
web_page_5 = requests.get('https://www.thomann.de/de/sennheiser_hd_25_reviews.htm?ar=379291&page=5&order=0&rating=0&reviewlang%5B%5D=1')

soup_1 = BeautifulSoup(web_page_1.text, 'html.parser')
soup_2 = BeautifulSoup(web_page_2.text, 'html.parser')
soup_3 = BeautifulSoup(web_page_2.text, 'html.parser')
soup_4 = BeautifulSoup(web_page_2.text, 'html.parser')
soup_5 = BeautifulSoup(web_page_2.text, 'html.parser')

# Filter out text ratings on the first page
# Identify and reference the corresponding section in the html code
all_text_1 = soup_1.find_all("div", class_ = "inner js-replace-text")

print(all_text_1[0].text.strip())  # output the first rating on the first page "[0]"
print(all_text_1[1].text.strip())  # output second rating on the first page "[1]"

# Filter out text ratings on the second page
# Identify and reference the corresponding section in the html code
all_text_2 = soup_2.find_all("div", class_ = "inner js-replace-text")

print(all_text_2[0].text.strip())  # output the first rating on the second page  "[0]"
print(all_text_2[1].text.strip())  # output the second rating on the second page "[1]"

# 2. text analysis (NLP)
