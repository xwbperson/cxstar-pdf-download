from utils.command import disposeBookInfo, isExit
from utils.download import pdfDownload
from utils.network import WebInfo
from utils.userInfo import User
from utils.userAgent import userAgent


if __name__ == '__main__':
    # 获取随机ua，本次下载操作中ua一致
    user_agent = userAgent()

    # 首次获取用户的authorization验证信息
    user = User()

    # 网络初始化
    web_info = WebInfo(user.authorization, user_agent)

    # 验证身份权限，并拿到用户信息
    user_info = web_info.getUserInfo()
    while user_info.status_code != 200:
        user.inputAuthorization()
        web_info.setAuthorization(user.authorization)
        user_info = web_info.getUserInfo()

    # 拿到用户信息中的schoolId并传给用户
    user.setSchoolId(user_info.json()["schoolId"])

    while True:
        # 拿到用户输入的书籍id
        user.inputBookId()
        # 验证书籍信息
        book_info = web_info.getBookInfo(user.book_id, user.school_id)
        while book_info.status_code != 200:
            user.setBookId()
            book_info = web_info.getBookInfo(user.book_id, user.school_id)

        book_info = book_info.json()
        # 打印书籍信息并获取书籍类型
        book_type = disposeBookInfo(book_info)

        if book_type == 1:
            book_data = web_info.getNewPdfInfo(user.book_id, user.school_id)
            pdfDownload(book_data, user.book_id, user_agent)
        elif book_type == 2:
            book_data = web_info.getOldPdfWebInfo(user.book_id, user.school_id)
            pdfDownload(book_data, user.book_id, user_agent)

        isExit()
