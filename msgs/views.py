from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from msgs.forms import MessageForm
from msgs.models import Room

User = get_user_model()

@login_required(login_url='/login/')
def chat(request, user):
    user = User.objects.get(username=user)
    try:
        room = Room.objects.get(from_user=request.user, to_user=user)
    except Room.DoesNotExist:
        room, created = Room.objects.get_or_create(to_user=request.user, from_user=user)

    messages = reversed(room.message_set.order_by('-timestamp')[:50])

    return render(request, "msgs/chat.html", {
        'room': room,
        'messages': messages,
        'form': MessageForm
    })

