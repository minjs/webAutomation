import time


class CrawlerThread:
    deals = {}

    def __init__(self):

    def triggerCrawler(self, trackList):
        try:
            for key, value in trackList.iteritems():
                checkin=value['checkin'].strftime('%m-%d-%Y')
                checkout=value['checkout'].strftime('%m-%d-%Y')

                self.crawler.lookup(self.driver, 'http://www.hotels.com', value['city'], checkin, checkout)
                self.crawler.resultsParse(self.driver, self.mongoClient, checkin, checkout, value['city'], value['state'])
        except:
            print "crawler is failed"
        return

if __name__ == "__main__":
    while True:
        cr = crawlerClient()
        tracklist = cr.findTracks()
        cr.triggerCrawler(tracklist)
        time.sleep(60*60*12)

