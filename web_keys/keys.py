from time import sleep, time

from selenium import webdriver
from time import sleep
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from conf import log_conf


# 构造浏览器对象，基于type_参数，构造对应的浏览器对象；
def open_browser(type_):
    driver = getattr(webdriver, type_)()
    return driver


# def execute_script(js):
#     return js


class Keyword:
    # 临时driver对象
    # driver = webdriver.Chrome()

    # 构造函数、
    def __init__(self, txt, log):
        self.driver = open_browser(txt)
        self.driver.implicitly_wait(5)
        # 日志生成器
        # self.log = log_conf.get_log('../conf/log.ini')
        self.log = log

    # 访问url

    def open(self, txt):
        self.driver.get(txt)

        # 定位元素

    def locate(self, name, value):
        return self.driver.find_element(name, value)

        # 输入元素

    def input(self, name, value, txt):
        self.locate(name, value).send_keys(txt)
        # qs = self.locate(name, value).clear()
        # qs.send_keys(txt)

    # 获取输入框中的值
    def get_putvalue(self, name, value):
        self.locate(name, value).get_attrbute('value')

    # 点击

    def click(self, name, value):
        self.locate(name, value).click()

    # 清空消息
    def clear(self, name, value):
        self.locate(name, value).clear()

    # 强制等待

    # 鼠标悬停才显示的元素
    def move_element(self, name, value):
        element = self.locate(name, value)
        ActionChains(self.driver).move_to_element(element).perform()

    def move_element_click(self, name, value):
        self.locate(name, value).click()

    def sleep(self, txt):
        sleep(int(txt))

    # 切换iframe  --传入一个参数可以是id、name、webelement
    def switch_frame(self, value, name=None):
        if name is None:
            self.driver.switch_to_frame(value)
        else:
            self.driver.switch_to.frame(self.locate(name, value))

    # 切出默认主框架
    def switch_maincontent(self):
        self.driver.switch_to.default_content()

    # 文本断言
    def assert_text(self, name, value, expected):
        try:
            reality = self.locate(name, value).text
            assert expected == reality, '断言失败，实际结果为:{}'.format(reality)
            return True
        except:
            return False

    # 断言实际结果是否包含在预期结果内
    def assert_almost_equal(self, name, value, expected):
        try:
            reality = self.locate(name, value).text
            assert expected in reality, '断言失败，实际结果为:{}'.format(reality)
            return True
        except Exception as e:
            print('断言失败信息:' + str(e))
            self.log.exception('出现异常，断言失败:实际结果与预期不符合:{}'.format(e))
            return False

    # 显示等待
    def web_el_wait(self, name, value):
        return WebDriverWait(self.driver, 10, 0.5).until(
            lambda el: self.locate(name, value), message='元素查找失败'
        )

    # select 下拉选方式
    # 1、通过value属性定位
    def select_value(self, name, value, txt):
        s = self.locate(name, value)
        ele = Select(s)
        ele.select_by_value(str(txt))

    # 2、通过文本属性定位
    def select_txt(self, name, value, txt):
        s = self.locate(name, value)
        sls = Select(s)
        sls.select_by_visible_text(txt)

    # Radio单选框
    def test_radio(self, i):
        for i in self.driver.find_element(By.NAME, value='subsityType'):
            i.click()

    # 创建时间
    def send_create_time(self, name, value, txt):
        js = 'document.getElementById("' + value + '").removeAttribute("readonly")'
        # print(js)
        # self.driver.execute_script('document.getElementById("beginTime_0").removeAttribute("readonly")')
        self.driver.execute_script(js)
        self.input(name, value, str(txt))

    # 切换窗口
    def switch_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

    # 切换到主窗口
    def switch_main_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    # 切换到弹出框
    # def execute_script(self, js):
    #     pass
    # 切换到confirm弹框的方法
    # 取消弹框
    def switch_alert_dismiss(self):
        al = self.driver.switch_to.alert
        # print(al.txt)
        al.dismiss()

    # 接受弹框
    def switch_alert_accept(self):
        al = self.driver.switch_to.alert
        al.accept()
