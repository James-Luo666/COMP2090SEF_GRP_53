import tkinter as tk
from tkinter import messagebox, simpledialog
from core import AttendanceSystemCore

class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System - Student")
        self.root.geometry("650x450")
        
        self.system = AttendanceSystemCore()
        self.current_user = None

        self.login_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)

        self.build_login_screen()
        self.build_main_screen()

        self.login_frame.pack(fill="both", expand=True)

    def build_login_screen(self):
        tk.Label(self.login_frame, text="Student Login", font=("Arial", 20, "bold")).pack(pady=40)

        tk.Label(self.login_frame, text="Student ID:").pack()
        self.entry_id = tk.Entry(self.login_frame)
        self.entry_id.pack(pady=5)
        self.entry_id.insert(0, "S001") 

        tk.Label(self.login_frame, text="Password:").pack()
        self.entry_pwd = tk.Entry(self.login_frame, show="*")
        self.entry_pwd.pack(pady=5)
        self.entry_pwd.insert(0, "14132449") 

        tk.Button(self.login_frame, text="Login", command=self.handle_login, width=15, bg="lightblue").pack(pady=20)

    def handle_login(self):
        t_id = self.entry_id.get()
        pwd = self.entry_pwd.get()
        
        user_obj = self.system.login(t_id, pwd)
        
        if user_obj and user_obj.get_role() == "Student":
            self.current_user = user_obj
            messagebox.showinfo("Success", f"Welcome, {user_obj.name}!")
            self.login_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
            self.update_display(f"Welcome to the system, {user_obj.name}.\nPlease select an action from the left menu.")
        else:
            messagebox.showerror("Error", "Invalid ID/Password or insufficient permissions.")

    def build_main_screen(self):
        # Left menu
        menu_frame = tk.Frame(self.main_frame, width=200, bg="#f0f0f0")
        menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right menu
        display_frame = tk.Frame(self.main_frame)
        display_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.display_text = tk.Text(display_frame, state="disabled", font=("Courier", 12))
        self.display_text.pack(fill="both", expand=True)

        # Left buttons
        buttons = [
            ("1. Course Attendance", self.action_attend),
            ("2. Attendence Record", self.action_record),
            ("3. Attendance rate", self.action_rate),
            ("4. Leave Application Approval", self.action_submit_leave),
            ("0. Logout", self.handle_logout)
        ]

        tk.Label(menu_frame, text="Menu", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        for text, cmd in buttons:
            tk.Button(menu_frame, text=text, command=cmd, width=20, anchor="w").pack(pady=5)

    
    def update_display(self, text_content):
        self.display_text.config(state="normal")
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, text_content)
        self.display_text.config(state="disabled")

    def action_attend(self):
        c_id = simpledialog.askstring("Input", "Enter Course ID you would like to check in:")
        if c_id:
            success, msg = self.system.student_check_in(self.current_user.user_id,c_id)
            messagebox.showinfo("Result", msg)

    def action_record(self):
        records = self.system.get_student_attendance_record(self.current_user.user_id)
        display_str = f"[Attendance record of {self.current_user.user_id} ]\n\n"
        if not records:
            display_str += "No records found.\n"
        else:
            for r in records:
                course_name = r.get("course_name","Unknown")
                status = r.get("status", "Not Recorded")
                c_id = r.get("course_id", "N/A")
                display_str += f"- [{c_id}] {course_name} | Status: {status}\n"
        
        self.update_display(display_str)

    def action_rate(self):
        c_id = simpledialog.askstring("Input", "Enter Course ID you would like to check:")
        if c_id:
            success, msg = self.system.get_student_attendance_rate(self.current_user.user_id, c_id)
            messagebox.showinfo("Result", msg) 

    def action_submit_leave(self):
        c_id = simpledialog.askstring("Input", "Enter Course ID you would like to take leave :")
        reason_text = simpledialog.askstring("Input", "Enter the reason why you would like to take leave ::")
        if c_id and reason_text:
            success, msg = self.system.student_apply_leave(self.current_user.user_id, c_id, reason_text)
            messagebox.showinfo("Result", msg)

    def handle_logout(self):
        self.current_user = None
        self.main_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGUI(root)
    root.mainloop()
 
    

    