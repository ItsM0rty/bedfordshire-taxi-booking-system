import customtkinter as CTk
from login import LoginPage
from register import RegisterPage
from dashboard import DashboardPage
from db_setup import init_db

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("dark-blue")

class MainApp(CTk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Taxi Booking System")
        self.resizable(False, False)

        try:
            import os
            from PIL import ImageTk
            anIconPath = os.path.join(os.path.dirname(__file__), "assets", "static", "img", "tbs_icon.png")
            if os.path.exists(anIconPath):
                self.wm_iconbitmap()
                self.iconpath = ImageTk.PhotoImage(file=anIconPath)
                self.iconphoto(False, self.iconpath)
        except Exception as anError:
            print(f"Icon loading failed: {anError}")

        init_db()

        self.container = CTk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        
        for aPageClass in (LoginPage, RegisterPage):
            aPage = aPageClass(self.container, self)
            self.pages[aPageClass] = aPage
            aPage.grid(row=0, column=0, sticky="nsew")
        
        self.show_page(LoginPage)

    def show_page(self, aPageClass):
        aPage = self.pages.get(aPageClass)
        if aPage:
            aPage.tkraise()

    def show_login(self):
        self.show_page(LoginPage)

    def show_register(self):
        self.show_page(RegisterPage)

    def show_dashboard(self, aUserRole, aUserName, aUserId=None):
        anOldDashboard = self.pages.get(DashboardPage)
        if anOldDashboard:
            anOldDashboard.destroy()
        
        aDashboard = DashboardPage(self.container, self, aUserRole, aUserName, aUserId)
        self.pages[DashboardPage] = aDashboard
        aDashboard.grid(row=0, column=0, sticky="nsew")
        aDashboard.tkraise()

if __name__ == "__main__":
    anApp = MainApp()
    anApp.mainloop()
