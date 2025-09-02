import tkinter as tk
from tkinter import ttk
from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditReservationPage

NAV_BG = "#f8c5d8"
NAV_FG = "#6a2c3b"
NAV_FG_HOVER = "#8a3a4d"
APP_BG = "#fff6fa"
PRIMARY = "#ffb3c9"
PRIMARY_HOVER = "#ff9db9"
TITLE_FG = "#6a2c3b"
MUTED = "#806e76"

class FlightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkyHigh Reservations")
        self.geometry("1000x650")
        self.minsize(900, 600)
        self.configure(bg=APP_BG)

        self._setup_style()

        # header
        nav = ttk.Frame(self, style="Nav.TFrame")
        nav.pack(fill="x")

        left = ttk.Frame(nav, style="Nav.TFrame")
        left.pack(side="left", padx=14, pady=8)
        ttk.Label(left, text="✈SkyHigh Reservations", style="Nav.Title.TLabel").pack(side="left")

        right = ttk.Frame(nav, style="Nav.TFrame")
        right.pack(side="right", padx=14, pady=8)

        self._make_nav_link(right, "Home", lambda: self.show("HomePage")).pack(side="left", padx=10)
        self._make_nav_link(right, "Book Flight", lambda: self.show("BookingPage")).pack(side="left", padx=10)
        self._make_nav_link(right, "View Reservations", lambda: self.show("ReservationsPage")).pack(side="left", padx=10)

        container = ttk.Frame(self, padding=0, style="App.TFrame")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            f = F(container, self)
            self.frames[F.__name__] = f
            f.grid(row=0, column=0, sticky="nsew")

        self.show("HomePage")

    def _make_nav_link(self, parent, text, command):
        lbl = ttk.Label(parent, text=text, style="Nav.Link.TLabel", cursor="hand2")
        def on_enter(_): lbl.configure(foreground=NAV_FG_HOVER, font=("Segoe UI", 10, "underline"))
        def on_leave(_): lbl.configure(foreground=NAV_FG, font=("Segoe UI", 10))
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)
        lbl.bind("<Button-1>", lambda _e: command())
        return lbl

    def show(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background=APP_BG)

        # Nav styles
        style.configure("Nav.TFrame", background=NAV_BG)
        style.configure("Nav.Title.TLabel", background=NAV_BG, foreground=NAV_FG,
                        font=("Segoe UI Semibold", 14))
        style.configure("Nav.Link.TLabel", background=NAV_BG, foreground=NAV_FG,
                        font=("Segoe UI", 10))

        # Headings / cards / buttons
        style.configure("Hero.Title.TLabel", background=APP_BG, foreground=TITLE_FG,
                        font=("Segoe UI Semibold", 32))
        style.configure("Hero.Sub.TLabel", background=APP_BG, foreground=MUTED,
                        font=("Segoe UI", 12))
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("Card.Title.TLabel", background="white", foreground=TITLE_FG,
                        font=("Segoe UI Semibold", 18))
        style.configure("Card.Text.TLabel", background="white", foreground=MUTED,
                        font=("Segoe UI", 10))

        style.configure("Primary.TButton", padding=(14, 10), font=("Segoe UI Semibold", 10))
        style.map("Primary.TButton",
                  background=[("!disabled", PRIMARY), ("active", PRIMARY_HOVER)],
                  foreground=[("!disabled", "white")])

        # Page title style (used in booking)
        style.configure("PageTitle.TLabel",
                        background=APP_BG, foreground=TITLE_FG,
                        font=("Segoe UI Semibold", 22))

if __name__ == "__main__":
    app = FlightApp()
    app.mainloop()


