# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import re
import time
import random
import requests
from hashlib import md5
from requests.cookies import RequestsCookieJar
# from ybtranslatespider.settings import YOU_DAO_FAN_YI_HEADERS


class YouDaoTranslateSpider(object):
    """有道在线翻译"""
    def __init__(self):
        """初始化"""
        self.base_url = "http://fanyi.youdao.com/"
        self.fy_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.js_url = "http://shared.ydstatic.com/fanyi/newweb/v1.0.25/scripts/newweb/fanyi.min.js"
        self.headers = {
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.132 Safari/537.36",
        }

    def get_sign_str(self):
        """获取签名认证参数sign生成所属的盐值"""
        response = requests.get(url=self.js_url, headers=self.headers).text
        if response:
            js_str = response.replace("\r\n", "").replace(" ", "")
            pattern = re.compile(r'sign:n\.md5\("(.*?)"\+e\+i\+"(.*?)"\)\}\};', re.S)
            salt_str = pattern.findall(js_str)

            return salt_str

    @staticmethod
    def generate_ts_salt():
        """
        随机生成时间戳和盐值
        有道翻译中生成时间戳的源代码js: r = "" + (new Date).getTime()
        有道翻译中生成盐值的源代码js: i = r + parseInt(10 * Math.random(), 10);
        :return:
        """
        ts = str(int(time.time()*1000))
        salt = ts + str(random.randint(0, 9))
        return ts, salt

    def generate_sign(self, word):
        """
        生成签名认证参数
        有道翻译中生成签名认证sign的源代码js:
        --------------------------------------------------------------
        r = "" + (new Date).getTime()
        i = r + parseInt(10 * Math.random(), 10);
        sign: n.md5("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj")
        --------------------------------------------------------------
        :param word: 待翻译参数
        :return:
        """
        #  salt_str=[('fanyideskweb', 'Nw(nmmbP%A-r6U3EUn]Aj')]
        salt_str = self.get_sign_str()

        ts, salt = self.generate_ts_salt()
        str_ = salt_str[0][0] + word + salt + salt_str[0][1]

        s = md5()
        s.update(str_.encode("utf-8"))
        sign = s.hexdigest()

        return salt, sign, ts

    def get_cookies(self):
        """
        获取cookies
        :return: 待有cookie值的jar对象
        """
        jar = RequestsCookieJar()
        response = requests.get(self.base_url)
        for key, value in response.cookies.items():
            jar.set(key, value)

        return jar

    def translate(self, word):
        """
        有道翻译
        :param word: 待翻译参数
        :return:
        """
        jar = self.get_cookies()
        salt, sign, ts = self.generate_sign(word)

        form_data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "a9c3483a52d7863608142cc3f302a0ba",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # self.headers.update(YOU_DAO_FAN_YI_HEADERS)  # 可动态设置请求头参数
        response = requests.post(
            url=self.fy_url,
            data=form_data,
            cookies=jar,
            headers=self.headers
        )
        if response:
            json_str = response.json()
            try:
                result = json_str.get("translateResult")[0][0].get("tgt")
                print(result)
                print(" ")
            except TypeError:
                print("翻译出错了，非常抱歉！\n")

    def run(self, nums=None):
        """
        程序入口
        :param nums: 业务需求序号
        :return:
        """
        if all([
            "3" != nums,
            nums is not None
        ]):
            while True:
                word = input("请输入要翻译的单词__<退出请输入3>：")
                if word and "3" != word:
                    self.translate(word)
                elif "3" == word:
                    return
                else:
                    print("非法输入，输入不能为空， 请重新输入。")
        else:
            print("谢谢使用，欢饮下次再来！")
            return


if __name__ == '__main__':
    y = YouDaoTranslateSpider()
    y.run()
