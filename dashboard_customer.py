import customtkinter as CTk
from tkinter import messagebox
import sqlite3
from datetime import datetime


class CustomerDashboardMixin:
    def show_customer_dashboard(self, aParent):
        aTabFrame = CTk.CTkFrame(aParent, fg_color="transparent")
        aTabFrame.pack(fill="x", pady=(0, 30))

        self.booking_tab = CTk.CTkButton(
            aTabFrame,
            text="Book a Ride",
            font=CTk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#FFD700",
            text_color="#000000",
            hover_color="#FFC700",
            height=44,
            corner_radius=8,
            command=lambda: self.show_booking_form(aParent),
        )
        self.booking_tab.pack(side="left", padx=(0, 12), fill="x", expand=True)

        self.bookings_tab = CTk.CTkButton(
            aTabFrame,
            text="My Bookings",
            font=CTk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#2D3748",
            text_color="#E2E8F0",
            hover_color="#374151",
            height=44,
            corner_radius=8,
            command=lambda: self.show_my_bookings(aParent),
        )
        self.bookings_tab.pack(side="left", fill="x", expand=True)

        self.content_area = CTk.CTkFrame(aParent, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True)
        self.show_booking_form(aParent)

    def show_booking_form(self, aParent):
        for aWidget in self.content_area.winfo_children():
            aWidget.destroy()

        self.booking_tab.configure(fg_color="#FFD700", text_color="#000000")
        self.bookings_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")

        aFormCard = CTk.CTkFrame(
            self.content_area,
            fg_color="#1A1F2E",
            corner_radius=12,
            border_width=1,
            border_color="#2D3748",
        )
        aFormCard.pack(fill="both", expand=True)

        aFormContent = CTk.CTkFrame(aFormCard, fg_color="transparent")
        aFormContent.pack(fill="both", expand=True, padx=30, pady=30)

        CTk.CTkLabel(
            aFormContent,
            text="Plan Your Journey",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        CTk.CTkLabel(
            aFormContent,
            text="Pickup Location",
            font=CTk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 8))
        self.pickup_entry = CTk.CTkEntry(
            aFormContent,
            placeholder_text="Enter your pickup location",
            height=45,
            border_width=2,
            border_color="#2D3748",
            fg_color="#0F1419",
            text_color="#E2E8F0",
            placeholder_text_color="#7A8195",
            font=CTk.CTkFont(size=12),
            corner_radius=8,
        )
        self.pickup_entry.pack(fill="x", pady=(0, 20))

        CTk.CTkLabel(
            aFormContent,
            text="Drop-off Location",
            font=CTk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 8))
        self.dropoff_entry = CTk.CTkEntry(
            aFormContent,
            placeholder_text="Where are you going?",
            height=45,
            border_width=2,
            border_color="#2D3748",
            fg_color="#0F1419",
            text_color="#E2E8F0",
            placeholder_text_color="#7A8195",
            font=CTk.CTkFont(size=12),
            corner_radius=8,
        )
        self.dropoff_entry.pack(fill="x", pady=(0, 20))

        aDtFrame = CTk.CTkFrame(aFormContent, fg_color="transparent")
        aDtFrame.pack(fill="x", pady=(0, 20))

        aDateCol = CTk.CTkFrame(aDtFrame, fg_color="transparent")
        aDateCol.pack(side="left", fill="both", expand=True, padx=(0, 10))
        CTk.CTkLabel(
            aDateCol,
            text="Date",
            font=CTk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 8))
        self.date_entry = CTk.CTkEntry(
            aDateCol,
            placeholder_text="YYYY-MM-DD",
            height=45,
            border_width=2,
            border_color="#2D3748",
            fg_color="#0F1419",
            text_color="#E2E8F0",
            placeholder_text_color="#7A8195",
            font=CTk.CTkFont(size=12),
            corner_radius=8,
        )
        self.date_entry.pack(fill="both", expand=True)

        aTimeCol = CTk.CTkFrame(aDtFrame, fg_color="transparent")
        aTimeCol.pack(side="left", fill="both", expand=True)
        CTk.CTkLabel(
            aTimeCol,
            text="Time",
            font=CTk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 8))
        self.time_entry = CTk.CTkEntry(
            aTimeCol,
            placeholder_text="HH:MM",
            height=45,
            border_width=2,
            border_color="#2D3748",
            fg_color="#0F1419",
            text_color="#E2E8F0",
            placeholder_text_color="#7A8195",
            font=CTk.CTkFont(size=12),
            corner_radius=8,
        )
        self.time_entry.pack(fill="both", expand=True)

        def set_now():
            aNow = datetime.now()
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, aNow.strftime("%Y-%m-%d"))
            self.time_entry.delete(0, "end")
            self.time_entry.insert(0, aNow.strftime("%H:%M"))

        CTk.CTkButton(
            aFormContent,
            text="Use Current Date & Time",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#4FC3F7",
            text_color="#0A192F",
            hover_color="#29B6F6",
            height=44,
            corner_radius=8,
            command=set_now,
        ).pack(fill="x", pady=(10, 10))

        CTk.CTkButton(
            aFormContent,
            text="Book Your Taxi",
            font=CTk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#FFD700",
            text_color="#000000",
            hover_color="#FFC700",
            height=50,
            corner_radius=8,
            command=self.submit_booking,
        ).pack(fill="x", pady=(10, 0))

    def submit_booking(self):
        aPickup = self.pickup_entry.get().strip()
        aDropoff = self.dropoff_entry.get().strip()
        aDate = self.date_entry.get().strip()
        aTime = self.time_entry.get().strip()

        if not all([aPickup, aDropoff, aDate, aTime]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            datetime.strptime(aDate, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        try:
            datetime.strptime(aTime, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM")
            return

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute(
                "INSERT INTO bookings (user_id, pickup_location, dropoff_location, booking_date, booking_time) VALUES (?, ?, ?, ?, ?)",
                (self.user_id, aPickup, aDropoff, aDate, aTime),
            )
            aConn.commit()
            aConn.close()
            messagebox.showinfo("Success", "Booking confirmed! Your taxi will arrive shortly.")
            self.pickup_entry.delete(0, "end")
            self.dropoff_entry.delete(0, "end")
            self.date_entry.delete(0, "end")
            self.time_entry.delete(0, "end")
        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to book taxi: {str(anError)}")

    def show_my_bookings(self, aParent):
        for aWidget in self.content_area.winfo_children():
            aWidget.destroy()

        self.booking_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")
        self.bookings_tab.configure(fg_color="#FFD700", text_color="#000000")

        aBookingsContainer = CTk.CTkFrame(self.content_area, fg_color="transparent")
        aBookingsContainer.pack(fill="both", expand=True)
        CTk.CTkLabel(
            aBookingsContainer,
            text="Your Bookings",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute(
                "SELECT id, pickup_location, dropoff_location, booking_date, booking_time, status, driver_id FROM bookings WHERE user_id = ? ORDER BY created_at DESC",
                (self.user_id,),
            )
            aBookings = aCur.fetchall()
            aConn.close()

            if not aBookings:
                anEmptyFrame = CTk.CTkFrame(
                    aBookingsContainer,
                    fg_color="#1A1F2E",
                    corner_radius=12,
                    border_width=1,
                    border_color="#2D3748",
                )
                anEmptyFrame.pack(fill="both", expand=True, pady=30)
                CTk.CTkLabel(
                    anEmptyFrame,
                    text="No bookings yet\nBook your first ride!",
                    font=CTk.CTkFont(family="Segoe UI", size=16),
                    text_color="#B0B8C1",
                ).pack(expand=True)
                return

            for aBooking in aBookings:
                aBookingId, aPickup, aDropoff, aDate, aTime, aStatus, aDriverId = aBooking
                aBookingCard = CTk.CTkFrame(
                    aBookingsContainer,
                    fg_color="#1A1F2E",
                    corner_radius=10,
                    border_width=1,
                    border_color="#2D3748",
                )
                aBookingCard.pack(fill="x", pady=12)
                anInfoFrame = CTk.CTkFrame(aBookingCard, fg_color="transparent")
                anInfoFrame.pack(fill="x", padx=20, pady=15)

                aRouteFrame = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                aRouteFrame.pack(fill="x", pady=(0, 10))
                CTk.CTkLabel(
                    aRouteFrame,
                    text=f"From: {aPickup}",
                    font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    text_color="#FFD700",
                ).pack(anchor="w")
                CTk.CTkLabel(
                    aRouteFrame, text="     |", font=CTk.CTkFont(size=10), text_color="#7A8195"
                ).pack(anchor="w", pady=(2, 2))
                CTk.CTkLabel(
                    aRouteFrame,
                    text=f"To: {aDropoff}",
                    font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    text_color="#4FC3F7",
                ).pack(anchor="w")

                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"{aDate} at {aTime}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=10)

                aStatusColors = {
                    "pending": "#FFD700",
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
                ).pack(anchor="w", pady=(10, 0))

                if aStatus == "pending":
                    aButtonRow = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                    aButtonRow.pack(fill="x", pady=(15, 0))

                    CTk.CTkButton(
                        aButtonRow,
                        text="Edit Booking",
                        font=CTk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                        fg_color="#4FC3F7",
                        hover_color="#29B6F6",
                        text_color="#FFFFFF",
                        height=32,
                        corner_radius=6,
                        command=lambda aBid=aBookingId, aP=aPickup, aD=aDropoff, aDt=aDate, aTm=aTime: self.edit_booking(aBid, aP, aD, aDt, aTm),
                    ).pack(side="left", fill="x", expand=True, padx=(0, 8))

                    CTk.CTkButton(
                        aButtonRow,
                        text="Cancel Booking",
                        font=CTk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                        fg_color="#FF6B6B",
                        hover_color="#FF5252",
                        text_color="#FFFFFF",
                        height=32,
                        corner_radius=6,
                        command=lambda aBid=aBookingId: self.cancel_booking(aBid),
                    ).pack(side="left", fill="x", expand=True)

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to fetch bookings: {str(anError)}")

    def edit_booking(self, aBookingId, aCurrentPickup, aCurrentDropoff, aCurrentDate, aCurrentTime):
        aDialog = CTk.CTkToplevel(self)
        aDialog.title("Edit Booking")
        aDialog.geometry("500x400")
        aDialog.transient(self)
        aDialog.grab_set()

        CTk.CTkLabel(
            aDialog,
            text="Edit Booking Details",
            font=CTk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#E2E8F0",
        ).pack(pady=(20, 20))

        aFormFrame = CTk.CTkFrame(aDialog, fg_color="transparent")
        aFormFrame.pack(fill="both", expand=True, padx=30, pady=10)

        CTk.CTkLabel(
            aFormFrame,
            text="Pickup Location",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 5))
        aPickupEntry = CTk.CTkEntry(
            aFormFrame,
            placeholder_text="Enter pickup location",
            height=40,
            width=400,
        )
        aPickupEntry.insert(0, aCurrentPickup)
        aPickupEntry.pack(fill="x", pady=(0, 15))

        CTk.CTkLabel(
            aFormFrame,
            text="Drop-off Location",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 5))
        aDropoffEntry = CTk.CTkEntry(
            aFormFrame,
            placeholder_text="Enter drop-off location",
            height=40,
            width=400,
        )
        aDropoffEntry.insert(0, aCurrentDropoff)
        aDropoffEntry.pack(fill="x", pady=(0, 15))

        aDtFrame = CTk.CTkFrame(aFormFrame, fg_color="transparent")
        aDtFrame.pack(fill="x", pady=(0, 15))

        aDateCol = CTk.CTkFrame(aDtFrame, fg_color="transparent")
        aDateCol.pack(side="left", fill="both", expand=True, padx=(0, 10))
        CTk.CTkLabel(
            aDateCol,
            text="Date (YYYY-MM-DD)",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 5))
        aDateEntry = CTk.CTkEntry(
            aDateCol,
            placeholder_text="YYYY-MM-DD",
            height=40,
        )
        aDateEntry.insert(0, aCurrentDate)
        aDateEntry.pack(fill="both", expand=True)

        aTimeCol = CTk.CTkFrame(aDtFrame, fg_color="transparent")
        aTimeCol.pack(side="left", fill="both", expand=True)
        CTk.CTkLabel(
            aTimeCol,
            text="Time (HH:MM)",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(0, 5))
        aTimeEntry = CTk.CTkEntry(
            aTimeCol,
            placeholder_text="HH:MM",
            height=40,
        )
        aTimeEntry.insert(0, aCurrentTime)
        aTimeEntry.pack(fill="both", expand=True)

        def save_changes():
            aPickup = aPickupEntry.get().strip()
            aDropoff = aDropoffEntry.get().strip()
            aDate = aDateEntry.get().strip()
            aTime = aTimeEntry.get().strip()

            if not all([aPickup, aDropoff, aDate, aTime]):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                datetime.strptime(aDate, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

            try:
                datetime.strptime(aTime, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM")
                return

            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute("SELECT driver_id FROM bookings WHERE id = ?", (aBookingId,))
                aResult = aCur.fetchone()
                aDriverId = aResult[0] if aResult else None

                if aDriverId:
                    if self.check_booking_overlap(aDriverId, aDate, aTime, aBookingId):
                        aConn.close()
                        messagebox.showerror(
                            "Overlap Detected",
                            "The assigned driver already has a booking at this time. Please select a different time.",
                        )
                        return

                aCur.execute(
                    "UPDATE bookings SET pickup_location = ?, dropoff_location = ?, booking_date = ?, booking_time = ? WHERE id = ?",
                    (aPickup, aDropoff, aDate, aTime, aBookingId),
                )
                aConn.commit()
                aConn.close()

                messagebox.showinfo("Success", "Booking updated successfully!")
                aDialog.destroy()
                aParent = self.content_area.master
                self.show_my_bookings(aParent)
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to update booking: {str(anError)}")

        CTk.CTkButton(
            aDialog,
            text="Save Changes",
            command=save_changes,
            width=400,
            height=40,
            fg_color="#FFD700",
            text_color="#000000",
        ).pack(pady=20)

    def cancel_booking(self, aBookingId):
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (aBookingId,))
                aConn.commit()
                aConn.close()
                messagebox.showinfo("Success", "Booking cancelled successfully.")
                aParent = self.content_area.master
                self.show_my_bookings(aParent)
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to cancel booking: {str(anError)}")

