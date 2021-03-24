import scrapy

from scrapy.loader import ItemLoader

from ..items import HoriconbankItem
from itemloaders.processors import TakeFirst


class HoriconbankSpider(scrapy.Spider):
	name = 'horiconbank'
	start_urls = ['https://www.horiconbank.com/blog.html']

	def parse(self, response):
		post_links = response.xpath('//article[@class="blog-feed-post blog-subpage"]')
		for post in post_links:
			url = post.xpath('.//p[@class="read-more"]/a/@href').get()
			date = post.xpath('.//time/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//div[@class="col-sm-12"]/h1/text()').get()
		description = response.xpath('//article//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=HoriconbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
