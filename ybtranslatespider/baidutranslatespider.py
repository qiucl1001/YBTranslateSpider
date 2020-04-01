# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import re
import execjs
import requests
from requests.cookies import RequestsCookieJar
from ybtranslatespider.settings import BAI_DU_TRANSLATE_CATEGORY_MAPPING


class BaiDuTranslateSpider(object):
    """百度在线翻译"""
    def __init__(self):
        """初始化"""
        self.fy_base_url = "https://fanyi.baidu.com/v2transapi"
        self.base_url = "https://fanyi.baidu.com/?aldtype=16047"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.132 Safari/537.36"
        }
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.token = None

    def get_file_content(self, file):
        """
        获取相应文件中的文本内容
        :param file: 文件所在的直接目录
        :return:
        """
        file_path = os.path.join(self.base_path, file)
        for filename in os.listdir(file_path):
            filename_abspath = os.path.join(file_path, filename)
            with open(filename_abspath, "r") as f:
                file_content = f.read()
                return file_content

    def generate_sign(self, word):
        """
        获取签名认证参数sign值
        :param word: 待翻译单词
        :return: 返回生成的随机的sign值
        """
        js_data = self.get_file_content("js")

        execjs_obj = execjs.compile(js_data)
        sign = execjs_obj.eval('e("{}")'.format(word))

        return sign

    def generate_token(self):
        """
        获取token参数值
        :return: token参数值
        """
        response = self.get_file_content("html")
        if response:
            html = response.replace("\r\n", "").replace(" ", "")
            pattern = re.compile(r"window\['common'\].*?token:'(.*?)',", re.S)
            token = re.findall(pattern, html)
            if token:
                self.token = token[0]

    def get_cookies(self):
        """获取cookies值"""
        jar = RequestsCookieJar()
        r = requests.get(url=self.base_url)
        for key, value in r.cookies.items():
            jar.set(key, value)
        print(r.cookies.items())
        return jar

    def translate(self, word, from_, to_):
        """
        百度在线翻译
        :param word: 待翻译的单词
        :param from_: 被翻译单词类型
        :param to_: 翻译后单词类型
        :return: 返回翻译结果
        """
        form_data = {
            "from": from_,
            "to": to_,
            "query": word,
            "transtype": "enter",
            "simple_means_flag": "3",
            "sign": self.generate_sign(word),
            "token": self.token,
            "domain": "common",
        }

        json_str = requests.post(
            url=self.fy_base_url,
            data=form_data,
            headers={
                # 待优化， 动态设置Cookie值
                "Cookie": "BAIDUID=274093F30F3C2D5356690905F600EA5B:FG=1; BIDUPSID=274093F30F3C2D5356690905F600EA5B; "
                          "PSTM=1548317989; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; to_lang_often=%5B%7B%"
                          "22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22"
                          "text%22%3A%22%u4E2D%u6587%22%7D%5D; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_"
                          "SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22"
                          "zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u8"
                          "2F1%u8BED%22%7D%5D; delPer=0; PSINO=7; BDRCVFR[1kRcOFa5hin]=mk3SLVN4HKm; Hm_lvt_64ecd82404c5"
                          "1e03dc91cb9e8c025574=1585211273,1585211296,1585212416,1585234931; Hm_lpvt_64ecd82404c51e03dc"
                          "91cb9e8c025574=1585236338; __yjsv5_shitong=1.0_7_5b42d2201e4b413234213e1a065505c8fffb_300_15"
                          "85236269445_111.75.98.119_32b9b0ee; yjs_js_security_passport=572d1544801fed34e8cc05e6a54dc9b"
                          "d70c3c19f_1585236270_js"
            }
        ).json()

        if json_str:
            try:
                result = json_str.get("translateResult")[0][0].get("tgt")
                print(result)
                print(" ")
            except TypeError:
                print("翻译出错了，非常抱歉！\n")

    def run(self, category):
        """
        程序入口
        :param category: 选择的翻译类型 e.g. 1--->英译汉  2---> 汉译英 ...
        """
        from_to_dict = BAI_DU_TRANSLATE_CATEGORY_MAPPING.get(category)
        from_ = from_to_dict.get("from")
        to_ = from_to_dict.get("to")
        print(from_, to_)
        if not self.token:
            self.generate_token()
        while True:
            word = input("请输入要翻译的单词__<退出请输入3>：")
            if word and "3" != word:
                self.translate(word, from_, to_)
            elif "3" != word:
                return
            else:
                print("非法输入，输入不能为空， 请重新输入。")


if __name__ == '__main__':
    b = BaiDuTranslateSpider()
    b.run("2")
