# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from ybtranslatespider.baidutranslatespider import BaiDuTranslateSpider
from ybtranslatespider.youdaotranslatespider import YouDaoTranslateSpider


class_mapping = {
    "1": YouDaoTranslateSpider,
    "2": BaiDuTranslateSpider
}


def create_spider(nums):
    """
    生成一个翻译类对象
    :param nums: 翻译类对象类型 百度翻译或有道翻译
    :return:
    """
    return class_mapping.get(nums)

