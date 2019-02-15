import scrapy

from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        start_urls = 'https://sport.detik.com/'
        yield scrapy.Request(url=start_urls, callback=self.parse)
        # urls = [
        #     # 'https://sport.detik.com/'
        #     'https://edition.cnn.com/2019/02/13/football/ajax-youth-academy-spt-intl/index.html'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        url = response.url
        for content in response.css('.detail_content'):
            # for title in response.css('.jdl'):
            # yield {'title': content.css('.jdl h1 ::text').get()}
            # for title in response.css('.detail_content>article'):
            yield {'title': content.css('.jdl h1 ::text').get(),
                   'content': content.xpath(".//div[@id='detikdetailtext']/descendant::text()").extract()}

    def parse(self, response):
        # for title in response.css('.post-header>h2'):
        #     yield {'title': title.css('a ::text').get()}
        #
        # for next_page in response.css('div.prev-post > a'):
        #     yield response.follow(next_page, self.parse)

        # links = response.xpath('//a/@href').extract()
        # for link in links:
        for link in response.css('.list_feed'):
            url = link.xpath('//a/@href').extract()

            for u in url:
                if len(str(u)) > 50:
                     yield scrapy.Request(u, callback=self.parse_content)

        # for title in response.css('.desc_nhl>a'):
        #     yield {'title': title.css('h2 ::text').get()}
        #
        # for title in response.css('.desc_nhl>span'):
        #     yield {'content': title.css('span ::text').get()}
        #
        # for next_page in response.css('div.prev-post > a'):
        #     yield response.follow(next_page, self.parse)
        # page        = response.url.split("/")[-2]
        # soup        = BeautifulSoup(page, 'lxml')
        # filename    = '%s.html' % page
        #
        # with open(filename, 'wb') as f:
        #      f.write(response)

        # with open(filename, 'wb') as f:
        #     for a in soup.find_all('article'):
        #         f.write(a.getText())
            # for t in a.find_all('div', {"class" : "m_content"}):
            #     for article in t.find_all("article", {"class" : "gtm_newsfeed_atikel"}):
            #         with open('smile.html', 'wb') as f:
            #             f.write(article)

