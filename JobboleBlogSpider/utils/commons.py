import hashlib

import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    """
    从字符串中提取数字
    :param text:
    :return:
    """
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


if __name__ == '__main__':
    # md5 的测试方法
    print(get_md5("http://jobbole.com".encode("utf-8")))
    print(get_md5("http://jobbole.com"))
