import sys
import json
import math
from enum import Enum

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QToolBar, QAction, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter, QFont

class ResourceType(Enum):
    WATER = "Water"
    OIL = "Oil"
    GAS = "Gas"
    STEAM = "Steam"
    ACID = "Acid"

class BuildingType(Enum):
    PUMP = "Pump"
    REFINERY = "Refinery"
    BOILER = "Boiler"
    MIXER = "Mixer"
    STORAGE = "Storage"
    PIPE = "Pipe"

class Resource:
    def __init__(self, resourceType, amount=0):
        self.type = resourceType
        self.amount = amount
        self.color = self.getColor()

    def getColor(self):
        colors = {
            ResourceType.WATER: QColor(100, 150, 255),
            ResourceType.OIL: QColor(50, 50, 50),
            ResourceType.GAS: QColor(200, 200, 100),
            ResourceType.STEAM: QColor(220, 220, 220),
            ResourceType.ACID: QColor(150, 255, 100)
        }
        return colors.get(self.type, QColor(128, 128, 128))
    
class Building:
    def __init__(self, x, y, buildingType):
        self.x = x
        self.y = y
        self.type = buildingType
        self.inputs = {}
        self.outputs = {}
        self.connectedBuildings = []
        self.productionRate = 1.0
        self.efficiency = 1.0
        self.working = False
        self.setupBuildingProperties()

    def setupBuildingProperties(self):
        if self.type == BuildingType.PUMP:
            self.outputs[ResourceType.WATER] = 0
            self.maxOutput = 50
            self.color = QColor(80, 120, 200)

        elif self.type == BuildingType.REFINERY:
            self.inputs[ResourceType.OIL] = 0
            self.outputs[ResourceType.GAS] = 0
            self.maxInput = 30
            self.maxOutput = 20
            self.color = QColor(150, 100, 50)

        elif self.type == BuildingType.BOILER:
            self.inputs[ResourceType.WATER] = 0
            self.outputs[ResourceType.STEAM] = 0
            self.maxInput = 40
            self.maxOutput = 35
            self.color = QColor(200, 100, 100)

        elif self.type == BuildingType.MIXER:
            self.inputs[ResourceType.WATER] = 0
            self.outputs[ResourceType.ACID] = 0
            self.maxInput = 25
            self.maxOutput = 40
            self.color = QColor(100, 200, 100)

        elif self.type == BuildingType.STORAGE:
            self.inputs[ResourceType.WATER] = 0
            self.inputs[ResourceType.OIL] = 0
            self.inputs[ResourceType.GAS] = 0
            self.maxStorage = 200
            self.color = QColor(120, 120, 120)

    def canProduce(self):
        if self.type == BuildingType.PUMP:
            return self.outputs[ResourceType.WATER] < self.maxOutput
        
        elif self.type == BuildingType.REFINERY:
            return (self.inputs[ResourceType.OIL] >= 2 and 
                   self.outputs[ResourceType.GAS] < self.maxOutput)
        
        elif self.type == BuildingType.BOILER:
            return (self.inputs[ResourceType.WATER] >= 1 and 
                   self.outputs[ResourceType.STEAM] < self.maxOutput)
        
        elif self.type == BuildingType.MIXER:
            return (self.inputs[ResourceType.WATER] >= 1 and 
                   self.inputs.get(ResourceType.ACID, 0) >= 1 and
                   self.outputs[ResourceType.ACID] < self.maxOutput)
        return False

    def Produce(self):
        if not self.canProduce():
            self.working = False
            return
        
        self.working = True
        
        if self.type == BuildingType.PUMP:
            self.outputs[ResourceType.WATER] += 2 * self.efficiency

        elif self.type == BuildingType.REFINERY:
            self.inputs[ResourceType.OIL] -= 2
            self.outputs[ResourceType.GAS] += 1 * self.efficiency

        elif self.type == BuildingType.BOILER:
            self.inputs[ResourceType.WATER] -= 1
            self.outputs[ResourceType.STEAM] += 1 * self.efficiency

        elif self.type == BuildingType.MIXER:
            self.inputs[ResourceType.WATER] -= 1
            self.outputs[ResourceType.ACID] += 2 * self.efficiency

        
        
