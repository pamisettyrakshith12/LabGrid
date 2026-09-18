import tkinter as tk
from tkinter import ttk


# ============================================================
# STUDENT DASHBOARD
# ============================================================

class StudentDashboard:

    def __init__(self, root, user):

        self.root = root
        self.user = user

        self.root.title("Student Dashboard - Computer Lab Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#F8FAFC")

        self.create_ui()

    # ========================================================
    # MAIN UI
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self.root,
            bg="#172554",
            width=240
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Label(
            self.sidebar,
            text="💻",
            font=("Segoe UI Emoji", 32),
            bg="#172554",
            fg="white"
        )

        logo.pack(pady=(35, 5))

        system_name = tk.Label(
            self.sidebar,
            text="Computer Lab\nManagement",
            font=("Segoe UI", 15, "bold"),
            bg="#172554",
            fg="white",
            justify="center"
        )

        system_name.pack(pady=(0, 35))

        # Navigation buttons
        self.create_nav_button(
            "🏠  Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "🖥  Computers",
            self.show_computers
        )

        self.create_nav_button(
            "⚠  Report Issue",
            self.show_report_issue
        )

        self.create_nav_button(
            "📋  My Issues",
            self.show_my_issues
        )

        # Spacer
        tk.Frame(
            self.sidebar,
            bg="#172554"
        ).pack(
            fill="both",
            expand=True
        )

        # Logout
        logout_button = tk.Button(
            self.sidebar,
            text="🚪  Logout",
            font=("Segoe UI", 11, "bold"),
            bg="#172554",
            fg="#CBD5E1",
            activebackground="#1E3A8A",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=25,
            command=self.logout
        )

        logout_button.pack(
            fill="x",
            pady=(0, 25),
            ipady=10
        )

        # ----------------------------------------------------
        # Main Content
        # ----------------------------------------------------

        self.content = tk.Frame(
            self.root,
            bg="#F8FAFC"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 11),
            bg="#172554",
            fg="#CBD5E1",
            activebackground="#1E3A8A",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=25,
            command=command
        )

        button.pack(
            fill="x",
            pady=2,
            ipady=10
        )

    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ========================================================
    # PAGE HEADER
    # ========================================================

    def create_header(self, title, subtitle):

        header = tk.Frame(
            self.content,
            bg="#F8FAFC"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 20)
        )

        title_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 25, "bold"),
            bg="#F8FAFC",
            fg="#0F172A"
        )

        title_label.pack(
            anchor="w"
        )

        subtitle_label = tk.Label(
            header,
            text=subtitle,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#64748B"
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 0)
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_content()

        self.create_header(
            f"Welcome, {self.user['full_name']} 👋",
            "Here's your computer lab overview."
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        stats_frame = tk.Frame(
            self.content,
            bg="#F8FAFC"
        )

        stats_frame.pack(
            fill="x",
            padx=35
        )

        self.create_stat_card(
            stats_frame,
            "🏫",
            "Total Labs",
            "7"
        )

        self.create_stat_card(
            stats_frame,
            "🖥",
            "Computers",
            "477"
        )

        self.create_stat_card(
            stats_frame,
            "⚠",
            "My Issues",
            "0"
        )

        # ----------------------------------------------------
        # Profile Section
        # ----------------------------------------------------

        profile_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        profile_frame.pack(
            fill="x",
            padx=35,
            pady=30
        )

        profile_title = tk.Label(
            profile_frame,
            text="👤  My Profile",
            font=("Segoe UI", 17, "bold"),
            bg="white",
            fg="#0F172A"
        )

        profile_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        # Profile information
        self.create_profile_row(
            profile_frame,
            "Full Name",
            self.user["full_name"]
        )

        self.create_profile_row(
            profile_frame,
            "Student ID",
            self.user["username"]
        )

        self.create_profile_row(
            profile_frame,
            "Batch",
            self.user["batch"]
        )

        self.create_profile_row(
            profile_frame,
            "Year",
            self.user["year"]
        )

        self.create_profile_row(
            profile_frame,
            "Section",
            self.user["section_name"]
        )

        self.create_profile_row(
            profile_frame,
            "Roll Number",
            str(self.user["roll"])
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        icon,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=220,
            height=120,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        card.pack_propagate(False)

        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI Emoji", 23),
            bg="white"
        )

        icon_label.pack(
            anchor="w",
            padx=20,
            pady=(15, 0)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#0F172A"
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748B"
        )

        title_label.pack(
            anchor="w",
            padx=20
        )

    # ========================================================
    # PROFILE ROW
    # ========================================================

    def create_profile_row(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=6
        )

        label_widget = tk.Label(
            row,
            text=label,
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748B",
            width=15,
            anchor="w"
        )

        label_widget.pack(
            side="left"
        )

        value_widget = tk.Label(
            row,
            text=value,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#0F172A",
            anchor="w"
        )

        value_widget.pack(
            side="left"
        )

    # ========================================================
    # COMPUTERS
    # ========================================================

    def show_computers(self):

        self.clear_content()

        self.create_header(
            "Computer Labs",
            "View laboratories and computer availability."
        )

        # Search
        search_frame = tk.Frame(
            self.content,
            bg="#F8FAFC"
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 15)
        )

        search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        search_entry.pack(
            side="left",
            ipady=8,
            fill="x",
            expand=True
        )

        search_button = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2"
        )

        search_button.pack(
            side="left",
            padx=(10, 0),
            ipadx=20,
            ipady=7
        )

        # Table
        table_frame = tk.Frame(
            self.content,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )

        columns = (
            "Lab",
            "Building",
            "Floor",
            "Capacity",
            "Status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=140
            )

        labs = [
            ("PG Lab", "AB3", "2", "68", "Operational"),
            ("CP Lab 1", "AB3", "3", "65", "Operational"),
            ("CP Lab 2", "AB3", "3", "67", "Operational"),
            ("Hardware Lab", "AB3", "2", "70", "Operational"),
            ("IT Lab 1", "AB2", "0", "70", "Operational"),
            ("IT Lab 2", "AB2", "0", "69", "Operational"),
            ("IT Lab 3", "AB2", "1", "68", "Operational")
        ]

        for lab in labs:
            tree.insert(
                "",
                "end",
                values=lab
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ========================================================
    # REPORT ISSUE
    # ========================================================

    def show_report_issue(self):

        self.clear_content()

        self.create_header(
            "Report an Issue",
            "Report a problem with a laboratory computer."
        )

        form = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        form.pack(
            fill="x",
            padx=35
        )

        # Computer ID
        tk.Label(
            form,
            text="Computer ID",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        computer_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        computer_entry.pack(
            fill="x",
            padx=30,
            ipady=8
        )

        # Issue type
        tk.Label(
            form,
            text="Issue Type",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        issue_type = ttk.Combobox(
            form,
            values=[
                "Hardware",
                "Software",
                "Network",
                "Operating System",
                "Other"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )

        issue_type.pack(
            fill="x",
            padx=30
        )

        # Priority
        tk.Label(
            form,
            text="Priority",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        priority = ttk.Combobox(
            form,
            values=[
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )

        priority.pack(
            fill="x",
            padx=30
        )

        # Description
        tk.Label(
            form,
            text="Description",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        description = tk.Text(
            form,
            height=6,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        description.pack(
            fill="x",
            padx=30
        )

        # Submit
        submit_button = tk.Button(
            form,
            text="SUBMIT ISSUE",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2"
        )

        submit_button.pack(
            anchor="e",
            padx=30,
            pady=25,
            ipadx=20,
            ipady=8
        )

    # ========================================================
    # MY ISSUES
    # ========================================================

    def show_my_issues(self):

        self.clear_content()

        self.create_header(
            "My Issues",
            "Track the issues you have reported."
        )

        table_frame = tk.Frame(
            self.content,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )

        columns = (
            "Issue ID",
            "Computer",
            "Issue Type",
            "Priority",
            "Status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=150
            )

        # No dummy issues
        # Real issues will be loaded from SQLite next.

        tree.pack(
            fill="both",
            expand=True
        )

        empty_label = tk.Label(
            table_frame,
            text="No issues reported yet.",
            font=("Segoe UI", 12),
            bg="white",
            fg="#64748B"
        )

        empty_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        from tkinter import messagebox

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if result:

            self.create_login_screen()

    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def create_login_screen(self):

        # This will be connected to ui.py properly.
        self.root.destroy()


# ============================================================
# FUNCTION USED BY auth.py
# ============================================================

def student_dashboard(user):

    root = tk.Tk()

    StudentDashboard(
        root,
        user
    )

    root.mainloop()