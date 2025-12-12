import customtkinter as CTk
from tkinter import messagebox
from PIL import Image
import sqlite3

class LoginPage(CTk.CTkFrame):
    def __init__(self, aParent, aController):
        super().__init__(aParent, fg_color="#ffffff")
        self.controller = aController
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        aLeftFrame = CTk.CTkFrame(self, fg_color="#FFD700", corner_radius=0)
        aLeftFrame.grid(row=0, column=0, sticky="nsew")
        
        aLeftInner = CTk.CTkFrame(aLeftFrame, fg_color="transparent")
        aLeftInner.pack(expand=True)
        
        CTk.CTkLabel(
            aLeftInner,
            text="Welcome back to",
            font=CTk.CTkFont(family="Segoe UI", size=42, weight="bold"),
            text_color="#000000"
        ).pack(anchor="center", pady=(0, 50))
        
        try:
            aLogoImg = Image.open("./assets/static/img/tbs_big.png")
            aLogoImg.thumbnail((600, 600), Image.LANCZOS)
            aCtkLogo = CTk.CTkImage(light_image=aLogoImg, dark_image=aLogoImg, size=(aLogoImg.width, aLogoImg.height))
            aLogoLabel = CTk.CTkLabel(aLeftInner, image=aCtkLogo, text="")
            aLogoLabel.image = aCtkLogo
            aLogoLabel.pack(pady=(5, 10))
        except:
            CTk.CTkLabel(
                aLeftInner,
                text="Taxi Booking\nSystem",
                font=CTk.CTkFont(family="Segoe UI", size=48, weight="bold"),
                text_color="#000000"
            ).pack(pady=(5, 10))
        
        aRightFrame = CTk.CTkFrame(self, fg_color="#ffffff")
        aRightFrame.grid(row=0, column=1, sticky="nsew")
        
        aFormContainer = CTk.CTkFrame(aRightFrame, fg_color="transparent")
        aFormContainer.pack(expand=True, padx=50, pady=50)
        
        CTk.CTkLabel(
            aFormContainer,
            text="Sign In",
            font=CTk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w", pady=(0, 30))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Email address",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 8))
        
        self.email = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="name@mail.com",
            width=280,
            height=44,
            font=CTk.CTkFont(family="Segoe UI", size=12),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.email.pack(pady=(0, 20))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Password",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 8))
        
        self.password = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="••••••••••••••••",
            show="*",
            width=280,
            height=44,
            font=CTk.CTkFont(size=12),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.password.pack(pady=(0, 20))
        
        CTk.CTkButton(
            aFormContainer,
            text="Login",
            width=280,
            height=44,
            font=CTk.CTkFont(size=13, weight="bold"),
            fg_color="#FFD700",
            text_color="#000000",
            hover_color="#FFC700",
            command=self.login,
            corner_radius=8
        ).pack(pady=(0, 20))
        
        aSignupFrame = CTk.CTkFrame(aFormContainer, fg_color="transparent")
        aSignupFrame.pack()
        
        CTk.CTkLabel(
            aSignupFrame,
            text="Not a member yet?",
            font=CTk.CTkFont(size=12),
            text_color="#666666"
        ).pack(side="left", padx=(0, 5))

        
        aSwitch = CTk.CTkLabel(
            aSignupFrame,
            text="Sign up",
            font=CTk.CTkFont(size=12, weight="bold"),
            text_color="#F6BE00",
            cursor="hand2"
        )
        aSwitch.pack(side="left")
        
        def on_enter(anEvent):
            aSwitch.configure(text_color="#FFD84A")

        def on_leave(anEvent):
            aSwitch.configure(text_color="#F6BE00")

        aSwitch.bind("<Enter>", on_enter)
        aSwitch.bind("<Leave>", on_leave)

        
        aSignupFrame.bind("<Button-1>", lambda anE: self.controller.show_register())
        aSignupFrame.winfo_children()[1].bind("<Button-1>", lambda anE: self.controller.show_register())

    def login(self):
        anEmail = self.email.get().strip()
        aPassword = self.password.get().strip()

        if not anEmail or not aPassword:
            messagebox.showerror("Error", "Email and password are required.")
            return

        if not "@" in anEmail:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute("SELECT role, id, name FROM users WHERE email=? AND password=?", (anEmail, aPassword))
            aRow = aCur.fetchone()
            aConn.close()

            if not aRow:
                messagebox.showerror("Error", "Invalid email or password.")
                self.password.delete(0, "end")
                return

            self.controller.show_dashboard(aRow[0].lower(), aRow[2], aRow[1])
        except Exception as anError:
            messagebox.showerror("Error", f"Login failed: {str(anError)}")
            self.password.delete(0, "end")
