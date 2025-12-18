import customtkinter as CTk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
import os
from PIL import ImageTk


class AdminDashboardMixin:
    def show_admin_dashboard(self, aParent):
        aTabFrame = CTk.CTkFrame(aParent, fg_color="transparent")
        aTabFrame.pack(fill="x", pady=(0, 30))

        self.users_tab = CTk.CTkButton(
            aTabFrame,
            text="Users",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#FFD700",
            text_color="#000000",
            hover_color="#FFC700",
            height=40,
            corner_radius=8,
            command=lambda: self.show_users_management(),
        )
        self.users_tab.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.bookings_admin_tab = CTk.CTkButton(
            aTabFrame,
            text="Bookings",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#2D3748",
            text_color="#E2E8F0",
            hover_color="#374151",
            height=40,
            corner_radius=8,
            command=lambda: self.show_bookings_management(),
        )
        self.bookings_admin_tab.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.reports_tab = CTk.CTkButton(
            aTabFrame,
            text="Reports",
            font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#2D3748",
            text_color="#E2E8F0",
            hover_color="#374151",
            height=40,
            corner_radius=8,
            command=lambda: self.show_reports(),
        )
        self.reports_tab.pack(side="left", fill="x", expand=True)

        self.admin_content_area = CTk.CTkFrame(aParent, fg_color="transparent")
        self.admin_content_area.pack(fill="both", expand=True)
        self.show_users_management()

    def show_users_management(self):
        for aWidget in self.admin_content_area.winfo_children():
            aWidget.destroy()

        self.users_tab.configure(fg_color="#FFD700", text_color="#000000")
        self.bookings_admin_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")
        self.reports_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")

        aContainer = CTk.CTkFrame(self.admin_content_area, fg_color="transparent")
        aContainer.pack(fill="both", expand=True)
        CTk.CTkLabel(
            aContainer,
            text="User Management",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute("SELECT id, name, email, phone, role FROM users ORDER BY id DESC")
            aUsers = aCur.fetchall()
            aConn.close()

            if not aUsers:
                CTk.CTkLabel(
                    aContainer, text="No users found.", font=CTk.CTkFont(size=14), text_color="#B0B8C1"
                ).pack(pady=20)
                return

            for aUser in aUsers:
                aUserId, aName, anEmail, aPhone, aRole = aUser
                aUserCard = CTk.CTkFrame(
                    aContainer,
                    fg_color="#1A1F2E",
                    corner_radius=10,
                    border_width=1,
                    border_color="#2D3748",
                )
                aUserCard.pack(fill="x", pady=8)
                anInfoFrame = CTk.CTkFrame(aUserCard, fg_color="transparent")
                anInfoFrame.pack(fill="x", padx=20, pady=15)

                anInfoGrid = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                anInfoGrid.pack(fill="x")

                aLeftCol = CTk.CTkFrame(anInfoGrid, fg_color="transparent")
                aLeftCol.pack(side="left", fill="both", expand=True)
                CTk.CTkLabel(
                    aLeftCol,
                    text=f"Name: {aName}",
                    font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    text_color="#E2E8F0",
                ).pack(anchor="w")
                CTk.CTkLabel(
                    aLeftCol,
                    text=f"Email: {anEmail}",
                    font=CTk.CTkFont(family="Segoe UI", size=10),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=(3, 0))

                aRightCol = CTk.CTkFrame(anInfoGrid, fg_color="transparent")
                aRightCol.pack(side="left", fill="both", expand=True)
                aRoleColors = {"customer": "#4FC3F7", "driver": "#FFD700", "admin": "#FF6B6B"}
                CTk.CTkLabel(
                    aRightCol,
                    text=f"Role: {aRole.capitalize()}",
                    font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                    text_color=aRoleColors.get(aRole.lower(), "#B0B8C1"),
                ).pack(anchor="w")
                CTk.CTkLabel(
                    aRightCol,
                    text=f"Phone: {aPhone}",
                    font=CTk.CTkFont(family="Segoe UI", size=10),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=(3, 0))

                CTk.CTkButton(
                    anInfoFrame,
                    text="Delete User",
                    font=CTk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                    fg_color="#FF6B6B",
                    hover_color="#FF5252",
                    text_color="#FFFFFF",
                    height=28,
                    width=100,
                    corner_radius=6,
                    command=lambda aUid=aUserId, aUname=aName: self.delete_user(aUid, aUname),
                ).pack(side="right", pady=(10, 0))

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to fetch users: {str(anError)}")

    def delete_user(self, aUserId, aUserName):
        if messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete user '{aUserName}'?\nThis action cannot be undone."
        ):
            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute("DELETE FROM bookings WHERE user_id = ?", (aUserId,))
                aCur.execute("DELETE FROM users WHERE id = ?", (aUserId,))
                aConn.commit()
                aConn.close()
                messagebox.showinfo("Success", f"User '{aUserName}' deleted successfully.")
                self.show_users_management()
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to delete user: {str(anError)}")

    def show_bookings_management(self):
        for aWidget in self.admin_content_area.winfo_children():
            aWidget.destroy()

        self.users_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")
        self.bookings_admin_tab.configure(fg_color="#FFD700", text_color="#000000")
        self.reports_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")

        aContainer = CTk.CTkFrame(self.admin_content_area, fg_color="transparent")
        aContainer.pack(fill="both", expand=True)
        CTk.CTkLabel(
            aContainer,
            text="All Bookings",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute(
                "SELECT b.id, u1.name, b.pickup_location, b.dropoff_location, b.booking_date, b.booking_time, b.status, u2.name FROM bookings b JOIN users u1 ON b.user_id = u1.id LEFT JOIN users u2 ON b.driver_id = u2.id ORDER BY b.created_at DESC"
            )
            aBookings = aCur.fetchall()
            aConn.close()

            if not aBookings:
                CTk.CTkLabel(
                    aContainer, text="No bookings found.", font=CTk.CTkFont(size=14), text_color="#B0B8C1"
                ).pack(pady=20)
                return

            for aBooking in aBookings:
                aBookingId, aCustomer, aPickup, aDropoff, aDate, aTime, aStatus, aDriver = aBooking
                aBookingCard = CTk.CTkFrame(
                    aContainer,
                    fg_color="#1A1F2E",
                    corner_radius=10,
                    border_width=1,
                    border_color="#2D3748",
                )
                aBookingCard.pack(fill="x", pady=8)
                anInfoFrame = CTk.CTkFrame(aBookingCard, fg_color="transparent")
                anInfoFrame.pack(fill="x", padx=20, pady=15)

                aHeader = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                aHeader.pack(fill="x", pady=(0, 10))
                CTk.CTkLabel(
                    aHeader,
                    text=f"Booking #{aBookingId}",
                    font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                    text_color="#FFD700",
                ).pack(side="left")
                aStatusColors = {
                    "pending": "#FFD700",
                    "assigned": "#81C784",
                    "completed": "#4CAF50",
                    "cancelled": "#E57373",
                }
                CTk.CTkLabel(
                    aHeader,
                    text=aStatus.capitalize(),
                    font=CTk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                    text_color=aStatusColors.get(aStatus, "#B0B8C1"),
                ).pack(side="right")

                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"Customer: {aCustomer}",
                    font=CTk.CTkFont(family="Segoe UI", size=11),
                    text_color="#E2E8F0",
                ).pack(anchor="w")
                if aDriver:
                    CTk.CTkLabel(
                        anInfoFrame,
                        text=f"Driver: {aDriver}",
                        font=CTk.CTkFont(family="Segoe UI", size=11),
                        text_color="#4FC3F7",
                    ).pack(anchor="w", pady=(3, 10))
                else:
                    CTk.CTkLabel(
                        anInfoFrame,
                        text="Driver: Not assigned",
                        font=CTk.CTkFont(family="Segoe UI", size=11),
                        text_color="#B0B8C1",
                    ).pack(anchor="w", pady=(3, 10))

                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"{aPickup} -> {aDropoff}",
                    font=CTk.CTkFont(family="Segoe UI", size=10),
                    text_color="#B0B8C1",
                ).pack(anchor="w")
                CTk.CTkLabel(
                    anInfoFrame,
                    text=f"{aDate} at {aTime}",
                    font=CTk.CTkFont(family="Segoe UI", size=10),
                    text_color="#B0B8C1",
                ).pack(anchor="w", pady=(3, 10))

                aButtonFrame = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
                aButtonFrame.pack(fill="x", pady=(5, 0))

                if aStatus == "pending" and not aDriver:
                    CTk.CTkButton(
                        aButtonFrame,
                        text="Assign Driver",
                        font=CTk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                        fg_color="#10B981",
                        hover_color="#059669",
                        text_color="#FFFFFF",
                        height=28,
                        width=100,
                        corner_radius=6,
                        command=lambda aBid=aBookingId, aBdate=aDate, aBtime=aTime: self.assign_driver_to_booking(aBid, aBdate, aBtime),
                    ).pack(side="left", padx=(0, 8))

                CTk.CTkButton(
                    aButtonFrame,
                    text="Delete",
                    font=CTk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                    fg_color="#FF6B6B",
                    hover_color="#FF5252",
                    text_color="#FFFFFF",
                    height=28,
                    width=80,
                    corner_radius=6,
                    command=lambda aBid=aBookingId: self.delete_booking(aBid),
                ).pack(side="right")

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to fetch bookings: {str(anError)}")

    def check_booking_overlap(self, aDriverId, aBookingDate, aBookingTime, anExcludeBookingId=None):
        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()

            aQuery = """
                SELECT id, booking_date, booking_time, status 
                FROM bookings 
                WHERE driver_id = ? AND booking_date = ? AND status IN ('pending', 'assigned')
            """
            aParams = [aDriverId, aBookingDate]

            if anExcludeBookingId:
                aQuery += " AND id != ?"
                aParams.append(anExcludeBookingId)

            aCur.execute(aQuery, aParams)
            anExistingBookings = aCur.fetchall()
            aConn.close()

            if not anExistingBookings:
                return False

            try:
                aBookingDatetime = datetime.strptime(f"{aBookingDate} {aBookingTime}", "%Y-%m-%d %H:%M")
            except ValueError:
                return False

            aRideDuration = timedelta(hours=1)
            aBookingEnd = aBookingDatetime + aRideDuration

            for anExistingId, anExistingDate, anExistingTime, anExistingStatus in anExistingBookings:
                try:
                    anExistingDatetime = datetime.strptime(f"{anExistingDate} {anExistingTime}", "%Y-%m-%d %H:%M")
                    anExistingEnd = anExistingDatetime + aRideDuration

                    if (aBookingDatetime < anExistingEnd and anExistingDatetime < aBookingEnd):
                        return True
                except ValueError:
                    continue

            return False
        except sqlite3.Error:
            return False

    def assign_driver_to_booking(self, aBookingId, aBookingDate, aBookingTime):
        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()

            aCur.execute("SELECT id, name FROM users WHERE LOWER(role) = 'driver' ORDER BY name")
            aDrivers = aCur.fetchall()
            aConn.close()

            if not aDrivers:
                messagebox.showwarning("No Drivers", "No drivers available. Please register drivers first.")
                return

            aDialog = CTk.CTkToplevel(self)
            aDialog.title("Assign Driver")
            aDialog.geometry("400x200")
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
                text="Select Driver",
                font=CTk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color="#E2E8F0",
            ).pack(pady=(20, 10))

            aDriverNames = [f"{aName} (ID: {aDid})" for aDid, aName in aDrivers]
            aDriverVar = CTk.StringVar(value=aDriverNames[0])
            aDriverMenu = CTk.CTkOptionMenu(
                aDialog,
                values=aDriverNames,
                variable=aDriverVar,
                width=300,
                height=35,
            )
            aDriverMenu.pack(pady=10)

            def confirm_assignment():
                aSelected = aDriverVar.get()
                aDriverId = int(aSelected.split("(ID: ")[1].split(")")[0])

                if self.check_booking_overlap(aDriverId, aBookingDate, aBookingTime, aBookingId):
                    messagebox.showerror(
                        "Overlap Detected",
                        "This driver already has a booking at this time. Please select a different driver or time.",
                    )
                    return

                try:
                    aConn = sqlite3.connect("taxi.db")
                    aCur = aConn.cursor()
                    aCur.execute(
                        "UPDATE bookings SET driver_id = ?, status = 'assigned' WHERE id = ?",
                        (aDriverId, aBookingId),
                    )
                    aConn.commit()

                    aCur.execute("SELECT name FROM users WHERE id = ?", (aDriverId,))
                    aDriverName = aCur.fetchone()[0]
                    aConn.close()

                    messagebox.showinfo("Success", f"Driver {aDriverName} assigned successfully!")
                    aDialog.destroy()
                    self.show_bookings_management()
                except sqlite3.Error as anError:
                    messagebox.showerror("Database Error", f"Failed to assign driver: {str(anError)}")

            CTk.CTkButton(
                aDialog,
                text="Assign",
                command=confirm_assignment,
                width=300,
                height=35,
                fg_color="#FFD700",
                text_color="#000000",
            ).pack(pady=10)

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to load drivers: {str(anError)}")

    def delete_booking(self, aBookingId):
        if messagebox.askyesno("Confirm", "Delete this booking?"):
            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute("DELETE FROM bookings WHERE id = ?", (aBookingId,))
                aConn.commit()
                aConn.close()
                messagebox.showinfo("Success", "Booking deleted successfully.")
                self.show_bookings_management()
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to delete booking: {str(anError)}")

    def show_reports(self):
        for aWidget in self.admin_content_area.winfo_children():
            aWidget.destroy()

        self.users_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")
        self.bookings_admin_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")
        self.reports_tab.configure(fg_color="#FFD700", text_color="#000000")

        aContainer = CTk.CTkFrame(self.admin_content_area, fg_color="transparent")
        aContainer.pack(fill="both", expand=True)
        CTk.CTkLabel(
            aContainer,
            text="Reports & Statistics",
            font=CTk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#E2E8F0",
        ).pack(anchor="w", pady=(0, 25))

        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            aCur.execute("SELECT COUNT(*) FROM users WHERE LOWER(role) = 'customer'")
            aTotalCustomers = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM users WHERE LOWER(role) = 'driver'")
            aTotalDrivers = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM bookings")
            aTotalBookings = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM bookings WHERE status = 'pending'")
            aPendingBookings = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM bookings WHERE status = 'assigned'")
            anAssignedBookings = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM bookings WHERE status = 'completed'")
            aCompletedBookings = aCur.fetchone()[0]
            aCur.execute("SELECT COUNT(*) FROM bookings WHERE status = 'cancelled'")
            aCancelledBookings = aCur.fetchone()[0]
            aConn.close()

            aStatsGrid = CTk.CTkFrame(aContainer, fg_color="transparent")
            aStatsGrid.pack(fill="x", pady=(0, 30))

            aRow1 = CTk.CTkFrame(aStatsGrid, fg_color="transparent")
            aRow1.pack(fill="x", pady=(0, 15))
            self.create_stat_card(aRow1, "Total Customers", str(aTotalCustomers), "#4FC3F7").pack(
                side="left", fill="both", expand=True, padx=(0, 10)
            )
            self.create_stat_card(aRow1, "Total Drivers", str(aTotalDrivers), "#FFD700").pack(
                side="left", fill="both", expand=True, padx=(0, 10)
            )
            self.create_stat_card(aRow1, "Total Bookings", str(aTotalBookings), "#10B981").pack(
                side="left", fill="both", expand=True
            )

            aRow2 = CTk.CTkFrame(aStatsGrid, fg_color="transparent")
            aRow2.pack(fill="x")
            self.create_stat_card(aRow2, "Pending", str(aPendingBookings), "#FFD700").pack(
                side="left", fill="both", expand=True, padx=(0, 10)
            )
            self.create_stat_card(aRow2, "Assigned", str(anAssignedBookings), "#81C784").pack(
                side="left", fill="both", expand=True, padx=(0, 10)
            )
            self.create_stat_card(aRow2, "Completed", str(aCompletedBookings), "#4CAF50").pack(
                side="left", fill="both", expand=True, padx=(0, 10)
            )
            self.create_stat_card(aRow2, "Cancelled", str(aCancelledBookings), "#E57373").pack(
                side="left", fill="both", expand=True
            )

        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to fetch reports: {str(anError)}")

    def create_stat_card(self, aParent, aTitle, aValue, aColor):
        aCard = CTk.CTkFrame(
            aParent, fg_color="#1A1F2E", corner_radius=10, border_width=2, border_color="#2D3748"
        )
        CTk.CTkLabel(aCard, text=aTitle, font=CTk.CTkFont(family="Segoe UI", size=11), text_color="#B0B8C1").pack(
            pady=(15, 5)
        )
        CTk.CTkLabel(
            aCard, text=aValue, font=CTk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color=aColor
        ).pack(pady=(0, 15))
        return aCard

