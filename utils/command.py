import sys


def disposeBookInfo(book_info):
    book_message = f"""==================================================
书名: 《{book_info["title"]}》
作者: {book_info["author"]}
大小: {book_info["fileSize"]}(官方标注大小，完全不代表下载后大小)
ISBN: {book_info["isbn"]}
出版社: {book_info["publisher"]}
出版时间: {book_info["publishDate"]}
--------------------------------------------------"""
    print(book_message)
    if int(book_info["isNewPdf"]) == 1:
        print("恭喜您，这是一本矢量pdf书籍，即将开始下载！\n==================================================")
        return 1
    elif int(book_info["fileType"]) == 0:
        print("恭喜您，这是一本图片版pdf书籍，即将开始下载！\n==================================================")
        return 2
    elif int(book_info["fileType"]) == 3:
        print("很抱歉，因为能力所限，暂时无法支持epub格式的书籍下载。\n==================================================")
        return 3
    else:
        print("很抱歉，您发现了我们暂时还没看到的书籍格式，请联系我们进行尝试！\n==================================================")
        return 4


def isExit():
    message = f"""==================================================
是否选择退出？
    退出: 请输入1
    继续: 请输入任意内容|直接回车 
=================================================="""
    print(message)
    cmd = input(">>> ")
    if cmd == "1":
        sys.exit()
