# Bedfordshire Taxi Booking System

A comprehensive desktop application for managing taxi bookings with role-based access control, built with **CustomTkinter** and **SQLite3**.

## 🚀 Features

### For Customers
- 📅 Book taxi rides with date/time selection
- 📋 View booking history
- ✏️ Edit pending bookings
- ❌ Cancel pending bookings
- 📊 Track booking status (pending → assigned → completed)

### For Drivers
- 🚗 View assigned rides
- 📞 Access customer contact information
- ✅ Mark rides as completed
- 🚫 Decline rides (with reason)

### For Administrators
- 👥 Manage users (view, delete)
- 📦 Manage all bookings
- 🔧 Assign drivers to bookings
- ⚠️ Prevent driver double-booking with overlap detection
- 📊 View system statistics and reports

## 📚 Complete Documentation

This project includes comprehensive documentation covering every aspect of the codebase:

### 📖 [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) - Start Here!
**Your gateway to all documentation**
- Overview of all documentation files
- Quick start guide for new developers
- Use case-specific learning paths
- Key insights and conventions

### 📝 [CODE_ANALYSIS.md](./CODE_ANALYSIS.md) - Detailed Analysis
**67KB of comprehensive code analysis** (~20,000 words)
- Segment-by-segment breakdown of entire codebase
- **CustomTkinter patterns** with real examples
- **SQLite3 workflows** and query patterns
- Data flow and component interaction
- Architecture analysis (strengths, weaknesses, improvements)

**Key sections:**
- ✅ Database Architecture (schema, migrations, connections)
- ✅ Application Entry Point (navigation, window management)
- ✅ Authentication System (login, registration)
- ✅ Dashboard System (customer, driver, admin)
- ✅ CustomTkinter Patterns (widgets, layouts, events, images)
- ✅ SQLite3 Workflows (queries, JOINs, transactions)

### 📐 [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) - Visual Documentation
**Complete class diagrams and visualizations**
- PlantUML class diagram (all classes and relationships)
- Mermaid diagram (GitHub-friendly format)
- Simplified component diagrams
- Database entity-relationship diagram
- Sequence diagrams (login, booking, assignment flows)
- Design pattern analysis
- Coupling and cohesion review

### ⚡ [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Cheat Sheet
**Quick lookup guide for common tasks**
- File responsibilities
- Database schema quick view
- CustomTkinter cheat sheet
- SQLite3 cheat sheet
- Common task walkthroughs
- Color palette
- Debugging tips
- Pro tips and common pitfalls

## 🎯 Quick Start

### Installation
```bash
# Install dependencies
pip install customtkinter pillow

# Run the application
python main.py
```

### First Steps
1. **Register an account** (choose role: Customer, Driver, or Admin)
2. **Login** with your credentials
3. **Explore** role-specific features

### For Developers
1. **Start with:** [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md)
2. **Understand architecture:** Read "System Overview" in [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)
3. **Study diagrams:** Review [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md)
4. **Quick reference:** Keep [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) handy

## 🏗️ Architecture Overview

### Design Pattern: Multiple Inheritance with Mixins
```python
class DashboardPage(
    CustomerDashboardMixin,    # Customer features
    DriverDashboardMixin,      # Driver features
    AdminDashboardMixin,       # Admin features
    CTkFrame                   # Base UI component
):
    pass
```

**Benefits:**
- ✅ Clean separation of role-specific functionality
- ✅ No code duplication
- ✅ Easy to extend with new roles
- ✅ Maintainable and testable

### Navigation: Frame Stacking
```python
# All pages exist simultaneously, stacked at same location
LoginPage.grid(row=0, column=0)
RegisterPage.grid(row=0, column=0)
DashboardPage.grid(row=0, column=0)

# Bring desired page to front
current_page.tkraise()
```

**Benefits:**
- ✅ Fast navigation (no widget recreation)
- ✅ Simple implementation
- ✅ State preservation

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,           -- 'Customer', 'Driver', or 'Admin'
    name TEXT,
    address TEXT,
    phone TEXT
)
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,         -- FK to users (customer)
    driver_id INTEGER,                -- FK to users (driver, nullable)
    pickup_location TEXT NOT NULL,
    dropoff_location TEXT NOT NULL,
    booking_date TEXT NOT NULL,       -- Format: 'YYYY-MM-DD'
    booking_time TEXT NOT NULL,       -- Format: 'HH:MM'
    status TEXT DEFAULT 'pending',    -- 'pending', 'assigned', 'completed', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (driver_id) REFERENCES users(id)
)
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.x | Core application |
| UI Framework | CustomTkinter | Modern, themed GUI |
| Database | SQLite3 | Embedded relational database |
| Images | PIL/Pillow | Image loading and processing |
| Dates | datetime | Date/time validation and calculations |

## 📂 Project Structure

```
bedfordshire-taxi-booking-system/
├── main.py                      # Entry point - MainApp class
├── db_setup.py                  # Database initialization
├── login.py                     # Login page
├── register.py                  # Registration page
├── dashboard.py                 # Dashboard container (multiple inheritance)
├── dashboard_customer.py        # Customer-specific features
├── dashboard_driver.py          # Driver-specific features
├── dashboard_admin.py           # Admin-specific features
├── assets/                      # Images and static files
│   └── static/img/
├── CODE_ANALYSIS.md             # 📚 Comprehensive code analysis
├── CLASS_DIAGRAM.md             # 📐 Class diagrams and visualizations
├── DOCUMENTATION_INDEX.md       # 📖 Documentation navigation
├── QUICK_REFERENCE.md           # ⚡ Quick reference guide
└── README.md                    # 👋 This file
```

## 🎨 Code Highlights

### CustomTkinter Modern UI
```python
# Modern card design with rounded corners
card = CTk.CTkFrame(
    parent,
    fg_color="#1A1F2E",
    corner_radius=12,
    border_width=1,
    border_color="#2D3748"
)

# Styled button with hover effect
button = CTk.CTkButton(
    parent,
    text="Book Now",
    fg_color="#FFD700",
    hover_color="#FFC700",
    font=CTk.CTkFont(size=14, weight="bold")
)
```

### SQLite3 Safe Queries
```python
# Parameterized query (prevents SQL injection)
cur.execute(
    "SELECT * FROM users WHERE email = ? AND password = ?",
    (email, password)
)
user = cur.fetchone()

# Complex JOIN query
cur.execute("""
    SELECT b.id, u1.name, u2.name 
    FROM bookings b
    JOIN users u1 ON b.user_id = u1.id
    LEFT JOIN users u2 ON b.driver_id = u2.id
    WHERE b.status = ?
""", ("pending",))
```

### Overlap Detection Algorithm
```python
def check_booking_overlap(driver_id, date, time, exclude_id=None):
    """
    Prevents double-booking drivers by detecting time conflicts
    Assumes 1-hour ride duration
    """
    # Query existing bookings for same driver and date
    existing = query_driver_bookings(driver_id, date, exclude_id)
    
    new_start = parse_datetime(date, time)
    new_end = new_start + timedelta(hours=1)
    
    for existing_booking in existing:
        existing_start = parse_datetime(existing_booking.date, existing_booking.time)
        existing_end = existing_start + timedelta(hours=1)
        
        # Check if time ranges overlap
        if new_start < existing_end and existing_start < new_end:
            return True  # Overlap detected
    
    return False  # No overlap
```

## 📊 Key Features Explained

### 1. Role-Based Access Control
- Users assigned roles during registration
- Dashboard automatically adapts to user role
- Each role has dedicated mixin with specific features
- Clean separation prevents code duplication

### 2. Dynamic UI Updates
- Content areas cleared and rebuilt after changes
- Always shows fresh data from database
- No manual state synchronization needed
- Simple but effective for desktop apps

### 3. Modal Dialogs for Editing
- Edit operations use `CTkToplevel` modal windows
- Blocks parent window until complete
- Pre-fills form with current values
- Validates before saving to database

### 4. Driver Assignment with Validation
- Admin can assign drivers to pending bookings
- Overlap detection prevents double-booking
- Shows only available drivers
- Updates booking status automatically

## 🔒 Security Notes

⚠️ **This application is designed for educational purposes and local use.**

**Known Limitations:**
- Passwords stored in plaintext (should use bcrypt/argon2)
- No session management
- No rate limiting
- No audit logging
- Basic input validation

**Suitable for:**
- ✅ Educational projects
- ✅ Single-user desktop applications
- ✅ Prototypes and demonstrations
- ✅ Learning CustomTkinter and SQLite3

**Not suitable for:**
- ❌ Multi-user production systems
- ❌ Internet-facing applications
- ❌ Systems handling sensitive data

**For production use, implement:**
- Password hashing (bcrypt, argon2)
- Session tokens and authentication
- Role-based access control (RBAC) middleware
- Input sanitization and validation
- Audit logging
- HTTPS/TLS for network communication

## 🚀 Extending the System

### Adding a New Feature
1. Identify which role it belongs to
2. Add method to appropriate mixin class
3. Follow existing patterns (UI cards, database queries)
4. Add navigation (button, tab, etc.)
5. Test thoroughly

**Example: Adding "Favorites" for customers**
```python
# In dashboard_customer.py

class CustomerDashboardMixin:
    # ... existing code ...
    
    def show_favorites(self):
        """Display customer's favorite locations"""
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Query database
        conn = sqlite3.connect("taxi.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM favorites WHERE user_id = ?",
            (self.user_id,)
        )
        favorites = cur.fetchall()
        conn.close()
        
        # Build UI
        for favorite in favorites:
            self.create_favorite_card(favorite)
```

### Adding a Database Table
```python
# In db_setup.py

def init_db():
    # ... existing tables ...
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
```

## 📖 Learning Resources

### For CustomTkinter
- [Official Documentation](https://customtkinter.tomschimansky.com/)
- [GitHub Repository](https://github.com/TomSchimansky/CustomTkinter)
- See **"CustomTkinter Patterns Summary"** in [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)

### For SQLite3
- [Python SQLite3 Docs](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- See **"SQLite3 Workflows Summary"** in [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)

### For This Project
- Read [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) for learning paths
- Study [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) for architecture
- Reference [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for quick help
- Deep dive with [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)

## 🤝 Contributing

To maintain consistency:
1. Follow existing naming conventions (Hungarian notation with 'a' prefix)
2. Use the same CustomTkinter patterns
3. Maintain consistent database query structure
4. Add error handling with user-friendly messages
5. Update documentation when adding features
6. Test all three user roles

## 📝 License

This project is for educational purposes.

## 📧 Support

- **Documentation Issues:** Check [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) for topic-specific guides
- **Code Questions:** See detailed explanations in [CODE_ANALYSIS.md](./CODE_ANALYSIS.md)
- **Quick Help:** Consult [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

---

**Project Version:** 1.0  
**Documentation Updated:** December 2024  
**Total Documentation:** ~30,000 words across 4 comprehensive files

---

## 🎓 What Makes This Documentation Unique

This project includes **production-quality documentation** that goes far beyond typical code comments:

### Comprehensive Coverage
- ✅ **67KB code analysis** with real examples from every file
- ✅ **Complete class diagrams** with all relationships visualized
- ✅ **Sequence diagrams** showing runtime interactions
- ✅ **Quick reference guide** for common tasks
- ✅ **Architecture analysis** with strengths/weaknesses

### Technology-Focused
- ✅ Deep dive into **CustomTkinter patterns**
- ✅ Extensive **SQLite3 workflow** documentation
- ✅ Real code examples for every pattern
- ✅ Practical tips and gotchas

### Developer-Friendly
- ✅ Multiple learning paths for different use cases
- ✅ Cheat sheets and quick references
- ✅ Common tasks and debugging tips
- ✅ Extension guides for adding features

**Perfect for:**
- 📚 Learning CustomTkinter and SQLite3
- 🏗️ Understanding desktop application architecture
- 🎓 Educational projects and coursework
- 🚀 Building similar applications
- 💼 Portfolio demonstration

---

**Built with ❤️ using Python, CustomTkinter, and SQLite3**
