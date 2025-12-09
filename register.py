import customtkinter as CTk
from tkinter import messagebox
from PIL import Image
import sqlite3

class RegisterPage(CTk.CTkFrame):
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
            text="Welcome to",
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
            text="Create Account",
            font=CTk.CTkFont(size=28, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w", pady=(0, 25))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Full Name",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.name = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="John Doe",
            width=280,
            height=40,
            font=CTk.CTkFont(size=11),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.name.pack(pady=(0, 14))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Address",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.address = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="123 Main St",
            width=280,
            height=40,
            font=CTk.CTkFont(size=11),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.address.pack(pady=(0, 14))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Phone Number",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.phone = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="+1 (555) 123-4567",
            width=280,
            height=40,
            font=CTk.CTkFont(size=11),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.phone.pack(pady=(0, 14))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Email address",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.email = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="name@mail.com",
            width=280,
            height=40,
            font=CTk.CTkFont(size=11),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.email.pack(pady=(0, 14))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Password",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.password = CTk.CTkEntry(
            aFormContainer,
            placeholder_text="••••••••••••••••",
            show="*",
            width=280,
            height=40,
            font=CTk.CTkFont(size=11),
            border_width=2,
            border_color="#E8E8F0",
            fg_color="#F5F5FA",
            text_color="#000000"
        )
        self.password.pack(pady=(0, 14))
        
        CTk.CTkLabel(
            aFormContainer,
            text="Account Type",
            font=CTk.CTkFont(size=11, weight="bold"),
            text_color="#333333"
        ).pack(anchor="w", pady=(0, 6))
        
        self.role = CTk.CTkOptionMenu(
            aFormContainer,
            values=["Customer", "Driver", "Admin"],
            width=280,
            font=CTk.CTkFont(size=11),
            fg_color="#F5F5FA",
            button_color="#FFD700",
            button_hover_color="#FFC700",
            text_color="#000000",
            dropdown_text_color="#000000",
            dropdown_fg_color="#F5F5FA",
            dropdown_hover_color="#E8E8F0"
        )
        self.role.set("Customer")
        self.role.pack(pady=(0, 20), anchor="w")
        
        CTk.CTkButton(
            aFormContainer,
            text="Create Account",
            width=280,
            height=44,
            font=CTk.CTkFont(size=13, weight="bold"),
            fg_color="#FFD700",
            text_color="#000000",
            hover_color="#FFC700",
            command=self.register,
            corner_radius=8
        ).pack(pady=(0, 15))
        
        aLoginFrame = CTk.CTkFrame(aFormContainer, fg_color="transparent")
        aLoginFrame.pack()
        
        CTk.CTkLabel(
            aLoginFrame,
            text="Already have an account?",
            font=CTk.CTkFont(size=12),
            text_color="#666666"
        ).pack(side="left", padx=(0, 5))
        
        aLoginLabel = CTk.CTkLabel(
            aLoginFrame,
            text="Login",
            font=CTk.CTkFont(size=12, weight="bold"),
            text_color="#F6BE00",
            cursor="hand2"
        )
        aLoginLabel.pack(side="left")

        def on_enter_login(anEvent):
            aLoginLabel.configure(text_color="#FFD84A")

        def on_leave_login(anEvent):
            aLoginLabel.configure(text_color="#F6BE00")

        aLoginLabel.bind("<Enter>", on_enter_login)
        aLoginLabel.bind("<Leave>", on_leave_login)
        
        aLoginFrame.bind("<Button-1>", lambda anE: self.controller.show_login())
        aLoginFrame.winfo_children()[1].bind("<Button-1>", lambda anE: self.controller.show_login())

    def register(self):
        anEmail = self.email.get().strip()
        aPassword = self.password.get().strip()
        aName = self.name.get().strip()
        anAddress = self.address.get().strip()
        aPhone = self.phone.get().strip()
        aRole = self.role.get()

        if not all([anEmail, aPassword, aName, anAddress, aPhone]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not "@" in anEmail:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if len(aPassword) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        if len(aPhone) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute("""
                INSERT INTO users (email, password, role, name, address, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (anEmail, aPassword, aRole, aName, anAddress, aPhone))
            aConn.commit()
            aConn.close()
            
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.email.delete(0, "end")
            self.password.delete(0, "end")
            self.name.delete(0, "end")
            self.address.delete(0, "end")
            self.phone.delete(0, "end")
            self.role.set("Customer")
            
            self.controller.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This email is already registered. Please use a different email or try logging in.")
        except Exception as anError:
            messagebox.showerror("Error", f"Registration failed: {str(anError)}")
