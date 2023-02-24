from dataclasses import dataclass, asdict
from requests_html import HTMLSession
import csv

@dataclass
class ServerPrice:
    server: str
    faction: str
    price: float

class GetData:
    def __init__(self, url, csv_file):
        self.url = url
        self.s = HTMLSession()
        self.csv_file = csv_file

    def get_json(self):
        resp = self.s.get(url=self.url)
        return resp.json()['payload']['results']
    
    def render_data(self):
        prices = []
        data = self.get_json()
        for item in data:
            if '[US]' in item['title']:
                title = item['title'].split(' [US] - ')
            else:
                title = item['title'].split(' [OCE] - ')
            new_server = ServerPrice(
                server= title[0],
                faction= title[1],
                price= f"{item['converted_unit_price'] *1000:.2f}"
            )
            prices.append(asdict(new_server))
        return prices
    
    def write_csv(self):
        data =  self.render_data()
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['server', 'faction', 'price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for price in data:
                writer.writerow(price)
