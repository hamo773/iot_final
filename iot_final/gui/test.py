from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QComboBox
from PyQt5.QtGui import QIcon,QImage,QPixmap
import gui
import requests  
from requests.auth import HTTPBasicAuth
import json  
#import time
import cv2
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtCore
import threading

    
params = {}
auth = {'admin', 'admin'}
url = 'http://192.168.78.130:8282/~/mn-cse/mn-name/Air_Conditioner'
url_create_ae = 'http://192.168.72.20:8282/~/mn-cse'
url_create_cnt = 'http://192.168.72.20:8282/~/mn-cse/mn-name/' + "sensor1"
url_create_con = 'http://192.168.72.20:8282/~/mn-cse/mn-name/' +"sensor1"  + "/DATA"
url_get_instruction = 'http://192.168.72.20:8282/~/mn-cse/mn-name/' + "sensor1" + "/instruction/la"
url_get_DATA = 'http://192.168.72.20:8282/~/mn-cse/mn-name/' + "sensor1" + "/DATA/la"
header_get_instruction = {'X-M2M-Origin': 'admin:admin'}
class Main(QMainWindow, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

            # do something
    
    #def setup_control(self):
        #T
        #self.img_path = "C:/Users/alks7/Pictures/Acer/Acer_Wallpaper_04_3840x2400.jpg"
        #self.display_img()

    #def display_img(self):
        #self.img = cv2.imread(self.img_path)
        #height, width, channel = self.img.shape
        #bytesPerline = 3 * width
        #self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        #self.ui.label.setPixmap(QPixmap.fromImage(self.qimg))    

fan_speed=1
temperature=0
history_t=[]
history_f=[]
def graph(self):
    plt.subplot(1,2,1)
    plt.plot(history_t)
    plt.xlabel("temparature")
    plt.show()
    plt.subplot(1,2,2)
    plt.plot(history_f)
    plt.xlabel("fan speed")
    plt.show()



    
def refresh(self):
        
    #global on
    global temperature
    global fan
    #global movie
    movie = QMovie('fan.gif')
    movie.setScaledSize(window.label_2.size())
    window.label_2.setMovie(movie)
    movie.start()
    def show():
        #movie = QMovie('fan.gif')
        #global on
        global temperature
        global fan
        #global movie
        #movie.start()
        while(True):
            
            x = requests.get(url_get_DATA,headers=header_get_instruction)
            pos=x.text.find('temperature&quot; val=&quot;')
            lenght= len('temperature&quot; val=&quot;')
            temperature = x.text[pos+lenght:pos+lenght+4]
            #print(temperature)
            pos=x.text.find('fan&quot; val=&quot;')
            lenght= len('fan&quot; val=&quot;')
            fan = x.text[pos+lenght:pos+lenght+4]
            temperature=float(temperature)
            fan=int(fan[0])
            history_f.append(fan)
            history_t.append(temperature)
            if fan !=0:
                img=cv2.imread("on.png")
                img=cv2.resize(img,(80,40))
                self.img=img
                height,width,channel=self.img.shape
                bytesPerline=3*width
                self.qimg=QImage(self.img,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
                window.label_3.setPixmap(QPixmap.fromImage(self.qimg))
                text="current temp:"+str(temperature)
                window.label.setText(text)
                #movie = QMovie('fan.gif')
                #movie.setScaledSize(window.label_2.size())
                #window.label_2.setMovie(movie)
                text2="fan speed:"+str(fan)
                
                movie.setSpeed(fan*50)
                movie.start() 
                window.label_4.setText(text2)
                
                #print("123")
                #time.sleep(1)

                
                
                
            else:
                img=cv2.imread("off.png")
                img=cv2.resize(img,(100,40))
                self.img=img
                height,width,channel=self.img.shape
                bytesPerline=3*width
                self.qimg=QImage(self.img,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
                window.label_3.setPixmap(QPixmap.fromImage(self.qimg))
                text="current temp:"+str(temperature)
                window.label.setText(text)
                #movie = QMovie('fan.gif')
                #movie.setScaledSize(window.label_2.size())
                #window.label_2.setMovie(movie)
                text2="off"
                window.label_4.setText(text2)
                movie.setSpeed(fan)
                movie.start()
                #movie.setPaused()
                #time.sleep(1)
    t1 = threading.Thread(target = show)
    t1.start() 
        

        
        
        



    
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    #movie = QMovie('fan.gif')
    window.show()
    window.pushButton.mousePressEvent = graph
    window.pushButton_2.mousePressEvent = refresh
    refresh(window)
    #window.pushButton_4.mousePressEvent = aug
    #window.pushButton_3.mousePressEvent = showmodel
    #window.pushButton_5.mousePressEvent = showal
    #window.pushButton_6.mousePressEvent = inference

    sys.exit(app.exec_())           