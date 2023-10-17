import ctypes
import datetime
import json
import random
import re
import sys
import threading
import time
import requests
from settings import Settings
from pathlib import Path

from PyQt5.QtCore import Qt, QMimeData, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QGroupBox, QPushButton,
                             QSpinBox, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem, QGridLayout, QTextEdit, QCheckBox, QFileDialog, QFrame, QDesktopWidget)
from loguru import logger
from selenium.common.exceptions import *
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("starter")

RARE_WORDS = "敳屮屰屲峫峭峮嵂掴掵掶掸掹掺掻掼掽掾掿拣揁揂揃嵄嵙嵚嵛嵜庋庌庍庎庑庖庘庛庝庞庠庡庢嵴嵵嵶嵷嶊嶋嶌嶍嶎嶏嶪嶫嶬嶭巗巘巙巚暀暁暂暃暄暅暆暇晕晖暊暋暌暍暎暏暐暑暒暓暔暕暖暗旸暙暚暛暜暝暞暟暠暡暣暤暥暦暧暨暩暪"


class Browser:
    """
    controller层 -- 浏览器驱动类
    该类实例化后，绑定一个webdriver
    进行自动化操作的控制
    """

    def __init__(self, view, interval, is_random_interval: bool, comment_path: str, limit: int,
                 is_like: bool, is_collect: bool, is_follow: bool,
                 is_comment: bool, is_check_shield: bool, add_text_signal,
                 is_skip_collect: bool, is_again_comment_collect: bool,
                 is_shield_retry: bool, shield_retry_count: int,
                 is_cyclic_mode: bool, interval_minute: int,
                 is_append_rare_word: bool, rare_words_num: int, category_key: str):
        self.category_key = category_key
        self.name = None  # 浏览器实例名字
        self.create_time = datetime.datetime.now().time()  # 实例创建时间
        self.limit = limit  # 任务数量最大限制
        self.__base_url = 'https://www.xiaohongshu.com/'  # 小红书基本网址
        self.view: MainWindow = view  # view层穿透，便于交互
        self.comment_path = comment_path  # 评论话术文件的路径地址
        self.task_urls = []  # 任务地址列表
        self.current_comment_url = ''  # 当前评论的地址
        self.current_comment = ''  # 当前评论的内容
        self.comments_list = [""]  # 评论的列表，源于评论话术文件
        self.success_comment_count = "--等待中--"
        self.failure_comment_count = "--等待中--"
        self.current_index = 0  # 当前正在处理的任务的序号
        self.driver = self.__chrome()  # webdriver-Chrome
        self.wait = WebDriverWait(self.driver, 100)  # webdriver等待器
        self.__pause = False  # 标志是否暂停浏览器操作的状态
        self.pause_time = "--未暂停--"  # 显示任务执行中暂停的时间点
        self.__interval = interval  # 操作之间的时间间隔
        self.__is_random_interval = is_random_interval  # 是否随机设置操作之间的时间间隔
        self.__is_like = is_like  # 是否进行点赞操作
        self.__is_collect = is_collect  # 是否进行收藏操作
        self.__is_follow = is_follow  # 是否进行关注操作
        self.__is_comment = is_comment  # 是否进行评论操作
        self.__is_check_shield = is_check_shield  # 是否检查评论被屏蔽操作
        self.__is_shield_retry = is_shield_retry  # 是否屏蔽后重试
        self.__user_id = 0  # 用户ID，一个web对应一个用户，用于标识当前用户
        self.__add_text_signal: AddTextSignal = add_text_signal  # 存储监控日志添加的信号
        self.__is_skip_collect = is_skip_collect  # 是否跳过已收藏的帖子
        self.__is_again_comment_collect = is_again_comment_collect  # 是否取消收藏再评论再收藏
        self.__shield_retry_count = shield_retry_count  # 重试次数
        self.__is_cyclic_mode = is_cyclic_mode  # 是否开启循环模式
        self.__is_append_rare_word = is_append_rare_word  # 是否添加生僻字
        self.__rare_words_num = rare_words_num  # 添加生僻字的数量
        self.__interval_minute = interval_minute  # 间隔分钟，当任务列表没变化时，循环模式下再次检测的时间

    def getPause(self):
        """
        获取浏览器暂停状态
        :return: bool，暂停状态
        """
        return self.__pause

    def setPause(self):
        """
        设置浏览器暂停状态并更改pause_time
        """
        self.__pause = not self.__pause
        if self.__pause:
            self.pause_time = self.__now_time()
        else:
            self.pause_time = "--未暂停--"

    def __get_rare_word(self):
        return ''.join(random.choices(RARE_WORDS, k=self.__rare_words_num))

    @staticmethod
    def __now_time():
        """
        获取当前时间
        :return: 当前时间
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        logger.info(f'Creating chrome driver.')
        options = Options()
        for key, value in options_dict.items():
            options.add_argument(f"--{key}={value}")
        service = Service(executable_path='./chromedriver.exe')
        return Chrome(service=service, options=options)

    def file2list(self, path: str = None):
        """
        将文件中的每一行处理成列表
        :param path: 文件路径
        :return: 列表
        """
        path = path or self.comment_path
        logger.info(f'Thread {self.name} notification: Load the txt file.')
        datas = []
        with open(path, "r", encoding="utf8") as fr:
            for line in fr:
                datas.append(line.strip("\n").strip())
        return datas

    def open(self, url=None):
        """
        打开指定网址
        :param url: 网址
        """
        url = url or self.__base_url
        self.driver.get(url)
        logger.info(f'Open url -- {url}')

    def close(self):
        """
        关闭浏览器
        """
        self.driver.close()
        self.driver.service.stop()
        logger.info(f'Thread {self.name} notification: Webdriver destruction.')

    def __wait4login(self):
        """
        等待用户登录
        :return: 布尔值，返回False则表示登录中途出现问题，无法再检测，返回True表示登录成功
        """
        self.__add_text_signal.signal.emit("提示：登录状态检测中")
        logger.info(
            f'Login state detection in progress.')
        while True:
            time.sleep(1)
            try:
                value = '//*[@id="global"]/div[2]/div[1]/ul/li[4]/div/a/span[2]'
                if self.driver.find_elements(By.XPATH, value)[-1].text == '我':
                    break
            except IndexError:
                pass
            except ConnectionError:
                logger.error(
                    f"Thread {self.name} notification: The Webdriver process has been lost.")
                return False
            except NoSuchWindowException:
                self.driver.service.stop()
                return False
            except Exception as e:
                logger.error(f"Thread {self.name} notification: {e}")
                return False
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：用户登录成功")
        logger.info(
            f'Thread {self.name} notification: The user has successfully logged in.')
        self.driver.minimize_window()
        return True

    def __search(self, key):
        """
        在搜索框中输入并搜索关键词
        :param key: 搜索关键词
        """
        self.driver.refresh()
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="search-input"]')))
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始搜索{key}")
        logger.info(f'Thread {self.name} notification: Begin search {key}.')
        search_input = self.driver.find_element(By.XPATH, '//input[@class="search-input"]')
        if search_input.get_attribute('value'):
            search_input.clear()
        search_input.send_keys(key)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search-icon"]')))
        search_btn = self.driver.find_element(By.XPATH, '//div[@class="search-icon"]')
        search_btn.click()
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：搜索{key}完毕")
        logger.info(f'Thread {self.name} notification: Search for "{key}" is complete.')

    def __filter(self, key: str):
        """
        根据指定关键词进行过滤操作
        :param key: 过滤关键词 比如：最新、最热、综合（默认）
        """
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="filter"]')))
        self.driver.find_element(By.XPATH, '//div[@class="filter"]').click()
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始进行筛选，按 {key} 进行筛选")
        logger.info(
            f'Thread {self.name} notification: Begin the selection process, filtering by {key}.')
        try:
            self.driver.find_element(By.XPATH, f'//span[text()=" {key} "]').click()
        except NoSuchElementException:
            if key == "综合":
                self.driver.find_element(By.XPATH, f'//span[text()=" 默认 "]').click()

    def __classify(self, key: str):
        """
        根据指定关键词进行分类操作
        :param key: 分类关键词 比如：全部、视频、图文
        """
        time.sleep(1)
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始进行分类，选中分类 --> {key}")
        logger.info(
            f'Thread {self.name} notification: Let\'s begin with categorization and sort based on the {key}.')
        try:
            classify_btn = self.driver.find_element(By.XPATH, f'//div[text()="{key.strip()}"]')
            self.driver.execute_script("arguments[0].click();", classify_btn)
        except NoSuchElementException:
            self.__filter(key)

    def __get_current_page_links(self):
        """
       获取当前页面的合法链接（单页未滚动）
       然后将连接存入require_comment_urls
       """
        time.sleep(1)
        sections = self.driver.find_elements(By.XPATH, '//section[@class="note-item"]')
        logger.debug(sections)
        for section in sections:
            if len(self.task_urls) == self.limit:
                break
            try:
                url = section.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if url not in self.task_urls:  # 修复重复的url问题
                    self.task_urls.append(url)
            except NoSuchElementException:
                pass

    def __collect_urls(self):
        """
        滚动页面，利用__get_current_page_links方法抓取
        同时统计链接的数量，最终数量小于任务目标量时也做了处理
        """
        self.driver.maximize_window()

        time.sleep(1)
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始统计链接抓取数量")
        logger.info(
            f'Thread {self.name} notification: Initiate the count of collected link quantity.')
        while len(self.task_urls) != self.limit:
            if self.__pause:
                self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：暂停中...")
            while self.__pause:
                time.sleep(1)
            self.__get_current_page_links()
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.find_element(By.XPATH, '//div[@class="end-container"]')
                self.__add_text_signal.signal.emit(
                    f"{self.__now_time()}  线程{self.name}提示：已经到底啦，链接数量貌似不足 {self.limit} 哦")
                break
            except NoSuchElementException:
                pass
        self.__add_text_signal.signal.emit(
            f"{self.__now_time()}  线程{self.name}提示：当前链接数量 {len(self.task_urls)}")
        logger.info(
            f'Thread {self.name} notification: The current number of links is {len(self.task_urls)}.')
        self.driver.minimize_window()

    def __like(self):
        """
        点赞操作
        """
        logger.info(f'Thread {self.name} notification: Click to like.')
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始点爱心")
        like = self.driver.find_element(By.XPATH, '//*[@id="noteContainer"]/div[3]/div[3]/div[1]/div[1]/span[1]')
        is_liked = like.find_element(By.TAG_NAME, 'use').get_attribute("xlink:href") == "#liked"
        if not is_liked:
            like.click()
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：结束点爱心")
        else:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：已经点过爱心了")

    def __get_collect_status(self):
        collect = self.driver.find_element(By.XPATH, '//span[@class="collect-wrapper"]')
        is_collected = collect.find_element(By.TAG_NAME, 'use').get_attribute("xlink:href") == "#collected"
        return collect, is_collected

    def __collect(self):
        """
        收藏操作
        """
        logger.info(f'Thread {self.name} notification: Click to collect.')
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始收藏")
        collect, is_collected = self.__get_collect_status()
        if not is_collected:
            collect.click()
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：结束收藏")
        else:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：已经收藏过了")

    def __cancel_collect(self):
        """
        取消收藏操作
        """
        logger.info(f'Thread {self.name} notification: Cancel collect.')
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：准备取消收藏")
        collect, is_collected = self.__get_collect_status()
        if is_collected:
            collect.click()
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：收藏过了，现在取消收藏")

    def __follow(self):
        """
        关注操作
        """
        logger.info(f'Thread {self.name} notification: Click to follow.')
        self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：开始关注")
        try:
            follow = self.driver.find_element(By.XPATH, '//*[@id="noteContainer"]/div[3]/div[1]/div/div[2]/button')
        except IndexError:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：关注失败")
            return
        try:
            follow.find_element(By.XPATH, '//span[text()="已关注"]')
        except Exception:
            follow.click()
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：关注成功")
        else:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：已经关注过了")

    def __comment(self, speech: str):
        """
        评论操作
        :param speech: 评论内容
        """
        time.sleep(1)
        comment_input = self.driver.find_element(By.XPATH, '//input[@class="comment-input"]')
        if comment_input.get_attribute("value"):
            comment_input.clear()
        comment_input.send_keys(speech)
        logger.info(f'Thread {self.name} notification: Sending a comment to the window.')
        time.sleep(1)
        comment_btn = self.driver.find_element(By.XPATH, '//button[@class="submit"]')
        logger.info(f'Thread {self.name} notification: Preparing to click on the comment button.')
        # comment_btn.click()  # 该点击在最小化时导致不可交互，应当用javascript模拟点击事件
        self.driver.execute_script("arguments[0].click();", comment_btn)
        logger.info(f'Thread {self.name} notification: commented on: \n\t\t{speech}')
        time.sleep(1)

    def __back_top(self):
        try:
            logger.info('Return to the top.')
            back_top = self.driver.find_element(By.XPATH, '//div[@class="back-top"]')
            self.driver.execute_script("arguments[0].click();", back_top)
        except NoSuchElementException:
            pass

    def __sleep(self):
        """
        暂时休眠，缓冲操作之间的空闲时间，防止被识别为机器
        :return:
        """
        interval = random.uniform(0.5, self.__interval) if self.__is_random_interval else self.__interval
        logger.info(f"Operation delay time: {interval}")
        time.sleep(interval)

    def __get(self, url: str):
        """
        打开指定网址并返回页面源码

        - 参考api
        https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id=652985ab0000000023019186&cursor=&top_comment_id=

        :param url: 网址
        :return: 页面源码
        """
        cookies = self.driver.get_cookies()
        headers = {
            'Cookie': '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        }
        response = requests.get(url, headers=headers)

        return response

    def __get_comment_status(self, url: str, comment: str):
        """
        获取评论状态
        :param url: 网址
        :param comment: 评论内容
        :return: 如果是-1，则被屏蔽，其他不管，当作未屏蔽处理
        """
        try:
            logger.info(
                f"Thread {self.name} notification: Searching for comments and their corresponding state values.")
            note_id = re.search(r'/explore/(\w{24})', url).group(1)
            response_data = json.loads(
                self.__get(f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={note_id}").text)
            self.__user_id = response_data["data"]["user_id"]
            for other_comment in response_data['data']['comments']:
                if other_comment['user_info']['user_id'] == self.__user_id and other_comment['content'] == comment:
                    if other_comment['status'] != -1:
                        return 0
                    return -1
            return -2
        except Exception as e:
            logger.error(f"Thread {self.name} notification: {e}")

    def __check_shield(self, url, comment):
        comment_status = self.__get_comment_status(url, comment)
        if comment_status == -1:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：评论已被屏蔽")
            return True
        elif comment_status == -2:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：评论失败")
            return True
        else:
            self.__add_text_signal.signal.emit(
                f"{self.__now_time()}  线程{self.name}提示：评论了 {comment}")
            return False

    def __task_execution(self, require_comment_urls):
        """
        执行任务操作
        """
        if self.__is_comment:
            self.comments_list = self.file2list(self.comment_path)
        for index, url in enumerate(require_comment_urls):
            self.__add_text_signal.signal.emit(
                f"{self.__now_time()}  线程{self.name}提示：操作第{index + 1}个任务中 url> {url}")
            logger.info(
                f'Thread {self.name} notification: Operating on the url in the {index + 1}th task: \n\t\t{url}')

            if self.__pause:
                self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：暂停中...")
            while self.__pause:
                time.sleep(1)
            self.current_comment_url = url
            self.current_index = index + 1
            self.open(url=url)
            time.sleep(1)
            self.current_comment = random.choice(self.comments_list) + self.__get_rare_word()
            if self.__is_like:
                self.__sleep()
                self.__like()
            if self.__is_follow:
                self.__sleep()
                self.__follow()
            if self.__is_comment and self.__is_again_comment_collect:
                self.__sleep()
                self.__cancel_collect()
            if self.__is_comment:
                self.__sleep()
                if self.__is_skip_collect and self.__get_collect_status()[1]:
                    self.__add_text_signal.signal.emit(
                        f"{self.__now_time()}  线程{self.name}提示：第{index + 1}个任务已跳过")
                    continue
                self.__comment(speech=self.current_comment)
                if self.__is_check_shield:  # 是否检查屏蔽
                    self.__sleep()
                    # 如果已经屏蔽 并且 需要重试
                    if self.__check_shield(url, self.current_comment) and self.__is_shield_retry:
                        self.failure_comment_count += 1
                        self.__sleep()  # 缓冲一下
                        for _ in range(self.__shield_retry_count):  # 尝试重试 最大次数 __shield_retry_count
                            self.current_comment = random.choice(self.comments_list) + self.__get_rare_word()
                            self.__comment(speech=self.current_comment)
                            self.__sleep()
                            if not self.__check_shield(url, self.current_comment):
                                self.failure_comment_count -= 1
                                self.success_comment_count += 1
                                # 当检查到没有被屏蔽后，跳出循环，不再重试
                                break
                    else:
                        self.success_comment_count += 1
                else:
                    self.success_comment_count = "未开启屏蔽检测"
                    self.failure_comment_count = "未开启屏蔽检测"
            else:
                self.success_comment_count = "未开启评论"
                self.failure_comment_count = "未开启评论"
            if self.__is_collect or (self.__is_comment and self.__is_again_comment_collect):
                self.__sleep()
                self.__collect()

            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：第{index + 1}个任务已完成")

    def __login_after(self, filter_key, keyword):
        """
        非循环模式下 登录后的具体操作
        :param filter_key: 过滤关键词
        :param keyword: 搜索关键词
        """
        try:
            collect_before_length = len(self.task_urls)
            self.__search(keyword)  # 开始搜索
            time.sleep(3)
            self.__filter(filter_key)  # 筛选
            if self.category_key == "先图文后视频":
                self.__classify("图文")  # 分类
                time.sleep(1)
                self.__collect_urls()  # 收集链接
                self.__back_top()  # 回到顶部
                self.limit *= 2
                time.sleep(1)
                self.__classify("视频")  # 分类
                time.sleep(1)
                self.__collect_urls()  # 收集链接
            else:
                self.__classify(self.category_key)  # 分类
                time.sleep(1)
                self.__collect_urls()  # 收集链接
            time.sleep(1)
            logger.info(f"Thread {self.name} notification: Task List\n{self.task_urls}")
            collect_after_length = len(self.task_urls)
            if collect_after_length > collect_before_length:
                if self.__is_cyclic_mode:
                    self.__task_execution(self.task_urls[collect_before_length:])
                else:
                    self.__task_execution(self.task_urls)
            else:
                if self.__is_cyclic_mode:
                    self.__add_text_signal.signal.emit(
                        f"{self.__now_time()}  线程{self.name}提示：任务列表没有变化，{self.__interval_minute}分钟后再去工作")
                    logger.info(
                        f"Thread {self.name} notification: The task list has not changed. Please return to work in {self.__interval_minute} minutes.")
                    time.sleep(self.__interval_minute * 60)  # 半小时后 再去工作
                else:
                    self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：任务列表没有变化")
                    logger.info(f"Thread {self.name} notification: The task list has not changed.")
            return True
        except NoSuchWindowException:
            self.driver.service.stop()
            return False
        except Exception as e:
            self.__add_text_signal.signal.emit(f"{self.__now_time()}  线程{self.name}提示：任务已经终止")
            logger.error(f"Thread {self.name} notification: {e}")
            return False

    def start(self, is_multiple: bool, keyword: str, filter_key: str):
        """
         启动浏览器
         :param is_multiple: 是否使用多关键词搜索
         :param keyword: 搜索关键词
         :param filter_key: 过滤关键词
         """
        index = 1
        self.open()
        if self.__wait4login():
            if self.__is_comment:
                self.success_comment_count = 0
                self.failure_comment_count = 0
            while True:
                logger.info(f"Thread {self.name} notification: The {index}th started")
                if is_multiple:
                    searches = self.file2list(keyword)
                    for search_line in searches:
                        if not self.__login_after(filter_key, search_line.strip("\n").strip()):
                            break
                else:
                    if not self.__login_after(filter_key, keyword):
                        break
                if not self.__is_cyclic_mode:
                    break
                index += 1
            self.close()


class BaseWidget(QWidget):
    """
    自定义窗口基类
    """

    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setAutoFillBackground(False)
        self.base_layout = QVBoxLayout(self)
        self.setLayout(self.base_layout)
        self.setStyleSheet("background-color: #ffffff;")
        self.centerWindow()

    def centerWindow(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


class BaseText(QLabel):
    """
    自定义文本类，继承自QLabel
    重写了样式 幼圆 加粗 16px 最小高度35
    """

    def __init__(self, text):
        super().__init__(text=text)
        self.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        font-family: YouYuan;
        """)
        self.setMinimumHeight(35)


class AddTextSignal(QObject):
    signal = pyqtSignal(str)


class ClickableText(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setMouseTracking(True)
        self.setToolTip('点击我即可复制哦~')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clipboard = QApplication.clipboard()
            mime_data = QMimeData()
            mime_data.setText(self.text())
            clipboard.setMimeData(mime_data)
            print("Text copied to clipboard:", self.text())


class MainWindow(BaseWidget):
    """
    view层 -- 主窗口类
    """

    def __init__(self):
        self.settings = Settings()
        logger.info("Load configurator.")
        super().__init__(self.settings.get('SoftwareConfig', 'title'))
        self.setWindowIcon(QIcon(self.settings.get('SoftwareConfig', 'icon')))
        self.current_time = None
        self.selected_comment_file_path = None
        self.selected_search_file_path = None
        self.threads = []
        self.initUI()
        self.initStyle()
        self.initEvents()
        self.filter_option = {
            self.filter_radio1: "综合",
            self.filter_radio2: "最新",
            self.filter_radio3: "最热"
        }
        self.category_option = {
            self.category_radio1: "全部",
            self.category_radio2: "图文",
            self.category_radio3: "视频",
            self.category_radio4: "先图文后视频"
        }
        self.loadConfig()
        self.onIsCyclicMode(self.is_cyclic_mode.isChecked())
        self.onIsCommentStateChanged(self.is_comment.isChecked())
        self.onIsRandomRareWord(self.is_random_rare_word.isChecked())
        self.onIsSkipCollect(self.is_skip_collect.isChecked())
        self.onIsAgainCommentCollect(self.is_again_comment_collect.isChecked())
        self.onIsCheckShield(self.is_check_shield.isChecked())
        self.onIsShieldRetry(self.is_shield_retry.isChecked())

    def initUI(self):
        """
        初始化控件
        :return:
        """
        logger.info('Initialize UI.')

        self.h_separator = QFrame()
        self.h_separator.setFrameShape(QFrame.HLine)
        self.h_separator.setLineWidth(1)
        self.v_separator1 = QFrame()
        self.v_separator1.setFrameShape(QFrame.VLine)
        self.v_separator1.setLineWidth(1)
        self.v_separator2 = QFrame()
        self.v_separator2.setFrameShape(QFrame.VLine)
        self.v_separator2.setLineWidth(1)

        self.total_layout = QHBoxLayout()
        self.monitor_layout = QVBoxLayout()
        self.fixed_monitor_layout = QGridLayout()
        self.fixed_monitor_label = QLabel("当前线程数据监控")
        self.fixed_monitor_label.setAlignment(Qt.AlignCenter)
        self.fixed_monitor_layout.addWidget(BaseText("线程序号："), 0, 0)
        self.thread_num_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.thread_num_label, 0, 1)
        self.fixed_monitor_layout.addWidget(BaseText("线程名："), 0, 2)
        self.thread_name_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.thread_name_label, 0, 3)
        self.fixed_monitor_layout.addWidget(BaseText("线程状态："), 0, 4)
        self.thread_status_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.thread_status_label, 0, 5)
        self.fixed_monitor_layout.addWidget(BaseText("创建时间："), 1, 0)
        self.create_time_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.create_time_label, 1, 1)
        self.fixed_monitor_layout.addWidget(BaseText("暂停时间："), 1, 2)
        self.last_pause_time_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.last_pause_time_label, 1, 3)
        self.fixed_monitor_layout.addWidget(BaseText("任务地址（单击复制）"), 4, 0)
        self.current_url_label = ClickableText()
        self.current_url_label.setWordWrap(True)
        self.fixed_monitor_layout.addWidget(self.current_url_label, 4, 1, 1, 5, alignment=Qt.AlignVCenter)
        self.fixed_monitor_layout.addWidget(BaseText("评论内容（单击复制）"), 5, 0)
        self.comment_content_label = ClickableText()
        self.comment_content_label.setWordWrap(True)
        self.fixed_monitor_layout.addWidget(self.comment_content_label, 5, 1, 1, 5, alignment=Qt.AlignVCenter)
        self.fixed_monitor_layout.addWidget(BaseText("工作时长："), 2, 0)
        self.working_time_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.working_time_label, 2, 1)
        self.fixed_monitor_layout.addWidget(BaseText("抓链进度："), 2, 2)
        self.progress1_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.progress1_label, 2, 3)
        self.fixed_monitor_layout.addWidget(BaseText("任务进度："), 2, 4)
        self.progress2_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.progress2_label, 2, 5)
        self.fixed_monitor_layout.addWidget(BaseText("成功评论："), 3, 0)
        self.success_comment_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.success_comment_label, 3, 1)
        self.fixed_monitor_layout.addWidget(BaseText("被屏蔽条数："), 3, 2)
        self.failure_comment_label = QLabel()
        self.fixed_monitor_layout.addWidget(self.failure_comment_label, 3, 3)
        self.dynamic_monitor_layout = QVBoxLayout()
        self.dynamic_monitor_title = QHBoxLayout()
        self.dynamic_monitor_label = QLabel("所有线程的监控日志区")
        self.dynamic_monitor_label.setContentsMargins(0, 5, 0, 5)
        self.dynamic_monitor_label.setAlignment(Qt.AlignCenter)
        self.dynamic_monitor_title.addWidget(self.dynamic_monitor_label)
        self.clear_log_button = QPushButton("清除")
        self.clear_log_button.setMaximumWidth(50)
        self.dynamic_monitor_title.addWidget(self.clear_log_button)
        self.dynamic_monitor_layout.addLayout(self.dynamic_monitor_title)
        self.dynamic_monitor_text = QTextEdit()
        self.dynamic_monitor_text.setReadOnly(True)
        self.dynamic_monitor_text.setMinimumSize(600, 500)
        self.dynamic_monitor_layout.addWidget(self.dynamic_monitor_text)
        self.monitor_layout.addWidget(self.fixed_monitor_label)
        self.monitor_layout.addLayout(self.fixed_monitor_layout)
        self.monitor_layout.addLayout(self.dynamic_monitor_layout)
        self.monitor_layout.setContentsMargins(10, 0, 10, 0)

        self.operate_layout = QVBoxLayout()
        self.keyword_input = QLineEdit()
        self.filter_radio1 = QRadioButton("综合")
        self.filter_radio2 = QRadioButton("最新")
        self.filter_radio3 = QRadioButton("最热")
        self.category_radio1 = QRadioButton("混合采集")
        self.category_radio2 = QRadioButton("采集图文")
        self.category_radio3 = QRadioButton("采集视频")
        self.category_radio4 = QRadioButton("先图文后视频")
        self.is_use_multiple_file = QCheckBox("使用多关键词搜索模式")
        self.btn_open_search_file = QPushButton("请选择多关键词文件")
        self.file_dialog = None
        self.keyword_group = QGroupBox("搜索词")
        self.keyword_layout = QVBoxLayout()
        self.keyword_layout.addWidget(self.is_use_multiple_file)
        self.keyword_layout.addWidget(self.btn_open_search_file)
        self.keyword_layout.addWidget(self.keyword_input)
        self.keyword_group.setLayout(self.keyword_layout)

        self.filter_classify_layout = QHBoxLayout()
        self.filter_group = QGroupBox("筛选依据")
        self.filter_layout = QVBoxLayout()
        self.filter_layout.addWidget(self.filter_radio1)
        self.filter_layout.addWidget(self.filter_radio2)
        self.filter_layout.addWidget(self.filter_radio3)
        self.filter_group.setLayout(self.filter_layout)
        self.category_group = QGroupBox("分类依据")
        self.category_layout = QVBoxLayout()
        self.category_layout.addWidget(self.category_radio1)
        self.category_layout.addWidget(self.category_radio2)
        self.category_layout.addWidget(self.category_radio3)
        self.category_layout.addWidget(self.category_radio4)
        self.category_group.setLayout(self.category_layout)
        self.filter_classify_layout.addWidget(self.filter_group)
        self.filter_classify_layout.addWidget(self.category_group)

        self.task_limit_group = QGroupBox("任务设置")
        self.task_limit_layout = QVBoxLayout()
        self.task_limit_spinbox = QSpinBox()
        self.task_limit_spinbox.setRange(1, 1000)  # 限制为1~1000之间的数字
        self.task_limit_layout.addWidget(QLabel("设置任务目标数量（单位） - 最大1000单位"))
        self.task_limit_layout.addWidget(self.task_limit_spinbox)
        self.target1_h_layout = QHBoxLayout()
        self.is_cyclic_mode = QCheckBox("循环模式")
        self.loop_interval_minute_label = QLabel("间隔时间(分钟)")
        self.loop_interval_minute = QSpinBox()
        self.loop_interval_minute.setRange(1, 10080)  # 限制为1~10080之间的数字 7天
        self.target1_h_layout.addWidget(self.is_cyclic_mode)
        self.target1_h_layout.addWidget(self.loop_interval_minute_label)
        self.target1_h_layout.addWidget(self.loop_interval_minute)
        self.target1_h_layout.addStretch()
        self.task_limit_layout.addLayout(self.target1_h_layout)
        self.target2_h_layout = QHBoxLayout()
        self.is_like = QCheckBox("顺手点赞")
        self.is_collect = QCheckBox("顺手收藏")
        self.is_follow = QCheckBox("顺手关注")
        self.target2_h_layout.addWidget(self.is_like)
        self.target2_h_layout.addWidget(self.is_collect)
        self.target2_h_layout.addWidget(self.is_follow)
        self.task_limit_layout.addLayout(self.target2_h_layout)
        self.target3_h_layout = QHBoxLayout()
        self.is_comment = QCheckBox("是否评论")
        self.is_skip_collect = QCheckBox("跳过已收藏")
        self.is_again_comment_collect = QCheckBox("再评论再收藏")
        self.target3_h_layout.addWidget(self.is_comment)
        self.target3_h_layout.addWidget(self.is_skip_collect)
        self.target3_h_layout.addWidget(self.is_again_comment_collect)
        self.target3_h_layout.addStretch()
        self.task_limit_layout.addLayout(self.target3_h_layout)
        self.target4_h_layout = QHBoxLayout()
        self.is_random_rare_word = QCheckBox("随机生僻字")
        self.rare_word_h_layout = QHBoxLayout()
        self.rare_word_label = QLabel("数量")
        self.rare_word_spinbox = QSpinBox()
        self.rare_word_spinbox.setRange(1, 20)  # 限制为1~20之间的数字
        self.rare_word_h_layout.addWidget(self.rare_word_label)
        self.rare_word_h_layout.addWidget(self.rare_word_spinbox)
        self.target4_h_layout.addWidget(self.is_random_rare_word)
        self.target4_h_layout.addLayout(self.rare_word_h_layout)
        self.target4_h_layout.addStretch()
        self.task_limit_layout.addLayout(self.target4_h_layout)
        self.target5_h_layout = QHBoxLayout()
        self.is_check_shield = QCheckBox("检查屏蔽")
        self.is_shield_retry = QCheckBox("屏蔽后重试")
        self.shield_retry_count = QSpinBox()
        self.shield_retry_count.setRange(1, 10)  # 限制为1~10之间的数字
        self.target5_h_layout.addWidget(self.is_check_shield)
        self.target5_h_layout.addWidget(self.is_shield_retry)
        self.target5_h_layout.addWidget(self.shield_retry_count)
        self.target5_h_layout.addStretch()
        self.task_limit_layout.addLayout(self.target5_h_layout)
        self.task_limit_group.setLayout(self.task_limit_layout)

        self.time_group = QGroupBox("时间设置")
        self.time_layout = QVBoxLayout()
        self.interval_label = QLabel("设置任务间隔时间（秒） - 最大300秒")
        self.task_interval_second = QSpinBox()
        self.task_interval_second.setRange(1, 300)  # 限制为1~300之间的数字
        self.is_random_interval = QCheckBox("间隔时间随机")
        self.btn_open_comment_file = QPushButton("请选择评论文案")
        self.time_layout.addWidget(self.interval_label)
        self.time_layout.addWidget(self.task_interval_second)
        self.time_layout.addWidget(self.is_random_interval)
        self.time_layout.addWidget(self.btn_open_comment_file)
        self.time_group.setLayout(self.time_layout)

        self.btn_h_layout = QHBoxLayout()
        self.run_button = QPushButton("Start")
        self.pause_button = QPushButton("暂停/恢复")
        self.save_button = QPushButton("保存配置")
        self.btn_h_layout.addWidget(self.run_button)
        self.btn_h_layout.addWidget(self.pause_button)
        self.btn_h_layout.addWidget(self.save_button)

        self.operate_layout.addWidget(self.keyword_group)
        self.operate_layout.addLayout(self.filter_classify_layout)
        self.operate_layout.addWidget(self.task_limit_group)
        self.operate_layout.addWidget(self.time_group)
        self.operate_layout.addLayout(self.btn_h_layout)
        self.operate_layout.setContentsMargins(0, 10, 10, 10)

        self.browsers_layout = QVBoxLayout()
        self.browsers_list = QListWidget()
        self.browsers_layout_title = QLabel("浏览器多开线程列表")
        self.browsers_layout_title.setAlignment(Qt.AlignCenter)
        self.browsers_layout.addWidget(self.browsers_layout_title)
        self.browsers_layout.addWidget(self.browsers_list)
        self.browsers_layout.setContentsMargins(10, 10, 0, 10)

        self.total_layout.addLayout(self.browsers_layout)
        self.total_layout.addWidget(self.v_separator1)
        self.total_layout.addLayout(self.monitor_layout)
        self.total_layout.addWidget(self.v_separator2)
        self.total_layout.addLayout(self.operate_layout)
        self.base_layout.addLayout(self.total_layout)

    def initStyle(self):
        """
        初始化样式
        :return:
        """
        logger.info('Initialize the UI style.')
        self.keyword_input.setStyleSheet("""
            QLineEdit {
                min-width: 300px;
                min-height: 30px;
                border: 1px solid #cccccc;
                border-radius: 15px;
                padding: 2px 5px;
                background-color: #f5f5f5;
            }
            QLineEdit:hover {
                border-color: #999999;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #007AFF;
                background-color: #ffffff;
                outline: none;
            }
        """)
        self.run_button.setStyleSheet("""
            QPushButton {
                height: 40px;
                font-size: 15px;
                color: white;
                border: none;
                border-radius: 5px;
                background-color: #007AFF;  /* 设置背景颜色 */
            }

            QPushButton:hover {
                background-color: #05A0E8;  /* 设置鼠标悬停时的背景颜色 */
            }
        """)
        self.pause_button.setStyleSheet("""
            QPushButton {
                height: 36px;
                font-size: 15px;
                color: #007AFF;
                border: 2px solid #007AFF;
                border-radius: 5px;
                background-color: white;  /* 设置背景颜色 */
            }

            QPushButton:hover {
                background-color: #f7f7f7;  /* 设置鼠标悬停时的背景颜色 */
            }
        """)
        self.save_button.setStyleSheet("""
            QPushButton {
                height: 36px;
                font-size: 15px;
                color: #007AFF;
                border: 2px solid #007AFF;
                border-radius: 5px;
                background-color: white;  /* 设置背景颜色 */
            }

            QPushButton:hover {
                background-color: #f7f7f7;  /* 设置鼠标悬停时的背景颜色 */
            }
        """)
        self.clear_log_button.setStyleSheet("""
            QPushButton {
                max-height: 36px;
                font-size: 15px;
                color: #007AFF;
                border: 2px solid #007AFF;
                border-radius: 10px;
                background-color: white;  /* 设置背景颜色 */
            }

            QPushButton:hover {
                background-color: #f7f7f7;  /* 设置鼠标悬停时的背景颜色 */
            }
        """)
        self.keyword_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;  /* 设置组框标题的字号 */
                font-weight: bold;  /* 设置标题文字为加粗 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; 
                padding: 0 3px;
            }
        """)
        self.filter_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;  /* 设置组框标题的字号 */
                font-weight: bold;  /* 设置标题文字为加粗 */
            }
        """)
        self.category_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;  /* 设置组框标题的字号 */
                font-weight: bold;  /* 设置标题文字为加粗 */
            }
        """)
        self.task_limit_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;  /* 设置组框标题的字号 */
                font-weight: bold;  /* 设置标题文字为加粗 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; 
                padding: 0 3px;
            }
                """)
        self.time_group.setStyleSheet("""
                    QGroupBox {
                        font-size: 16px;  /* 设置组框标题的字号 */
                        font-weight: bold;  /* 设置标题文字为加粗 */
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top center; 
                        padding: 0 3px;
                    }
                        """)
        self.fixed_monitor_label.setStyleSheet('color: #007AFF; font-size: 17px; font-weight: bold;')
        self.browsers_layout_title.setStyleSheet('color: #007AFF; font-size: 17px; font-weight: bold;')
        self.dynamic_monitor_label.setStyleSheet('color: #007AFF; font-size: 17px; font-weight: bold;')
        self.dynamic_monitor_text.setStyleSheet(
            'background-color: #f9f9f9; border: none; color: #333; font-size: 16px;')
        self.browsers_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QListWidget::item{
                font-size: 15px;
                min-height: 35px;
            }
        """)
        self.btn_open_search_file.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: #3498db;
                min-height: 30px;
                border-style: solid;
                padding: 2px 5px;
                border-width: 1px;
                border-radius: 15px;
                border-color: #2980b9;
            }
        
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.btn_open_comment_file.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: #3498db;
                min-height: 30px;
                border-style: solid;
                padding: 2px 5px;
                border-width: 1px;
                border-radius: 15px;
                border-color: #2980b9;
            }
        
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.h_separator.setStyleSheet("background-color: #f8f8f8 !important; border: none;")
        self.v_separator1.setStyleSheet("background-color: #f8f8f8 !important; border: none;")
        self.v_separator2.setStyleSheet("background-color: #f8f8f8 !important; border: none;")

    def initEvents(self):
        """
        初始化事件
        :return:
        """
        logger.info('Initialize the events.')
        self.clear_log_button.clicked.connect(self.clear_dynamic_log)
        self.is_use_multiple_file.stateChanged.connect(self.toggle_search_input_mode)
        self.btn_open_search_file.clicked.connect(lambda: self.open_file_dialog_window("SEARCH"))
        self.is_random_interval.stateChanged.connect(self.toggle_interval_mode)
        self.is_cyclic_mode.stateChanged.connect(self.onIsCyclicMode)
        self.is_comment.stateChanged.connect(self.onIsCommentStateChanged)
        self.is_skip_collect.stateChanged.connect(self.onIsSkipCollect)
        self.is_again_comment_collect.stateChanged.connect(self.onIsAgainCommentCollect)
        self.is_random_rare_word.stateChanged.connect(self.onIsRandomRareWord)
        self.is_check_shield.stateChanged.connect(self.onIsCheckShield)
        self.is_shield_retry.stateChanged.connect(self.onIsShieldRetry)
        self.btn_open_comment_file.clicked.connect(lambda: self.open_file_dialog_window("COMMENTS"))
        self.pause_button.clicked.connect(self.pause_thread)
        self.run_button.clicked.connect(self.start_automation)
        self.save_button.clicked.connect(self.save_config)
        self.browsers_list.clicked.connect(self.update_thread_information)
        self.add_text_signal = AddTextSignal()
        self.add_text_signal.signal.connect(self.append_dynamic_log)

    def start_automation(self):
        """
        启动小红书自动化
        首先获取用户输入的搜索关键词，如果勾选了“使用多个关键词文件”，则通过文件选择框获取关键词文件路径，并将其中的关键词作为搜索关键词使用。
        判断用户勾选的筛选条件和分类条件，并传递参数给 create_browser 方法创建浏览器实例并开始自动化操作。
        同时也记录了线程、时间等信息
        """
        logger.info(
            'According to the parameters, a browser instance is generated and prepared to start automation.')
        keyword = self.keyword_input.text()
        if self.is_use_multiple_file.isChecked():
            if not self.selected_search_file_path:
                self.add_text_signal.signal.emit("提示：请务必指定一个关键词文件，该文件是txt文本，每一行是一个关键词")
                return
            else:
                keyword = self.selected_search_file_path
                logger.info(f'The file that prepares multiple searches is {keyword}')
        else:
            if not keyword:
                self.add_text_signal.signal.emit("提示：请务必输入搜索关键词")
                return
            else:
                logger.info(f'The word to be searched is {keyword}')
        filter_key = next(self.filter_option[item] for item in self.filter_option if item.isChecked())
        logger.info(f'The selected keywords are {filter_key}')
        category_key = next(self.category_option[item] for item in self.category_option if item.isChecked())
        logger.info(f'The keywords of the category are {category_key}')
        limit = self.task_limit_spinbox.value()
        logger.info(f'The number of tasks is {limit}')
        if self.is_skip_collect.isChecked():
            if not self.is_comment.isChecked():
                self.add_text_signal.signal.emit("提示：使用 跳过收藏 需要勾选 是否评论")
                return
            else:
                logger.info(f'Activate skip favorite mode.')

        if self.is_again_comment_collect.isChecked():
            if not self.is_comment.isChecked():
                self.add_text_signal.signal.emit("提示：使用 取消收藏再评论再收藏 需要勾选 是否评论")
                return
            else:
                logger.info(f'Enabled the mode of canceling a favorite, commenting, and then favorite again.')
        if self.is_comment.isChecked():
            if not self.selected_comment_file_path:
                self.add_text_signal.signal.emit(
                    "提示：请务必指定一个评论话术文件，该文件是txt文本，每一行都属于评论的内容。")
                return
            else:
                logger.info(
                    f'The commentary discourse file is {self.selected_comment_file_path}')

        thread = threading.Thread(
            target=self.create_and_execute_browser,
            args=(keyword, filter_key, category_key, limit),
            daemon=True)
        self.threads.append(dict(thread=thread))
        thread.start()
        logger.info('<create_browser> Thread started!')
        self.threads[-1].setdefault("id", thread.ident)
        if self.is_use_multiple_file.isChecked():
            thread.name = f"{filter_key}-多关键词-{category_key}-{thread.ident}"
        else:
            thread.name = f"{filter_key}-{keyword}-{category_key}-{thread.ident}"
        self.threads[-1].setdefault("name", thread.name)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.threads[-1].setdefault("time", now_time)
        self.load_thread_items()
        time.sleep(1)
        monitor = threading.Thread(
            target=self.start_thread_monitoring,
            daemon=True)
        monitor.start()
        logger.info('<msg_monitor> Thread started!')

    def pause_thread(self):
        """
        暂停用户当前选中的线程实例对应的浏览器的任务操作
        每次暂停以一个任务为最小基本单元，不可分割，不可扩大；
        一个任务可能包含以下流程：点赞、收藏、关注、评论等。
        :return:
        """
        current_row = self.browsers_list.currentIndex().row()
        if current_row != -1:
            logger.info('Emit to pause the thread.')
            self.threads[current_row].get('browser').setPause()

    def loadConfig(self):
        logger.info("The configuration is loading")
        if self.settings.get('SearchConfig', 'search-mode') == 'multiple':
            self.is_use_multiple_file.setChecked(True)
            if self.settings.get("SearchConfig", "search-key") == '':
                self.btn_open_search_file.setText("请选择多关键词文件")
            else:
                self.selected_search_file_path = self.settings.get("SearchConfig", "search-key")
                self.btn_open_search_file.setText(self.selected_search_file_path.split('/')[-1])
        else:
            self.is_use_multiple_file.setChecked(False)
            self.keyword_input.setText(self.settings.get("SearchConfig", "search-key"))
            self.btn_open_search_file.setVisible(False)
        for item, text in self.filter_option.items():
            if text == self.settings.get("FilterClassify", "filter-mode"):
                item.setChecked(True)
                break
        for item, text in self.category_option.items():
            if text == self.settings.get("FilterClassify", "category-mode"):
                item.setChecked(True)
                break
        self.task_limit_spinbox.setValue(int(self.settings.get("TaskConfig", "task-count")))
        self.is_cyclic_mode.setChecked(self.settings.get("TaskConfig", "cyclic-mode"))
        self.loop_interval_minute.setValue(int(self.settings.get("TaskConfig", "interval-minute")))
        self.is_like.setChecked(self.settings.get("TaskConfig", "is-like"))
        self.is_collect.setChecked(self.settings.get("TaskConfig", "is-collect"))
        self.is_follow.setChecked(self.settings.get("TaskConfig", "is-follow"))
        self.is_comment.setChecked(self.settings.get("TaskConfig", "is-comment"))
        self.is_skip_collect.setChecked(self.settings.get("TaskConfig", "is-skip-collect"))
        self.is_again_comment_collect.setChecked(self.settings.get("TaskConfig", "is-again-comment-collect"))
        self.is_random_rare_word.setChecked(self.settings.get("TaskConfig", "is-random-rare-word"))
        self.rare_word_spinbox.setValue(int(self.settings.get("TaskConfig", "rare-word-count")))
        self.is_check_shield.setChecked(self.settings.get("TaskConfig", "is-check-shield"))
        self.is_shield_retry.setChecked(self.settings.get("TaskConfig", "is-shield-retry"))
        self.shield_retry_count.setValue(int(self.settings.get("TaskConfig", "retry-count")))
        self.task_interval_second.setValue(int(self.settings.get("TimeConfig", "task-interval-time")))
        self.is_random_interval.setChecked(self.settings.get("TimeConfig", "is-random-interval-time"))
        if self.settings.get("TimeConfig", "comment-text") == '':
            self.btn_open_comment_file.setText("请选择评论文案")
        else:
            self.selected_comment_file_path = self.settings.get("TimeConfig", "comment-text")
            self.btn_open_comment_file.setText(self.selected_comment_file_path.split('/')[-1])
        self.add_text_signal.signal.emit("提示：配置加载成功")
        logger.info("Configuration loaded successfully.")

    def save_config(self):
        logger.info("Saving configuration...")
        if self.is_use_multiple_file.isChecked():
            self.settings.set("SearchConfig", "search-mode", "multiple")
            self.settings.set("SearchConfig", "search-key",
                              f"{self.selected_search_file_path if self.selected_search_file_path else ''}")
        else:
            self.settings.set("SearchConfig", "search-mode", "single")
            self.settings.set("SearchConfig", "search-key", f"{self.keyword_input.text()}")
        filter_key = next(self.filter_option[item] for item in self.filter_option if item.isChecked())
        self.settings.set("FilterClassify", "filter-mode", f"{filter_key}")
        category_key = next(self.category_option[item] for item in self.category_option if item.isChecked())
        logger.debug(f"filter_key = {filter_key}, category_key = {category_key}.")
        self.settings.set("FilterClassify", "category-mode", f"{category_key}")
        self.settings.set("TaskConfig", "task-count", f"{self.task_limit_spinbox.value()}")
        self.settings.set("TaskConfig", "cyclic-mode", f"{self.is_cyclic_mode.isChecked()}")
        self.settings.set("TaskConfig", "interval-minute", f"{self.loop_interval_minute.value()}")
        self.settings.set("TaskConfig", "is-like", f"{self.is_like.isChecked()}")
        self.settings.set("TaskConfig", "is-collect", f"{self.is_collect.isChecked()}")
        self.settings.set("TaskConfig", "is-follow", f"{self.is_follow.isChecked()}")
        self.settings.set("TaskConfig", "is-comment", f"{self.is_comment.isChecked()}")
        self.settings.set("TaskConfig", "is-skip-collect", f"{self.is_skip_collect.isChecked()}")
        self.settings.set("TaskConfig", "is-again-comment-collect", f"{self.is_again_comment_collect.isChecked()}")
        self.settings.set("TaskConfig", "is-random-rare-word", f"{self.is_random_rare_word.isChecked()}")
        self.settings.set("TaskConfig", "rare-word-count", f"{self.rare_word_spinbox.value()}")
        self.settings.set("TaskConfig", "is-check-shield", f"{self.is_check_shield.isChecked()}")
        self.settings.set("TaskConfig", "is-shield-retry", f"{self.is_shield_retry.isChecked()}")
        self.settings.set("TaskConfig", "retry-count", f"{self.shield_retry_count.value()}")
        self.settings.set("TimeConfig", "task-interval-time", f"{self.task_interval_second.value()}")
        self.settings.set("TimeConfig", "is-random-interval-time", f"{self.is_random_interval.isChecked()}")
        self.settings.set("TimeConfig", "comment-text",
                          f"{self.selected_comment_file_path if self.selected_comment_file_path else ''}")
        self.settings.save()
        self.add_text_signal.signal.emit("提示：当前配置保存成功")
        logger.info("The configuration has been successfully saved.")

    def create_and_execute_browser(self, keyword: str, filter_key: str, category_key: str, limit: int):
        """
        该方法用于创建浏览器实例并执行小红书自动化操作。
        根据用户设置的各项操作条件，进行对应的操作（收藏、点赞、关注、评论等）。
        同时，通过检查屏蔽用户的条件过滤掉需要跳过的用户
        :param keyword:搜索关键词或关键词文件路径
        :param filter_key:筛选条件，包括“综合”、“最新”、“最热”
        :param category_key:分类条件，包括“视频”、“图文”、“全部”
        :param limit:搜索结果数目限制
        :return:
        """
        is_random_interval = self.is_random_interval.isChecked()
        interval = self.task_interval_second.value()
        is_like = self.is_like.isChecked()
        is_collect = self.is_collect.isChecked()
        is_follow = self.is_follow.isChecked()
        is_comment = self.is_comment.isChecked()
        is_check_shield = self.is_check_shield.isChecked()
        is_skip_collect = self.is_skip_collect.isChecked()
        is_again_comment_collect = self.is_again_comment_collect.isChecked()
        is_shield_retry = self.is_shield_retry.isChecked()
        shield_retry_count = self.shield_retry_count.value()
        is_cyclic_mode = self.is_cyclic_mode.isChecked()
        interval_minute = self.loop_interval_minute.value()
        is_append_rare_word = self.is_random_rare_word.isChecked()
        rare_words_num = self.rare_word_spinbox.value() if is_append_rare_word else 0

        browser = Browser(view=self, is_random_interval=is_random_interval, interval=interval,
                          comment_path=self.selected_comment_file_path,
                          is_like=is_like, is_collect=is_collect, is_follow=is_follow,
                          is_comment=is_comment, limit=limit, is_check_shield=is_check_shield,
                          add_text_signal=self.add_text_signal, is_skip_collect=is_skip_collect,
                          is_again_comment_collect=is_again_comment_collect,
                          is_shield_retry=is_shield_retry, shield_retry_count=shield_retry_count,
                          is_cyclic_mode=is_cyclic_mode, interval_minute=interval_minute,
                          is_append_rare_word=is_append_rare_word, rare_words_num=rare_words_num,
                          category_key=category_key)
        self.threads[-1].setdefault("browser", browser)
        logger.info('Creating a browser and executing automation.')
        browser.start(self.is_use_multiple_file.isChecked(), keyword, filter_key)

    def load_thread_items(self):
        """
        将线程实例信息加载到列表中显示出来。为每个线程分配一个 id、名称等信息。
        :return:
        """
        self.browsers_list.clear()
        for thread in self.threads:
            item = QListWidgetItem(f"{thread.get('id', '未获取到线程id')} ——> {thread.get('name', '未命名')}")
            self.browsers_list.addItem(item)
        logger.info('Loading items into a list control.')
        self.browsers_list.setCurrentRow(len(self.threads) - 1)
        self.browsers_list.item(len(self.threads) - 1).setSelected(True)

    def update_thread_information(self):
        """
        监视当前选中的线程实例的状态，并在界面上显示相关信息，如运行时间、浏览器的评论 URL、当前评论内容和任务进度等信息
        :return:
        """
        index = self.browsers_list.currentIndex().row()
        thread = self.threads[index].get('thread')
        try:
            browser = self.threads[index].get('browser')
            browser.name = self.threads[index].get('name', '未命名')
            self.last_pause_time_label.setText(browser.pause_time)
            self.last_pause_time_label.setStyleSheet(
                "color: #FF0000;" if browser.getPause() else "color: #007AFF;")
            self.current_url_label.setText(browser.current_comment_url)
            self.comment_content_label.setText(browser.current_comment)
            if thread.is_alive():
                time_difference = self.calculate_time_difference(browser.create_time, self.current_time)
                self.working_time_label.setText("%d 小时 %d 分钟 %d 秒" % time_difference)
                self.working_time_label.setStyleSheet("color: #007AFF;")
            else:
                self.working_time_label.setStyleSheet("color: #FF0000;")

            self.progress1_label.setText(f"{len(browser.task_urls)} / {browser.limit}")
            self.progress2_label.setText(f"{browser.current_index} / {browser.limit}")
            self.success_comment_label.setText(f"{browser.success_comment_count}")
            self.failure_comment_label.setText(f"{browser.failure_comment_count}")
        except Exception as e:
            logger.error(f"Thread {thread.name} notification: {e}")
        self.thread_num_label.setText(str(self.threads[index].get('id', '未获取到线程id')))
        self.thread_name_label.setText(self.threads[index].get('name', '未命名'))
        if thread and isinstance(thread, threading.Thread):
            self.thread_status_label.setText("正常存活中" if thread.is_alive() else "已终止")
            self.thread_status_label.setStyleSheet(
                "color: #007AFF;" if thread.is_alive() else "color: #FF0000;")
        self.create_time_label.setText(self.threads[index].get('time', '创建时间显示异常'))

    def start_thread_monitoring(self):
        """
        线程启动监视系统，每秒钟轮询一次当前选中的线程实例，调用 show_msg 方法显示状态信息
        :return:
        """
        logger.info(
            'The monitoring system with a one-second polling interval has been activated.')
        while True:
            self.current_time = datetime.datetime.now().time()
            time.sleep(2)
            self.update_thread_information()

    def toggle_interval_mode(self):
        """
        勾选“开启随机时间间隔”选项时改变界面的设置，显示相应的文本框提示信息
        :return:
        """
        if self.is_random_interval.isChecked():
            self.interval_label.setText("设置任务间隔的最大时间（秒）")
        else:
            self.interval_label.setText("设置任务间隔时间（秒）")

    def toggle_search_input_mode(self):
        """
        勾选“使用多个关键词文件”选项时改变界面的设置，隐藏或显示搜索框和文件选择按钮
        :return:
        """
        self.keyword_input.setVisible(not self.is_use_multiple_file.isChecked())
        self.btn_open_search_file.setVisible(self.is_use_multiple_file.isChecked())

    def open_file_dialog_window(self, class_):
        """
        打开文件选择对话框，让用户选择评论话术文件或关键词文件
        :param class_:区分是评论话术文件还是关键词文件
        :return:
        """
        logger.info('Open the file window and get ready to select a file.')
        self.file_dialog = QFileDialog(filter="*.txt")
        self.file_dialog.setWindowTitle("小红书自动跑-请选择文件...")
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        if self.file_dialog.exec_() == QFileDialog.Accepted:
            if class_ == "COMMENTS":
                self.selected_comment_file_path = self.file_dialog.selectedFiles()[0]
                self.btn_open_comment_file.setText(self.selected_comment_file_path.split('/')[-1])
            elif class_ == "SEARCH":
                self.selected_search_file_path = self.file_dialog.selectedFiles()[0]
                self.btn_open_search_file.setText(self.selected_search_file_path.split('/')[-1])

    def onIsCommentStateChanged(self, state):
        if state == Qt.Unchecked:
            self.is_check_shield.setEnabled(False)
            self.is_random_rare_word.setEnabled(False)
            self.is_shield_retry.setEnabled(False)
            self.rare_word_label.setEnabled(False)
            self.rare_word_spinbox.setEnabled(False)
        else:
            self.is_check_shield.setEnabled(True)
            self.is_random_rare_word.setEnabled(True)
            self.is_shield_retry.setEnabled(True)
            self.rare_word_label.setEnabled(True)
            self.rare_word_spinbox.setEnabled(True)

    def onIsSkipCollect(self, state):
        if state == Qt.Unchecked:
            self.is_again_comment_collect.setEnabled(True)
        else:
            self.is_again_comment_collect.setEnabled(False)

    def onIsAgainCommentCollect(self, state):
        if state == Qt.Unchecked:
            self.is_skip_collect.setEnabled(True)
        else:
            self.is_skip_collect.setEnabled(False)

    def onIsCyclicMode(self, state):
        if state == Qt.Unchecked:
            self.loop_interval_minute_label.setVisible(False)
            self.loop_interval_minute.setVisible(False)
        else:
            self.loop_interval_minute_label.setVisible(True)
            self.loop_interval_minute.setVisible(True)

    def onIsRandomRareWord(self, state):
        if state == Qt.Unchecked:
            self.rare_word_label.setVisible(False)
            self.rare_word_spinbox.setVisible(False)
        else:
            self.rare_word_label.setVisible(True)
            self.rare_word_spinbox.setVisible(True)

    def onIsCheckShield(self, state):
        if state == Qt.Unchecked:
            self.is_shield_retry.setVisible(False)
            self.is_shield_retry.setChecked(False)
        else:
            self.is_shield_retry.setVisible(True)

    def onIsShieldRetry(self, state):
        if state == Qt.Unchecked:
            self.shield_retry_count.setVisible(False)
        else:
            self.shield_retry_count.setVisible(True)

    @staticmethod
    def calculate_time_difference(time1, time2):
        """
        该方法用于计算两个时间间隔的小时、分钟和秒数。
        :param time1: 时间 1
        :param time2: 时间 2
        :return:返回一个包含小时、分钟和秒数的元组
        """
        today = datetime.datetime.today()
        datetime1 = datetime.datetime.combine(today, time1)
        datetime2 = datetime.datetime.combine(today, time2)
        if datetime2 < datetime1:
            datetime2 -= datetime.timedelta(days=1)
        timedelta = datetime2 - datetime1
        total_seconds = timedelta.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return hours, minutes, seconds

    @staticmethod
    def get_format(color: int):
        _format = QTextCharFormat()
        _format.setForeground(color)
        return _format

    def append_dynamic_log(self, output):
        dmt_cursor = QTextCursor(self.dynamic_monitor_text.document())
        dmt_cursor.movePosition(QTextCursor.End)
        start_index = output.find("评论已被屏蔽")
        while start_index != -1:
            dmt_cursor.insertText(output[:start_index], self.get_format(Qt.black))  # 设置黑色样式
            dmt_cursor.insertText("评论已被屏蔽", self.get_format(Qt.red))  # 设置红色样式
            output = output[start_index + 6:]
            start_index = output.find("评论已被屏蔽")
        dmt_cursor.insertText(output, self.get_format(Qt.black))  # 设置黑色样式
        dmt_cursor.insertBlock()

    def clear_dynamic_log(self):
        self.dynamic_monitor_text.clear()
        logger.info("Clear Logs.")

    def close(self):
        """
        关闭应用程序前会关闭所有已经创建的浏览器实例
        :return:
        """
        for thread in self.threads:
            browser = thread.get("browser")
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
        logger.info('Close the app.')
        super().close()


BASEDIR = Path(__file__).parent.absolute()
LOG_DIR = BASEDIR / "logs"
LOG_FILE = LOG_DIR / "record_{time}.log"
LOG_ROTATION = "00:00"
LOG_RETENTION = "10 days"

LOG_CONFIG = {
    "normal_handler": {
        "file": LOG_FILE,
        "level": "INFO",
        "rotation": LOG_ROTATION,
        "retention": LOG_RETENTION,
        "enqueue": True,
        "encoding": "utf-8",
        'compression': "zip",
    }
}


def setup_logger():
    """
    安装日志
    """
    for log_handler, log_conf in LOG_CONFIG.items():
        log_file = log_conf.pop('file', None)
        logger.add(log_file, **log_conf)
    logger.info("setup logging success")


if __name__ == '__main__':
    setup_logger()
    app = QApplication(sys.argv)
    logger.info('Instantiate the app.')
    window = MainWindow()
    logger.info('Displaying application windows.')
    window.show()
    sys.exit(app.exec_())
