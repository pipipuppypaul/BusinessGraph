import scrapy
import json
import urllib
import datetime

# scrapy crawl ND_biz
class NdBusinessSpider(scrapy.Spider):
    name = "ND_biz"

    def start_requests(self):
        urls = [
            # 'https://firststop.sos.nd.gov/search/business',
            'http://firststop.sos.nd.gov/api/Records/businesssearch'
        ]
        headers = {
            "accept": '*/*',
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "authorization": "undefined",
            # "content-length": "66",
            "content-type": "application/json",
            "cookie": "ASP.NET_SessionId=qn4faj4uxnmcww0oer5e44es; _ga=GA1.2.2106051216.1670786715; _gid=GA1.2.1026958051.1670786715",
            "origin": "https://firststop.sos.nd.gov",
            "referer": "https://firststop.sos.nd.gov/search/business",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": 'macOS',
            "sec-fetch-dest": 'empty',
            "sec-fetch-mode": 'cors',
            "sec-fetch-site": 'same-origin',
            "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }

        payload = {"search_value": "X", "starts_with_yn": "true", "active_only_yn": "true"}
        cookies = {"ASP.NET_SessionId": "qn4faj4uxnmcww0oer5e44es",
                   "_ga": "GA1.2.2106051216.1670786715",
                   "_gid": "GA1.2.1026958051.1670786715"}
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, method='POST',
                                 headers=headers, body=json.dumps(payload),
                                 cookies=cookies,
                                 meta={'handle_httpstatus_all': True})

    def parse(self, response):
        if not response:
            print("no response")
        print(f"response@{datetime.datetime.now()}:", response.text)
        print(response.css('rows').get())  # always empty


