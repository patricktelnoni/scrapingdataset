import scrapy, csv
from dataset.items import DatasetItem

class TirtoSpider(scrapy.Spider):
    name = "tirto"
    id = 1
    def start_requests(self):
        start_urls = 'https://tirto.id/q/olahraga-Tp/'
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse_content(self, response):
        doc = DatasetItem()
        with open('datasettirto.csv', 'a') as f:

            writer = csv.writer(f)
            for content in response.css('.row my-5'):
                judul = content.xpath(".//div[@class='row m-0']/a/h1::text").extract()
                # isi   = content.xpath(".//div[@class='row m-0']/a::h6()").extract()
                # isi_article     = content.css('div.row m-0 ::text').extract()
                cleaned_article = content.xpath('normalize-space(.//div[@id="detikdetailtext"])').extract()
                doc['title']    = content.css('.//div[@class="row m-0"]/a::h6()').get()
                doc['content']  = cleaned_article
                data = [
                        self.id,
                        'olahraga',
                        doc['title'],
                        doc['content']
                ]
                yield {'judul':judul,'isi': cleaned_article}
                writer.writerow(data)
                self.id += 1
                # yield {'title': content.css('.jdl h1 ::text').get(),
                #        'content': isi_article}
        f.close()

    def parse(self, response):
        for link in response.css('.container-fluid'):
            url = link.xpath('//a/@href').extract()

            for u in url:
                yield {'url': u}
                # if len(str(u)) > 50:
                #      yield scrapy.Request(u, callback=self.parse_content)



