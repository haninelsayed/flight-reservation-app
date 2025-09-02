# ✈️ SkyHigh Reservations

A desktop flight reservation system built with **Python, Tkinter, SQLite, and TkCalendar**.  
Users can book flights, view reservations in a table, and edit or delete them - all in a pastel-styled interface.

---

## 🚀 Features
- **Home Page** - quick navigation to booking and reservations.
- **Book Flight** - form with:
  - Name
  - Flight number
  - Departure / Destination
  - Date (calendar picker)
  - Seat number
- **View Reservations** - table with all reservations:
  - Inline **Edit | Delete** actions
  - Auto-refresh after any change
- **SQLite backend** - local file database (`flights.db`)
- **Pastel pink theme** - custom styling with ttk

---

## 🛠️ Tech Stack
- Python 3.9+
- Tkinter (built-in)
- SQLite3 (built-in)
- [tkcalendar](https://pypi.org/project/tkcalendar/)

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/haninelsayed/flight-reservation-app.git
   cd flight-reservation-app
   2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
---

## ▶️ Usage
Run the app:
```bash
python main.py


