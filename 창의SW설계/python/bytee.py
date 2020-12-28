import serial
from openpyxl import load_workbook
arduino=serial.Serial('COM5',9600)
tempEx=load_workbook(filename='people.xlsx')
sheet1=tempEx['Sheet1']
f=open('sample.txt','r')
x=[]
i=1
x=f.read()
temps=[]
for i in sheet1.rows:
    k=i[0].value
    
    if k in x:
        my_str= i[0].value
        my_str1=i[1].value
        my_str2=i[2].value
        my_str3=i[3].value
        my_str_bytes = str.encode(my_str)
        type(my_str_bytes) 
        print(my_str_bytes)
        my_str_bytes2 =str.encode(my_str2)
        type(my_str_bytes2)
        print(my_str_bytes2)
        my_str_bytes3=str.encode(my_str3)
        type(my_str_bytes3)
        print(my_str_bytes3)
        while True:
            arduino.write(my_str_bytes+b'/'+my_str_bytes2+b'/'+my_str_bytes3+b'\0')
            

