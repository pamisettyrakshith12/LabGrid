from student_ui import student_dashboard
import tkinter as tk
from tkinter import messagebox

from auth import login


# ============================================================
# COMPUTER LAB MANAGEMENT SYSTEM - LOGIN UI
# ============================================================

class ComputerLabSystem:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # Window Settings
        # ----------------------------------------------------

        self.root.title("Computer Lab Management System")
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)
        self.root.configure(bg="#0F172A")

        self.create_login_ui()

    # ========================================================
    # LOGIN UI
    # ========================================================

    def create_login_ui(self):

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # ----------------------------------------------------
        # Main Container
        # ----------------------------------------------------

        main_frame = tk.Frame(
            self.root,
            bg="#0F172A"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # LEFT SIDE
        # ====================================================

        left_frame = tk.Frame(
            main_frame,
            bg="#172554",
            width=500
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        left_frame.pack_propagate(False)

        # Computer Icon
        icon = tk.Label(
            left_frame,
            text="💻",
            font=("Segoe UI Emoji", 60),
            bg="#172554",
            fg="white"
        )

        icon.pack(
            pady=(100, 20)
        )

        # Application Title
        title = tk.Label(
            left_frame,
            text="Computer Lab\nManagement System",
            font=("Segoe UI", 28, "bold"),
            bg="#172554",
            fg="white",
            justify="center"
        )

        title.pack()

        # Description
        description = tk.Label(
            left_frame,
            text="Manage computers • Report issues • Track maintenance",
            font=("Segoe UI", 11),
            bg="#172554",
            fg="#CBD5E1"
        )

        description.pack(
            pady=20
        )

        # ====================================================
        # RIGHT SIDE
        # ====================================================

        right_frame = tk.Frame(
            main_frame,
            bg="#F8FAFC"
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        login_title = tk.Label(
            right_frame,
            text="Welcome Back",
            font=("Segoe UI", 26, "bold"),
            bg="#F8FAFC",
            fg="#0F172A"
        )

        login_title.pack(
            pady=(80, 5)
        )

        subtitle = tk.Label(
            right_frame,
            text="Sign in to continue",
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#64748B"
        )

        subtitle.pack(
            pady=(0, 35)
        )

        # ====================================================
        # USERNAME
        # ====================================================

        username_label = tk.Label(
            right_frame,
            text="User ID",
            font=("Segoe UI", 11, "bold"),
            bg="#F8FAFC",
            fg="#334155"
        )

        username_label.pack(
            anchor="w",
            padx=80
        )

        self.username_entry = tk.Entry(
            right_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#0F172A",
            relief="solid",
            bd=1
        )

        self.username_entry.pack(
            fill="x",
            padx=80,
            ipady=10,
            pady=(5, 20)
        )

        # ====================================================
        # PASSWORD
        # ====================================================

        password_label = tk.Label(
            right_frame,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            bg="#F8FAFC",
            fg="#334155"
        )

        password_label.pack(
            anchor="w",
            padx=80
        )

        self.password_entry = tk.Entry(
            right_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#0F172A",
            show="●",
            relief="solid",
            bd=1
        )

        self.password_entry.pack(
            fill="x",
            padx=80,
            ipady=10,
            pady=(5, 10)
        )

        # ====================================================
        # LOGIN BUTTON
        # ====================================================

        login_button = tk.Button(
            right_frame,
            text="LOGIN",
            font=("Segoe UI", 12, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login_user
        )

        login_button.pack(
            fill="x",
            padx=80,
            ipady=10,
            pady=(25, 15)
        )

        # ====================================================
        # ENTER KEY
        # ====================================================

        self.root.bind(
            "<Return>",
            lambda event: self.login_user()
        )

        # Focus username field
        self.username_entry.focus()

    # ========================================================
    # LOGIN FUNCTION
    # ========================================================

    def login_user(self):

        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()

        # ----------------------------------------------------
        # Empty Fields
        # ----------------------------------------------------

        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter User ID and Password."
            )

            return

        # ----------------------------------------------------
        # Authenticate Using auth.py
        # ----------------------------------------------------

        try:

            user = login(
                username,
                password
            )

        except Exception as error:

            messagebox.showerror(
                "Login Error",
                f"An error occurred during login:\n\n{error}"
            )

            return

        # ----------------------------------------------------
        # Login Failed
        # ----------------------------------------------------

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid User ID or Password."
            )

            self.password_entry.delete(
                0,
                tk.END
            )

            return

        # ----------------------------------------------------
        # Login Successful
        # ----------------------------------------------------

        self.show_login_success(user)

    # ========================================================
    # LOGIN SUCCESS
    # ========================================================

    def show_login_success(self, user):

        role = user["role"]
        name = user["full_name"]

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {name}!\n\n"
            f"Role: {role.title()}"
        )

        # ----------------------------------------------------
        # Temporary Dashboard Routing
        # ----------------------------------------------------
        # We will replace this with the actual GUI dashboards.

        if role == "student":

            student_dashboard(user)

        elif role == "faculty":

            self.show_dashboard_message(
                "Faculty Dashboard",
                name
            )

        elif role == "technician":

            self.show_dashboard_message(
                "Technician Dashboard",
                name
            )

        elif role == "admin":

            self.show_dashboard_message(
                "Admin Dashboard",
                name
            )

    # ========================================================
    # TEMPORARY DASHBOARD
    # ========================================================

    def show_dashboard_message(self, dashboard_name, name):

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(
            self.root,
            bg="#F8FAFC"
        )

        frame.pack(
            fill="both",
            expand=True
        )

        title = tk.Label(
            frame,
            text=f"Welcome, {name}",
            font=("Segoe UI", 28, "bold"),
            bg="#F8FAFC",
            fg="#0F172A"
        )

        title.pack(
            pady=(180, 10)
        )

        dashboard_label = tk.Label(
            frame,
            text=dashboard_name,
            font=("Segoe UI", 18),
            bg="#F8FAFC",
            fg="#2563EB"
        )

        dashboard_label.pack()

        info = tk.Label(
            frame,
            text="Dashboard UI will be built next.",
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#64748B"
        )

        info.pack(
            pady=10
        )

        logout_button = tk.Button(
            frame,
            text="LOGOUT",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.create_login_ui
        )

        logout_button.pack(
            pady=20,
            ipadx=30,
            ipady=8
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ComputerLabSystem(root)

    root.mainloop()