import serial
from openpyxl import load_workbook
def do_mp3():
    arduino=serial.Serial('COM5',9600)
    tempEx=load_workbook(filename='people.xlsx')

    sheet1 = tempEx['Sheet1']
    f=open('sample.txt','r')
    x=[]
    x=f.read()
    

    
    for i in sheet1.rows:
        k=i[0].value
        if k in x:
            temp=i[4].value
            

    print(temp)
   
    arduino.write(temp)
do_mp3()
