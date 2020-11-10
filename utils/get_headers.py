import requests
from lxml import etree

#获取多个请求头
url = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'
response = requests.get(url)
html = etree.HTML(response.text)
headers = []

def get_headers():
    for i in range(1, 51):
        xpath = '//*[@id="content"]/table/tbody/tr[' + str(i) + ']/td[1]/a/text()'
        headers.append(html.xpath(xpath)[0])
    return headers

if __name__ == '__main__':
    headers = get_headers()
    for header in headers:
        print(header)