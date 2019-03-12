import scrapy, csv
from dataset.items import DatasetItem

class DetikSpider(scrapy.Spider):
    name = "detik"
    id = 1
    def start_requests(self):
        # start_urls = 'https://www.detik.com/'
        # yield scrapy.Request(url=start_urls, callback=self.parse)
        urls = [
                'https://sport.detik.com/',
                'https://finance.detik.com/',
                'https://hot.detik.com/',
                'https://inet.detik.com/'
                'https://oto.detik.com/'
         ]
        for url in urls:
             yield scrapy.Request(url=url, callback=self.parse_subdomain)

    def parse_content(self, response):
        doc         = DatasetItem()
        url         = response.request.url
        category    = url.split("/")[2].split(".")[0]
        with open('datasetdetik.csv', 'a') as f:
            writer = csv.writer(f)
            for content in response.css('.detail_content'):
                cleaned_article = content.xpath('normalize-space(.//div[@id="detikdetailtext"])').extract()
                doc['title']    = content.css('.jdl h1 ::text').get()
                doc['content']  = cleaned_article
                data = [
                        # self.id,
                        category,
                        doc['title'],
                        doc['content']
                ]
                yield {'category': category, 'judul': doc['title'], 'isi': doc['content']}
                writer.writerow(data)
        f.close()
        self.id += 1

    def parse_subdomain(self, response):
        selector = response.css('.list_feed') if response.css('.list_feed') is not None else response.css('.m_content')
        for link in selector:
            url = link.xpath('//a/@href').extract()
            for u in url:
                if len(str(u)) > 50:
                     yield scrapy.Request(u, callback=self.parse_content)

    def parse(self, response):
        for link in response.css('.menu'):
            subdomain = link.xpath('///ul/li/a/@href').extract()
            for url in subdomain:
                has_title = url.split("/")
                yield {'has_title':has_title}
                # if len(has_title)== 3:
                for i in range(2,3):
                    urlready = url+"/"+str(i)
                    yield scrapy.Request(urlready, callback=self.parse_subdomain)
                    # yield {"url": u, "contain slash":len(u.split("/"))}