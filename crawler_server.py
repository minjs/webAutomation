import os
from bottle import route, run, request, response
import Queue
from hotels_crawler import hotels_crawler
from travelocity_crawler import TravelocityCrawler


q = Queue.Queue()

#@route('/query', method='PUT')
@route('/query', method='GET')
def query():
    city = request.GET.get('city')
    state = request.GET.get('state')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    print city, state, checkin, checkout

    if not city or not state or not checkin or not checkout:
        return {"success": False}

    #blocked call
    crawler = hotels_crawler()
    print crawler
    driver = crawler.init_driver("phantomjs")

    mongo=crawler.init_mongoClient('10.9.8.92')
    dest = city + ", " + state 
    crawler.lookup(driver, 'http://www.hotels.com', dest, checkin, checkout)
    crawler.resultsParse(driver, mongo, checkin, checkout, city, state)
    driver.close()

    t_crawler = TravelocityCrawler('10.9.8.92', 27017, "phantomjs")
    t_list=t_crawler.do_search('', city, state, checkin, checkout)
    for e in t_list:
        try:
                t_crawler.upsertMongo(e)
            print "Updating MongoDB for "+json.dumps(e, indent=4)
        except Exception as ex:
                print "Updateing MongoDB failed."
                print str(ex)
    return {"success": True}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8899))
    run(host='0.0.0.0', port=port, debug=True)
