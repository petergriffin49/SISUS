from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import F
from datetime import datetime
from .models import *
from .forms import *
import random

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


def itemEditAdd(item_obj):
    itemEdit_obj = Item_Edit(
        item=item_obj,
        amount=newObj.Item_amount,
        time=datetime.today().strftime('%Y-%m-%d'),
    )
    itemEdit_obj.save()

# add an Item_Edit object based on the given Item obj
def itemEditAdd(item_obj):
    # delete any obj that has the same itemid and date
    myItem = item_obj
    myTime = datetime.today().strftime('%Y-%m-%d')
    items_to_delete = Item_Edit.objects.filter(item=myItem, time=myTime)
    items_to_delete.delete()
    
    # create new one
    itemEdit_obj = Item_Edit(
        item=item_obj,
        amount=item_obj.Item_amount,
        time=datetime.today().strftime('%Y-%m-%d'),
    )
    itemEdit_obj.save()

@login_required
def AddItemInv(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            
            newObj = form.save() # saves the new item obj 
            r = lambda: random.randint(0,255)
            newObj.Item_color = '#%02X%02X%02X' % (r(),r(),r()) # add a random color to the item
            newObj.save()
            
            #
            new_userObj = Item_User(
                item=newObj,
                user=request.user,
            )
            new_userObj.save() # saves the user - item relation object

            itemEditAdd(newObj)

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
    user = request.user
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item_edited = form.save() # saves the item obj, now edited

            itemEditAdd(item_edited)

            return redirect('Item Details', item_id=item.id,)  # Redirect to a detail page or wherever you prefer
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/EditItem.html', {'form': form, 'item': item})


# [analytics]
@login_required
def Analytics(request):

    user = request.user
    user_items = Item_User.objects.filter(user=user).values_list('item', flat=True)
    item_edits = Item_Edit.objects.filter(item__in=user_items)

    days = 7

    context_dict = {}
    ROCN_dict = {}
    ROCA_dict = {}
    
    # For all items the user currently possesses:
    for edit in item_edits:
        # Names of all items the user currently possesses
        itemName = edit.item.Item_name

        current_date = datetime.today().date()
        # Last time the item has been edited
        days_difference = (current_date - edit.time).days
        
        if itemName in context_dict:
            # If the item has been edited in the last seven days
            if days_difference < days:
                context_dict[itemName][0][days-days_difference-1] = edit.amount

        else:
            context_dict[itemName] = [[],edit.item.Item_color]
            for i in range(days):
                context_dict[itemName][0] += [0]
            
            if days_difference < days:
                context_dict[itemName][0][days-days_difference-1] = edit.amount
        
    # fix lists
    for key in context_dict:
        myList = context_dict[key][0]
        for i in range(len(myList)):
            if i > 0:
                if myList[i] == 0:
                    myList[i] = myList[i-1]
    
    
    for item in context_dict:
        l = context_dict[item][0]
        
        i = round((l[6] - l[0]) / float(7),2)
        ROCA_dict[i] = 0
        ROCN_dict[item] = 0
        
        
    context = {
        'datasets': context_dict,
        'rateOfChange': zip(ROCA_dict,ROCN_dict)
    }

    return render(request, 'inventory/Analytics.html', context)


