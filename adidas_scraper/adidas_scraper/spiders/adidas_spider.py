import scrapy
import re
import json
from adidas_scraper.items import AdidasScraperItem

def collect_men_bottoms(response):
    rows = response.selector.css("div.size_chart_table > table > tbody > tr")
    my_dict = {}
    fields = rows[0].css("th::text").extract()
    for row in rows[1:]:
        size = row.css("td ::text").extract_first()
        my_dict[size] = {}
        columns = row.css("td ::text").extract()[1:]
        for i in range(0, len(columns)):
            my_dict[size][fields[i + 1].replace(u'\xa0', u' ')] = columns[i].replace(u'\xa0', u' ')
    return my_dict




def collect_shoes(response):
    rows = response.selector.css("div.size_chart_table > table > tbody > tr")
    my_dict = {}
    first_keys = rows[0].css("td ::text").extract()
    second_keys = rows[1].css("td ::text").extract()

    for i in range(0, len(first_keys)):
        my_dict[first_keys[i] + "_" + second_keys[i]] = []
    for row in rows[2:]:
        columns = row.css("td::text").extract()
        for i in range(0, len(columns)):
            my_dict[first_keys[i] + "_" + second_keys[i]].append(columns[i].replace(u'\xa0', u' '))
    return my_dict

class AdidasSpider(scrapy.Spider):

    name = "adidas"
    first_url = "https://www.adidas.com/api/plp/content-engine?sitePath=us&query={0}&start={1}"
    details_url = "https://www.adidas.com/api/products/{0}?sitePath=us"
    size_url = "https://www.adidas.com/api/products/{0}/availability?sitePath=us"

    def start_requests(self):
        yield scrapy.Request("https://www.adidas.com/us", callback=self.parse_first)

    def parse_first(self, response):
        # keywords = ["men", "women", "kids", "back_to_school", "accessories"]
        # keywords = ["shoes", "sneakers", "socks", "swim", "basketball", "football", "sports", "running", "golf",
        #             "tracksuits", "new", "tennis", "workout", "weightlifting", "girls-back_to_school"]
        # keywords = ["women-tops"]
        links = response.selector.css("ul > li > a::attr(href)").extract()
        keywords = [link.replace("/us/", "") for link in links if link.startswith("/us/")]
        print(keywords)
        for keyword in keywords:
            yield scrapy.Request(self.first_url.format(keyword, str(0)), callback=self.parse, meta={"keyword": keyword,
                                                                                                    "page": 0})

    def parse(self, response):
        keyword = response.meta["keyword"]
        page = response.meta["page"]
        data = json.loads(response.text)
        for d in data["raw"]["itemList"]["items"]:
            for c in d["colorVariations"]:
                yield scrapy.Request(self.details_url.format(c), callback=self.parse_details)
            if len(d["colorVariations"]) == 0:
                yield scrapy.Request(self.details_url.format(d["productId"]), callback=self.parse_details)
        if len(data["raw"]["itemList"]["items"]) > 0:
            yield scrapy.Request(self.first_url.format(keyword, str(page + 48)), callback=self.parse, meta={"keyword": keyword,
                                                                                                    "page": page + 48})


    def parse_details(self, response):
        data = json.loads(response.text)
        # itm = AdidasScraperItem()
        itm = {}
        itm["id_model"] = data["model_number"]
        itm["url"] = "https:" + data["meta_data"]["canonical"]
        itm["title"] = data["meta_data"]["page_title"]
        try:
            itm["description"] = data["product_description"]["text"]
        except:
            itm["description"] = None
        itm["images"] = [img["image_url"] for img in data["view_list"]]
        itm["age_group"] = None
        itm["capacity"] = None
        itm["color"] = data["attribute_list"]["color"]
        itm["id_color"] = data["id"]
        itm["UPC"] = None
        categories = [c["text"] for c in data["breadcrumb_list"]]
        if categories:
            itm["category"] = ">".join(categories)
        else:
            itm["category"] = None
        itm["full_price"] = data["pricing_information"]["standard_price"]
        try:
            itm["price_with_discount"] = data["pricing_information"]["sale_price"]
        except:
            itm["price_with_discount"] = None
        try:
            itm["videos"] = data["description_assets"]["video_url"]
        except:
            itm["videos"] = None
        itm["attributes"] = {}
        try:
            itm["attributes"]["sport"] = data["attribute_list"]["sport"]
        except:
            pass
        try:
            itm["attributes"]["gender"] = data["attribute_list"]["gender"]
        except:
            pass
        try:
            itm["attributes"]["color"] = data["attribute_list"]["color"]
        except:
            pass
        itm["additional_features"] = []
        try:
            itm["additional_features"] += [d["description"] for d in
                                          data["product_description"]["wash_care_instructions"]["care_instructions"]]
        except:
            pass
        try:
            itm["additional_features"] += [d for d in
                                          data["product_description"]["wash_care_instructions"]["extra_care_instructions"]]
        except:
            pass
        try:
            itm["additional_features"] += data["product_description"]["usps"]
        except:
            pass
        try:
            itm["additional_features"] += [d for d in
                                          data["product_description"]["product_highlights"]["copy"]]
        except:
            pass

        size_chart_link = "https://www.adidas.com" + data["attribute_list"]["size_chart_link"]
        itm["size_chart_link"] = size_chart_link
        # yield scrapy.Request(size_chart_link, callback=self.parse_size_chart, meta={"item": itm})
        yield scrapy.Request(self.size_url.format(itm["id_color"]), callback=self.parse_size, meta={"item": itm})


    # def parse_size_chart(self, response):
    #     print(response.url)
    #     keys = {}
    #     itm = response.meta["item"]
    #     # if "m_bottoms" in response.url or "glove" in response.url or "f_balls" in response.url:
    #     #     my_dict = collect_men_bottoms(response)
    #     # elif "athletic-socks" in response.url:
    #     #     sample_url = "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-og-athletic-socks"
    #     #     pass
    #     # elif "m_tops" in response.url:
    #     if "-shoes" in response.url:
    #         my_dict = collect_shoes(response)
    #     elif "size-m_tops" in response.url:
    #         my_dict = collect_size_m_tops(response)
    #     else:
    #         my_dict = collect_men_bottoms(response)
    #     print(my_dict)
    #     text = open("size_chart.json", "a")
    #     text.write(json.dumps({response.url: my_dict}, indent=4))
    #     text.close()
    #
    #     itm["attributes"]["size_chart"] = my_dict

        # yield scrapy.Request(self.size_url.format(itm["id_color"]), callback=self.parse_size, meta={"item": itm})




    def parse_size(self, response):
        itm_dict = response.meta["item"]
        data = json.loads(response.text)
        for var in data["variation_list"]:
            itm = AdidasScraperItem()
            for k in itm_dict:
                itm[k] = itm_dict[k]
            itm["id_size"] = var["sku"]
            itm["attributes"]["size"] = var["size"]
            itm["in_stock"] = True if var["availability_status"] == "IN_STOCK" else False
            yield itm