# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from ybtranslatespider.mapping import create_spider


def main():
    print("1：有道在线翻译")
    print("2: 百度在线翻译")
    print("3: 退出翻译系统\n")
    nums = input("请输入你要选择哪种翻译，并输入对应序号：")

    if all([
        "3" != nums,
        nums in ["1", "2"]
    ]):
        create_spider(nums)().run(nums)
    else:
        return


if __name__ == '__main__':
    main()
