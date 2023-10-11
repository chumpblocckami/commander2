import re

import requests

from src.banned import BANNED_CARDS, BANNED_KEYWORDS


class Checker():

    def __init__(self):
        self.url = "https://api.scryfall.com/cards/named?exact="
        self.banned_cards = BANNED_CARDS
        self.banned_keywords = BANNED_KEYWORDS

    def deck_check(self, deck):
        output = []
        for card in deck:
            output.append(self.card_check(card))
        return output

    def check_price(self, card, card_data):
        try:
            min_price = float(card_data["prices"]["eur"])
            if not min_price:
                return f"{card} doesn't have any price info!"
            if min_price < 2.0:
                return True, f"{card} is below price treshold ({min_price} euro) ✅"
            else:
                return False, f"{card} is above price treshold (**{min_price}** euro) ❌"
        except:
            return False, f"{card} not found!"

    def check_text(self, card_name, card_data):
        texts = card_data["oracle_text"] if "oracle_text" in card_data else ""
        for keyword in self.banned_keywords:
            if re.findall(keyword, texts, flags=re.IGNORECASE):
                return False, f"Card is not legal because has '{keyword}' keyword in text! ❌"
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
            return {card: card_data["details"]}

        is_priced, cost_label = self.check_price(card, card_data)
        is_legal, text_label = self.check_text(card, card_data)
        is_banned, banned_label = self.check_banned(card)
        img = self.get_image(card_data)
        legality_label = "✅" if all([is_priced, is_legal, is_banned]) else "❌"
        return {"label": f"{card} {legality_label}",
                "data":
                    {
                        "price": cost_label,
                        "keywords": text_label,
                        "banlist": banned_label
                    },
                "resources":
                    {"img": img}
                }


if __name__ == "__main__":
    checker = Checker()
    print(checker.deck_check(["vedalken engineer", ""]))
