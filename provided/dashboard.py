import tkinter as tk

def dashboard_fun():
    def exit():
        root.destroy()
        print('App closed successfully')

    root = tk.Tk()
    root.geometry('1000x1000')
    tk.Label(text='WELCOME TO THE DASHBOARD', font=('Arial', 56)).pack(padx=10, pady=5)
    tk.Button(text='Exit', font=('Arial', 56), command=exit).pack(pady=5)
    root.mainloop()
