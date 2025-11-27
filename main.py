import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from szb_edzesmodul import (
    SZBTrainingEntry, szb_load_sessions, szb_save_sessions, szb_stats
)
import matplotlib.pyplot as plt

DATAFILE = "data/sessions.json"


class SZBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edzésnapló – SZB")


        self.sessions = szb_load_sessions(DATAFILE)


        tk.Label(root, text="Dátum (YYYY-MM-DD):").grid(row=0, column=0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row=0, column=1)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(root, text="Edzés típusa:").grid(row=1, column=0)
        self.entry_type = tk.Entry(root)
        self.entry_type.grid(row=1, column=1)

        tk.Label(root, text="Mennyiség (km / perc / db):").grid(row=2, column=0)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=2, column=1)

        tk.Button(root, text="Hozzáadás", command=self.add_session).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Törlés", command=self.delete_session).grid(row=3, column=1, pady=5)
        tk.Button(root, text="Grafikon", command=self.show_plot).grid(row=4, column=0, columnspan=2)


        self.listbox = tk.Listbox(root, width=50)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=10)

        self.refresh_list()


    def add_session(self):
        date = self.entry_date.get()
        training_type = self.entry_type.get()
        amount = self.entry_amount.get()

        if not (date and training_type and amount):
            messagebox.showwarning("Hiba", "Minden mezőt ki kell tölteni!")
            return

        try:
            float(amount)
        except ValueError:
            messagebox.showwarning("Hiba", "A mennyiségnek számnak kell lennie!")
            return

        session = SZBTrainingEntry(date, training_type, amount)
        self.sessions.append(session)
        szb_save_sessions(DATAFILE, self.sessions)
        self.refresh_list()

    def delete_session(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Hiba", "Nincs kiválasztva elem.")
            return

        index = sel[0]
        del self.sessions[index]
        szb_save_sessions(DATAFILE, self.sessions)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for s in self.sessions:
            self.listbox.insert(tk.END, f"{s.date} – {s.training_type} – {s.amount}")

    def show_plot(self):
        if not self.sessions:
            messagebox.showinfo("Nincs adat", "Nincs megjeleníthető adat.")
            return

        dates = [s.date for s in self.sessions]
        values = [float(s.amount) for s in self.sessions]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, values, marker="o")
        plt.title("Edzésmennyiség alakulása")
        plt.xlabel("Dátum")
        plt.ylabel("Mennyiség")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    root = tk.Tk()
    app = SZBApp(root)
    root.mainloop()
