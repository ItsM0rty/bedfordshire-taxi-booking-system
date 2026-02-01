# Quick Reference Guide - Bedfordshire Taxi Booking System

## 🚀 Quick Start for Developers

### Understanding the System in 5 Minutes

1. **What it is:** Desktop taxi booking app with 3 user roles (Customer, Driver, Admin)
2. **Tech stack:** Python + CustomTkinter (UI) + SQLite3 (database)
3. **Architecture:** Frame stacking navigation + Mixin-based role system
4. **Entry point:** `main.py` → Creates window → Shows login page

---

## 📂 File Responsibilities

| File | Purpose | Key Classes |
|------|---------|-------------|
| `main.py` | Application entry & navigation | `MainApp` |
| `db_setup.py` | Database initialization | `init_db()` function |
| `login.py` | Login page | `LoginPage` |
| `register.py` | Registration page | `RegisterPage` |
| `dashboard.py` | Dashboard container | `DashboardPage` |
| `dashboard_customer.py` | Customer features | `CustomerDashboardMixin` |
| `dashboard_driver.py` | Driver features | `DriverDashboardMixin` |
| `dashboard_admin.py` | Admin features | `AdminDashboardMixin` |

---

## 🗄️ Database Schema (Quick View)

### users table
```sql
id, email, password, role, name, address, phone
```

### bookings table
```sql
id, user_id, driver_id, pickup_location, dropoff_location,
booking_date, booking_time, status, created_at
```

**Key Relationships:**
- `bookings.user_id` → `users.id` (customer)
- `bookings.driver_id` → `users.id` (driver, nullable)

**Status Flow:**
`pending` → `assigned` → `completed` or `cancelled`

---

## 🎨 CustomTkinter Cheat Sheet

### Common Widgets
```python
# Frame (container)
frame = CTk.CTkFrame(parent, fg_color="#1A1F2E", corner_radius=10)

# Label (text display)
label = CTk.CTkLabel(parent, text="Hello", font=CTk.CTkFont(size=14))

# Entry (text input)
entry = CTk.CTkEntry(parent, placeholder_text="Enter text", width=200)

# Button (clickable)
button = CTk.CTkButton(parent, text="Click", command=callback)

# OptionMenu (dropdown)
menu = CTk.CTkOptionMenu(parent, values=["A", "B"], command=callback)

# Textbox (multi-line)
textbox = CTk.CTkTextbox(parent, height=100)

# Scrollable Frame
scroll = CTk.CTkScrollableFrame(parent)

# Modal Dialog
dialog = CTk.CTkToplevel(parent)
dialog.transient(parent)
dialog.grab_set()
```

### Layout Methods
```python
# Pack (simple linear layout)
widget.pack(side="left", fill="x", expand=True, padx=10, pady=5)

# Grid (table layout)
widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
parent.grid_rowconfigure(0, weight=1)    # Make row expandable
parent.grid_columnconfigure(0, weight=1) # Make column expandable
```

### Getting/Setting Values
```python
# Entry
value = entry.get()
entry.delete(0, "end")
entry.insert(0, "new text")

# Textbox
text = textbox.get("1.0", "end-1c")
textbox.insert("1.0", "new text")

# OptionMenu
value = menu.get()
menu.set("new value")

# Update appearance
widget.configure(fg_color="#FF0000", text_color="#FFFFFF")
```

---

## 💾 SQLite3 Cheat Sheet

### Connection Pattern
```python
conn = sqlite3.connect("taxi.db")
cur = conn.cursor()
try:
    # ... queries ...
    conn.commit()  # For INSERT/UPDATE/DELETE
finally:
    conn.close()
```

### Query Patterns
```python
# SELECT single row
cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
row = cur.fetchone()  # Returns tuple or None

# SELECT multiple rows
cur.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
rows = cur.fetchall()  # Returns list of tuples

# INSERT
cur.execute(
    "INSERT INTO bookings (user_id, pickup_location) VALUES (?, ?)",
    (user_id, pickup)
)
conn.commit()

# UPDATE
cur.execute(
    "UPDATE bookings SET status = ? WHERE id = ?",
    ("completed", booking_id)
)
conn.commit()

# DELETE
cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
conn.commit()

# COUNT
cur.execute("SELECT COUNT(*) FROM users WHERE role = ?", ("customer",))
count = cur.fetchone()[0]

# INNER JOIN
cur.execute("""
    SELECT b.id, u.name 
    FROM bookings b 
    JOIN users u ON b.user_id = u.id
""")

# LEFT JOIN (nullable relationship)
cur.execute("""
    SELECT b.id, u.name 
    FROM bookings b 
    LEFT JOIN users u ON b.driver_id = u.id
""")
```

### Error Handling
```python
try:
    cur.execute("...")
except sqlite3.IntegrityError:
    # UNIQUE constraint violation (duplicate email, etc.)
except sqlite3.OperationalError:
    # Table doesn't exist, database locked, etc.
except sqlite3.Error as e:
    # General database error
```

---

## 🎯 Common Tasks

### Task: Add a New Customer Feature
1. Open `dashboard_customer.py`
2. Add method to `CustomerDashboardMixin`
3. Follow existing patterns (create card, query database, show results)
4. Add button/tab to trigger your feature
5. Test with customer login

### Task: Add a New Database Column
1. Open `db_setup.py`
2. Add migration check:
   ```python
   try:
       cur.execute("SELECT new_column FROM table LIMIT 1")
   except sqlite3.OperationalError:
       cur.execute("ALTER TABLE table ADD COLUMN new_column TEXT")
   ```
3. Update queries in relevant dashboard files
4. Delete `taxi.db` and restart (for testing)

### Task: Create a Modal Dialog
```python
def show_dialog(self):
    dialog = CTk.CTkToplevel(self)
    dialog.title("My Dialog")
    dialog.geometry("400x300")
    dialog.transient(self)
    dialog.grab_set()
    
    # Add content
    CTk.CTkLabel(dialog, text="Content").pack(pady=20)
    
    def on_submit():
        # Do something
        dialog.destroy()
    
    CTk.CTkButton(dialog, text="Submit", command=on_submit).pack(pady=10)
```

### Task: Add a New Page
```python
# 1. Create new file: my_page.py
import customtkinter as CTk

class MyPage(CTk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Add widgets...

# 2. In main.py, import and create
from my_page import MyPage

# In MainApp.__init__:
for page_class in (LoginPage, RegisterPage, MyPage):
    page = page_class(self.container, self)
    self.pages[page_class] = page
    page.grid(row=0, column=0, sticky="nsew")

# 3. Navigate to it
self.show_page(MyPage)
```

---

## 🎨 Color Palette

```python
# Brand Colors
GOLD = "#FFD700"           # Primary accent
GOLD_HOVER = "#FFC700"     # Hover state

# Dark Theme
DARK_BG = "#0F1419"        # Page background
CARD_BG = "#1A1F2E"        # Card background
BORDER = "#2D3748"         # Card borders
INACTIVE_TAB = "#2D3748"   # Inactive button

# Text Colors
TEXT_PRIMARY = "#E2E8F0"   # Main text
TEXT_SECONDARY = "#B0B8C1" # Secondary text
TEXT_MUTED = "#7A8195"     # Placeholder/muted

# Status Colors
SUCCESS = "#4CAF50"        # Success/completed
SUCCESS_LIGHT = "#81C784"  # Assigned
WARNING = "#FFD700"        # Pending
ERROR = "#FF6B6B"          # Error/cancelled
INFO = "#4FC3F7"           # Info/driver

# Light Mode (for auth pages)
WHITE = "#ffffff"          # Background
LIGHT_GRAY = "#F5F5FA"     # Input background
BORDER_LIGHT = "#E8E8F0"   # Input border
```

---

## 🔍 Debugging Tips

### UI Not Updating?
```python
# After database change, refresh the UI
self.show_my_bookings(parent)  # Recreates content from database
```

### Widget Not Visible?
```python
# Check packing/gridding
widget.pack(fill="both", expand=True)  # For pack
widget.grid(row=0, column=0, sticky="nsew")  # For grid

# Verify parent frame is visible
parent.tkraise()  # Bring to front
```

### Database Query Not Working?
```python
# Print the query results
result = cur.fetchall()
print(f"Query returned: {result}")

# Check for None
if result:
    # Process result
else:
    print("No results found")
```

### Image Not Loading?
```python
# Check file path
import os
path = os.path.join(os.path.dirname(__file__), "assets", "...")
print(f"Looking for image at: {path}")
print(f"File exists: {os.path.exists(path)}")

# Keep reference
label.image = ctk_image  # Prevent garbage collection
```

---

## 📊 Key Data Flows

### Login Flow
```
User enters credentials → LoginPage.login()
→ Query database for user
→ MainApp.show_dashboard(role, name, id)
→ Create DashboardPage with user context
→ Dispatch to role-specific mixin
```

### Booking Flow
```
Customer fills form → CustomerDashboardMixin.submit_booking()
→ Validate date/time formats
→ INSERT into bookings (status='pending')
→ Show success message
→ Clear form
```

### Driver Assignment Flow
```
Admin clicks "Assign Driver" → AdminDashboardMixin.assign_driver_to_booking()
→ Query available drivers
→ Show dropdown modal
→ Admin selects driver
→ Check for time overlaps
→ UPDATE bookings (set driver_id, status='assigned')
→ Refresh booking list
```

---

## 🔐 User Roles & Capabilities

### Customer
- ✅ Create bookings
- ✅ View own bookings
- ✅ Edit pending bookings
- ✅ Cancel pending bookings
- ❌ See other customers' bookings
- ❌ Assign drivers

### Driver
- ✅ View assigned rides
- ✅ See customer contact info
- ✅ Decline assigned rides
- ✅ Mark rides as completed
- ❌ Create bookings
- ❌ See unassigned bookings

### Admin
- ✅ View all users
- ✅ Delete users (cascade to bookings)
- ✅ View all bookings
- ✅ Assign drivers to bookings
- ✅ Delete bookings
- ✅ View system statistics
- ✅ Prevent driver double-booking
- ❌ Edit user passwords

---

## 💡 Pro Tips

### CustomTkinter
1. Set appearance mode **before** creating widgets
2. Use `fg_color="transparent"` for layout frames
3. Keep image references to prevent GC
4. Use `StringVar` for dynamic text updates
5. `transient()` + `grab_set()` for modal dialogs

### SQLite3
1. **Always** use `?` placeholders (prevents SQL injection)
2. **Always** call `commit()` after write operations
3. **Always** close connections (use try/finally)
4. Use `LEFT JOIN` for nullable relationships
5. Handle `IntegrityError` for unique constraints

### Architecture
1. Add features to appropriate mixin
2. Follow existing patterns (don't reinvent)
3. Refresh UI after database changes
4. Use consistent naming (Hungarian notation)
5. Add error handling with user-friendly messages

---

## 📚 Documentation Links

- **Full Code Analysis:** [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)
- **Class Diagrams:** [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md)
- **Documentation Index:** [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md)

---

## 🚨 Common Pitfalls

### ❌ Forgetting to Commit
```python
cur.execute("INSERT INTO ...")
# Missing: conn.commit()
```
**Result:** Data not persisted

### ❌ Not Closing Connections
```python
conn = sqlite3.connect("taxi.db")
# ... do stuff ...
# Missing: conn.close()
```
**Result:** Database locks, memory leaks

### ❌ SQL Injection Vulnerability
```python
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
```
**Solution:** Use parameterized queries
```python
cur.execute("SELECT * FROM users WHERE email = ?", (email,))
```

### ❌ Image Garbage Collection
```python
image = CTk.CTkImage(...)
label = CTk.CTkLabel(parent, image=image)
# Missing: label.image = image
```
**Result:** Image disappears

### ❌ Modal Not Actually Modal
```python
dialog = CTk.CTkToplevel(parent)
# Missing: dialog.transient(parent)
# Missing: dialog.grab_set()
```
**Result:** Parent still interactive

---

## ⚡ Performance Notes

- Database queries are **synchronous** (block UI thread)
- No caching (every refresh queries database)
- No pagination (loads all results)
- No indexes (except primary keys)

**For large datasets:** Consider background threading, caching, or pagination

---

## 🔒 Security Notes

⚠️ **This app is NOT production-ready for security**

**Known Issues:**
- Passwords in plaintext
- No session management
- No rate limiting
- No audit trail

**For production:** Hash passwords, add authentication, implement RBAC

---

**Last Updated:** December 2024  
**Version:** 1.0
