from bs4 import BeautifulSoup


def htmlPath(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 书的页数
    sum_num = soup.find(id="sumNumb")
    sum_num_value = sum_num.text

    # 可预览的页数
    max_num = soup.find(id="maxNumb")
    max_num_value = max_num.text

    # 文件path
    path = soup.find(id="path")
    path_value = path.text

    # 获取书名
    title = soup.find('title')
    title_value = title.text
    book_name = title_value.split("-")[0]

    # 获取文件路径值
    file_path = soup.find(id="cente")
    file_path_value = file_path.get("value")

    return {
        "totalPage": sum_num_value,
        "webPath": file_path_value,
        "title": book_name,
        "trialPage": max_num_value,
        "filePath": path_value
    }


# 将所有递归函数，用于替换所有键为 'pageno' 的值为 'page'
def jsonPath(obj):
    if isinstance(obj, dict):
        modified_obj = {}
        for key, value in obj.items():
            if key == "pageno":
                modified_obj["page"] = value
            elif key == "text":
                modified_obj["title"] = value
            else:
                modified_obj[key] = jsonPath(value)
        return modified_obj
    elif isinstance(obj, list):
        return [jsonPath(item) for item in obj]
    else:
        return obj
