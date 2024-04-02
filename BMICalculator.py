from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

import tkinter
from tkinter import ttk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

window=tkinter.Tk()
window.title("BMI Calculator")
frame=tkinter.Frame(window)
frame.pack()

def save():
    userFName = userFirstNametxt.get()
    userLName = userLastNametxt.get()
    userHeightUnit=userHeightUnitBox.get()
    userWeightUnit=userWeightUnitBox.get()
    userAge = userAgeBox.get()
    userHeight = userHeightBox.get()
    userWeight = userWeightBox.get()

    if userFName == '' or userLName == '' or userHeight=='' or userWeight=='' or userHeightUnit=='' or userWeightUnit=='':
        tkinter.messagebox.showwarning(title="Error",message="Please fill the blank fields")
    else:
     try:
        if userHeightUnit=='inches':
           userHeight=float(userHeight)*0.0254
        if userWeightUnit=='lbs':
           userWeight=float(userWeight)*0.453

        bmi_category = calculateBMI(userHeight, userWeight)

     except ValueError:
        tkinter.messagebox.showwarning(title="Error",message="Please enter valid Height & Weight")

     else:

      userData = [userFName, userLName, userAge, userHeight, userWeight, bmi_category]
      display_BMI(userData)

      with open('bmidata.csv','a') as filewriter:
          filewritercsv=csv.writer(filewriter)
          filewritercsv.writerow(userData)

def showbargraph():
    bmi_count={'Obese':0,'Overweight':0,'Normal':0,'Underweight':0}
    category=[]
    count=[]
    with open('bmidata.csv', 'r') as filereader:
        filereadercsv=csv.reader(filereader)
        for row in filereadercsv:
            if row[5]=='Obese':
               bmi_count['Obese']+=1
            elif row[5]=='Overweight':
                bmi_count['Overweight'] += 1
            elif row[5] == 'Normal':
                bmi_count['Normal'] += 1
            elif row[5] == 'Underweight':
                bmi_count['Underweight'] += 1

    for k,v in bmi_count.items():
        if v!=0 :
         category.append(k)
         count.append(v)

    import matplotlib.pyplot as plt

    fig1,ax1 = plt.subplots()
    plt.title("Graphical Distribution of BMI Categories")
    ax1.pie(count,labels=category,shadow=True, startangle=90,autopct='%1.1f%%')

    canvas = FigureCanvasTkAgg(fig1,master=window)

    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def display_BMI(userdata):
    tkinter.messagebox.showinfo(title='BMI Result', message='The BMI Category for '+userdata[0]+" "+userdata[1]+' is ' +userdata[5])
def calculateBMI(height,weight):
    height=float(height)/100
    weight=float(weight)
    bmi=weight/(height**2)

    if bmi>30:
       return 'Obese'
    elif bmi>=25:
        return 'Overweight'
    elif bmi>=18.5:
        return 'Normal'
    elif bmi<18.5:
        return 'Underweight'

def clear():
    userFirstNametxt.delete(0,'end')
    userLastNametxt.delete(0,'end')
    userAgeBox.delete(0,'end')
    userHeightBox.delete(0,'end')
    userWeightBox.delete(0,'end')

userInfoFrame=tkinter.LabelFrame(frame,text='User Information')
userInfoFrame.grid(row=0,column=0,stick='news')

userFirstNameLabel=tkinter.Label(userInfoFrame,text='First Name')
userFirstNameLabel.grid(row=0,column=0)

userFirstNametxt=tkinter.Entry(userInfoFrame)
userFirstNametxt.grid(row=0,column=1)

userLastNameLabel=tkinter.Label(userInfoFrame,text='Last Name')
userLastNameLabel.grid(row=0,column=3)

userLastNametxt=tkinter.Entry(userInfoFrame)
userLastNametxt.grid(row=0,column=4)

userAgeLabel=tkinter.Label(userInfoFrame,text='Age')
userAgeLabel.grid(row=1,column=0)

userAgeBox=tkinter.Spinbox(userInfoFrame,from_=2,to=100)
userAgeBox.grid(row=1,column=1)

userMeasurementFrame=tkinter.LabelFrame(frame,text='User Measurement')
userMeasurementFrame.grid(row=1,column=0,sticky='news')

userHeightLabel=tkinter.Label(userMeasurementFrame,text="Height(m)")
userHeightLabel.grid(row=2,column=0)

userHeightBox=tkinter.Spinbox(userMeasurementFrame,from_=50,to=272)
userHeightBox.grid(row=2,column=1)

userHeightUnitBox=ttk.Combobox(userMeasurementFrame,values=['centimeters','inches'])
userHeightUnitBox.grid(row=2,column=2)

userWeightLabel=tkinter.Label(userMeasurementFrame,text="Weight")
userWeightLabel.grid(row=2,column=3)

userWeightBox=tkinter.Spinbox(userMeasurementFrame,from_=10,to=500)
userWeightBox.grid(row=2,column=4)

userWeightUnitBox=ttk.Combobox(userMeasurementFrame,values=['kg','lbs'])
userWeightUnitBox.grid(row=2,column=5)

saveButton=tkinter.Button(frame,text='Calculate BMI',command=save)
saveButton.grid(row=2,column=0)

clearButton=tkinter.Button(frame,text='Clear Details',command=clear)
clearButton.grid(row=3,column=0)

showGraphButton=tkinter.Button(frame,text='Show Graph',command=showbargraph)
showGraphButton.grid(row=4,column=0)

window.mainloop()

