# 🎮 CS2 Statistics Dashboard

A web-based analytics dashboard for **Counter-Strike 2 (CS2)** match data, built as a **Python Advanced course project**.

The application provides:
- User authentication (Student / Admin)
- Match statistics and visualizations
- Team management through an admin panel
- Data stored and accessed via a database and API

---

## 🚀 Features

### 🔐 Authentication & Roles
- **Login & Register system**
- Two roles:
  - **Student**
    - View teams, logos, matches, and statistics
  - **Admin**
    - Full access to dashboard
    - Add, update, and delete teams (CRUD)

### 📊 Dashboard (Student View)
- Team logos (loaded from database)
- Filters:
  - Team
  - Map
  - Event
- Metrics:
  - Matches played
  - Wins
  - Losses
  - Win rate (%)
- Charts:
  - **Map Win Percentage**
  - **Team Wins**
- Match history table

### 🛠 Admin Panel
- Sidebar-based admin tools
- Full **CRUD operations** for teams:
  - Create new teams
  - Read/view teams
  - Update team logos
  - Delete teams
- Role-protected (students cannot access)

---

## 🏗 Project Architecture

Student username and password: student , 123123
Admin username and password: admin , admin123