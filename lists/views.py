from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from lists.models import Item
# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	items = Item.objects.all()
#	for item in items:
#		item.delete()
	return render(request, 'home.html', {'items':items})