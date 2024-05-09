from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

def new_list(request):
    list_user = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_user)
    return redirect('/lists/the-new-page/')

def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # return render(request, 'home.html')
    
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    
    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()
    
    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']#(1)
    #     Item.objects.create(text = new_item_text)#(2)
    # else:
    #     new_item_text = ''
    # return render(request,'home.html',{
    #     'new_item_text': new_item_text
    #     })
    
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-new-page/')
    
    # items = Item.objects.all()
    # return render(request,'home.html',{'items':items})
    return render(request,'home.html')
    
def view_list(request):
    items = Item.objects.all()
    return render(request,'list.html',{'items':items})

# home_page = None
# Create your views here.

