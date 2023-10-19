import time
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Browser:
    """
    controller层 -- 浏览器驱动类
    该类实例化后，绑定一个webdriver
    进行自动化操作的控制
    """

    def __init__(self):
        self.__base_url = 'https://www.xiaohongshu.com/'  # 小红书基本网址
        self.driver = self.__chrome()  # webdriver-Chrome
        self.page_source = ""

    def __chrome(self):
        """
        初始化webdriver，返回Chrome驱动实例
        :return: Chrome驱动实例
        """
        options_dict = {
            "disable-blink-features": "AutomationControlled",
            "excludeSwitches": ["enable-automation"],
            "ignore-certificate-errors": True,
            "window-size": "1250,900",
            "no-sandbox": True
        }
        options = Options()
        for key, value in options_dict.items():
            options.add_argument(f"--{key}={value}")
        service = Service(executable_path='../chromedriver.exe')
        return Chrome(service=service, options=options)

    def open(self, url=None):
        """
        打开指定网址
        :param url: 网址
        """
        url = url or self.__base_url
        self.driver.get(url)
        self.page_source = self.driver.page_source

    def close(self):
        """
        关闭浏览器
        """
        self.driver.close()
        self.driver.service.stop()

    def is_invalid_url(self):
        time.sleep(2)
        pattern = re.compile(re.escape("当前内容无法展示"))
        if pattern.search(self.page_source):
            print("无效")
        else:
            print("有效")



if __name__ == '__main__':
    browser = Browser()
    # browser.open("https://www.xiaohongshu.com/explore/6530d2b6000000001f006251")
    browser.open("https://www.xiaohongshu.com/explore/65309638000000001f03b405")
    browser.is_invalid_url()
