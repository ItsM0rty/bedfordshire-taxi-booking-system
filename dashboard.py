import customtkinter as CTk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

from dashboard_customer import CustomerDashboardMixin
from dashboard_driver import DriverDashboardMixin
from dashboard_admin import AdminDashboardMixin

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("blue")


class DashboardPage(
    CustomerDashboardMixin,
    DriverDashboardMixin,
    AdminDashboardMixin,
    CTk.CTkFrame,
):
    def __init__(self, aParent, aController, aUserRole, aUserName, aUserId=None):
        super().__init__(aParent, fg_color="#0F1419")
        self.controller = aController
        self.user_role = aUserRole
        self.user_name = aUserName
        self.user_id = aUserId

        self.pack_propagate(False)
        self.grid_propagate(False)

        aMainContainer = CTk.CTkFrame(self, fg_color="transparent")
        aMainContainer.pack(fill="both", expand=True)

        aHeaderFrame = CTk.CTkFrame(aMainContainer, fg_color="#1A1F2E", corner_radius=0)
        aHeaderFrame.pack(fill="x", pady=0)

        aHeaderContent = CTk.CTkFrame(aHeaderFrame, fg_color="transparent")
        aHeaderContent.pack(fill="x", padx=40, pady=30)

        aTitleFrame = CTk.CTkFrame(aHeaderContent, fg_color="transparent")
        aTitleFrame.pack(fill="x", pady=(0, 15))

        if self.user_role.lower() == "customer":
            aDashboardTitle = "Customer Dashboard"
        elif self.user_role.lower() == "driver":
            aDashboardTitle = "Driver Dashboard"
        elif self.user_role.lower() == "admin":
            aDashboardTitle = "Admin Dashboard"
        else:
            aDashboardTitle = "TBS Taxi Service"

        CTk.CTkLabel(
            aTitleFrame,
            text=aDashboardTitle,
            font=CTk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#FFD700",
        ).pack(side="left")

        CTk.CTkButton(
            aTitleFrame,
            text="Logout",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            text_color="#FFFFFF",
            corner_radius=8,
            height=36,
            command=self.logout,
        ).pack(side="right")

        CTk.CTkLabel(
            aHeaderContent,
            text=f"Welcome back, {self.user_name.capitalize()}!",
            font=CTk.CTkFont(family="Segoe UI", size=16),
            text_color="#B0B8C1",
        ).pack(anchor="w")

        aContentScroll = CTk.CTkScrollableFrame(aMainContainer, fg_color="transparent")
        aContentScroll.pack(fill="both", expand=True)

        aContentFrame = CTk.CTkFrame(aContentScroll, fg_color="transparent")
        aContentFrame.pack(fill="both", expand=True, padx=40, pady=40)

        if self.user_role.lower() == "customer":
            self.show_customer_dashboard(aContentFrame)
        elif self.user_role.lower() == "driver":
            self.show_driver_dashboard(aContentFrame)
        elif self.user_role.lower() == "admin":
            self.show_admin_dashboard(aContentFrame)
    def logout(self):
        self.controller.show_login()
