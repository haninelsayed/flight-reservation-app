import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import add_reservation

class BookingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="App.TFrame")
        self.controller = controller

        ttk.Label(self, text="New Reservation", style="PageTitle.TLabel").pack(pady=16)

        self.vars = {
            k: tk.StringVar()
            for k in ("name", "flight_number", "departure", "destination", "seat_number")
        }
        self.date_var = tk.StringVar()

        form = ttk.Frame(self, padding=12)
        form.pack(pady=10)

        rows = [
            ("Name", "name"),
            ("Flight #", "flight_number"),
            ("From", "departure"),
            ("To", "destination"),
            ("Seat", "seat_number"),
        ]

        for i, (label_text, key) in enumerate(rows):
            ttk.Label(form, text=label_text, width=20).grid(row=i, column=0, padx=6, pady=6, sticky="e")
            ttk.Entry(form, textvariable=self.vars[key], width=32).grid(row=i, column=1, padx=6, pady=6)

        date_row = len(rows)
        ttk.Label(form, text="Date", width=20).grid(row=date_row, column=0, padx=6, pady=6, sticky="e")
        self.date_entry = DateEntry(
            form,
            width=29,
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False,
        )
        self.date_entry.grid(row=date_row, column=1, padx=6, pady=6, sticky="w")
        self.date_var.set(self.date_entry.get_date().strftime("%Y-%m-%d"))

        ttk.Button(self, text="Save", style="Primary.TButton", command=self.save).pack(pady=12)

    def save(self):
        data = {k: v.get().strip() for k, v in self.vars.items()}
        picked = self.date_entry.get_date()
        data["date"] = picked.strftime("%Y-%m-%d")

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill all fields.")
            return
        if not self._looks_like_iso_date(data["date"]):
            messagebox.showerror("Error", "Date must be YYYY-MM-DD.")
            return

        add_reservation(**data)
        messagebox.showinfo("Saved", "Reservation added.")

        for v in self.vars.values(): v.set("")
        self.date_entry.set_date(datetime.today())

        self.controller.show("ReservationsPage")
        self.controller.frames["ReservationsPage"].refresh()

    def _looks_like_iso_date(self, s: str) -> bool:
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except ValueError:
            return False




