import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import get_reservations, update_reservations, delete_reservation

PRIMARY = "#ffb3c9"
PRIMARY_HOVER = "#ff9db9"
APP_BG = "#fff6fa"
TITLE_FG = "#6a2c3b"
MUTED = "#806e76"

class ReservationsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="App.TFrame")
        self.controller = controller
        self._setup_style()

        # Title
        header = ttk.Frame(self, style="App.TFrame")
        header.pack(fill="x", padx=24, pady=(22, 8))
        ttk.Label(header, text="Your Reservations", style="HeroTitle.TLabel").pack(anchor="w")

        # Tools (search + CTA)
        tools = ttk.Frame(self, style="App.TFrame")
        tools.pack(fill="x", padx=24, pady=(0, 8))

        self.search_var = tk.StringVar()
        self.search = ttk.Entry(tools, textvariable=self.search_var, width=44)
        self.search.pack(side="left")
        self.search.insert(0, "Search by name, flight, city, date…")
        self.search.bind("<FocusIn>", lambda e: self._clear_placeholder())
        self.search.bind("<Return>", lambda e: self.refresh())

        ttk.Button(
            tools, text="Book New Flight", style="Primary.TButton",
            command=lambda: controller.show("BookingPage")
        ).pack(side="right")

        card = ttk.Frame(self, style="Card.TFrame", padding=0)
        card.pack(fill="both", expand=True, padx=24, pady=10)

        cols = ("id", "flight_number", "name", "departure", "destination", "date", "seat_number", "actions")
        self.tree = ttk.Treeview(card, columns=cols, show="headings", height=16, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        labels = {
            "flight_number": "Flight Number",
            "name": "Name",
            "departure": "Departure",
            "destination": "Destination",
            "date": "Date",
            "seat_number": "Seat",
            "actions": "Actions",
        }
        self.tree.heading("id", text="id")
        self.tree.column("id", width=0, stretch=False)

        for key in ("flight_number","name","departure","destination","date","seat_number","actions"):
            self.tree.heading(key, text=labels[key])

        self.tree.column("flight_number", width=140, anchor="w")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("departure", width=120, anchor="w")
        self.tree.column("destination", width=120, anchor="w")
        self.tree.column("date", width=130, anchor="w")
        self.tree.column("seat_number", width=90, anchor="w")
        self.tree.column("actions", width=130, anchor="center")

        self.tree.bind("<Button-1>", self._on_click_actions)

    def on_show(self):
        self.refresh()

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("App.TFrame", background=APP_BG)
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("HeroTitle.TLabel", background=APP_BG, foreground=TITLE_FG,
                        font=("Segoe UI Semibold", 28))
        style.configure("Primary.TButton", padding=(14, 8), font=("Segoe UI Semibold", 10))
        style.map("Primary.TButton",
                  background=[("!disabled", PRIMARY), ("active", PRIMARY_HOVER)],
                  foreground=[("!disabled", "white")])
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _clear_placeholder(self):
        if self.search_var.get().lower().startswith("search"):
            self.search_var.set("")

    def _filtered_rows(self):
        rows = get_reservations()
        q = self.search_var.get().strip().lower()
        if not q or q.startswith("search"):
            return rows
        def match(row):
            return any(q in str(cell).lower() for cell in row[1:])
        return [r for r in rows if match(r)]

    def refresh(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for row in self._filtered_rows():
            rid, name, flight, dep, dest, date, seat = row
            actions = "Edit | Delete"
            self.tree.insert("", "end", values=(rid, flight, name, dep, dest, date, seat, actions))

    def _get_selection(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])["values"]

    def _on_click_actions(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell": return
        col = self.tree.identify_column(event.x)
        if col != f"#{len(self.tree['columns'])}": return
        row_id = self.tree.identify_row(event.y)
        if not row_id: return
        self.tree.selection_set(row_id)

        bbox = self.tree.bbox(row_id, col)
        if not bbox: return
        x, y, w, h = bbox
        if (event.x - x) <= w / 2:
            self._edit_selected()
        else:
            self._delete_selected()

    def _edit_selected(self):
        vals = self._get_selection()
        if not vals:
            return
        rid, flight_number, name, departure, destination, date_str, seat_number, _ = vals
        EditDialog(
            self,
            res_id=rid,
            fields={
                "name": name,
                "flight_number": flight_number,
                "departure": departure,
                "destination": destination,
                "date": date_str,
                "seat_number": seat_number
            },
            on_saved=self.refresh
        )

    def _delete_selected(self):
        vals = self._get_selection()
        if not vals:
            return
        rid = vals[0]
        if not messagebox.askyesno("Delete", f"Delete reservation #{rid}?"):
            return
        delete_reservation(rid)
        self.refresh()


class EditDialog(tk.Toplevel):
    """Edit popup; Date field uses a calendar and updates only changed fields."""
    def __init__(self, parent, res_id, fields: dict, on_saved=None):
        super().__init__(parent)
        self.title(f"Edit Reservation #{res_id}")
        self.configure(bg="white")
        self.resizable(False, False)
        self.grab_set()

        self.res_id = res_id
        self.on_saved = on_saved
        self.original = fields.copy()
        self.vars = {k: tk.StringVar(value=v) for k, v in fields.items() if k != "date"}

        body = ttk.Frame(self, padding=16)
        body.pack(fill="both", expand=True)

        order = [
            ("Flight Number", "flight_number"),
            ("Name", "name"),
            ("Departure", "departure"),
            ("Destination", "destination"),
            ("Date (YYYY-MM-DD)", "date"),
            ("Seat", "seat_number"),
        ]

        for i, (label, key) in enumerate(order):
            ttk.Label(body, text=label, width=20).grid(row=i, column=0, sticky="w", padx=(0, 10), pady=6)
            if key == "date":
                self.date_entry = DateEntry(body, width=26, date_pattern="yyyy-mm-dd", showweeknumbers=False)
                try:
                    self.date_entry.set_date(datetime.strptime(self.original["date"], "%Y-%m-%d"))
                except Exception:
                    self.date_entry.set_date(datetime.today())
                self.date_entry.grid(row=i, column=1, pady=6, sticky="w")
            else:
                ttk.Entry(body, textvariable=self.vars[key], width=28).grid(row=i, column=1, pady=6)

        btns = ttk.Frame(body)
        btns.grid(row=len(order), column=0, columnspan=2, pady=(12, 0))
        ttk.Button(btns, text="Save", style="Primary.TButton", command=self._save).pack(side="left")
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=8)

    def _save(self):
        changes = {}
        for k, var in self.vars.items():
            val = var.get().strip()
            if val != self.original[k]:
                changes[k] = val
        new_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        if new_date != self.original["date"]:
            changes["date"] = new_date

        if not changes:
            self.destroy()
            return

        for col, new_val in changes.items():
            update_reservations(self.res_id, col, new_val)

        if self.on_saved:
            self.on_saved()
        self.destroy()






