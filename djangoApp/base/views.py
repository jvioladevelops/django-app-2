from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms = [
#     {'id' :1, 'name': 'Lets learn python!'},
#     {'id' :2, 'name': 'Lets learn something!'},
#     {'id' :3, 'name': 'Lets learn new!'},
# ]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
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
