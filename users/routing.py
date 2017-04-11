from channels.routing import route, include

from users.consumers import ws_connect, ws_disconnect
from msgs.consumers import ws_connect_chat, ws_disconnect_chat, ws_receive_chat

inner_routes = [
    route("websocket.connect_chat", ws_connect_chat, path=r'^(?P<room>\w+)$'),
    route("websocket.receive_chat", ws_receive_chat),
    route("websocket.disconnect_chat", ws_disconnect_chat),
]


channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    include(inner_routes, path=r'^/chat/')
]
