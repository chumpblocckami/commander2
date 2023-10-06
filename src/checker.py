import requests


class Checker():

    def __init__(self):
        self.url = "https://api.scryfall.com/cards/search?order=eur&dir=asc&unique=prints&q="

    def deck_check(self, deck):
        output = []
        for card in deck:
            output.append(self.card_check(card))
        return output

    def card_check(self, card):
        try:
            card_data = requests.get(f"{self.url}{card}").json()
            min_price = min([float(x["prices"]["eur"]) for x in card_data["data"] if x["prices"]["eur"]])
            if not min_price:
                return f"{card} doesn't have any price info!"
            if min_price < 2.0:
                return f"{card} is legal! (min price is {min_price} eur)✅"
            else:
                return f"{card} is not legal! (min price is**{min_price}** eur)❌"
        except:
            return f"{card} not found!"


if __name__ == "__main__":
    checker = Checker()
    print(checker.deck_check(["Forest"]))
