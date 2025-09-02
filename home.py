import tkinter as tk
from tkinter import ttk

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="App.TFrame")
        self.controller = controller

        # Hero
        hero = ttk.Frame(self, style="App.TFrame")
        hero.pack(fill="x", pady=(28, 8))
        ttk.Label(hero, text="Welcome to SkyHigh Reservations", style="Hero.Title.TLabel").pack()
        ttk.Label(
            hero,
            text="Book your flights and manage your reservations with our simple and intuitive system.",
            style="Hero.Sub.TLabel",
            anchor="center",
            wraplength=820,
            justify="center"
        ).pack(pady=(8, 10))

        cards_row = ttk.Frame(self, style="App.TFrame")
        cards_row.pack(pady=20)

        def make_card(parent, emoji, title, text, btn_text, btn_cmd):
            card = ttk.Frame(parent, style="Card.TFrame")
            card.grid_propagate(False)
            card.configure(width=460, height=280)
            card.pack_propagate(False)

            inner = ttk.Frame(card, style="Card.TFrame", padding=24)
            inner.pack(fill="both", expand=True)

            icon = tk.Label(inner, text=emoji, bg="white", fg="#ff5c8a", font=("Segoe UI Emoji", 36))
            icon.pack(pady=(4, 8))

            ttk.Label(inner, text=title, style="Card.Title.TLabel").pack(pady=(0, 6))
            ttk.Label(inner, text=text, style="Card.Text.TLabel",
                      wraplength=360, justify="center").pack(pady=(0, 14))

            ttk.Button(inner, text=btn_text, style="Primary.TButton", command=btn_cmd).pack()
            return card

        wrap = ttk.Frame(cards_row, style="App.TFrame")
        wrap.pack()

        c1 = make_card(
            wrap, "🛫", "Book a Flight",
            "Reserve your next flight by providing your details and flight information.",
            "Book Flight", lambda: controller.show("BookingPage")
        ); c1.grid(row=0, column=0, padx=16, pady=10)

        c2 = make_card(
            wrap, "🧾", "View Reservations",
            "Manage your existing reservations, view details, edit or cancel if needed.",
            "View Reservations", lambda: controller.show("ReservationsPage")
        ); c2.grid(row=0, column=1, padx=16, pady=10)

        wrap.grid_columnconfigure(0, weight=1)
        wrap.grid_columnconfigure(1, weight=1)

