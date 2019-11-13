from django.db import models

# Create your models here.


class Speed(models.Model):
    speed_time = models.DateTimeField(auto_now_add=True)
    speed_value = models.CharField(max_length=50)

    def __str__(self):
        return 'time: ' + str(self.speed_time)


class State(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    # allFlags
    acReliableFlag = models.CharField(max_length=20)
    acBrReliableFlag = models.CharField(max_length=20)
    startFlag = models.CharField(max_length=20)
    runFlag = models.CharField(max_length=20)
    driveReadyFlag = models.CharField(max_length=20)
    SafetyFlag = models.CharField(max_length=20)
    brFlag = models.CharField(max_length=20)
    zfAllowFlag = models.CharField(max_length=20)
    ycAllowFlag = models.CharField(max_length=20)

    acFinal = models.CharField(max_length=20)
    brFinal = models.CharField(max_length=20)
    finalSendTorque = models.CharField(max_length=20)
    gear = models.CharField(max_length=20)
    rotateSpeed = models.CharField(max_length=20)
    speed = models.CharField(max_length=20)
    # mcMessages
    mcReady = models.CharField(max_length=20)
    ycReady = models.CharField(max_length=20)
    resolverFlag = models.CharField(max_length=20)
    currentOverloadFlag = models.CharField(max_length=20)
    voltageOverloadFlag = models.CharField(max_length=20)
    ctlPointFlag = models.CharField(max_length=20)
    voltageUnderloadFlag = models.CharField(max_length=20)
    powerLimitFlag = models.CharField(max_length=20)
    mcTempFlag = models.CharField(max_length=20)
    motorTempFlag = models.CharField(max_length=20)

    mcuTemp = models.CharField(max_length=20)
    motorTemp = models.CharField(max_length=20)
    AIRFlag = models.CharField(max_length=20)
    dcMainVoltage = models.CharField(max_length=20)
    dcMainCurrent = models.CharField(max_length=20)
    acCurrent = models.CharField(max_length=20)
    power = models.CharField(max_length=20)
    batVoltage = models.CharField(max_length=20)
    batCurrent = models.CharField(max_length=20)
    batSoc = models.CharField(max_length=20)
    batMaxTemp = models.CharField(max_length=20)
    batMaxCellVolt = models.CharField(max_length=20)
