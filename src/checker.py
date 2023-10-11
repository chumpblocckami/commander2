import re
import string

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.banned import BANNED_CARDS, BANNED_KEYWORDS
from src.variables import SCRYFALL_URL, MKM_URL, HEADERS


class Checker:
    def __init__(self):
        self.url = SCRYFALL_URL
        self.url_mkm = MKM_URL
        self.banned_cards = BANNED_CARDS
        self.banned_keywords = BANNED_KEYWORDS
        self.headers = HEADERS

    def deck_check(self, deck):
        output = []
        for card in deck:
            output.append(self.card_check(card))
        return output

    def check_price_scryfall(self, card, card_data):
        try:
            min_price = float(card_data["prices"]["eur"])
            if not min_price:
                return f"{card} doesn't have any price info!"
            if min_price < 2.0:
                return True, f"{card} is below price treshold ({min_price} euro) ✅"
            else:
                return False, f"{card} is above price treshold (**{min_price}** euro) ❌"
        except Exception as e:
            print(f"{e}")
            return False, f"{card} not found!"

    def check_price_mkm(self, card):
        card_no_punct = card.translate(str.maketrans("", "", string.punctuation))
        card = "-".join([token.capitalize() for token in card_no_punct.split(" ")])
        r = requests.get(f"{self.url_mkm}/{card}", headers=self.headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features="html.parser")

            dl = soup.find("dl")
            data = {
                dt.text.lower().replace(" ", "_"): dd.text
                for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"))
            }

            min_price = float(data["price_trend"][:-1].replace(",", "."))
            if not min_price:
                return f"{card} doesn't have any price info!"
            if min_price < 2.0:
                return True, f"{card} is below price treshold ({min_price} euro) ✅"
            else:
                return False, f"{card} is above price treshold (**{min_price}** euro) ❌"
        else:

            return False, f"Didn't find {card} on MKM! ❌"

    def check_text(self, card_name, card_data):
        texts = card_data["oracle_text"] if "oracle_text" in card_data else ""
        for keyword in self.banned_keywords:
            if re.findall(keyword, texts, flags=re.IGNORECASE):
                return (
                    False,
                    f"Card is not legal because has '{keyword}' keyword in text! ❌",
                )
        return True, f"{card_name} does not have illegal keywords! ✅"

    def check_banned(self, card_name):
        if card_name.lower() in self.banned_cards:
            return False, f"{card_name} is in the banlist! ❌"
        else:
            return True, f"{card_name} is not in the banlist! ✅"

    def get_image(self, card_data):
        try:
            return card_data["image_uris"]["small"]
        except Exception as e:
            print(f"{e}")
            return ""

    def card_check(self, card):
        card_data = requests.get(f"{self.url}{card}").json()
        if "status" in card_data and card_data["status"] == 404:
            return {
                "label": card,
                "data": {
                    "price": card_data["details"],
                    "keywords": card_data["details"],
                    "banlist": card_data["details"],
                },
                "resources": {},
            }

        is_priced, cost_label = self.check_price_mkm(card)
        is_legal, text_label = self.check_text(card, card_data)
        is_banned, banned_label = self.check_banned(card)
        img = self.get_image(card_data)
        legality_label = "✅" if all([is_priced, is_legal, is_banned]) else "❌"
        return {
            "label": f"{card} {legality_label}",
            "data": {
                "price": cost_label,
                "keywords": text_label,
                "banlist": banned_label,
            },
            "resources": {"img": img},
        }


if __name__ == "__main__":
    checker = Checker()
    # print(checker.deck_check(["gaea's touch", ""]))
    for i in tqdm(range(0, 100)):
        checker.check_price_mkm("Harmonize")
