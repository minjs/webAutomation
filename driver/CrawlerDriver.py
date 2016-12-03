from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging


class CrawlerDriver:
    """
        Using Phantomjs or firefox as driver
    """

    driver = None

    def __init__(self):
        timeout = 15
        browser = None
        proxy = None
        ua = None
        if not browser:
            browser = "phantomjs"

        if browser == "firefox":
            profile = webdriver.FirefoxProfile("/home/u738/.mozilla/firefox")
            profile.set_preference("geo.enabled", False)
            driver = webdriver.Firefox(profile)
        elif browser == "phantomjs":
            if proxy is not None:
                service_args = [
                    '--proxy='+proxy,
                ]
                timeout = 30
            else:
                service_args = None

            if ua is None:
                user_agent = (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
                )
            else:
                user_agent = (
                    ua
                )
            dc = dict(DesiredCapabilities.PHANTOMJS)
            dc["phantomjs.page.settings.userAgent"] = user_agent
            driver = webdriver.PhantomJS('phantomjs', service_args=service_args, desired_capabilities=dc)
            driver.set_window_size(2048, 4076)
        else:
            logging.error("Browser is not supported %s", browser)
            return
        self.driver = WebDriverWait(driver, timeout)

    def close(self):
        self.driver.close()