import argparse
import requests
from lxml import html

class Book(object):
    def __init__(self, title, subtitle, price):
        self.title = title
        self.subtitle = subtitle
        self.price = price

    def __repr__(self):
        return self.title + " : " + self.subtitle + " : Rs." + self.price

    def __str__(self):
        return self.title + " : " + self.subtitle + " : Rs." + self.price


class FlipkartSearch(object):
    def __init__(self, title):
        self.title = title

    def get_results(self):
        # requests.get("http://www.flipkart.com/search?q=refactoring")
        res = requests.get("http://www.flipkart.com/ph/search/pr?q=" + self.title)
        tree = html.fromstring(res.text)
        numprod = tree.xpath("/html/body/div/div/div/div[2]/div[1]/header/h2/span/span[2]/span[2]/text()")[0]
        print numprod
        if int(numprod) == 1:
            print "Single match"
            prodinfo = tree.xpath("/html/body/div/div/div/div[2]/div[1]/ul/li[1]/section/a/div[2]")
            title = prodinfo[0].xpath("span[1]/text()")
            subtitle = prodinfo[0].xpath("span[2]/text()")
            price = prodinfo[0].xpath("span[4]/text()")
            print price
        else:
            print numprod + " matches"
            # Grabbing the first match
            # For subsequent matches, /html/body/div/div/div/div[2]/div[1]/ul[1]/li[2]/section/a/div[2]
            prodinfo = tree.xpath("/html/body/div/div/div/div[2]/div[1]/ul[1]/li[1]/section/a/div[2]")
            print prodinfo
            title = prodinfo[0].xpath("span[1]/text()")
            print title
            subtitle = prodinfo[0].xpath("span[2]/text()")
            print subtitle
            price = prodinfo[0].xpath("span[3]/text()")
            print price
        result = Book(title[0], subtitle[0], price[0][3:])  # price comes as Rs.234, strip off Rs.
        return result

class AmazonSearch(object):
    def __init__(self, title):
        self.title = title.replace(" ", "+")

    def get_results(self):
        print self.title
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
        }
        res = requests.get("http://www.amazon.in/gp/aw/s/ref=is_box_?x=0&y=0&k=" + self.title, headers=headers)
        tree = html.fromstring(res.text)
        prodinfo = tree.xpath("/html/body/div[6]/div/div[1]")
        prodinfo = prodinfo[0]
        print "Prod", prodinfo
        title = prodinfo.xpath("/html/body/div[6]/div/div[1]/a/table/tbody/tr/td[2]/span[1]/a/text()")
        print title
        subtitle = prodinfo.xpath("a/table/tbody/tr/td[2]/span[2]/text()")
        print subtitle
        price = prodinfo.xpath("a/table/tbody/tr/td[2]/span[3]/span/text()")
        print price
        result = Book(title[0], subtitle[0], price[0][3:])  # price comes as Rs.234, strip off Rs.
        return result

class InfibeamSearch(object):
    def __init__(self, title):
        self.title = title.replace(" ", "+")

    def get_results(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
        }
        res = requests.get("http://www.infibeam.com/Books/search?q=" + self.title, headers=headers)
        tree = html.fromstring(res.text)
        prodinfo = tree.xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]")
        prodinfo = prodinfo[0]
        title = prodinfo.xpath("div/div[1]/div[1]/div[2]/a/div/text()")[0].replace("\n", "")
        authors = prodinfo.xpath("div/div[1]/div[1]/div[2]/div[2]/a")
        auths = ""
        for a in authors:
            auths += a.xpath("text()")[0].encode("utf-8")
            auths += ", "
        price = prodinfo.xpath("div/div[2]/div[1]/span/text()")[0].replace(",", "")
        result = Book(title, auths, price)  # price comes as Rs.234, strip off Rs.
        return result


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--title', help='Book title in quotes', required=True)
    # args = parser.parse_args()
    # title = args.title
    title = "Refactoring"
    title = "Collected Papers David Parnas"
    search = InfibeamSearch(title)
    print "Finally", search.get_results()
    # $REVIEW$ use threads for multiple sites?

if __name__ == '__main__':
    main()
