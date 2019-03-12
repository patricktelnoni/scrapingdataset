import scrapy, csv
from dataset.items import DatasetItem
# from html.parser import HTMLParser


# class MLStripper(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.fed = []
#     def handle_data(self, d):
#         self.fed.append(d)
#     def get_data(self):
#         return ''.join(self.fed)



class KompasSpider(scrapy.Spider):
    name = "kompas"
    id = 1
    def start_requests(self):
        start_urls = 'https://kompas.com/'
        yield scrapy.Request(url=start_urls, callback=self.parse)
        # urls = [
        #     # 'https://sport.detik.com/'
        #     'https://edition.cnn.com/2019/02/13/football/ajax-youth-academy-spt-intl/index.html'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    # def strip_tags(self, html):
    #     s = MLStripper()
    #     s.feed(html)
    #     return s.get_data()

    def parse_content(self, response):
        doc         = DatasetItem()
        category    = response.request.url.split("/")[2].split(".")[0]

        with open('datasetkompas.csv', 'a') as f:
            writer = csv.writer(f)
            judul           = response.xpath('//h1[@class="read__title"]/text()').extract()
            cleaned_article = [p for p in response.xpath('//div[@class="read__content"]/descendant::text()').extract()]
            doc['title']    = judul
            doc['content']  = cleaned_article
            data = [
                    # self.id,
                    category,
                    doc['title'],
                    doc['content']
            ]
            yield {'judul': judul, 'isi': cleaned_article}
            writer.writerow(data)

                # yield {'title': content.css('.jdl h1 ::text').get(),
                #        'content': isi_article}
        f.close()
        self.id += 1

    def parsemenu(self, response):
        for link in response.css('.latest--news'):
            url = link.xpath('//a/@href').extract()
            for u in url:
                if len(str(u)) > 50:
                    # yield {"url": u}
                    yield scrapy.Request(u, callback=self.parse_content)

    def parse(self, response):
        for link in response.css('.nav__wrap'):
            url = link.xpath('//li[@class="nav__item"]/a/@href').extract()
            for u in url:
                # yield {"url": u}
                yield scrapy.Request(u, callback=self.parsemenu)



