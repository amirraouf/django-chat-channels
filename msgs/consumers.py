import json
from channels import Group
from channels.sessions import channel_session
from .models import Room


@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'chat':
            return
        room = Room.objects.get(label=label)
    except ValueError:
        return
    except Room.DoesNotExist:
        return



    Group('chat-' + label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        return
    except Room.DoesNotExist:
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        return

    if set(data.keys()) != set(('handle', 'message')):
        return

    if data:
        m = room.messages.create(**data)

        # See above for the note about Group
        Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-' + label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
