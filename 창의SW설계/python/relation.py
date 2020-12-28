from openpyxl import load_workbook
def do_relation():
    tempEx=load_workbook(filename='people.xlsx')

    sheet1 = tempEx['Sheet1']
    f=open('sample.txt','r')
    x=[]
    x=f.read()
    

    temps = []

    for i in sheet1.rows:
        k=i[0].value
        if k in x:
            이름= i[0].value
            나이 = i[1].value
            신분 = i[2].value
            관계=i[3].value
            temp = (이름, 나이, 신분, 관계)
            temps.append(temp)

    print(temps)

