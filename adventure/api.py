from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
import queue

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


# @csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    # get room exits
    exits = []
    if room.n_to:
        exits.append('n')
    if room.s_to:
        exits.append('s')
    if room.e_to:
        exits.append('e')
    if room.w_to:
        exits.append('w')
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'exits': exits}, safe=True)


# @csrf_exempt
@api_view(["GET"])
def room_view(request):
    user = request.user
    player = user.player
    room = player.room()
    # BFS starting with player's current room, developing coordinates
    # TODO only do this once for each create_world
    x = 0
    y = 0
    q = queue.Queue()
    rooms_graph = {}
    q.put([room, x, y])
    while not q.empty():
        q_item = q.get()
        current_room = q_item[0]
        # print(current_room.id)
        x = q_item[1]
        y = q_item[2]
        rooms_graph[current_room.id] = [x, y]
        if current_room.n_to and current_room.n_to not in rooms_graph:
            q.put([Room.objects.get(id=current_room.n_to), x, y + 1])
        if current_room.e_to and current_room.e_to not in rooms_graph:
            q.put([Room.objects.get(id=current_room.e_to), x + 1, y])
        if current_room.s_to and current_room.s_to not in rooms_graph:
            q.put([Room.objects.get(id=current_room.s_to), x, y - 1])
        if current_room.w_to and current_room.w_to not in rooms_graph:
            q.put([Room.objects.get(id=current_room.w_to), x - 1, y])
    # print(rooms_graph)

    return JsonResponse({"username": player.user.username, "roomsGraph": rooms_graph})


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        # get room exits
        exits = []
        if room.n_to:
            exits.append('n')
        if room.s_to:
            exits.append('s')
        if room.e_to:
            exits.append('e')
        if room.w_to:
            exits.append('w')
        return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'exits': exits}, safe=True)
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'exits': exits, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'exits': exits, 'error_msg': "You cannot move that way."}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
