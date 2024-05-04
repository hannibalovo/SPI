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

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser= webdriver.Chrome()
        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(row_text, [row.text for row in rows])    
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三听说有一个在线待办事项的应用#他去看了这个应用的首页
        self.browser.get('http://localhost:8000')
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
        time.sleep(1)#(4)
        
        # 
        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')#(1)
        # self.assertIn('1: Buy flowers', [row.text for row in rows])
        #个文本输入框，可以输入其他待办事项#显示了#他输入了"gift to girlfriend"
        
        self.check_for_row_in_list_table('1: Buy flowers')
        
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # 页面再次更新，她的清单中显示了这两个待办事项
        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn('1: Buy flowers',[row.text for row in rows])
        # self.assertIn('2: Give a gift to Lisi',[row.text for row in rows])
        # 
        
        self.check_for_row_in_list_table('1: Buy flowers')
        self.check_for_row_in_list_table('2: Give a gift to Lisi')
        
        self.fail('Finish the test!')
        #她的清单中显示了这两个待办事项
if __name__ == '__main__':
    unittest.main()