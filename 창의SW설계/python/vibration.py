import serial

def do_vibration(x):
    arduino=serial.Serial('COM5',9600)
    f1=open('sample1.txt','r')
    f2=open('sample2.txt','r')
    f3=open('sample3.txt','r')
    
    x1=[]
    x2=[]
    x3=[]
    x1=f1.readlines()
    x2=f2.readlines()
    x3=f3.readlines()
    while True:
        if x in x1:
            arduino.write(b'c')
           
        elif x in x2:
            arduino.write(b'd')
          
        elif x in x3:
            arduino.write(b'e')
         
        

