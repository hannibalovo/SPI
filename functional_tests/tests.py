from selenium import webdriver
# import unittest

# class NewVisitorTest(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_can_start_a_list_and_retrieve_it_later(self):
#     # 张三听说有一个在线待办事项的应用# 他去看了这个应用的首页
#         self.browser.get('http://localhost:8000')
#     #他注意到网页里包含"TO-Do"这个词
#         self.assertIn('To-Do',self.browser.title),"browser title was:"+ self.browser.title
#         self.fail('Finish the test!')
#     # 应用有一个输入待办事项的文本输入框
#     # 他在文本输入框中输入了“Buy flowers"
#     # 他访问那个URL，发现他的待办事项列表还在#他满意的离开了
# if __name__ == '__main__':
#     unittest.main()

from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
MAX_WAIT = 10

# class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser= webdriver.Chrome()
        
    def tearDown(self):
        self.browser.quit()
        
    # def check_for_row_in_list_table(self, row_text):
    def wait_for_row_in_list_table(self, row_text):
        # table = self.browser.find_element(By.ID, 'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn(row_text, [row.text for row in rows]) 
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')#(3)
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return 
            except (AssertionError, WebDriverException)as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
                   
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三听说有一个在线待办事项的应用#他去看了这个应用的首页
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        
        #他注意到网页的标题和头部都包含"To-Do"这个词
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text #(1)
        self.assertIn('To-Do',header_text)
        #应有一个个输入待办事项的文本输入框
        inputbox= self.browser.find_element(By.ID,'id_new_item')#(1)
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
        #他在文本输入框中输入了“Buy flowers'
        inputbox.send_keys('Buy flowers')#(2)
        #他按了回车键键后，页面更新了#待办事项表格中显示了“1:Buyflowers"
        inputbox.send_keys(Keys.ENTER)#(3)
        # time.sleep(1)#(4)
        
        # 
        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')#(1)
        # self.assertIn('1: Buy flowers', [row.text for row in rows])
        #个文本输入框，可以输入其他待办事项#显示了#他输入了"gift to girlfriend"
        
        self.wait_for_row_in_list_table('1: Buy flowers')
        
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        
        # 页面再次更新，她的清单中显示了这两个待办事项
        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn('1: Buy flowers',[row.text for row in rows])
        # self.assertIn('2: Give a gift to Lisi',[row.text for row in rows])
        # 
        
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')
        # 他注意到清单有个唯一的URL
        zhangsan_list_url=self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')#(1)

        # 个新用户王五访问网站杂 王不-#我们使用一个新浏览器会话#确保张三的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Chrome()
        # 王五访问首页#页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text= self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('BGive a gift to Lisi',page_text)
        #王五输入个新待办事项项，新建一个个清单"id new item')
        inputbox= self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # 王五获得了他的唯-URL#
        wangwu_list_url= self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)
        #这个面还是没有张三的清单= 
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)
        #两人人都很满意，然后去睡觉了
    
        # 没问题也会强制中断,先注释掉
        # self.fail('Finish the test!')
        #她的清单中显示了这两个待办事项
        
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
# 她看到输入框完美地居中显示
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+ inputbox.size['width']/2,
            512,delta=10
            )
        
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
# 她看到输入框完美地居中显示
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+ inputbox.size['width']/2,
            512,delta=10
            )
# if __name__ == '__main__':
#     unittest.main()