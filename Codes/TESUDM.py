#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from PIL import Image, ImageTk
import cv2, os
from tkinter import filedialog
from win32api import GetSystemMetrics
from tkinter import ttk
import pandas as pd


# In[2]:


topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None

sys_width = int(GetSystemMetrics(0)*0.70)
sys_height = int(GetSystemMetrics(1)*0.70)

dataset=pd.read_csv('../Res/usrData/dataset.csv', encoding='latin-1').values


# In[3]:


#1-ANTI-TERMITE TREATMENT
#2-CONCRETE WORKS
#3-MASONORY WORKS
#4-TILE WORK
#5-PLUMBING WORK
#6-ELECTRICAL WORK
#7-PAINTING
#8-DOORS AND WINDOWS
#9-ROOF WORK

PLUMBING = []
plum_data = []
ELECTRICAL = []
elec_data = []
DOORS_AND_WINDOWS = []
dnw_data = []

for i in range(len(dataset)):
    if(int(str(dataset[i][0]).split(".")[0])==5):
        PLUMBING.append([dataset[i][1], dataset[i][4], dataset[i][3], dataset[i][2]])
    elif(int(str(dataset[i][0]).split(".")[0])==6):
        ELECTRICAL.append([dataset[i][1], dataset[i][4], dataset[i][3], dataset[i][2]])
    elif(int(str(dataset[i][0]).split(".")[0])==8):
        DOORS_AND_WINDOWS.append([dataset[i][1], dataset[i][4], dataset[i][3], dataset[i][2]])


# In[4]:


def mouse_st_XY(event):
    global topy, topx
    topx, topy = event.x, event.y

def mouse_ed_XY(event):
    global rect_id, canvas
    global topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)
    
def capture_data(ch):
    global topy, topx, botx, boty
    
    pp = Calculations()
    
    if(ch == 0):
        pp.area_calc("Please insert the Square feet of the whole project plan.", ch)
    elif(ch == 1):
        pp.area_calc("Please insert the Square feet of the Selected Area.", ch)
        sub_img = cvimg[topy:boty, topx:botx]
        cv2.imwrite("../Res/outputData/img.jpg", sub_img)
    else:
        pp.area_calc("Please insert the Square feet of the Selected Area.", ch)
        sub_img = cvimg[topy:boty, topx:botx]
        cv2.imwrite("../Res/outputData/img.jpg", sub_img)
    
def read_img(plan_path):
    global img, cvimg, canvas, canvas
    img = ImageTk.PhotoImage(Image.open(plan_path))
    cvimg = cv2.imread(plan_path)

def exit():
    global root, window, add_file_win, calculate, selection, get_data
    try:
        selection.destroy()
        calculate.destroy()
        add_file_win.destroy()
        get_data.destroy()
        root.deiconify()
    except Exception as e:
        print(e)
        
def add_row(_row):
    _row = _row+1
    return _row

def go_back():
    global selection
    try:
        selection.deiconify()
    except Exception as e:
        print(e)


# In[5]:


def add_file():
    global add_file_win, img_plan, render_plan, render_plan_resized, add_file_win_frame
    
    add_file_win.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    
    img = Image.open(add_file_win.filename)
    wid, hei = img.size
    resized_img = img.resize((int((wid*0.45)+(sys_width*0.3)), int((hei*0.45)+(sys_width*0.3))))
    render_plan = ImageTk.PhotoImage(img)
    render_plan_resized = ImageTk.PhotoImage(resized_img)
    img_plan = tk.Label(add_file_win_frame, image=render_plan_resized)
    img_plan.grid(column=1, row=2, pady=(10, 5), padx=10, rowspan=8)
    
    comfirm = tk.Label(add_file_win_frame, text="Comfirm The Image : ", font=("Arial Bold", 18))
    comfirm.grid(column=2, row=2, pady=(5, 5), padx=(30, 0), columnspan=2)
    
    yes_button = tk.Button(add_file_win_frame, text="Yes", bg="green", fg="White", font=("Arial Bold", 18), width=8, bd=0, command=third_page)
    yes_button.grid(column=2, row=3, pady=(5, 5), padx=(25, 5))
    
    no_button = tk.Button(add_file_win_frame, text="No", bg="red", fg="White", font=("Arial Bold", 18), width=8, bd=0, command=add_file)
    no_button.grid(column=3, row=3, pady=(5, 5), padx=5)


# In[6]:


def second_page():
    global add_file_win, root, add_file_win_frame
    
    root.withdraw()
    
    add_file_win = tk.Toplevel()
    add_file_win.title("Take-off and Estimating Software")
    add_file_win.configure(background='white')
    add_file_win.geometry(f"{sys_width}x{sys_height}")
    
    add_file_win_frame = scrool_bar(add_file_win)
    
    add_button = tk.Button(add_file_win_frame, text="Add File", bg="red", fg="White", font=("Arial Bold", 14), bd=0, command=add_file)
    add_button.grid(column=1, row=1, pady=(5, 5), padx=40)


# In[7]:


def third_page():
    
    global add_file_win, selection, Var2
    
    add_file_win.withdraw()
    
    selection = tk.Toplevel()
    selection.title("Take-off and Estimating Software")
    selection.configure(background='white')
    selection.geometry(f"{sys_width}x{sys_height}")
    
    selection_frame = scrool_bar(selection)
    
    Var2 = tk.IntVar()
    
    package = tk.Label(selection_frame, text="Please Select a Package\n------------------------", bg="white", fg="blue", font=("Arial Bold", int(sys_height*0.035)))
    package.grid(column=0, row=0, pady=(int(sys_height*0.1), 5), padx=int(sys_width*0.35))
    
    r1 = tk.Label(selection_frame, text = "Currently on Economy Package, Check the box to get Luxury.", font=("Arial Bold", int(sys_height*0.025)), bg="white", padx=5)
    r2 = tk.Checkbutton(selection_frame, text = "Luxury", variable = Var2, onvalue = 1, offvalue = 0, font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=5)

    r1.grid(column=0, row=1, pady=(5, 5), padx=20)
    r2.grid(column=0, row=2, pady=(5, 5), padx=20)
    
    service = tk.Label(selection_frame, text="Please Select a Service\n------------------------", bg="white", fg="blue", font=("Arial Bold", int(sys_height*0.035)))
    service.grid(column=0, row=3, pady=(5, 5), padx=20)
    
    op1 = tk.Button(selection_frame, text="Anti-termite treatment", bg="blue", fg="White", font=("Arial Bold", int(sys_height*0.025)), bd=0, command=lambda:fourth_page(0))
    op1.grid(column=0, row=4, pady=(5, 5), padx=20)
    
    op2 = tk.Button(selection_frame, text="Rooms, Living areas and other", bg="blue", fg="White", font=("Arial Bold", int(sys_height*0.025)), bd=0, command=lambda:fourth_page(1))
    op2.grid(column=0, row=5, pady=(5, 5), padx=20)
    
    op3 = tk.Button(selection_frame, text="Bathrooms", bg="blue", fg="White", font=("Arial Bold", int(sys_height*0.025)), bd=0, command=lambda:fourth_page(2))
    op3.grid(column=0, row=6, pady=(5, 5), padx=(20))
    


# In[8]:


def fourth_page(ch):
    
    if(ch==0):
        cho = "Anti-termite treatment"
    elif(ch==1):
        cho = "Rooms, Living areas and other"
    else:
        cho = "Bathrooms"
    
    global render_plan, rect_id, topx, topy, botx, boty, canvas, root, window, add_file_win, calculate, render_plan_resized, selection
    
    read_img(add_file_win.filename)
    
    selection.withdraw()
    
    calculate = tk.Toplevel()
    calculate.title("Take-off and Estimating Software")
    calculate.configure(background='white')
    calculate.geometry(f"{sys_width}x{sys_height}")
    
    cal_frame = scrool_bar(calculate)

    Logo = tk.Label(cal_frame, text=f"{cho}", font=("Arial Bold", int(sys_height*0.03)), bg="white", fg="blue")
    canvas = tk.Canvas(cal_frame, width=img.width(), height=img.height(), borderwidth=0, highlightthickness=0)
    canvas.create_image(0, 0, image=render_plan, anchor=tk.NW)
    rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(8, 8), fill='', outline='black')

    canvas.bind('<Button-1>', mouse_st_XY)
    canvas.bind('<B1-Motion>', mouse_ed_XY)

    calculate_button = tk.Button(cal_frame, text="Calculate", bg="blue", fg="White", font=("Arial Bold", int(sys_height*0.022)), bd=0, command=lambda:capture_data(ch))
    close_button = tk.Button(cal_frame, text="Exit", bg="red", fg="White", font=("Arial Bold", int(sys_height*0.022)), bd=0, command=exit)

    Logo.grid(column=1, row=0, pady=(20, 0), columnspan = 6)
    canvas.grid(column=1, row=1, padx=40, pady=(15, 30), columnspan = 6)
    calculate_button.grid(column=1, row=2, pady=(0, 20), padx=2)
    close_button.grid(column=6, row=2, pady=(0, 20), padx=2)


# In[9]:


class Calculations:
    def area_calc(self, msg, ch):
        
        self.bill_data = []
        self.total=0

        _row = 0

        global sqft, area, Var2
        
        if(Var2.get()==0):
            self.pkg="ECONOMY"
        else:
            self.pkg="LUXURY"

        area = tk.Toplevel()
        area.title("Take-off and Estimating Software")
        area.configure(background='white')
        area.geometry(f"{sys_width}x{sys_height}")

        area_frame = scrool_bar(area)

        infolab = tk.Label(area_frame, text=f"{msg}", bg="white", fg="blue", font=("Arial Bold", int(sys_height*0.035)))

        sqft = tk.Entry(area_frame, width=50)
        sqft_lab = tk.Label(area_frame, text="Squre ft : ", font=("Arial Bold", int(sys_height*0.02)), bg="white")

        infolab.grid(column = 0, row=_row, padx=10, pady=10, columnspan=5)
        _row = add_row(_row)
        sqft.grid(column = 1, row=_row, padx=10, pady=10, sticky="W")
        sqft_lab.grid(column = 0, row=_row, padx=10, pady=10, sticky="W")
        _row = add_row(_row)

        if(ch>0):
            notice_lab = tk.Label(area_frame, text="Notice: CONCRETE WORK, MASONORY WORK, TILE WORK, PAINTING, ROOF WORK calculates automatically.\nPlease select materials for PLUMBING WORK, ELECTRICAL WORK,\nDOORS AND WINDOWS manually as your wish.", font=("Arial Bold", int(sys_height*0.02)), bg="yellow")
            notice_lab.grid(column = 0, row=_row, padx=20, pady=10, columnspan=6, sticky="W")
            _row = add_row(_row)
            
            plumbing = tk.Label(area_frame, text = f"PACKAGE : {self.pkg}", font=("Arial Bold", int(sys_height*0.026)), bg="white", pady=10, fg="blue")
            plumbing.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
            _row = add_row(_row)

            plumbing = tk.Label(area_frame, text = "PLUMBING WORK", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            plumbing.grid(column = 0, row=_row, padx=20, pady=10, sticky="W", columnspan=6)
            _row = add_row(_row)

            for p in range(len(PLUMBING)):
                if(PLUMBING[p][1]=="BOTH" or PLUMBING[p][1]==self.pkg):
                    exec(f'self.plum_{p} = tk.Entry(area_frame, width=10)')
                    exec(f'self.plum_{p}.insert(0, 0)')
                    exec(f'self.plumbing_{p} = tk.Label(area_frame, text = PLUMBING[p][0], font=("Arial Bold", int(sys_height*0.022)), bg="white", pady=5)')
                    exec(f'self.plum_{p}.grid(column = 0, row=_row, padx=5, pady=10, sticky="N")')
                    exec(f'self.plumbing_{p}.grid(column = 1, row=_row, padx=5, pady=10, sticky="W", columnspan=6)')
                    _row = add_row(_row)
                else:
                    pass

            elecctrical = tk.Label(area_frame, text = "ELECTRICAL WORK", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            elecctrical.grid(column = 0, row=_row, padx=20, pady=10, sticky="W", columnspan=6)
            _row = add_row(_row)

            for e in range(len(ELECTRICAL)):
                if(ELECTRICAL[e][1]=="BOTH" or ELECTRICAL[e][1]==self.pkg):
                    exec(f'self.elec_{e} = tk.Entry(area_frame, width=10)')
                    exec(f'self.elec_{e}.insert(0, 0)')
                    exec(f'self.electirc_{e} = tk.Label(area_frame, text = ELECTRICAL[e][0], font=("Arial Bold", int(sys_height*0.022)), bg="white", pady=5)')
                    exec(f'self.elec_{e}.grid(column = 0, row=_row, padx=5, pady=10, sticky="N")')
                    exec(f'self.electirc_{e}.grid(column = 1, row=_row, padx=5, pady=10, sticky="W", columnspan=6)')
                    _row = add_row(_row)
                else:
                    pass

            DnW = tk.Label(area_frame, text = "DOORS AND WINDOWS", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            DnW.grid(column = 0, row=_row, padx=20, pady=10, sticky="W", columnspan=6)
            _row = add_row(_row)

            for d in range(len(DOORS_AND_WINDOWS)):
                if(DOORS_AND_WINDOWS[d][1]=="BOTH" or DOORS_AND_WINDOWS[d][1]==self.pkg):
                    exec(f'self.dnw_{d} = tk.Entry(area_frame, width=10)')
                    exec(f'self.dnw_{d}.insert(0, 0)')
                    exec(f'self.doornwin_{d} = tk.Label(area_frame, text = DOORS_AND_WINDOWS[d][0], font=("Arial Bold", int(sys_height*0.022)), bg="white", pady=5)')
                    exec(f'self.dnw_{d}.grid(column = 0, row=_row, padx=5, pady=10, sticky="N")')
                    exec(f'self.doornwin_{d}.grid(column = 1, row=_row, padx=5, pady=10, sticky="W", columnspan=6)')
                    _row = add_row(_row)
                else:
                    pass
            

        comfirm_button = tk.Button(area_frame, text="Done", bg="green", fg="White", font=("Arial Bold", int(sys_height*0.025)), bd=0, command=lambda:self.get_data(ch))
        comfirm_button.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
        _row = add_row(_row)

    def get_data(self, ch):

        global sqft, area

        s = sqft.get()
    
        if(ch>0):
            for p in range(len(PLUMBING)):
                if(PLUMBING[p][1]=="BOTH" or PLUMBING[p][1]==self.pkg):
                    exec(f'plum_data.append([PLUMBING[{p}][0], self.plum_{p}.get(), PLUMBING[{p}][2], PLUMBING[{p}][3]])')
                else:
                    pass

            for e in range(len(ELECTRICAL)):
                if(ELECTRICAL[e][1]=="BOTH" or ELECTRICAL[e][1]==self.pkg):
                    exec(f'elec_data.append([ELECTRICAL[{e}][0], self.elec_{e}.get(), ELECTRICAL[{e}][2], ELECTRICAL[{e}][3]])')
                else:
                    pass

            for d in range(len(DOORS_AND_WINDOWS)):
                if(DOORS_AND_WINDOWS[d][1]=="BOTH" or DOORS_AND_WINDOWS[d][1]==self.pkg):
                    exec(f'dnw_data.append([DOORS_AND_WINDOWS[{d}][0], self.dnw_{d}.get(), DOORS_AND_WINDOWS[{d}][2], DOORS_AND_WINDOWS[{d}][3]])')
                else:
                    pass
            
        
        area.withdraw()

        self.get_data = tk.Toplevel()
        self.get_data.title("Take-off and Estimating Software")
        self.get_data.configure(background='white')
        self.get_data.geometry(f"{sys_width}x{sys_height}")
        
        self.get_data_frame = scrool_bar(self.get_data)
        
        if(ch>0):
            self.calculate_data(s, plum_data, elec_data, dnw_data, ch)
        else:
            self.calculate_data(s, [], [], [], ch)

        back_btn = tk.Button(self.get_data_frame, text="Back", bg="blue", fg="White", font=("Arial Bold", int(sys_height*0.023)), bd=0, command=go_back)
        back_btn.grid(column=0, row=1, padx=40, pady=(40, 0), sticky="W")

        data_lab = tk.Label(self.get_data_frame, text="Calculated Data", font=("Arial Bold", int(sys_height*0.044)), bg="white", fg="blue")
        data_lab.grid(column=0, row=0, padx=40, pady=(40, 0))

    def calculate_data(self, s, plum_data, elec_data, dnw_data, ch):
        
        if(ch>0):
            _row = 2

            plumbing = tk.Label(self.get_data_frame, text = "PLUMBING WORK", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            plumbing.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
            _row = add_row(_row)

            for data in plum_data:
                if(data[3]=="Sq.ft."):
                    value = (int(s)*int(data[2].split('.')[1]))*int(data[1])
                else:
                    value = int(data[2].split('.')[1])*int(data[1])

                exec(f"data_{_row} = tk.Label(self.get_data_frame, text='{data[0]} - Rs. {value}', font=('Arial Bold', int(sys_height*0.023)), bg='white', fg='black')")
                exec(f"data_{_row}.grid(column=0, row={_row}, padx=40, pady=10, sticky='W')")

                self.bill_data.append([data[0], value])
                self.total+=(int(s)*int(data[2].split('.')[1]))*int(data[1])
                _row = add_row(_row)

            elecctrical = tk.Label(self.get_data_frame, text = "ELECTRICAL WORK", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            elecctrical.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
            _row = add_row(_row)

            for data in elec_data:

                if(data[3]=="Sq.ft."):
                    value = (int(s)*int(data[2].split('.')[1]))*int(data[1])
                else:
                    value = int(data[2].split('.')[1])*int(data[1])

                exec(f"data_{_row} = tk.Label(self.get_data_frame, text='{data[0]} - Rs. {value}', font=('Arial Bold', int(sys_height*0.023)), bg='white', fg='black')")
                exec(f"data_{_row}.grid(column=0, row={_row}, padx=40, pady=10, sticky='W')")

                self.bill_data.append([data[0], value])
                self.total+=(int(s)*int(data[2].split('.')[1]))*int(data[1])
                _row = add_row(_row)

            DnW = tk.Label(self.get_data_frame, text = "DOORS AND WINDOWS", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            DnW.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
            _row = add_row(_row)            

            for data in dnw_data:

                if(data[3]=="Sq.ft."):
                    value = (int(s)*int(data[2].split('.')[1]))*int(data[1])
                else:
                    value = int(data[2].split('.')[1])*int(data[1])

                exec(f"data_{_row} = tk.Label(self.get_data_frame, text='{data[0]} - Rs. {value}', font=('Arial Bold', int(sys_height*0.023)), bg='white', fg='black')")
                exec(f"data_{_row}.grid(column=0, row={_row}, padx=40, pady=10, sticky='W')")

                self.bill_data.append([data[0], value])
                self.total+=(int(s)*int(data[2].split('.')[1]))*int(data[1])
                _row = add_row(_row)

            total_lab = tk.Label(self.get_data_frame, text=f'Total - {self.total}', font=('Arial Bold', int(sys_height*0.025)), bg='white', fg='red')
            total_lab.grid(column=0, row=_row, padx=20, pady=20, sticky='W')
            _row = add_row(_row)

            self.bill_data.append(["Total", self.total])

            write_csv_data = pd.DataFrame(self.bill_data)
            write_csv_data.to_csv('../Res/out1.csv')
        else:
            _row = 2

            anti_termite = tk.Label(self.get_data_frame, text = f"ANTI-TERMITE TREATEMENT COST - Rs. {int(s)*55}", font=("Arial Bold", int(sys_height*0.025)), bg="white", pady=10, fg="red")
            anti_termite.grid(column = 0, row=_row, padx=20, pady=20, sticky="W", columnspan=6)
            _row = add_row(_row)


# In[10]:


def scrool_bar(window):
    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=1)
    
    scrl_canvas = tk.Canvas(main_frame, bg="white")
    scrl_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    scrl_bar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=scrl_canvas.yview)
    scrl_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
    scrl_canvas.configure(yscrollcommand=scrl_bar.set)
    scrl_canvas.bind('<Configure>', lambda e: scrl_canvas.configure(scrollregion = scrl_canvas.bbox("all")))
    
    sframe = tk.Frame(scrl_canvas, bg="white")
    
    scrl_canvas.create_window((0, 0), window=sframe, anchor="nw")
    
    return sframe


# In[11]:


root = tk.Tk()

root.title("Take-off and Estimating Software")
root.configure(background='white')
root.geometry(f"{sys_width}x{sys_height}")

n_rows =3
n_columns =3
for i in range(n_rows):
    root.grid_rowconfigure(i,  weight=1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight=1)

Logo = tk.Label(root, text="Welcome to the Sri Lanka’s\nfirst ever take-off and estimating\nSoftware", font=("Arial Bold", int(sys_height*0.044)), bg="white", fg="blue")
Logo.grid(column=1, row=0, pady=(20, 0))

render = ImageTk.PhotoImage(Image.open("../Res/imgs/bg/logo_img.png").resize((int(sys_width*0.5), int(sys_height*0.65))))
imgg = tk.Label(root, image=render)
imgg.grid(column=1, row=2, pady=(10, 5), padx=20)

estimate_button = tk.Button(root, text="Start Estimate", bg="red", fg="White", font=("Arial Bold", int(sys_height*0.023)), bd=0, command=second_page)

estimate_button.grid(column=1, row=3, pady=(5, 15), padx=20)

root.mainloop()


# In[ ]:




