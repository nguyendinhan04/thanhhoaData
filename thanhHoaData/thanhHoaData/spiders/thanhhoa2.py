import scrapy


class Thanhhoa2Spider(scrapy.Spider):
    name = "thanhhoa2"
    allowed_domains = ["opendata.thanhhoa.gov.vn"]
    start_urls = ["https://opendata.thanhhoa.gov.vn"]

    def parse(self, response):
        linh_vucs = response.xpath("//div[@class = 'linh-vuc']")
        for linh_vuc in linh_vucs:
            name = linh_vuc.xpath(".//a/div[2]/text()").get()
            link = linh_vuc.xpath(".//a/@href").get()

            yield response.follow(url=link, callback=self.parse_linh_vuc_thong_tin, meta={"linh_vuc": name.strip()})
    def parse_linh_vuc_thong_tin(self,response):
        link = response.xpath("//div[@class = 'custom-nav']/ul[@class = 'nav']/li[1]/a/@href").get()
        yield response.follow(url=link, callback=self.parse_linh_vuc_du_lieu, meta=response.meta)


    def parse_linh_vuc_du_lieu(self, response):
        linh_vuc = response.meta["linh_vuc"]
        data_sets = response.xpath("//div[@class = 'dataset-item-content-vertical']")


        for data_set in data_sets:
            name = data_set.xpath(".//div[1]/div/a/text()").get()
            link = data_set.xpath(".//div[4]/a[1]/@href").get()
            # data_type = data_set.xpath(".//div[4]/a/text()").get()
            
            yield response.follow(url=link, callback=self.parse_file_dowload, meta = {'linh_vuc': linh_vuc, 'name': name})
            pass
        pass
    
    def parse_file_dowload(self,response):
        linh_vuc = response.meta["linh_vuc"]
        name = response.meta['name']
        items = response.xpath("//*[@id='display_vertical']/div/div/div/div/div[2]/div/div[6]/div[2]/ul/li")
        for item in items:
            type_file = item.xpath(".//a/span/text()").get()
            link = item.xpath(".//a/@href").get()
            yield {
                "linh_vuc": linh_vuc,
                "dataset_name": name,
                "type_file": type_file,
                "link": link
            }
        pass