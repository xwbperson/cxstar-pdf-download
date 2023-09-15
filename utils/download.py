import os
import requests
from pypdf import PdfWriter, PdfReader
from multiprocessing.dummy import Pool
from reportlab.pdfgen import canvas
from PIL import Image
from utils.encrypt import createVerificationData
from utils.file import createFolder, deleteFolderAndFile


# 获取单页pdf信息,并返回接受到的内容
def getPagePdfInfo(url, ua):
    headers = {
        'User-Agent': ua,
        'Referer': 'https://www.cxstar.com/'
    }
    return requests.get(url, headers=headers, stream=True).content


def pdfDownload(book_data, book_id, ua):
    # 书名
    book_name = book_data["title"]
    # 页数
    total_page = int(book_data["totalPage"])
    # 目录数据
    catalog = book_data["catalog"]
    # 链接地址
    file_path = book_data["filePath"]

    pdf_name = book_name + ".pdf"
    merger = PdfWriter()
    createFolder(book_id)

    print("正在下载单页pdf中,请等待...")
    page_pdf_list = [(file_path + "&pageno=" + str(i), book_id + "/" + str(i) + ".pdf", ua) for i in
                     range(total_page)]
    pool = Pool()
    if not book_data.get("webPath"):
        pool.map(pagePdfDownload, page_pdf_list)
    else:
        pool.map(saveImagePdf, page_pdf_list)
    pool.close()
    pool.join()

    print("正在合并所有pdf中...")
    for i in range(total_page):
        temp_file_name = book_id + "/" + str(i) + ".pdf"
        merger.append(temp_file_name)

    merger.write(pdf_name)
    merger.close()

    # 删除缓存的文件及目录
    print("正在删除临时文件及目录...")
    deleteFolderAndFile(book_id)

    print("正在为书籍增加书签中...")
    addBookMark(pdf_name, catalog)

    current_path = os.getcwd()
    print("下载完毕，书籍位置：" + current_path + "\\" + pdf_name)


# 下载单页pdf到指定位置
def pagePdfDownload(page_pdf):
    url = page_pdf[0]
    file_name = page_pdf[1]
    ua = page_pdf[2]
    temp = getPagePdfInfo(url, ua)
    temp_file_name = file_name
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(temp)


# 将图片保存为pdf并下载
def saveImagePdf(page_pdf):
    verification = createVerificationData()
    url = f'{page_pdf[0]}&nonce={verification["nonce"]}&stime={verification["stime"]}&sign={verification["sign"]}'
    file_name = page_pdf[1]
    ua = page_pdf[2]
    temp = getPagePdfInfo(url, ua)
    temp_file_name = file_name.split(".")[0] + ".png"

    with open(temp_file_name, "wb") as f:
        f.write(temp)

    # 将图片转换为PDF
    image = Image.open(temp_file_name)
    image_width, image_height = image.size

    pdf_file_name = file_name
    pdf = canvas.Canvas(pdf_file_name, pagesize=(image_width, image_height))
    pdf.drawImage(temp_file_name, 0, 0, width=image_width, height=image_height)
    pdf.save()


# pdf增加目录列表
def addBookMark(file_name, catalog):
    pdf_file = open(file_name, 'rb')
    # 创建一个PdfFileReader对象
    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    # 添加一页到新PDF
    total_pages = len(pdf_reader.pages)
    for i in range(total_pages):
        pdf_writer.add_page(pdf_reader.pages[i])

    for i in range(len(catalog)):
        catalog_data = catalog[i]
        bookmark = pdf_writer.add_outline_item(catalog_data["title"], int(catalog_data["page"])-1)
        children = catalog_data.get("children", [])

        for j in range(len(children)):
            bookdata2 = children[j]
            bookmark2 = pdf_writer.add_outline_item(bookdata2["title"], int(bookdata2["page"])-1, parent=bookmark)
            sub_children = bookdata2.get("children", [])

            for k in range(len(sub_children)):
                pdf_writer.add_outline_item(sub_children[k]["title"], int(sub_children[k]["page"])-1, parent=bookmark2)

    # 创建一个新的PDF文件并保存
    output_pdf_file = open(file_name, 'wb')
    pdf_writer.write(output_pdf_file)

    # 关闭文件
    pdf_file.close()
    output_pdf_file.close()
