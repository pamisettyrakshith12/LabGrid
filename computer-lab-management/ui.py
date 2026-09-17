import tkinter as tk
from tkinter import messagebox


# -----------------------------
# Main Application
# -----------------------------
class ComputerLabSystem:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Computer Lab Management System")
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)
        self.root.configure(bg="#0F172A")

        self.create_login_ui()

    # -----------------------------
    # Login UI
    # -----------------------------
    def create_login_ui(self):

        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_frame = tk.Frame(
            self.root,
            bg="#0F172A"
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # Left Section
        # -------------------------
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

        # System icon
        icon = tk.Label(
            left_frame,
            text="💻",
            font=("Segoe UI Emoji", 60),
            bg="#172554",
            fg="white"
        )
        icon.pack(pady=(100, 20))

        # Title
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
        description.pack(pady=20)

        # -------------------------
        # Right Section
        # -------------------------
        right_frame = tk.Frame(
            main_frame,
            bg="#F8FAFC"
        )
        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Login heading
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

        # -------------------------
        # User ID
        # -------------------------
        user_label = tk.Label(
            right_frame,
            text="User ID",
            font=("Segoe UI", 11, "bold"),
            bg="#F8FAFC",
            fg="#334155"
        )
        user_label.pack(
            anchor="w",
            padx=80
        )

        self.user_entry = tk.Entry(
            right_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#0F172A",
            relief="solid",
            bd=1
        )
        self.user_entry.pack(
            fill="x",
            padx=80,
            ipady=10,
            pady=(5, 20)
        )

        # -------------------------
        # Password
        # -------------------------
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

        # -------------------------
        # Login Button
        # -------------------------
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
            command=self.login
        )
        login_button.pack(
            fill="x",
            padx=80,
            ipady=10,
            pady=(25, 15)
        )

        # Bind Enter key
        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

        # Focus user ID
        self.user_entry.focus()

    # -----------------------------
    # Login Function
    # -----------------------------
    def login(self):

        user_id = self.user_entry.get().strip()
        password = self.password_entry.get()

        if not user_id or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter User ID and Password."
            )
            return

        # Temporary login logic
        # Database authentication will be connected next.
        messagebox.showinfo(
            "Login",
            f"Login UI working!\n\nUser ID: {user_id}"
        )


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":

    root = tk.Tk()

    app = ComputerLabSystem(root)

    root.mainloop()