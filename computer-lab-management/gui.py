import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


DATABASE = "computer_lab.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please enter username and password."
        )
        return

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        AND password_hash = ?
    """, (username, password_hash))

    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {user['full_name']}!\n\n"
            f"Role: {user['role'].title()}"
        )
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


# -----------------------------
# LabGrid Login Window
# -----------------------------

root = tk.Tk()

root.title("LabGrid")
root.geometry("500x400")
root.resizable(False, False)

title = tk.Label(
    root,
    text="LabGrid",
    font=("Arial", 30, "bold")
)
title.pack(pady=(55, 5))

subtitle = tk.Label(
    root,
    text="Computer Laboratory Management System",
    font=("Arial", 11)
)
subtitle.pack(pady=(0, 35))


username_label = tk.Label(
    root,
    text="Username",
    font=("Arial", 11)
)
username_label.pack()

username_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 11)
)
username_entry.pack(pady=(5, 18))


password_label = tk.Label(
    root,
    text="Password",
    font=("Arial", 11)
)
password_label.pack()

password_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 11),
    show="*"
)
password_entry.pack(pady=(5, 25))


login_button = tk.Button(
    root,
    text="LOGIN",
    width=22,
    font=("Arial", 11, "bold"),
    command=login
)
login_button.pack()


root.mainloop()