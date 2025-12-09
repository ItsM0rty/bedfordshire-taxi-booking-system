from tkinter import *
from tkinter import messagebox
from dashboard import *

def login_fun():
    email = email_entry.get()
    password = pass_entry.get()
    if email == '' or password == '':
        messagebox.showwarning('Emtpy Fields Detected' , "Please don't leave any field empty")
    elif email.lower().strip() == 'admin@gmail.com' and password == '123':
        messagebox.showinfo(f'Welcome {email}', 'You have succesfully logged in')
        root.destroy()
        dashboard_fun()
    else:
        messagebox.showerror('Retry','Your Credentials seems to be invalid, please retry again')
        email_entry.delete(0,END)
        pass_entry.delete(0,END)


root = Tk()
root.title('Login App')
root.config(bg='Skyblue')
root.geometry('900x500')

Label(text='Email', font=('Arial', 40), bg='skyblue', fg='White').pack(pady=5)
email_entry = Entry(font=('Arial', 40))
email_entry.pack(pady=5)
Label(text='Password', font=('Arial', 40), bg='skyblue', fg='White').pack(pady=5)
pass_entry = Entry(font=('Arial', 40), show='*')
pass_entry.pack(pady=5)

Button(text='Login', font=('Arial', 40), bg='Red', fg='white', command=login_fun).pack(pady=5)
root.mainloop()
