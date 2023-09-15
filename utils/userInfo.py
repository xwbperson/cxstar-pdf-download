class User(object):
    def __init__(self):
        self.book_id = None
        self.authorization = None
        self.school_id = 'null'
        message = '==================================================\n请输入代表您身份信息的Authorization:'
        print(message)
        self.authorization = input(">>> ")
        if self.authorization.startswith("Bearer "):
            self.authorization = self.authorization[7:]

    def inputAuthorization(self):
        message = '==================================================\n身份验证失败，请您重新输入您的Authorization:'
        print(message)
        self.authorization = input(">>> ")
        if self.authorization.startswith("Bearer "):
            self.authorization = self.authorization[7:]

    def inputBookId(self):
        message = '==================================================\n请您输入要下载的书籍ID:（例如：218c9e1a0013f2XXXX）'
        print(message)
        self.book_id = input(">>> ")
        while len(self.book_id) != 18:
            print("书籍id错误，请重新输入:")
            self.book_id = input(">>> ")

    def setSchoolId(self, school_id):
        self.school_id = school_id

    def setBookId(self):
        print("书籍id经网络验证，确认书籍不存在，请重新输入:")
        self.book_id = input(">>> ")
        while len(self.book_id) != 18:
            print("书籍id错误，请重新输入:")
            self.book_id = input(">>> ")
