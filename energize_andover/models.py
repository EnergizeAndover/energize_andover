from django.db import models

# Create your models here.
class School(models.Model):
    Name = models.CharField(max_length=30)
    def get_panels(self):
        return Panel.objects.filter(School__pk=self.pk)
    def get_room(self):
        return Room.objects.filter(School__pk=self.pk)

    def __str__(self):
        return self.Name



class Panel(models.Model):
    Name = models.CharField(max_length=30)
    Location = models.CharField(max_length=30)
    Panels = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )

    def Rooms(self):
        return Room.objects.filter(Panel__pk=self.pk)

    def __str__(self):
        return self.Name

class Room(models.Model):
    Name = models.CharField(max_length=30)
    Oldname = models.CharField(max_length=30)
    Type = models.CharField(max_length=30)
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )
    Panels = models.ManyToManyField(Panel,)

    def __str__(self):
        return self.Name


class Circuits(models.Model):
    Name = models.CharField(max_length=100)
    Number = models.IntegerField()
    Panel = models.ForeignKey(
        Panel,
        on_delete=models.CASCADE,
    )
    Rooms = models.ManyToManyField(Room)

    def __str__(self):
        out = str(self.Panel) + ', curcuit' + str(self.Number) + ': '
        for room in self.Rooms:
            out += str(room) + ' '
        return out

