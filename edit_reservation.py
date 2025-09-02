import tkinter as tk
from tkinter import messagebox
from database import update_reservations, delete_reservation

class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Edit / Delete Reservation", font=("Arial", 18)).pack(pady=10)

        self.res_id = tk.StringVar()
        self.column = tk.StringVar()
        self.new_value = tk.StringVar()

        form = tk.Frame(self); form.pack(pady=8)
        for i,(label,var) in enumerate([
            ("Reservation ID", self.res_id),
            ("Field to update (name, flight_number, departure, destination, date, seat_number)", self.column),
            ("New value", self.new_value),
        ]):
            tk.Label(form, text=label, anchor="w", width=48).grid(row=i, column=0, sticky="w", padx=6, pady=4)
            tk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, padx=6, pady=4)

        tk.Button(self, text="Update", command=self.update).pack(pady=6)
        tk.Button(self, text="Delete", command=self.delete).pack(pady=6)
        tk.Button(self, text="Back", command=lambda: controller.show("HomePage")).pack()

    def update(self):
        try:
            rid = int(self.res_id.get())
        except ValueError:
            messagebox.showerror("Error", "Reservation ID must be a number."); return

        col = self.column.get().strip()
        val = self.new_value.get().strip()
        if not col or not val:
            messagebox.showerror("Error", "Field and value are required."); return

        try:
            update_reservations(rid, col, val)
            messagebox.showinfo("Updated", f"{col} updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        try:
            rid = int(self.res_id.get())
        except ValueError:
            messagebox.showerror("Error", "Reservation ID must be a number."); return
        delete_reservation(rid)
        messagebox.showinfo("Deleted", f"Reservation {rid} deleted.")
