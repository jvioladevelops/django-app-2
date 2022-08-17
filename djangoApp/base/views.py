from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id' :1, 'name': 'Lets learn python!'},
#     {'id' :2, 'name': 'Lets learn something!'},
#     {'id' :3, 'name': 'Lets learn new!'},
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #ensure that whatever value we have in the topic name it in 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # The form already knows which values to extract
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            # since the name is in url.py I can access the home url by just the name
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    #making sure the primary key patcahes to prefill form
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        #the data from POST will replace whatever data for room
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})