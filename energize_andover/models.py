from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class School(models.Model):
    Name = models.CharField(max_length=30)
    # Notes = models.CharField(max_length=1000, default='')

    def panels(self):
        return Panel.objects.filter(School__pk=self.pk)

    def rooms(self):
        return Room.objects.filter(School__pk=self.pk)

    def closets(self):
        return Closet.objects.filter(School__pk=self.pk)

    def devices(self):
        return Device.objects.filter(School__pk=self.pk)
        """
        panels = self.panels()
        devs = []
        for i in panels:
            for j in i.circuits():
                for k in j.devices():
                    if k not in devs:
                        devs.append(k)
        return devs
        """

    def __str__(self):
        return self.Name


class Closet(models.Model):
    Name = models.CharField(max_length=30)
    Old_Name = models.CharField(max_length=20, default='')
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Notes = models.CharField(max_length=1000, default='')
    QID = models.IntegerField(default=0)

    def __str__(self):
        return self.Old_Name

    def to_string(self):
        return self.Old_Name + " / " + self.Name


class Panel(models.Model):
    Name = models.CharField(max_length=30)
    Voltage = models.CharField(max_length=20, default='0')
    Location = models.CharField(max_length=30, default='')
    FQN = models.CharField(max_length=50, default="MWSB")
    QID = models.IntegerField(default=0)
    Panels = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Closet = models.ForeignKey(
        Closet,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Notes = models.CharField(max_length=1000, default='')

    def rooms(self):
        return Room.objects.filter(Panels__pk=self.pk)

    def circuits(self):
        return Circuit.objects.filter(Panel=self.pk)

    def panels(self):
        return Panel.objects.filter(Panels__pk=self.pk)

    def fqn(self):
        return self.FQN

    def __str__(self):
        return self.Name

    def to_string(self):
        try:
            return self.FQN + " (" + self.Name + "), Rm. " + self.Closet.Name
        except:
            return self.FQN + " (" + self.Name + ")"


class Room(models.Model):
    Name = models.CharField(max_length=30)
    OldName = models.CharField(max_length=30, default='')
    Type = models.CharField(max_length=30, default='')
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Panels = models.ManyToManyField(Panel,
                                    blank=True,)
    Notes = models.CharField(max_length=1000, default = '')
    QID = models.IntegerField(default=0)

    def panels(self):
        return self.Panels.all()

    def school(self):
        return self.School

    def circuits(self):
        return Circuit.objects.filter(Rooms__pk=self.pk)

    def __str__(self):
        return self.OldName

    def to_string(self):
        return self.Name + " / " + self.OldName + " / " + self.Type


class Circuit(models.Model):
    Name = models.CharField(max_length=100)
    Number = models.CharField(default = "0", max_length = 10)
    FQN = models.CharField(max_length=50, default="MWSB")
    Function = models.CharField(default = "NA", max_length = 50)
    Panel = models.ForeignKey(
        Panel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Rooms = models.ManyToManyField(Room,
                        blank=True)
    Notes = models.CharField(max_length=1000, default = '')

    def rooms(self):
        return self.Rooms.all()

    def devices(self):
        return Device.objects.filter(Circuit__pk=self.pk)

    def school (self):
        return self.Panel.School

    def __str__(self):
        out = str(self.Panel) + ', circuit ' + str(self.Number) + ': '
        #rooms = self.Rooms.all()
        #for room in rooms:
        #    out += room.__str__()
        return out

    def to_string(self):
        to_str = self.FQN + " | " + self.Name
        if not len(self.devices()) == 0:
            dev = " | 1) " + self.devices()[0].to_string()
            rm = self.devices()[0].Room
            for i in range(1, len(self.devices())):
                dev += ("; " + str(i+1) + ") " + self.devices()[i].to_string())
            to_str += (dev)
        return to_str


class Device(models.Model):
    Name = models.CharField(max_length=50)
    Circuit = models.ManyToManyField(
        Circuit,
        blank=True,
    )
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    Associated_Devices = models.ManyToManyField(
        'self',
        blank=True,
    )
    Power = models.CharField(max_length=10)
    Location = models.CharField(max_length=30)
    Room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    Number = models.IntegerField(default = 0)
    Notes = models.CharField(max_length=1000, default = '')

    def circuits(self):
        return self.Circuit.all()

    def rooms(self):
        return self.Room

    def __str__(self):
        str = self.Name
        if self.Room is not None:
            str+=(", Rm:" + self.Room.Name)
        return str

    def to_string(self):
        to_str = self.Name
        if self.Room is not None:
            to_str += (", Rm: " + self.Room.Name)
        return to_str


class Transformer(models.Model):
    Name = models.CharField(max_length=50, default = '')
    Notes = models.CharField(max_length=1000, default = '')
    FQN = models.CharField(max_length=50, default = '')
    School = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.Name


class SpecialUser(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Authorized_Schools = models.ManyToManyField(School, blank=True)
    Notes = models.CharField(max_length=1000, default='')
