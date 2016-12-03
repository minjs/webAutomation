import logging

from notifier.Emailer import Emailer
from DealseaCrawler import DealseaCrawler
from DealseaKeywords import DealseaKeywords

if __name__ == "__main__":
    exampleName = ["Armani Jeans", "Prada", "Chanel", "Dior", "Bergdorf Goodman", "Nordstrom",
                         "Tory Burch", "Gucci", "UGG", "Under Armour", "Ralph Lauren Luxury",
                         "Macys", "Coach", "Kate Spade", "Nordstrom", "Bloomingdales",
                         "Estee Lauder", "Bon Ton", "Canada Goose", "Eddie Bauer", "Neiman Marcus",
                         "Rebecca Minkoff", "Saks Off 5TH", "Florsheim"]

    brandfile = "./data/brandnames"

    keywords = DealseaKeywords()
    keys = keywords.parse_text_keywords(brandfile)
    keys.extend(exampleName)

    uniqueKeys = list(set(keys))
    exampleConfig = {
        "min": {
            "contact": {
                "email": "renmin21cn@gmail.com",
                "phone": "6083344957"
            },
            "keywords": keys
        }
    }

    crawler = DealseaCrawler(exampleConfig)

    result = crawler.execute_search()
    logging.debug(result)

    email = Emailer()
    receiver = ['renmin21cn@yahoo.com', '805049201@qq.com']
    email.send_email(result, receiver)

    print result