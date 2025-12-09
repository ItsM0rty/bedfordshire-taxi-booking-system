# Bedfordshire Taxi Booking System - Comprehensive Code Analysis

## Table of Contents
1. [System Overview](#system-overview)
2. [Database Architecture](#database-architecture)
3. [Application Entry Point](#application-entry-point)
4. [Authentication System](#authentication-system)
5. [Dashboard Architecture](#dashboard-architecture)
6. [CustomTkinter Patterns](#customtkinter-patterns)
7. [SQLite3 Workflows](#sqlite3-workflows)
8. [Data Flow & Component Interaction](#data-flow--component-interaction)

---

## System Overview

The Bedfordshire Taxi Booking System is a desktop application built with CustomTkinter that implements a role-based taxi booking platform. The system supports three user roles:
- **Customers**: Book rides, view and manage their bookings
- **Drivers**: View assigned rides, accept/decline rides, mark rides as completed
- **Admins**: Manage users, assign drivers to bookings, view system reports

### Technology Stack
- **UI Framework**: CustomTkinter (modern UI library based on Tkinter)
- **Database**: SQLite3 (embedded relational database)
- **Image Processing**: PIL/Pillow (for logo and icon handling)

### Architecture Style
- **Page-based navigation**: Using frame stacking pattern
- **Mixin architecture**: Multiple inheritance for role-based dashboard features
- **Direct database access**: Raw SQL queries without ORM
- **Modal dialogs**: CTkToplevel for edit/confirmation operations

---

## Database Architecture

### File: `db_setup.py`

The database initialization module creates and maintains the SQLite database schema.

#### Database Schema

**Table: users**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    name TEXT,
    address TEXT,
    phone TEXT
)
```

Fields:
- `id`: Auto-incrementing primary key
- `email`: Unique identifier for login (with UNIQUE constraint)
- `password`: Plain text password (NOTE: Security concern - should be hashed)
- `role`: User role ('Customer', 'Driver', 'Admin')
- `name`: User's full name
- `address`: User's address
- `phone`: Contact number

**Table: bookings**
```sql
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    driver_id INTEGER,
    pickup_location TEXT NOT NULL,
    dropoff_location TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (driver_id) REFERENCES users(id)
)
```

Fields:
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key to users table (customer who made the booking)
- `driver_id`: Foreign key to users table (assigned driver, nullable)
- `pickup_location`: Text description of pickup address
- `dropoff_location`: Text description of destination
- `booking_date`: Date in 'YYYY-MM-DD' format
- `booking_time`: Time in 'HH:MM' format
- `status`: Booking state ('pending', 'assigned', 'completed', 'cancelled')
- `created_at`: Automatic timestamp when booking is created

#### Database Migration Pattern

```python
try:
    aCur.execute("SELECT driver_id FROM bookings LIMIT 1")
except sqlite3.OperationalError:
    print("Migrating database: Adding driver_id column to bookings table...")
    aCur.execute("ALTER TABLE bookings ADD COLUMN driver_id INTEGER")
    print("Migration completed successfully!")
```

This migration pattern demonstrates a simple schema evolution strategy:
1. Try to query a column that may not exist
2. Catch `OperationalError` if column doesn't exist
3. Use `ALTER TABLE` to add the missing column

**Pattern Analysis**: This is a basic migration approach suitable for single-user desktop apps, but not production-ready. Production systems would use migration tools like Alembic or Flyway.

#### Connection Management Pattern

```python
def init_db():
    aConn = sqlite3.connect("taxi.db")  # Create/connect to database file
    aCur = aConn.cursor()
    # ... execute CREATE TABLE statements ...
    aConn.commit()  # Commit the transaction
    aConn.close()   # Close connection
```

**Pattern**: Simple connection lifecycle - open, execute, commit, close. This ensures database file is created in the current working directory on first run.

---

## Application Entry Point

### File: `main.py`

The main application class that initializes the window and manages page navigation.

#### Class: `MainApp`

```python
class MainApp(CTk.CTk):
    def __init__(self):
        super().__init__()
        # Window configuration
        self.geometry("1000x800")
        self.title("Taxi Booking System")
        self.resizable(False, False)
```

**Inheritance**: `MainApp` extends `CTk.CTk`, which is the CustomTkinter root window class (equivalent to `tkinter.Tk`).

#### Global Appearance Configuration

```python
CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("dark-blue")
```

**CustomTkinter Pattern**: These global settings must be called before creating any windows:
- `set_appearance_mode()`: Sets light/dark/system theme
- `set_default_color_theme()`: Sets color palette ("blue", "green", "dark-blue")

#### Icon Loading Pattern

```python
try:
    import os
    from PIL import ImageTk
    anIconPath = os.path.join(os.path.dirname(__file__), "assets", "static", "img", "tbs_icon.png")
    if os.path.exists(anIconPath):
        self.wm_iconbitmap()  # Clear default icon
        self.iconpath = ImageTk.PhotoImage(file=anIconPath)
        self.iconphoto(False, self.iconpath)  # Set custom icon
except Exception as anError:
    print(f"Icon loading failed: {anError}")
```

**Pattern Analysis**:
- Uses PIL's `ImageTk.PhotoImage` for icon handling
- Stores icon in `self.iconpath` to prevent garbage collection
- Graceful degradation with exception handling
- `iconphoto(False, ...)` means "set as default icon for this window only"

#### Container Frame Pattern

```python
self.container = CTk.CTkFrame(self, fg_color="transparent")
self.container.pack(fill="both", expand=True)
self.container.grid_rowconfigure(0, weight=1)
self.container.grid_columnconfigure(0, weight=1)
```

**CustomTkinter Layout Pattern**:
- Creates a transparent container frame that fills the entire window
- Configures grid weights so child frames can expand
- All pages will be gridded into this container at `row=0, column=0`
- Pages are stacked on top of each other using `tkraise()`

#### Page Registry Pattern

```python
self.pages = {}

for aPageClass in (LoginPage, RegisterPage):
    aPage = aPageClass(self.container, self)
    self.pages[aPageClass] = aPage
    aPage.grid(row=0, column=0, sticky="nsew")

self.show_page(LoginPage)
```

**Navigation Pattern**:
- Dictionary stores page instances keyed by class type
- All pages are created upfront and gridded to same location
- `sticky="nsew"` makes frames expand in all directions
- Only LoginPage and RegisterPage are pre-created
- DashboardPage is created dynamically (because it needs user data)

#### Dynamic Dashboard Creation

```python
def show_dashboard(self, aUserRole, aUserName, aUserId=None):
    anOldDashboard = self.pages.get(DashboardPage)
    if anOldDashboard:
        anOldDashboard.destroy()  # Destroy old dashboard to refresh state
    
    aDashboard = DashboardPage(self.container, self, aUserRole, aUserName, aUserId)
    self.pages[DashboardPage] = aDashboard
    aDashboard.grid(row=0, column=0, sticky="nsew")
    aDashboard.tkraise()
```

**Pattern Rationale**:
- Dashboard is destroyed and recreated on each login to ensure fresh state
- Prevents stale data from previous sessions
- Passes user context (role, name, ID) to dashboard

---

## Authentication System

### File: `login.py` - LoginPage Class

The login page implements a split-screen design with branding on the left and form on the right.

#### Two-Column Layout Pattern

```python
self.grid_columnconfigure(0, weight=1)
self.grid_columnconfigure(1, weight=1)
self.grid_rowconfigure(0, weight=1)

aLeftFrame = CTk.CTkFrame(self, fg_color="#FFD700", corner_radius=0)
aLeftFrame.grid(row=0, column=0, sticky="nsew")

aRightFrame = CTk.CTkFrame(self, fg_color="#ffffff")
aRightFrame.grid(row=0, column=1, sticky="nsew")
```

**CustomTkinter Grid Pattern**:
- Page frame configured with 2 equal-weight columns and 1 row
- Left column: Golden yellow branding area
- Right column: White form area
- `corner_radius=0` creates sharp corners for full-width sections

#### Image Loading with Fallback

```python
try:
    aLogoImg = Image.open("./assets/static/img/tbs_big.png")
    aLogoImg.thumbnail((600, 600), Image.LANCZOS)  # Resize while maintaining aspect ratio
    aCtkLogo = CTk.CTkImage(light_image=aLogoImg, dark_image=aLogoImg, 
                            size=(aLogoImg.width, aLogoImg.height))
    aLogoLabel = CTk.CTkLabel(aLeftInner, image=aCtkLogo, text="")
    aLogoLabel.image = aCtkLogo  # Keep reference to prevent garbage collection
    aLogoLabel.pack(pady=(5, 10))
except:
    # Fallback to text if image fails to load
    CTk.CTkLabel(
        aLeftInner,
        text="Taxi Booking\nSystem",
        font=CTk.CTkFont(family="Segoe UI", size=48, weight="bold"),
        text_color="#000000"
    ).pack(pady=(5, 10))
```

**CustomTkinter Image Pattern**:
- Use PIL to load and resize image
- `CTkImage` wrapper required for customtkinter compatibility
- Can specify different images for light/dark modes
- Store reference in label to prevent garbage collection
- Graceful fallback to text if image unavailable

#### CustomTkinter Entry Widget Styling

```python
self.email = CTk.CTkEntry(
    aFormContainer,
    placeholder_text="name@mail.com",  # Grayed-out hint text
    width=280,
    height=44,
    font=CTk.CTkFont(family="Segoe UI", size=12),
    border_width=2,
    border_color="#E8E8F0",  # Light gray border
    fg_color="#F5F5FA",      # Input background color
    text_color="#000000"      # Text color when typing
)
self.email.pack(pady=(0, 20))

self.password = CTk.CTkEntry(
    aFormContainer,
    placeholder_text="••••••••••••••••",
    show="*",  # Hide password characters
    width=280,
    height=44,
    # ... similar styling ...
)
```

**CustomTkinter Entry Features**:
- `placeholder_text`: Shows hint when empty
- `show="*"`: Password masking
- Rich styling options: border, colors, fonts
- Explicit dimensions instead of grid weights

#### Interactive Label Pattern (Hover Effects)

```python
aSwitch = CTk.CTkLabel(
    aSignupFrame,
    text="Sign up",
    font=CTk.CTkFont(size=12, weight="bold"),
    text_color="#F6BE00",
    cursor="hand2"  # Changes cursor to pointing hand
)
aSwitch.pack(side="left")

def on_enter(anEvent):
    aSwitch.configure(text_color="#FFD84A")  # Lighter gold on hover

def on_leave(anEvent):
    aSwitch.configure(text_color="#F6BE00")  # Original color

aSwitch.bind("<Enter>", on_enter)
aSwitch.bind("<Leave>", on_leave)

# Make label clickable
aSignupFrame.bind("<Button-1>", lambda anE: self.controller.show_register())
aSwitch.bind("<Button-1>", lambda anE: self.controller.show_register())
```

**Pattern Analysis**:
- Labels can act as clickable links with proper styling
- Event binding pattern: `<Enter>` for hover, `<Leave>` for mouse exit
- `<Button-1>` is left mouse click
- Bind to both parent frame and label for better UX
- `configure()` method dynamically updates widget properties

#### Login Authentication Flow

```python
def login(self):
    anEmail = self.email.get().strip()
    aPassword = self.password.get().strip()

    # Validation
    if not anEmail or not aPassword:
        messagebox.showerror("Error", "Email and password are required.")
        return

    if not "@" in anEmail:
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    # Database query
    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        aCur.execute("SELECT role, id, name FROM users WHERE email=? AND password=?", 
                     (anEmail, aPassword))
        aRow = aCur.fetchone()
        aConn.close()

        if not aRow:
            messagebox.showerror("Error", "Invalid email or password.")
            self.password.delete(0, "end")  # Clear password field
            return

        # Navigate to dashboard with user context
        self.controller.show_dashboard(aRow[0].lower(), aRow[2], aRow[1])
    except Exception as anError:
        messagebox.showerror("Error", f"Login failed: {str(anError)}")
        self.password.delete(0, "end")
```

**SQLite3 Authentication Pattern**:
1. **Input Validation**: Check for empty fields and basic email format
2. **Connection**: Open database connection
3. **Parameterized Query**: Use `?` placeholders to prevent SQL injection
4. **Fetch Result**: `fetchone()` returns single row or None
5. **Connection Cleanup**: Always close connection
6. **Navigation**: Pass user data to controller for dashboard creation
7. **Error Handling**: Clear sensitive data (password) on failure

**Security Concerns**:
- Passwords stored in plaintext (should use bcrypt/argon2)
- Basic email validation (just checks for "@")
- No rate limiting or account lockout

### File: `register.py` - RegisterPage Class

Similar layout to LoginPage but with more form fields.

#### CustomTkinter OptionMenu Widget

```python
self.role = CTk.CTkOptionMenu(
    aFormContainer,
    values=["Customer", "Driver", "Admin"],  # Dropdown options
    width=280,
    font=CTk.CTkFont(size=11),
    fg_color="#F5F5FA",                    # Background when closed
    button_color="#FFD700",                 # Dropdown arrow button color
    button_hover_color="#FFC700",           # Dropdown arrow hover color
    text_color="#000000",                   # Selected value text color
    dropdown_text_color="#000000",          # Dropdown list text color
    dropdown_fg_color="#F5F5FA",           # Dropdown list background
    dropdown_hover_color="#E8E8F0"         # Dropdown item hover color
)
self.role.set("Customer")  # Set default value
```

**CustomTkinter OptionMenu Features**:
- Dropdown select with rich styling options
- Default value set with `.set()`
- Get selected value with `.get()`
- Separate styling for closed state, dropdown, and hover

#### Registration Validation Flow

```python
def register(self):
    anEmail = self.email.get().strip()
    aPassword = self.password.get().strip()
    aName = self.name.get().strip()
    anAddress = self.address.get().strip()
    aPhone = self.phone.get().strip()
    aRole = self.role.get()

    # Multi-field validation
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
```

**Validation Strategy**: Incremental validation with early returns

#### Insert with Unique Constraint Handling

```python
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
    # Clear form fields
    self.email.delete(0, "end")
    self.password.delete(0, "end")
    self.name.delete(0, "end")
    self.address.delete(0, "end")
    self.phone.delete(0, "end")
    self.role.set("Customer")
    
    self.controller.show_login()  # Navigate to login page
    
except sqlite3.IntegrityError:
    # Catch duplicate email (UNIQUE constraint violation)
    messagebox.showerror("Error", "This email is already registered. Please use a different email or try logging in.")
except Exception as anError:
    messagebox.showerror("Error", f"Registration failed: {str(anError)}")
```

**SQLite3 Insert Pattern**:
- Use parameterized INSERT with multiple values
- `commit()` to persist changes
- `IntegrityError` specifically catches unique constraint violations
- Clear form on success
- Navigate to login page after successful registration

---

## Dashboard Architecture

The dashboard system uses **multiple inheritance with mixins** to provide role-specific functionality.

### File: `dashboard.py` - DashboardPage Class

```python
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
```

**Multiple Inheritance Pattern**:
- Inherits from three mixin classes PLUS CTkFrame
- Mixins provide methods for each role type
- Method Resolution Order (MRO): CustomerDashboardMixin → DriverDashboardMixin → AdminDashboardMixin → CTkFrame
- All mixin methods have access to `self.user_id`, `self.user_role`, etc.

#### Dashboard Header Structure

```python
aHeaderFrame = CTk.CTkFrame(aMainContainer, fg_color="#1A1F2E", corner_radius=0)
aHeaderFrame.pack(fill="x", pady=0)

aHeaderContent = CTk.CTkFrame(aHeaderFrame, fg_color="transparent")
aHeaderContent.pack(fill="x", padx=40, pady=30)

aTitleFrame = CTk.CTkFrame(aHeaderContent, fg_color="transparent")
aTitleFrame.pack(fill="x", pady=(0, 15))

# Dynamic title based on role
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
```

**Layout Pattern**:
- Nested frames for precise control
- `pack(side="left")` and `pack(side="right")` for horizontal layout
- Role-based title rendering
- Logout button always visible

#### Scrollable Content Area Pattern

```python
aContentScroll = CTk.CTkScrollableFrame(aMainContainer, fg_color="transparent")
aContentScroll.pack(fill="both", expand=True)

aContentFrame = CTk.CTkFrame(aContentScroll, fg_color="transparent")
aContentFrame.pack(fill="both", expand=True, padx=40, pady=40)

# Dispatch to role-specific dashboard
if self.user_role.lower() == "customer":
    self.show_customer_dashboard(aContentFrame)
elif self.user_role.lower() == "driver":
    self.show_driver_dashboard(aContentFrame)
elif self.user_role.lower() == "admin":
    self.show_admin_dashboard(aContentFrame)
```

**CustomTkinter Scrollable Pattern**:
- `CTkScrollableFrame` automatically adds scrollbars when content overflows
- Pass `aContentFrame` to mixin methods so they can populate content
- Dispatch pattern based on user role

---

## Customer Dashboard

### File: `dashboard_customer.py` - CustomerDashboardMixin Class

The customer dashboard provides booking creation and management functionality.

#### Tab Navigation Pattern

```python
def show_customer_dashboard(self, aParent):
    aTabFrame = CTk.CTkFrame(aParent, fg_color="transparent")
    aTabFrame.pack(fill="x", pady=(0, 30))

    self.booking_tab = CTk.CTkButton(
        aTabFrame,
        text="Book a Ride",
        font=CTk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        fg_color="#FFD700",      # Active tab color
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
        fg_color="#2D3748",      # Inactive tab color
        text_color="#E2E8F0",
        hover_color="#374151",
        height=44,
        corner_radius=8,
        command=lambda: self.show_my_bookings(aParent),
    )
    self.bookings_tab.pack(side="left", fill="x", expand=True)

    self.content_area = CTk.CTkFrame(aParent, fg_color="transparent")
    self.content_area.pack(fill="both", expand=True)
    self.show_booking_form(aParent)  # Show booking form by default
```

**Tab Pattern**:
- Buttons styled to look like tabs (different colors for active/inactive)
- Store tab buttons as instance variables to update styling later
- Content area below tabs is reused
- Lambda functions to pass parent parameter

#### Content Swapping Pattern

```python
def show_booking_form(self, aParent):
    # Clear existing content
    for aWidget in self.content_area.winfo_children():
        aWidget.destroy()

    # Update tab styling to show active tab
    self.booking_tab.configure(fg_color="#FFD700", text_color="#000000")
    self.bookings_tab.configure(fg_color="#2D3748", text_color="#E2E8F0")

    # Build new content
    aFormCard = CTk.CTkFrame(
        self.content_area,
        fg_color="#1A1F2E",
        corner_radius=12,
        border_width=1,
        border_color="#2D3748",
    )
    aFormCard.pack(fill="both", expand=True)
    # ... add form widgets ...
```

**Pattern Analysis**:
1. Destroy all existing widgets in content area
2. Update tab button colors to show active state
3. Create new content from scratch
4. CustomTkinter card styling: `corner_radius` for rounded corners, `border_width` and `border_color` for outlines

#### Date/Time Input Layout

```python
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
    # ... styling ...
)
self.date_entry.pack(fill="both", expand=True)

aTimeCol = CTk.CTkFrame(aDtFrame, fg_color="transparent")
aTimeCol.pack(side="left", fill="both", expand=True)
# ... similar for time ...
```

**Two-Column Layout Pattern**:
- Parent frame with transparent background
- Two child frames packed side-by-side with `side="left"`
- `padx=(0, 10)` adds spacing between columns
- Both columns expand equally with `expand=True`

#### Booking Submission with Date/Time Validation

```python
def submit_booking(self):
    aPickup = self.pickup_entry.get().strip()
    aDropoff = self.dropoff_entry.get().strip()
    aDate = self.date_entry.get().strip()
    aTime = self.time_entry.get().strip()

    if not all([aPickup, aDropoff, aDate, aTime]):
        messagebox.showerror("Error", "All fields are required.")
        return

    # Validate date format
    try:
        datetime.strptime(aDate, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        return

    # Validate time format
    try:
        datetime.strptime(aTime, "%H:%M")
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Use HH:MM")
        return

    # Insert booking
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
        
        # Clear form
        self.pickup_entry.delete(0, "end")
        self.dropoff_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.time_entry.delete(0, "end")
    except sqlite3.Error as anError:
        messagebox.showerror("Database Error", f"Failed to book taxi: {str(anError)}")
```

**Validation Strategy**:
1. Check all required fields are filled
2. Validate date format using `datetime.strptime()`
3. Validate time format
4. Insert into database with user_id
5. Default status is 'pending' (from table definition)
6. Clear form on success

#### Displaying Bookings with JOIN Query

```python
def show_my_bookings(self, aParent):
    # ... clear content and update tabs ...

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
            # Show empty state
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

        # Display each booking
        for aBooking in aBookings:
            aBookingId, aPickup, aDropoff, aDate, aTime, aStatus, aDriverId = aBooking
            # ... create booking card ...
```

**SQLite3 Query Pattern**:
- SELECT specific columns (not `SELECT *`)
- WHERE clause with parameterized user_id
- ORDER BY created_at DESC for chronological order
- Check if result is empty and show friendly message
- Iterate through results to create UI cards

#### Dynamic Booking Card with Status Colors

```python
for aBooking in aBookings:
    aBookingId, aPickup, aDropoff, aDate, aTime, aStatus, aDriverId = aBooking
    
    # Create card
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

    # Route display with colors
    aRouteFrame = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
    aRouteFrame.pack(fill="x", pady=(0, 10))
    CTk.CTkLabel(
        aRouteFrame,
        text=f"From: {aPickup}",
        font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        text_color="#FFD700",  # Gold for pickup
    ).pack(anchor="w")
    CTk.CTkLabel(
        aRouteFrame, 
        text="     |", 
        font=CTk.CTkFont(size=10), 
        text_color="#7A8195"
    ).pack(anchor="w", pady=(2, 2))
    CTk.CTkLabel(
        aRouteFrame,
        text=f"To: {aDropoff}",
        font=CTk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        text_color="#4FC3F7",  # Blue for dropoff
    ).pack(anchor="w")

    # Status with color mapping
    aStatusColors = {
        "pending": "#FFD700",    # Gold
        "assigned": "#81C784",   # Green
        "completed": "#4CAF50",  # Dark green
        "cancelled": "#E57373",  # Red
    }
    aStatusText = aStatus.capitalize()
    aStatusColor = aStatusColors.get(aStatus, "#B0B8C1")  # Default gray
    CTk.CTkLabel(
        anInfoFrame,
        text=f"Status: {aStatusText}",
        font=CTk.CTkFont(family="Segoe UI", size=11, weight="bold"),
        text_color=aStatusColor,
    ).pack(anchor="w", pady=(10, 0))

    # Conditional action buttons
    if aStatus == "pending":
        aButtonRow = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
        aButtonRow.pack(fill="x", pady=(15, 0))

        CTk.CTkButton(
            aButtonRow,
            text="Edit Booking",
            # ... styling ...
            command=lambda aBid=aBookingId, aP=aPickup, aD=aDropoff, aDt=aDate, aTm=aTime: self.edit_booking(aBid, aP, aD, aDt, aTm),
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        CTk.CTkButton(
            aButtonRow,
            text="Cancel Booking",
            # ... styling ...
            command=lambda aBid=aBookingId: self.cancel_booking(aBid),
        ).pack(side="left", fill="x", expand=True)
```

**Pattern Analysis**:
- **Visual Hierarchy**: Route shown with connecting pipe character
- **Color Coding**: Different colors for pickup, dropoff, and status
- **Dictionary Lookup**: Status colors mapped in dictionary with fallback
- **Conditional UI**: Only show Edit/Cancel buttons for pending bookings
- **Lambda Capture**: Must capture loop variables in lambda default parameters

#### Modal Dialog Pattern - Edit Booking

```python
def edit_booking(self, aBookingId, aCurrentPickup, aCurrentDropoff, aCurrentDate, aCurrentTime):
    aDialog = CTk.CTkToplevel(self)  # Create modal dialog
    aDialog.title("Edit Booking")
    aDialog.geometry("500x400")
    aDialog.transient(self)  # Set parent window
    aDialog.grab_set()       # Make modal (blocks parent)

    # ... create form widgets ...

    aPickupEntry = CTk.CTkEntry(aFormFrame, ...)
    aPickupEntry.insert(0, aCurrentPickup)  # Pre-fill with current value
    
    # ... more entries ...

    def save_changes():
        aPickup = aPickupEntry.get().strip()
        # ... get other values ...

        # Validation
        if not all([aPickup, aDropoff, aDate, aTime]):
            messagebox.showerror("Error", "All fields are required.")
            return

        # ... validate formats ...

        # Check for driver overlap
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

            # Update booking
            aCur.execute(
                "UPDATE bookings SET pickup_location = ?, dropoff_location = ?, booking_date = ?, booking_time = ? WHERE id = ?",
                (aPickup, aDropoff, aDate, aTime, aBookingId),
            )
            aConn.commit()
            aConn.close()

            messagebox.showinfo("Success", "Booking updated successfully!")
            aDialog.destroy()  # Close modal
            aParent = self.content_area.master
            self.show_my_bookings(aParent)  # Refresh booking list
        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to update booking: {str(anError)}")

    CTk.CTkButton(
        aDialog,
        text="Save Changes",
        command=save_changes,
        # ... styling ...
    ).pack(pady=20)
```

**CustomTkinter Modal Dialog Pattern**:
1. **Create**: `CTkToplevel(parent)` creates new window
2. **Transient**: `transient(parent)` links dialog to parent
3. **Modal**: `grab_set()` blocks interaction with parent
4. **Pre-fill**: Use `insert(0, value)` to populate fields
5. **Nested Function**: Define callback inside method to access local variables
6. **Refresh**: Reload list after successful update
7. **Cleanup**: `destroy()` closes dialog

**Business Logic**: Checks if driver is assigned and validates no time conflicts

#### Cancel Booking Pattern

```python
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
            self.show_my_bookings(aParent)  # Refresh list
        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to cancel booking: {str(anError)}")
```

**Pattern**: 
- Confirmation dialog before destructive action
- Soft delete (status change, not actual DELETE)
- Refresh UI after change

---

## Driver Dashboard

### File: `dashboard_driver.py` - DriverDashboardMixin Class

The driver dashboard shows assigned rides and allows drivers to accept/decline/complete them.

#### Driver Query with JOIN

```python
def show_assigned_rides(self):
    for aWidget in self.driver_content_area.winfo_children():
        aWidget.destroy()

    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        aCur.execute(
            """SELECT b.id, b.pickup_location, b.dropoff_location, b.booking_date, 
                      b.booking_time, b.status, u.name, u.phone 
               FROM bookings b 
               JOIN users u ON b.user_id = u.id 
               WHERE b.driver_id = ? 
               ORDER BY b.created_at DESC""",
            (self.user_id,),
        )
        aRides = aCur.fetchall()
        aConn.close()
```

**SQLite3 JOIN Pattern**:
- JOIN bookings with users to get customer details
- Select from bookings (b) and users (u) tables
- `ON b.user_id = u.id` links customer to booking
- WHERE filters for current driver's assignments
- Returns customer name and phone for driver to contact

#### Display Customer Information

```python
for aRide in aRides:
    aBookingId, aPickup, aDropoff, aDate, aTime, aStatus, aCustomerName, aCustomerPhone = aRide
    
    # ... create card ...
    
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
```

**Design Pattern**: Driver needs customer contact info to coordinate pickup

#### Decline Ride with Reason

```python
def decline_ride(self, aBookingId):
    aDialog = CTk.CTkToplevel(self)
    aDialog.title("Decline Ride")
    aDialog.geometry("500x300")
    aDialog.transient(self)
    aDialog.grab_set()

    # ... labels ...

    aReasonText = CTk.CTkTextbox(
        aReasonFrame,
        height=120,
        width=440,
        font=CTk.CTkFont(family="Segoe UI", size=12),
    )
    aReasonText.pack(fill="both", expand=True)
    aReasonText.insert("1.0", "")  # Start with empty text

    def confirm_decline():
        aReason = aReasonText.get("1.0", "end-1c").strip()  # Get all text

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
            self.show_assigned_rides()  # Refresh list
        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to decline ride: {str(anError)}")
```

**CustomTkinter Textbox Pattern**:
- `CTkTextbox`: Multi-line text input widget
- `insert("1.0", text)`: Insert at line 1, character 0
- `get("1.0", "end-1c")`: Get from start to end, excluding final newline
- Text indices use "line.char" format

**Business Logic**:
- Unassign driver (set driver_id to NULL)
- Reset status to 'pending' so admin can reassign
- Reason is shown to admin but not stored (could be enhancement)

#### Complete Ride

```python
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
```

**Pattern**: Simple status update with confirmation

---

## Admin Dashboard

### File: `dashboard_admin.py` - AdminDashboardMixin Class

The admin dashboard has three tabs: Users, Bookings, and Reports.

#### Three-Tab Layout

```python
def show_admin_dashboard(self, aParent):
    aTabFrame = CTk.CTkFrame(aParent, fg_color="transparent")
    aTabFrame.pack(fill="x", pady=(0, 30))

    self.users_tab = CTk.CTkButton(
        aTabFrame,
        text="Users",
        # ... styling ...
        command=lambda: self.show_users_management(),
    )
    self.users_tab.pack(side="left", padx=(0, 8), fill="x", expand=True)

    self.bookings_admin_tab = CTk.CTkButton(
        aTabFrame,
        text="Bookings",
        # ... styling ...
        command=lambda: self.show_bookings_management(),
    )
    self.bookings_admin_tab.pack(side="left", padx=(0, 8), fill="x", expand=True)

    self.reports_tab = CTk.CTkButton(
        aTabFrame,
        text="Reports",
        # ... styling ...
        command=lambda: self.show_reports(),
    )
    self.reports_tab.pack(side="left", fill="x", expand=True)

    self.admin_content_area = CTk.CTkFrame(aParent, fg_color="transparent")
    self.admin_content_area.pack(fill="both", expand=True)
    self.show_users_management()  # Default tab
```

**Pattern**: Same tab pattern as customer dashboard but with three buttons

#### User Management Display

```python
def show_users_management(self):
    # ... update tab colors ...

    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        aCur.execute("SELECT id, name, email, phone, role FROM users ORDER BY id DESC")
        aUsers = aCur.fetchall()
        aConn.close()

        for aUser in aUsers:
            aUserId, aName, anEmail, aPhone, aRole = aUser
            
            # Create user card
            aUserCard = CTk.CTkFrame(...)
            
            # Two-column info display
            anInfoGrid = CTk.CTkFrame(anInfoFrame, fg_color="transparent")
            anInfoGrid.pack(fill="x")

            aLeftCol = CTk.CTkFrame(anInfoGrid, fg_color="transparent")
            aLeftCol.pack(side="left", fill="both", expand=True)
            CTk.CTkLabel(aLeftCol, text=f"Name: {aName}", ...).pack(anchor="w")
            CTk.CTkLabel(aLeftCol, text=f"Email: {anEmail}", ...).pack(anchor="w", pady=(3, 0))

            aRightCol = CTk.CTkFrame(anInfoGrid, fg_color="transparent")
            aRightCol.pack(side="left", fill="both", expand=True)
            
            # Color-coded role
            aRoleColors = {"customer": "#4FC3F7", "driver": "#FFD700", "admin": "#FF6B6B"}
            CTk.CTkLabel(
                aRightCol,
                text=f"Role: {aRole.capitalize()}",
                text_color=aRoleColors.get(aRole.lower(), "#B0B8C1"),
                ...
            ).pack(anchor="w")
            CTk.CTkLabel(aRightCol, text=f"Phone: {aPhone}", ...).pack(anchor="w", pady=(3, 0))

            # Delete button
            CTk.CTkButton(
                anInfoFrame,
                text="Delete User",
                command=lambda aUid=aUserId, aUname=aName: self.delete_user(aUid, aUname),
                ...
            ).pack(side="right", pady=(10, 0))
```

**Pattern Analysis**:
- List all users with full details
- Two-column layout for organized information
- Role color coding for quick identification
- Delete action per user

#### Cascade Delete Pattern

```python
def delete_user(self, aUserId, aUserName):
    if messagebox.askyesno(
        "Confirm Delete", 
        f"Are you sure you want to delete user '{aUserName}'?\nThis action cannot be undone."
    ):
        try:
            aConn = sqlite3.connect("taxi.db")
            aCur = aConn.cursor()
            # Delete bookings first (foreign key constraint)
            aCur.execute("DELETE FROM bookings WHERE user_id = ?", (aUserId,))
            # Then delete user
            aCur.execute("DELETE FROM users WHERE id = ?", (aUserId,))
            aConn.commit()
            aConn.close()
            messagebox.showinfo("Success", f"User '{aUserName}' deleted successfully.")
            self.show_users_management()  # Refresh list
        except sqlite3.Error as anError:
            messagebox.showerror("Database Error", f"Failed to delete user: {str(anError)}")
```

**SQLite3 Delete Pattern**:
- Manual cascade: Delete related records first
- Required because foreign key constraints would prevent deletion
- Could also delete bookings where driver_id matches
- Transaction ensures both deletes succeed or fail together

#### Bookings Management with Complex JOIN

```python
def show_bookings_management(self):
    # ... update tabs ...

    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        aCur.execute(
            """SELECT b.id, u1.name, b.pickup_location, b.dropoff_location, 
                      b.booking_date, b.booking_time, b.status, u2.name 
               FROM bookings b 
               JOIN users u1 ON b.user_id = u1.id 
               LEFT JOIN users u2 ON b.driver_id = u2.id 
               ORDER BY b.created_at DESC"""
        )
        aBookings = aCur.fetchall()
        aConn.close()
```

**SQLite3 Multiple JOIN Pattern**:
- `JOIN users u1`: Get customer name (always exists)
- `LEFT JOIN users u2`: Get driver name (may not exist)
- Table aliases (u1, u2) disambiguate user roles
- LEFT JOIN ensures bookings without drivers still appear
- u2.name will be NULL for unassigned bookings

#### Conditional Assign Driver Button

```python
for aBooking in aBookings:
    aBookingId, aCustomer, aPickup, aDropoff, aDate, aTime, aStatus, aDriver = aBooking
    
    # ... create card ...
    
    # Show driver status
    if aDriver:
        CTk.CTkLabel(
            anInfoFrame,
            text=f"Driver: {aDriver}",
            text_color="#4FC3F7",
        ).pack(anchor="w", pady=(3, 10))
    else:
        CTk.CTkLabel(
            anInfoFrame,
            text="Driver: Not assigned",
            text_color="#B0B8C1",
        ).pack(anchor="w", pady=(3, 10))

    # Assign button only for pending unassigned bookings
    if aStatus == "pending" and not aDriver:
        CTk.CTkButton(
            aButtonFrame,
            text="Assign Driver",
            command=lambda aBid=aBookingId, aBdate=aDate, aBtime=aTime: 
                    self.assign_driver_to_booking(aBid, aBdate, aBtime),
            ...
        ).pack(side="left", padx=(0, 8))
```

**Pattern**: Conditional UI based on booking state and driver assignment

#### Time Overlap Detection Algorithm

```python
def check_booking_overlap(self, aDriverId, aBookingDate, aBookingTime, anExcludeBookingId=None):
    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()

        # Query existing bookings for same driver and date
        aQuery = """
            SELECT id, booking_date, booking_time, status 
            FROM bookings 
            WHERE driver_id = ? AND booking_date = ? AND status IN ('pending', 'assigned')
        """
        aParams = [aDriverId, aBookingDate]

        # Exclude current booking when editing
        if anExcludeBookingId:
            aQuery += " AND id != ?"
            aParams.append(anExcludeBookingId)

        aCur.execute(aQuery, aParams)
        anExistingBookings = aCur.fetchall()
        aConn.close()

        if not anExistingBookings:
            return False

        # Parse new booking time
        try:
            aBookingDatetime = datetime.strptime(f"{aBookingDate} {aBookingTime}", "%Y-%m-%d %H:%M")
        except ValueError:
            return False

        # Assume 1 hour ride duration
        aRideDuration = timedelta(hours=1)
        aBookingEnd = aBookingDatetime + aRideDuration

        # Check each existing booking for overlap
        for anExistingId, anExistingDate, anExistingTime, anExistingStatus in anExistingBookings:
            try:
                anExistingDatetime = datetime.strptime(
                    f"{anExistingDate} {anExistingTime}", "%Y-%m-%d %H:%M"
                )
                anExistingEnd = anExistingDatetime + aRideDuration

                # Overlap detection: two time ranges overlap if:
                # start1 < end2 AND start2 < end1
                if (aBookingDatetime < anExistingEnd and anExistingDatetime < aBookingEnd):
                    return True
            except ValueError:
                continue

        return False
    except sqlite3.Error:
        return False
```

**Algorithm Analysis**:
1. **Query**: Get all driver's bookings for same date (pending/assigned only)
2. **Exclude**: Optionally exclude current booking (for edits)
3. **Parse**: Convert date/time strings to datetime objects
4. **Duration**: Assume 1-hour booking slots (hardcoded)
5. **Overlap Logic**: Classic interval overlap detection
   - Two intervals [A_start, A_end] and [B_start, B_end] overlap if:
   - A_start < B_end AND B_start < A_end
6. **Error Handling**: Return False if any parsing fails

**Use Case**: Prevents double-booking drivers

#### Assign Driver with Dropdown

```python
def assign_driver_to_booking(self, aBookingId, aBookingDate, aBookingTime):
    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        # Query available drivers
        aCur.execute("SELECT id, name FROM users WHERE LOWER(role) = 'driver' ORDER BY name")
        aDrivers = aCur.fetchall()
        aConn.close()

        if not aDrivers:
            messagebox.showwarning("No Drivers", "No drivers available. Please register drivers first.")
            return

        # Create modal dialog
        aDialog = CTk.CTkToplevel(self)
        aDialog.title("Assign Driver")
        aDialog.geometry("400x200")
        aDialog.transient(self)
        aDialog.grab_set()

        # Dropdown with driver names
        aDriverNames = [f"{aName} (ID: {aDid})" for aDid, aName in aDrivers]
        aDriverVar = CTk.StringVar(value=aDriverNames[0])  # Default to first driver
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
            # Parse ID from string like "John Doe (ID: 5)"
            aDriverId = int(aSelected.split("(ID: ")[1].split(")")[0])

            # Check for time conflicts
            if self.check_booking_overlap(aDriverId, aBookingDate, aBookingTime, aBookingId):
                messagebox.showerror(
                    "Overlap Detected",
                    "This driver already has a booking at this time. Please select a different driver or time.",
                )
                return

            # Assign driver
            try:
                aConn = sqlite3.connect("taxi.db")
                aCur = aConn.cursor()
                aCur.execute(
                    "UPDATE bookings SET driver_id = ?, status = 'assigned' WHERE id = ?",
                    (aDriverId, aBookingId),
                )
                aConn.commit()

                # Get driver name for confirmation message
                aCur.execute("SELECT name FROM users WHERE id = ?", (aDriverId,))
                aDriverName = aCur.fetchone()[0]
                aConn.close()

                messagebox.showinfo("Success", f"Driver {aDriverName} assigned successfully!")
                aDialog.destroy()
                self.show_bookings_management()  # Refresh list
            except sqlite3.Error as anError:
                messagebox.showerror("Database Error", f"Failed to assign driver: {str(anError)}")

        CTk.CTkButton(
            aDialog,
            text="Assign",
            command=confirm_assignment,
            ...
        ).pack(pady=10)
```

**Pattern Analysis**:
1. Query all drivers from database
2. Create dropdown with formatted names (includes ID for parsing)
3. Use `StringVar` to track selected value
4. Parse ID from formatted string
5. Validate no time conflicts
6. Update booking with driver_id and change status to 'assigned'
7. Query driver name again for confirmation message

**CustomTkinter OptionMenu with Variable**:
- `CTk.StringVar()`: Tkinter variable for value binding
- `variable=aDriverVar`: Links dropdown to variable
- `aDriverVar.get()`: Retrieves selected value

#### Reports and Statistics

```python
def show_reports(self):
    # ... update tabs ...

    try:
        aConn = sqlite3.connect("taxi.db")
        aCur = aConn.cursor()
        
        # Count queries
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

        # Display statistics in grid
        aStatsGrid = CTk.CTkFrame(aContainer, fg_color="transparent")
        aStatsGrid.pack(fill="x", pady=(0, 30))

        # Row 1: User statistics
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

        # Row 2: Booking status statistics
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
```

**SQLite3 Aggregation Pattern**:
- Multiple `COUNT(*)` queries to gather statistics
- WHERE clause filters by role/status
- `LOWER(role)` for case-insensitive comparison
- `fetchone()[0]` to extract count value

**Layout Pattern**: Two rows of stat cards, each row uses `side="left"` packing

#### Reusable Stat Card Component

```python
def create_stat_card(self, aParent, aTitle, aValue, aColor):
    aCard = CTk.CTkFrame(
        aParent, 
        fg_color="#1A1F2E", 
        corner_radius=10, 
        border_width=2, 
        border_color="#2D3748"
    )
    
    # Title label
    CTk.CTkLabel(
        aCard, 
        text=aTitle, 
        font=CTk.CTkFont(family="Segoe UI", size=11), 
        text_color="#B0B8C1"
    ).pack(pady=(15, 5))
    
    # Value label with color coding
    CTk.CTkLabel(
        aCard, 
        text=aValue, 
        font=CTk.CTkFont(family="Segoe UI", size=32, weight="bold"), 
        text_color=aColor
    ).pack(pady=(0, 15))
    
    return aCard
```

**Reusable Component Pattern**:
- Method creates and returns a frame
- Caller packs the returned frame
- Parameterized for flexibility (title, value, color)
- Consistent styling across all stat cards

---

## CustomTkinter Patterns Summary

### Widget Hierarchy
- `CTk.CTk`: Root window (inherits from tkinter.Tk)
- `CTkFrame`: Container widget
- `CTkLabel`: Text display
- `CTkEntry`: Single-line text input
- `CTkTextbox`: Multi-line text input
- `CTkButton`: Clickable button
- `CTkOptionMenu`: Dropdown select
- `CTkCheckBox`: Checkbox
- `CTkScrollableFrame`: Frame with automatic scrollbars
- `CTkToplevel`: Modal dialog window

### Color System
CustomTkinter uses hex colors for styling:
- `fg_color`: Foreground/background color
- `text_color`: Text color
- `border_color`: Border color
- `hover_color`: Color when hovering
- `button_color`: For OptionMenu dropdown button
- `placeholder_text_color`: Entry hint text color

### Layout Management
- **Pack**: Simple vertical/horizontal layout
  - `side="left"/"right"/"top"/"bottom"`
  - `fill="x"/"y"/"both"`
  - `expand=True` for proportional sizing
  - `padx`/`pady` for spacing
- **Grid**: Table-like layout
  - `row`, `column` for positioning
  - `sticky="nsew"` for stretching
  - `grid_rowconfigure()`/`grid_columnconfigure()` with `weight` for resizing

### Font System
```python
CTk.CTkFont(
    family="Segoe UI",  # Font family
    size=14,            # Font size
    weight="bold"       # "normal" or "bold"
)
```

### Frame Stacking Navigation
1. Create container frame with grid
2. Create all page frames
3. Grid all pages to same location (row=0, column=0)
4. Use `tkraise()` to bring page to front
5. Only top frame is visible

### Modal Dialog Pattern
```python
aDialog = CTk.CTkToplevel(parent)
aDialog.transient(parent)  # Link to parent
aDialog.grab_set()         # Make modal
# ... add content ...
aDialog.destroy()          # Close dialog
```

### Image Handling
```python
from PIL import Image
import customtkinter as CTk

# Load with PIL
aImg = Image.open("path/to/image.png")
aImg.thumbnail((width, height), Image.LANCZOS)

# Wrap for CustomTkinter
aCtkImg = CTk.CTkImage(
    light_image=aImg,
    dark_image=aImg,  # Can be different image
    size=(aImg.width, aImg.height)
)

# Display in label
aLabel = CTk.CTkLabel(parent, image=aCtkImg, text="")
aLabel.image = aCtkImg  # Prevent garbage collection
```

### Event Binding
```python
widget.bind("<Enter>", callback)    # Mouse hover
widget.bind("<Leave>", callback)    # Mouse leave
widget.bind("<Button-1>", callback) # Left click
widget.bind("<Button-3>", callback) # Right click
```

### Widget State Management
```python
widget.configure(parameter=value)  # Update any property
entry.get()                        # Get entry value
entry.delete(0, "end")             # Clear entry
entry.insert(0, "text")            # Set entry value
textbox.get("1.0", "end-1c")      # Get textbox content
textbox.insert("1.0", "text")     # Set textbox content
```

---

## SQLite3 Workflows Summary

### Connection Lifecycle
```python
# Open connection
aConn = sqlite3.connect("database.db")
aCur = aConn.cursor()

# Execute queries
aCur.execute("SELECT ...", (params,))
aResult = aCur.fetchone()  # or fetchall()

# Commit changes (for INSERT/UPDATE/DELETE)
aConn.commit()

# Close connection
aConn.close()
```

### Query Patterns

#### SELECT Single Row
```python
aCur.execute("SELECT col1, col2 FROM table WHERE id = ?", (value,))
aRow = aCur.fetchone()  # Returns tuple or None
if aRow:
    col1, col2 = aRow
```

#### SELECT Multiple Rows
```python
aCur.execute("SELECT * FROM table WHERE condition = ?", (value,))
aRows = aCur.fetchall()  # Returns list of tuples
for aRow in aRows:
    # Process each row
```

#### INSERT
```python
aCur.execute(
    "INSERT INTO table (col1, col2) VALUES (?, ?)",
    (val1, val2)
)
aConn.commit()
```

#### UPDATE
```python
aCur.execute(
    "UPDATE table SET col1 = ? WHERE id = ?",
    (new_value, row_id)
)
aConn.commit()
```

#### DELETE
```python
aCur.execute("DELETE FROM table WHERE id = ?", (row_id,))
aConn.commit()
```

#### COUNT
```python
aCur.execute("SELECT COUNT(*) FROM table WHERE condition = ?", (value,))
aCount = aCur.fetchone()[0]
```

### JOIN Patterns

#### INNER JOIN (Only matching rows)
```python
aCur.execute("""
    SELECT a.col1, b.col2 
    FROM table_a a
    JOIN table_b b ON a.id = b.foreign_key
    WHERE a.id = ?
""", (value,))
```

#### LEFT JOIN (All from left, matching from right)
```python
aCur.execute("""
    SELECT b.col1, u.name
    FROM bookings b
    LEFT JOIN users u ON b.driver_id = u.id
""")
# u.name will be None if no driver assigned
```

### Parameterized Queries
Always use `?` placeholders to prevent SQL injection:
```python
# CORRECT
aCur.execute("SELECT * FROM users WHERE email = ?", (email,))

# WRONG - SQL injection vulnerability
aCur.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Transaction Management
SQLite uses implicit transactions:
- Each connection has a transaction
- Must call `commit()` to persist changes
- Can call `rollback()` to undo changes
- Connection closes automatically rollback uncommitted changes

### Error Handling
```python
try:
    aConn = sqlite3.connect("db.db")
    aCur = aConn.cursor()
    aCur.execute("...")
    aConn.commit()
except sqlite3.IntegrityError:
    # Constraint violation (UNIQUE, FOREIGN KEY, etc.)
except sqlite3.OperationalError:
    # Database locked, table doesn't exist, etc.
except sqlite3.Error as e:
    # Generic database error
finally:
    aConn.close()
```

### Data Type Handling
SQLite has dynamic typing:
- INTEGER: Python int
- TEXT: Python str
- REAL: Python float
- BLOB: Python bytes
- NULL: Python None

### Date/Time Storage
This app stores dates/times as TEXT:
```python
# Store
booking_date = "2024-01-15"
booking_time = "14:30"

# Validate
from datetime import datetime
datetime.strptime(booking_date, "%Y-%m-%d")
datetime.strptime(booking_time, "%H:%M")

# Query by date
aCur.execute("SELECT * FROM bookings WHERE booking_date = ?", (date,))
```

---

## Data Flow & Component Interaction

### Application Lifecycle

1. **Startup** (`main.py`):
   ```
   main.py → init_db() → Create tables
           → MainApp() → Create window
           → Create container frame
           → Create LoginPage, RegisterPage
           → Show LoginPage
           → mainloop() [blocks until window closes]
   ```

2. **Login Flow**:
   ```
   LoginPage.login() → Validate input
                    → Query database for user
                    → MainApp.show_dashboard(role, name, id)
                    → Destroy old dashboard (if exists)
                    → Create new DashboardPage with user data
                    → DashboardPage.__init__() dispatches to role-specific mixin
   ```

3. **Registration Flow**:
   ```
   RegisterPage.register() → Validate input
                          → INSERT into users table
                          → MainApp.show_login()
                          → LoginPage raised to front
   ```

4. **Dashboard Navigation**:
   ```
   DashboardPage → show_customer/driver/admin_dashboard()
                → Create tab buttons
                → Create content_area frame
                → Show default content
   
   Tab Click → Clear content_area children
            → Update tab button colors
            → Create new content
   ```

5. **Customer Booking Flow**:
   ```
   Customer clicks "Book a Ride" tab
   → show_booking_form()
   → User fills form
   → Clicks "Book Your Taxi"
   → submit_booking()
   → Validate inputs
   → INSERT into bookings (status='pending', driver_id=NULL)
   → Success message
   → Clear form
   ```

6. **Admin Assignment Flow**:
   ```
   Admin views Bookings tab
   → show_bookings_management()
   → Query all bookings with JOINs
   → Display cards with "Assign Driver" button (if pending)
   → Admin clicks "Assign Driver"
   → assign_driver_to_booking()
   → Query available drivers
   → Show modal with dropdown
   → Admin selects driver
   → confirm_assignment()
   → check_booking_overlap()
   → UPDATE bookings SET driver_id=X, status='assigned'
   → Refresh booking list
   ```

7. **Driver Workflow**:
   ```
   Driver logs in
   → show_driver_dashboard()
   → show_assigned_rides()
   → Query bookings with driver_id=self.user_id
   → JOIN with users to get customer info
   → Display rides with action buttons
   
   Driver clicks "Mark as Completed"
   → complete_ride()
   → UPDATE bookings SET status='completed'
   → Refresh ride list
   
   Driver clicks "Decline Ride"
   → decline_ride()
   → Show modal with textbox
   → Driver enters reason
   → UPDATE bookings SET driver_id=NULL, status='pending'
   → Refresh ride list
   ```

8. **Customer Edit Flow**:
   ```
   Customer views "My Bookings" tab
   → show_my_bookings()
   → Query bookings with user_id=self.user_id
   → Display with Edit/Cancel buttons (if status='pending')
   → Customer clicks "Edit Booking"
   → edit_booking()
   → Show modal pre-filled with current values
   → Customer modifies and clicks "Save Changes"
   → Validate new values
   → Check if driver is assigned
   → If assigned, check_booking_overlap()
   → UPDATE bookings with new values
   → Refresh booking list
   ```

### Database Entity Relationships

```
users (1) ──────────────────┐
  │                         │
  │ user_id                 │ driver_id
  │                         │
  ▼                         │
bookings (many)             │
  │                         │
  └─────────────────────────┘
```

- **One-to-Many**: One user (customer) has many bookings
- **One-to-Many**: One user (driver) is assigned to many bookings
- **Self-referencing**: users table referenced twice in bookings

### State Management

The application uses **no global state**. All state is:
1. **Database State**: Persistent in SQLite file
2. **Widget State**: Stored in widget properties
3. **Session State**: Passed through constructor parameters
   - `user_id`, `user_role`, `user_name` stored in DashboardPage instance

### UI Update Pattern

**Refresh Strategy**: Destroy and recreate
```
User action → Database change → Destroy content_area children
                              → Re-query database
                              → Recreate UI from fresh data
```

**Why this works**: 
- Simple implementation
- No need to track which widgets need updating
- Always shows latest data from database
- Acceptable for small datasets (< 1000 records)

### Validation Layers

1. **Frontend Validation** (immediate feedback):
   - Check required fields
   - Validate formats (email, date, time)
   - Basic length checks

2. **Database Constraints** (data integrity):
   - UNIQUE constraint on email
   - FOREIGN KEY constraints
   - NOT NULL constraints

3. **Business Logic Validation** (application rules):
   - Driver overlap detection
   - Role-based access (implicit in UI)
   - Edit restrictions (only pending bookings)

### Security Considerations

**Current Issues**:
1. Passwords stored in plaintext
2. No session management (anyone with access can use any role)
3. No authentication tokens
4. SQL injection prevented (parameterized queries ✓)
5. No audit trail
6. No rate limiting

**Suitable For**: 
- Single-user desktop application
- Trusted environment
- Educational/prototype purposes

**Not Suitable For**:
- Multi-user systems
- Internet-facing applications
- Production environments

---

## Architecture Strengths

1. **Clear Separation**: Each dashboard role is a separate mixin
2. **Reusable Patterns**: Modal dialogs, stat cards, tab navigation
3. **Consistent Styling**: Centralized color palette and fonts
4. **Simple Navigation**: Frame stacking is easy to understand
5. **Direct Database Access**: No ORM overhead, full SQL control
6. **Graceful Degradation**: Try/except blocks with user feedback

## Architecture Weaknesses

1. **No Service Layer**: Business logic mixed with UI code
2. **Duplicate Code**: Many similar queries across files
3. **No Caching**: Every UI refresh queries database
4. **Tight Coupling**: UI directly depends on database schema
5. **Limited Testability**: Hard to unit test mixed UI/logic
6. **No Abstraction**: Database connection code repeated everywhere

## Potential Improvements

1. **Data Access Layer**:
   ```python
   class BookingRepository:
       def get_user_bookings(self, user_id):
           # Centralize query logic
           
       def create_booking(self, booking_data):
           # Centralize insert logic
   ```

2. **Configuration Management**:
   ```python
   class Config:
       DB_PATH = "taxi.db"
       WINDOW_SIZE = "1000x800"
       THEME = "dark"
   ```

3. **Password Hashing**:
   ```python
   import bcrypt
   hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   ```

4. **Connection Pooling**:
   ```python
   class DatabaseManager:
       def __init__(self):
           self.conn = sqlite3.connect("taxi.db")
           
       def __enter__(self):
           return self.conn.cursor()
           
       def __exit__(self, *args):
           self.conn.commit()
   ```

5. **Validation Classes**:
   ```python
   class BookingValidator:
       @staticmethod
       def validate_date(date_str):
           # Centralize validation logic
   ```

---

## Conclusion

The Bedfordshire Taxi Booking System demonstrates a straightforward application architecture using CustomTkinter and SQLite3. The codebase is well-structured for a desktop application, with clear role separation through mixins and consistent UI patterns. While it lacks some production-ready features (security, testing, abstraction), it serves as an excellent example of modern Python GUI development with direct database access.

The use of CustomTkinter provides a modern, polished UI compared to vanilla Tkinter, and the frame stacking navigation pattern keeps the codebase simple. The mixin architecture elegantly handles role-based functionality without excessive inheritance chains.

For educational purposes or as a prototype, this architecture is appropriate. For production use, consider adding a service layer, proper authentication, and automated testing.
