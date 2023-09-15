import random
import requests
from utils.analysis import htmlPath, jsonPath
from utils.encrypt import createVerificationData


class WebInfo(object):
    def __init__(self, token, ua):
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'Cookie': 'token=' + token,
            'Referer': 'https://www.cxstar.com/',
            'User-Agent': ua,
        }

    def getUserInfo(self):
        url = 'https://m.cxstar.com/api/user'
        return requests.get(url, headers=self.headers)

    def setAuthorization(self, token):
        self.headers["Authorization"] = 'Bearer ' + token
        self.headers["Cookie"] = 'token=' + token

    def getBookInfo(self, book_id, school_id):
        url = f'https://m.cxstar.com/api/books/{book_id}?pinst={school_id}'
        return requests.get(url, headers=self.headers)

    def getNewPdfInfo(self, book_id, school_id):
        verification = createVerificationData()
        url = f'https://www.cxstar.com/api/books/{book_id}/pdf'
        params = {
            'pinst': school_id,
            'nonce': verification["nonce"],
            'stime': verification["stime"],
            'sign': verification["sign"],
            'typecode': 'ebook',
        }
        res = requests.get(url, headers=self.headers, params=params)
        is_buy = self.getIsBuyNewPdf(book_id)
        if is_buy:
            return res.json()
        book_data = res.json()
        print("当前用户权限所限，只能下载试看内容！")
        book_data["totalPage"] = book_data["trialPage"]
        return book_data

    def getIsBuyNewPdf(self, book_id):
        verification = createVerificationData()
        url = f'https://www.cxstar.com/api/books/{book_id}/access'
        params = {
            'nonce': verification["nonce"],
            'stime': verification["stime"],
            'sign': verification["sign"],
            'typecode': 'ebook',
        }
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 200:
            return res.json()["access"]
        return False

    # 获取旧版pdf的页面，并解析，将有效数据返回
    def getOldPdfWebInfo(self, book_id, school_id):
        url = f'https://www.cxstar.com/onlinebook?ruid={book_id}&school={school_id}&typecode=ebook&pageno='
        res = requests.get(url, headers=self.headers)
        html_content = res.text
        # 拿到书名、文件路径、页数、可预览页数
        book_data = htmlPath(html_content)

        # 获取目录数据
        catalog = self.getBookCatalog(book_id)
        book_data["catalog"] = jsonPath(catalog)

        is_buy = self.getIsBuyOldPdf(book_id, book_data)
        if is_buy != -1:
            return book_data

        print("当前用户权限所限，只能下载试看内容！")
        book_data["totalPage"] = book_data["trialPage"]
        return book_data

    # 如果用户拥有该书的权限,则给原filePath增加预览权限
    def getIsBuyOldPdf(self, book_id, book_data):
        page_no = random.randint(int(book_data["trialPage"]), int(book_data["totalPage"]))
        url = 'https://www.cxstar.com/onlinebook/readRule'
        params = {
            'BookId': book_id,
            'FilePath': book_data["filePath"],
            'PageNo': page_no,
            'borrowtoken': '',
            'typecode': 'ebook'
        }
        return requests.get(url, headers=self.headers, params=params).json()["code"]

    # 获取旧版pdf的书签列表
    def getBookCatalog(self, book_id):
        url = "https://www.cxstar.com/onlinebook/GetBookCatalog"
        params = {
            'bookruid': book_id,
            'typecode': 'ebook'
        }
        return requests.post(url, headers=self.headers, params=params).json()
