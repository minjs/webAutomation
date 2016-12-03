from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from driver import CrawlerDriver


class HotelCrawler(CrawlerDriver):
    def __init__(self, browser):
        return

    def lookup(self, uri, destination, checkinDate, checkoutDate):
        self.driver.get(uri)

        try:
            dest = self.driver.wait.until(EC.presence_of_element_located((By.NAME, "q-destination")))
            dest.clear()
            dest.send_keys(destination)

            #checkin=driver.find_element_by_name('q-localised-check-in')
            checkin = self.driver.find_element_by_xpath('//*[@id="qf-0q-localised-check-in"]')
            #checkin.clear()
            checkin.send_keys(checkinDate)

            #checkout=driver.find_element_by_name('q-localised-check-out')
            checkout = self.driver.find_element_by_xpath('//*[@id="qf-0q-localised-check-out"]')
            #checkout.clear()
            checkout.send_keys(checkoutDate)

            #room selection
            select=Select(self.driver.find_element_by_id('qf-0q-compact-occupancy'))
            select.select_by_index(0)

            search=self.driver.find_element_by_xpath('//*[@id="main-content"]/main/div/div/div[1]/div/div[1]/div[1]/div/div/form/fieldset[6]/button')

            print "start searching"
            print search.text
            search.click()
            print "end searchig"

            return
            #click somewhere

        except TimeoutException:
            print("lookup exception")
            #result analysis

    def resultsParse(self, driver, mongo, checkin, checkout, city, state):
        try:
            print "waiting"
            driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hotel-wrap")))
            print "get results"
            results=driver.find_element_by_class_name("hotel-wrap")
            print "parse results"
            hotels=driver.find_elements_by_class_name('p-name')
            print "find hotels, address, prices, ranks"
            addrs=driver.find_elements_by_class_name('p-adr')
            prices=driver.find_elements_by_class_name('price')

            ranks=driver.find_elements_by_class_name('guest-rating-value')

            print len(hotels), len(prices)

            for hotel, addr, pricestr in zip(hotels, addrs, prices):
                tmp=pricestr.text.split('$')
                price=tmp[-1]
                data = {
                    "name": hotel.text,
                    "city": city,
                    "state": state,
                    "address": addr.text,
                    "price": price,
                    "checkin": checkin,
                    "checkout": checkout,
                    "source": "www.hotels.com"
                }
                print hotel.text, pricestr.text, price
                #self.insertMongo(mongo, data)
                #self.upsertMongo(mongo, data)

        except TimeoutException as e:
            print("resultsParse exception %s", str(e))

    def upsertMongo(self, mongoClient, data):
                upd = {
                        "source": data["source"],
                        "name": data["name"],
                        "city": data["city"],
                        "state": data["state"],
            "address": data["address"],
                        "checkin": data['checkin'],
                        "checkout": data['checkout'],
                }
                data = {
                        "$set": {
                                "source": data["source"],
                                "name": data["name"],
                                "city": data["city"],
                                "state": data["state"],
                "address": data["address"],
                                "checkin": data['checkin'],
                                "checkout": data['checkout'],
                                "price": data["price"],
                        },
                        "$currentDate": {"lastModified": True}
                }
                mongoClient.spear.hotel.update(upd, data, upsert=True)

    def close(self, driver):
        driver.close()

    def insertMongo(self, mongoClient, data):
        print data
        mongoClient.spear.hotel.insert(data)

if __name__ == "__main__":
    hotel = HotelCrawler()
    #driver = hotel.init_driver("firefox")
    #mongo=hotel.init_mongoClient('10.9.8.92')
    city="san francisco"
    state="ca"
    dest = city+ ", " + state
    hotel.lookup('http://www.hotels.com', dest, "2-10-2016", "2-11-2016")
    hotel.resultsParse("2-10-2016", "2-11-2016", city, state)
