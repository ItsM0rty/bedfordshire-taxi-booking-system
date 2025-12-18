import customtkinter as CTk
from tkinter import messagebox
import sqlite3
import os
from PIL import ImageTk


class DriverDashboardMixin:
    def show_driver_dashboard(self, aParent):
        self.driver_content_area = CTk.CTkFrame(aParent, fg_color="transparent")
        self.driver_content_area.pack(fill="both", expand=True)
        self.show_assigned_rides()

    def decline_ride(self, aBookingId):
        aDialog = CTk.CTkToplevel(self)
        aDialog.title("Decline Ride")
        aDialog.geometry("500x300")
        aDialog.transient(self)
        aDialog.grab_set()
        
        try:
            anIconPath = os.path.join(os.path.dirname(__file__), "assets", "static", "img", "tbs_icon.png")
            if os.path.exists(anIconPath):
                aDialog.wm_iconbitmap()
                iconpath = ImageTk.PhotoImage(file=anIconPath)
                aDialog.iconphoto(False, iconpath)
        except Exception as anError:
            pass

        CTk.CTkLabel(
            aDialog,
            text="Decline Ride",
            font=CTk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#E2E8F0",
        ).pack(pady=(20, 10))

        CTk.CTkLabel(
            aDialog,
            text="Please provide a reason for declining this ride:",
            font=CTk.CTkFont(family="Segoe UI", size=12),
            text_color="#B0B8C1",
        ).pack(pady=(0, 10))

        aReasonFrame = CTk.CTkFrame(aDialog, fg_color="transparent")
        aReasonFrame.pack(fill="both", expand=True, padx=30, pady=10)

        aReasonText = CTk.CTkTextbox(
            aReasonFrame,
            height=120,
            width=440,
            font=CTk.CTkFont(family="Segoe UI", size=12),
        )
        aReasonText.pack(fill="both", expand=True)
        aReasonText.insert("1.0", "")

        def confirm_decline():
            aReason = aReasonText.get("1.0", "end-1c").strip()

            if not aReason:
                messagebox.showerror("Error", "Please provide a reason for declining the ride.")
                return

            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute(
                    "UPDATE bookings SET driver_id = NULL, status = 'pending' WHERE id = ?",
                    (aBookingId,),
                )
                aConn.commit()
                aConn.close()

                messagebox.showinfo("Success", f"Ride declined. Reason: {aReason}")
                aDialog.destroy()
                self.show_assigned_rides()
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to decline ride: {str(anError)}")

        CTk.CTkButton(
            aDialog,
            text="Confirm Decline",
            command=confirm_decline,
            width=440,
            height=40,
            fg_color="#FF6B6B",
            text_color="#FFFFFF",
            hover_color="#FF5252",
        ).pack(pady=20)

    def show_assigned_rides(self):
        for aWidget in self.driver_content_area.winfo_children():
            aWidget.destroy()

        aContainer = CTk.CTkFrame(self.driver_content_area, fg_color="transparent")
        aContainer.pack(fill="both", expand=True)
        CTk.CTkLabel(
            aContainer,
            text="My Assigned Rides",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute(
                "SELECT b.id, b.pickup_location, b.dropoff_location, b.booking_date, b.booking_time, b.status, u.name, u.phone FROM bookings b JOIN users u ON b.user_id = u.id WHERE b.driver_id = ? ORDER BY b.created_at DESC",
                (self.user_id,),
            )
            aRides = aCur.fetchall()
            aConn.close()

            if not aRides:
                anEmptyFrame = CTk.CTkFrame(
                    aContainer,
                    fg_color="#1A1F2E",
                    corner_radius=12,
                    border_width=1,
                    border_color="#2D3748",
                )
                anEmptyFrame.pack(fill="both", expand=True, pady=30)
                CTk.CTkLabel(
                    anEmptyFrame,
                    text="No assigned rides yet\nAccept rides from Available Rides!",
                    font=CTk.CTkFont(family="Segoe UI", size=16),
                    text_color="#B0B8C1",
                ).pack(expand=True)
                return

            for aRide in aRides:
                aBookingId, aPickup, aDropoff, aDate, aTime, aStatus, aCustomerName, aCustomerPhone = aRide
                aRideCard = CTk.CTkFrame(
                    aContainer,
                    fg_color="#1A1F2E",
                    corner_radius=10,
                    border_width=1,
                    border_color="#2D3748",
                )
                aRideCard.pack(fill="x", pady=12)
                anInfoFrame = CTk.CTkFrame(aRideCard, fg_color="transparent")
                anInfoFrame.pack(fill="x", padx=20, pady=15)

                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Customer: {aCustomerName}",
                    font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    text_color="#E2E8F0",
                ).pack(anchor="w")
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Phone: {aCustomerPhone}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=(3, 10))
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Pickup: {aPickup}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#FFD700",
                ).pack(anchor="w")
                CTk.CTkLabel(
                    anInfoFrame, text="     |", font=CTk.CTkFont(size=10), text_color="#7A8195"
                ).pack(anchor="w", pady=(2, 2))
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Dropoff: {aDropoff}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#4FC3F7",
                ).pack(anchor="w", pady=(0, 10))
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"{aDate} at {aTime}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=(0, 10))

                aStatusColors = {
                    "assigned": "#81C784",
                    "completed": "#4CAF50",
                    "cancelled": "#E57373",
                }
                aStatusText = aStatus.capitalize()
                aStatusColor = aStatusColors.get(aStatus, "#B0B8C1")
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Status: {aStatusText}",
                    font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                    text_color=aStatusColor,
                ).pack(anchor="w", pady=(0, 15))

                if aStatus == "assigned":
                    aButtonRow = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                    aButtonRow.pack(fill="x", pady=(10, 0))

                    CTk.CTkButton(
                        aButtonRow,
                        text="Decline Ride",
                        font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                        fg_color="#FF6B6B",
                        hover_color="#FF5252",
                        text_color="#FFFFFF",
                        height=36,
                        corner_radius=6,
                        command=lambda aBid=aBookingId: self.decline_ride(aBid),
                    ).pack(side="left", fill="x", expand=True, padx=(0, 8))

                    CTk.CTkButton(
                        aButtonRow,
                        text="Mark as Completed",
                        font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                        fg_color="#4CAF50",
                        hover_color="#388E3C",
                        text_color="#FFFFFF",
                        height=36,
                        corner_radius=6,
                        command=lambda aBid=aBookingId: self.complete_ride(aBid),
                    ).pack(side="left", fill="x", expand=True)

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to fetch assigned rides: {str(anError)}")

    def complete_ride(self, aBookingId):
        if messagebox.askyesno("Confirm", "Mark this ride as completed?"):
            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute("UPDATE bookings SET status = 'completed' WHERE id = ?", (aBookingId,))
                aConn.commit()
                aConn.close()
                messagebox.showinfo("Success", "Ride marked as completed!")
                self.show_assigned_rides()
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to complete ride: {str(anError)}")

