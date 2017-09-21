#GalczakP12
#Programmer: Anthony Galczak
#EMail: agalczak@cnm.edu
#Purpose: Implement a GUI with GeoPoint class using a database

#Importing Libraries
import wx
from math import sqrt
import sqlite3

#---GeoPoint class---
class GeoPoint(object):
    def __init__(self, x=0, y=0, z=0, description = 'TBD'):
        self.x = x
        self.y = y
        self.z = z
        self.description = description
        
    def SetPoint(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def GetPoint(self):
        return self.x, self.y, self.z

    def Distance(self, toPoint):
        return sqrt(
            (self.x - toPoint.x)**2 +
            (self.y - toPoint.y)**2 +
            (self.z - toPoint.z)**2)
        
    def SetDescription(self, description):
        self.description = description

    def GetDescription(self):
        return self.description
    
    PointCoords = property(GetPoint, SetPoint)
    PointDescription = property(GetDescription, SetDescription)
    
#Submit Function
def submit(event):
#Initialization
    pointList = []
    shortestPoint = []
#GUI Capture Values
    userx = int(xGUI.GetValue())
    usery = int(yGUI.GetValue())
    userz = int(zGUI.GetValue())
    userlocation = GeoPoint(userx, usery, userz, 'Users Location')
#Database Interaction
    conn = sqlite3.connect('P12Points.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM Points')
    myTable = curs.fetchall()
#Assigning individual indices
    for row in myTable:
        newX = row[0]
        newY = row[1]
        newZ = row[2]
        newDescription = row[3]
#Instantiating the point into GeoPoint
        newPoint = GeoPoint(newX, newY, newZ, newDescription)
#Appending pointList with Points
        pointList.append(newPoint)
#Calculating distances and finding shortest point distance
    shortestPoint = pointList[0]
    for point in pointList:
        if point.Distance(userlocation) < shortestPoint.Distance(userlocation):
            shortestPoint = point
#Outputting Results  to User/GUI
    output.SetValue("You are closest to %s which is located at %s" % (shortestPoint.PointDescription, shortestPoint.PointCoords))

#-----GUI-----
#Instantiating wx App
GUI = wx.App()
#Display Main Window
win = wx.Frame(None, title = 'Point Calculator', size = (500, 400))
#Display xyz Window and Label
xGUI = wx.TextCtrl(win, pos = (5, 140), size = (60, 25))
xLabel = wx.StaticText (win, pos = (5, 115), size = (60, 25), label = 'x-Coord')                        
yGUI = wx.TextCtrl(win, pos = (5, 200), size = (60, 25))
yLabel = wx.StaticText (win, pos = (5, 175), size = (60, 25), label = 'y-Coord')
zGUI = wx.TextCtrl(win, pos = (5, 260), size = (60, 25))
zLabel = wx.StaticText (win, pos = (5, 235), size = (60, 25), label = 'z-Coord')
#Display Output Window and Label
output = wx.TextCtrl(win, pos = (240, 140), size = (200, 200), style = wx.TE_MULTILINE)
outputLabel = wx.StaticText(win, pos = (240, 115), size = (200, 25), label = 'Output')
#Submit Button and Binding
submitButton = wx.Button(win, label = 'Submit Coords', pos = (80, 200), size = (100, 25))
submitButton.Bind(wx.EVT_BUTTON, submit)
#Show "win" and GUI Loop
win.Show()
GUI.MainLoop()