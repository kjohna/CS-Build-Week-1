from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(blank=True, null=True)
    s_to = models.IntegerField(blank=True, null=True)
    e_to = models.IntegerField(blank=True, null=True)
    w_to = models.IntegerField(blank=True, null=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        print(
            f"connect dest: {destinationRoomID} to self: {self.id} dir: {direction}")
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
                destinationRoom.s_to = self.id
                print(f"connect {self.id} to {direction} neighbor {self.n_to}")
                print(f"self.n_to = {self.n_to}")
                print(f"destinationRoom.s_to = {destinationRoom.s_to}")
            elif direction == "s":
                self.s_to = destinationRoomID
                destinationRoom.n_to = self.id
                print(f"connect {self.id} to {direction} neighbor")
            elif direction == "e":
                self.e_to = destinationRoomID
                destinationRoom.w_to = self.id
                print(f"connect {self.id} to {direction} neighbor")
            elif direction == "w":
                self.w_to = destinationRoomID
                destinationRoom.e_to = self.id
                print(f"connect {self.id} to {direction} neighbor")
            else:
                print("Invalid direction")
                return
            self.save()
            # can't save destination room this way? best to run connect rooms in both directions.
            # destinationRoom.save()
            print("rooms saved")

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
