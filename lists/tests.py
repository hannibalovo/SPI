from django.test import TestCase
from django.urls import resolve
from lists.views import home_page #(1)
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item,List

class HomePageTest(TestCase):
    
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')#(2)
    #     self.assertEqual(found.func, home_page)#(3)
    
    # def test_home_page_return_correct_html(self):
    #     request = HttpRequest()#(1)
    #     response =home_page(request)#(2)
    #     html =response.content.decode('utf8')#(3)
    #     self.assertTrue(html.startswith('<html>'))#(4)
    #     self.assertIn('<title>To-Do lists</title>',html)
    #     self.assertTrue(html.endswith('</html>'))#(4)
    
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new',data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)#(1)
        new_item = Item.objects.first()#(2)
        self.assertEqual(new_item.text,'A new list item')#(3)
        
        # self.assertIn('A new list item',response.content.decode())
        # self.assertTemplateUsed(response,'home.html')
        
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',data={'item_text': 'A new list item'})
        # self.assertEqual(response.status_code,302)
        # self.assertEqual(response['location'],'/lists/the-new-page/')
        new_list = List.objects.first()
        # self.assertRedirects(response,'/lists/the-new-page/')
        self.assertRedirects(response, f'/lists/{new_list.id}/')


    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')      
    #     self.assertEqual(Item.objects.count(), 0)
        
    # def test_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #     response =self.client.get('/')
    #     self.assertIn('itemey 1',response.content.decode())
    #     self.assertIn('itemey 2',response.content.decode())
        

class ItemModelest(TestCase):

    def test_saving_and_retrieving_items(self):
        # #####################必须加这个,创建list的实例,否则会出现################
        # django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id的非空约束错误
        list_instance = List.objects.create()  # 创建一个有效的 List 实例
        # #####################实例list实例,不然本编译器会报错####################
        
        first_item= Item()
        first_item.text='The first list item'
        # #####################加上实例化的代码,下面second也是如此##############
        first_item.list = list_instance  # 为第一个 Item 实例指定有效的 List 对象
        first_item.save()
        
        second_item= Item()
        second_item.text = 'Item the second'
        # #####################加上实例化代码
        second_item.list = list_instance  # 为第二个 Item 实例指定相同的有效的 List 对象
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first list item')
        self.assertEqual(second_saved_item.text,'Item the second')
        
class ListViewTest(TestCase):  
    def test_uses_list_template(self):
        # response = self.client.get('/lists/the-new-page/')
        list_user = List.objects.create()
        response = self.client.get(f'/lists/{list_user.id}/')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_all_list_items(self):
        corrent_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=corrent_list)
        Item.objects.create(text='itemey 2',list=corrent_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1',list=other_list)
        Item.objects.create(text='other list item 2',list=other_list)
        response = self.client.get(f'/lists/{corrent_list.id}/')
        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')#(1)
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')#(1)
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        corrtect_list = List.objects.create()
        response =self.client.get(f'/lists/{corrtect_list.id}/')
        self.assertEqual(response.context['list'],corrtect_list)
        
        # list_user = List.objects.create()
        # Item.objects.create(text='itemey 1',list=list_user)
        # Item.objects.create(text='itemey 2',list=list_user)
        
        # Item.objects.create(text='itemey 1')
        # Item.objects.create(text='itemey 2')
        # response = self.client.get('/lists/the-new-page/')
        # self.assertContains(response,'itemey 1')
        # self.assertContains(response,'itemey 2')#(1)
        
        
class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        onther_list=List.objects.create()
        corrtect_list =List.objects.create()
        self.client.post(
            f'/lists/{corrtect_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item =Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,corrtect_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        corrtect_list =List.objects.create()
        response = self.client.post(
            f'/lists/{corrtect_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
            )
        self.assertRedirects(response,f'/lists/{corrtect_list.id}/')