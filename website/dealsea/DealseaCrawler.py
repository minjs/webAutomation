from selenium.common.exceptions import TimeoutException
from driver.CrawlerDriver import CrawlerDriver


class DealseaCrawler(CrawlerDriver):
    config = {}
    results = {}
    keywords = []
    uri = "https://dealsea.com"
    """
        config is map of usrname and keywords list and contact.
        {
            <usrname>: {
                "contact":{
                    "email": "",
                    "phone": ""
                },
                "keywords": ["", ""]
            }
        }
    """
    def __init__(self, config):
        CrawlerDriver.__init__(self)
        self.config = config
        self.consolidate_keywords()

    def consolidate_keywords(self):
        keys = []
        for key in self.config:
            keys = keys + self.config[key]["keywords"]
        self.keywords = list(set(keys))

    """

    """
    def execute_search(self):
        return self.lookup(self.uri)

    def lookup(self, uri):
        dealsSummary = {}
        driver = self.driver._driver
        driver.get(uri)
        try:
            print "start searching"
            deals = driver.find_elements_by_class_name("dealbox")
            length = len(deals)
            for index in xrange(1, length):
                si = str(index)

                dealcontentstr = '//*[@id="fp-deals"]/div[' + si + ']/div[2]'
                dealbox = driver.find_element_by_xpath(dealcontentstr)

                '''
                try:
                    expire = dealbox.find_element_by_link_text("Expired")
                    print("this deal is expired")
                    continue
                except Exception:
                    pass
                '''
                detailstr = './strong/a'
                dealelement = dealbox.find_element_by_xpath(detailstr)
                dealtext = dealelement.text
                dealurl = dealelement.get_attribute("href")
                dealurl += " "
                #scan the keyword list
                for keyword in self.keywords:
                    if keyword.lower() in dealtext.lower():
                        dealDetail = {
                            "brand": keyword,
                            "description": dealtext,
                            "hashcode": hash(dealtext),
                            "link": dealurl
                        }
                        if keyword in dealsSummary:
                            ds = dealsSummary[keyword]
                            existFlag = False
                            for sds in ds:
                                if sds["hashcode"] == hash(dealtext):
                                    existFlag = True
                                    break
                            if not existFlag:
                                ds.append(dealDetail)
                                dealsSummary[keyword] = ds
                        else:
                            ds = [
                                dealDetail
                            ]
                            dealsSummary[keyword] = ds
            print "end searching"
        except TimeoutException:
            print("lookup exception")
        except Exception as e:
            print("Can not find this element %s" % e)
        return dealsSummary

