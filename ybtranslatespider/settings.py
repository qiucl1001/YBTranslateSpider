# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

# 有道翻译网站基本请求头配置: [可选]
YOU_DAO_FAN_YI_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "fanyi.youdao.com",
    "Origin": "http://fanyi.youdao.com",
    "X-Requested-With": "XMLHttpRequest",
}


# 翻译种类，可扩展
BAI_DU_TRANSLATE_CATEGORY_MAPPING = {
    "1": {
        "from": "en",
        "to": "zh"
    },
    "2": {
        "from": "zh",
        "to": "en"
    },
}