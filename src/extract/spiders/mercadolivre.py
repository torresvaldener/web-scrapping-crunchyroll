import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/mang%C3%A1-livro"]
    page_count = 1
    max_pages = 15

    def parse(self, response):
        mangas = response.css('div.ui-search-result__content')
        for manga in mangas:
            yield {
                'titulo': manga.css('h2.ui-search-item__title::text').get(),
                'preco': manga.css('span.andes-money-amount__fraction::text').get(),
                'preco_centavos': manga.css('span.andes-money-amount__cents::text').get(),
                'avaliacao': manga.css('span.ui-search-reviews__rating-number::text').get(),
                'avaliacao_quantidade': manga.css('span.ui-search-reviews__amount::text').get()
                }
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)

