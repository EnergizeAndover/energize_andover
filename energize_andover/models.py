from django.db import models

# Create your models here.
class School(models.Model):
    Name = models.CharField(max_length=30)

    def panels(self):
        return Panel.objects.filter(School__pk=self.pk)

    def rooms(self):
        return Room.objects.filter(School__pk=self.pk)

    def closets(self):
        return Closet.objects.filter(School__pk=self.pk)

    def __str__(self):
        return self.Name



class Closet(models.Model):
    Name = models.CharField(max_length=30)
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        default=1,
    )


class Panel(models.Model):
    Name = models.CharField(max_length=30)
    Voltage = models.CharField(max_length=20, default='0')
    Location = models.CharField(max_length=30, default='')
    Panels = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        default=1
    )
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        default=1
    )
    Closet = models.ForeignKey(
        Closet,
        on_delete=models.CASCADE,
        default=1,
    )


    def Rooms(self):
        return Room.objects.filter(Panel__pk=self.pk)

    def __str__(self):
        return self.Name

class Room(models.Model):
    Name = models.CharField(max_length=30)
    OldName = models.CharField(max_length=30, default='')
    Type = models.CharField(max_length=30, default='')
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        default=1
    )
    Panels = models.ManyToManyField(Panel,)

    def __str__(self):
        return self.Name


class Circuits(models.Model):
    Name = models.CharField(max_length=100)
    Number = models.IntegerField(default=0)
    Panel = models.ForeignKey(
        Panel,
        on_delete=models.CASCADE,
        default=1
    )
    Rooms = models.ManyToManyField(Room)

    def __str__(self):
        out = str(self.Panel) + ', curcuit' + str(self.Number) + ': '
        for room in self.Rooms:
            out += str(room) + ' '
        return out

