# ✈️ SkyHigh Reservations

A desktop flight reservation system built with **Python, Tkinter, SQLite, and TkCalendar**.  
Users can book flights, view reservations in a table, and edit or delete them - all in a pastel-styled interface.

---

## 🚀 Features
- **Home Page** – quick navigation to booking and reservations.
- **Book Flight** – form with:
  - Name
  - Flight number
  - Departure / Destination
  - Date (calendar picker)
  - Seat number
- **View Reservations** – table with all reservations:
  - Inline **Edit | Delete** actions
  - Auto-refresh after any change
- **SQLite backend** – local file database (`flights.db`)
- **Pastel pink theme** – custom styling with ttk

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
   git clone https://github.com/your-username/skyhigh-reservations.git
   cd skyhigh-reservations
   python -m venv .venv
  # Windows (PowerShell)
  .venv\Scripts\activate
  # macOS/Linux
  source .venv/bin/activate
  pip install -r requirements.txt
  Then to run the app:
  python main.py


