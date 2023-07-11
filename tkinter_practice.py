from tkinter import *
from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Entry(frm, text="input goal").grid(column=0, row=1)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# # btn = ttk.Button(frm, text="hello")
# # print(btn.configure().keys())
# root.mainloop()



# #Import the required Libraries
# from tkinter import *
# from tkinter import ttk

# #Create an instance of Tkinter frame
# win= Tk()

# #Set the geometry of Tkinter frame
# win.geometry("750x250")

# def display_text():
#    global entry
#    string= entry.get()
#    label.configure(text=string)

# #Initialize a Label to display the User Input
# label=Label(win, text="", font=("Courier 12 bold"))
# label.pack()

# #Create an Entry widget to accept User Input
# entry= Entry(win, width= 40)
# entry.focus_set()
# entry.pack()

# #Create a Button to validate Entry Widget
# ttk.Button(win, text= "Okay",width= 20, command= display_text).pack(pady=20)

# win.mainloop()

root = Tk()
root.title("testing")
root.geometry("500x500")
root.grid()
frm = ttk.Frame(root)
frm.grid(column=0, row=0)

label1 = Label(frm, text="Pressure you are trying to reach (Pa): ")
label1.pack(pady=5)

label2 = Label(frm, text="")
label2.pack()

pressure_entry = Entry(frm, width=20)
pressure_entry.pack(pady = 5)
pressure_entry.focus_set()

my_var = 0

def display_text():
    global pressure_entry
    string= pressure_entry.get()
    # print(string)
    my_var = string
    label2.configure(text=string)
    

ttk.Button(frm, text= "Enter", width= 20, command=display_text).pack(pady=5)
ttk.Button(frm, text= "Proceed", width= 20, command=frm.quit).pack(pady=5)

root.mainloop()