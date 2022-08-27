import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
from urllib.parse import quote

settings = get_project_settings()
crawler1 = CrawlerProcess(settings)
crawler2 = CrawlerProcess(settings)
crawler3 = CrawlerProcess(settings)
crawler1.crawl("baiduspider1")
crawler2.crawl("baiduspider2")
crawler3.crawl("baiduspider3")
crawler1.start()
crawler2.start()
crawler3.start()
