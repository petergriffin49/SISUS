from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from .forms import *

# [log in crap]
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'user/register.html', context)

def logout_view(request):
    logout(request)
    #return render(request, 'user/logout.html')
    return redirect('login')

# [home screen]
@login_required
def HomePage(request):
    context = {
        
    }
    template = loader.get_template("inventory/Home.html")
    return HttpResponse(template.render(context,request))

# control room [inventory]
@login_required
def Controlroom(request):
    template = loader.get_template("inventory/Controlroom.html")
    Item_list = Item.objects.all()
    context = {
        "Item_list": Item_list,
    }
    return HttpResponse(template.render(context,request))

@login_required
def AddItemInv(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()  # Save the new object
            return redirect('inventory')  # Redirect to a success page
    else:
        form = ItemForm()
    
    return render(request, 'inventory/AddItem.html', {'form': form})

@login_required
def DeleteItem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('inventory')  # Redirect to an appropriate page after deletion

# [specific item page]
@login_required
def Itemdetails(request, item_id):
    template = loader.get_template("inventory/Itemdetails.html")
    context = {
        "Item": Item.objects.get(id = item_id),
    }
    return HttpResponse(template.render(context,request))
    
# [hanalytics]
@login_required
def Analytics(request):
    context = {
        
    }
    template = loader.get_template("inventory/Analytics.html")
    return HttpResponse(template.render(context,request))