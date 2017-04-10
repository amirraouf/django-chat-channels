from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


@login_required(login_url='/login/')
def chat(request, user):
    try:
        room = Room.objects.get(from_user=request.user, to_user=user)
    except Room.DoesNotExist:
        room, created = Room.objects.get_or_create(to_user=request.user, from_user=user)

    messages = reversed(room.message_set.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })

