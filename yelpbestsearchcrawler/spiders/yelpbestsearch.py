import scrapy
from yelpbestsearchcrawler.items import YelpbestsearchcrawlerItem
from bs4 import BeautifulSoup

class YelpbestsearchSpider(scrapy.Spider):
    name = 'yelpbestsearch'
    pool_urls = ["https://www.yelp.com/search?cflt=reiki&find_loc=San%20Diego%2C%20CA"]
    number_pages = 24

    def start_requests(self):
        base_page_2_url = "https://www.yelp.com/search?cflt=reiki&find_loc=San+Diego%2C+CA&start="
        for i in range(0, self.number_pages):
            url_request = base_page_2_url + str(i*10)
            self.pool_urls.append(url_request)

        for url in self.pool_urls:
            print("start crawl url {}".format(url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Start get data \n")
        lst = response.css('main').css('ul').css('li').extract()
        for itm in lst:
            item = self.parse_li(itm)
            print(type(itm))

            if item != None:
                yield item

    def parse_li(self, html_doc):
        soup = BeautifulSoup(html_doc)

        image = soup.find("img")
        if image == None: # no image => not item
            return None

        image = image['src']
        url_profile = soup.h3
        if url_profile == None: # no h3 tag => not item
            return None

        url_profile = url_profile.a['href']
        name = soup.h3.text

        # build categories
        buttons = soup.find_all("button")
        categories = self.build_categories(buttons)

        review_count = soup.select("span[class*=reviewCount]")
        if len(review_count) != 0: 
            review_count = review_count[0].text

        star = soup.select("div[class*=i-stars]")
        if len(star) != 0: 
            star = star[0]['aria-label']

        ps = soup.find_all("p")
        short_description = self.find_description(ps)

        item = YelpbestsearchcrawlerItem()
        item['name'] = name
        item['url_profile'] = url_profile
        item['star'] = star
        item['categories'] = categories
        item['review_count'] = review_count
        item['short_description'] = short_description

        return item

    def build_categories(self, buttons):
        i = 0
        categories = ""

        for button in buttons: 
            i += 1
            if i == len(buttons): 
                break
            
            categories += button.text + ", "
        
        categories += buttons[i-1].text
        return categories

    def find_description(self, ps):
        for p in ps: 
            if "more" in p.text: 
                return p.text