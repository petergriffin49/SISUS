from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import F
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
    #return render(request, 'user/logout.html')
    logout(request)
    return redirect('login')

# [home screen]
@login_required
def HomePage(request):

    user = request.user
    items_for_user = Item_User.objects.filter(user=user).select_related('item')
    user_items = [item_user.item for item_user in items_for_user]
    Item_list = Item.objects.filter( # Item_list
        id__in=[item.id for item in user_items]
    ).filter(Item_amount__lte=F('Item_lowStock'))
    
    Username = user.get_full_name()
    context = {
        "lowStock_list": Item_list,
        "Username": Username,
    }
    template = loader.get_template("inventory/Home.html")
    return HttpResponse(template.render(context,request))

# control room  / maximal view [inventory]
@login_required
def Controlroom(request):
    user = request.user
    items_for_user = Item_User.objects.filter(user=user).select_related('item')
    Item_list = [item_user.item for item_user in items_for_user]
    
    Username = user.get_full_name()
    context = {
        "Item_list": Item_list,
        "Username": Username,
    }
    template = loader.get_template("inventory/Controlroom.html")
    return HttpResponse(template.render(context,request))
@login_required
def Maximalview(request):
    user = request.user
    items_for_user = Item_User.objects.filter(user=user).select_related('item')
    Item_list = [item_user.item for item_user in items_for_user]

    Username = user.get_full_name()
    context = {
        "Item_list": Item_list,
        "Username": Username,
    }
    template = loader.get_template("inventory/maximal.html")
    return HttpResponse(template.render(context,request))
    
@login_required
def AddItemInv(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            newObj = form.save() # saves the new item obj
            
            new_userObj = Item_User(
                item=newObj,
                user=request.user,
            )
            new_userObj.save() # saves the user - item relation object
            
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

@login_required
def EditItem(request, itemID):
    item = get_object_or_404(Item, id=itemID)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('Item Details', item_id=item.id)  # Redirect to a detail page or wherever you prefer
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/EditItem.html', {'form': form, 'item': item})


# [analytics]
@login_required
def Analytics(request):
    context = {}
    template = loader.get_template("inventory/Analytics.html")
    return HttpResponse(template.render(context,request))