import tkinter as tk
from tkinter import messagebox, simpledialog
from core import AttendanceSystemCore

class TeacherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System - Teacher")
        self.root.geometry("650x450")
        
        self.system = AttendanceSystemCore()
        self.current_user = None

        self.login_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)

        self.build_login_screen()
        self.build_main_screen()

        self.login_frame.pack(fill="both", expand=True)

    def build_login_screen(self):
        tk.Label(self.login_frame, text="Teacher Login", font=("Arial", 20, "bold")).pack(pady=40)

        tk.Label(self.login_frame, text="Teacher ID:").pack()
        self.entry_id = tk.Entry(self.login_frame)
        self.entry_id.pack(pady=5)
        self.entry_id.insert(0, "T001") 

        tk.Label(self.login_frame, text="Password:").pack()
        self.entry_pwd = tk.Entry(self.login_frame, show="*")
        self.entry_pwd.pack(pady=5)
        self.entry_pwd.insert(0, "admin123") 

        tk.Button(self.login_frame, text="Login", command=self.handle_login, width=15, bg="lightblue").pack(pady=20)

    def handle_login(self):
        t_id = self.entry_id.get()
        pwd = self.entry_pwd.get()
        
        user_obj = self.system.login(t_id, pwd)
        
        if user_obj and user_obj.get_role() == "Teacher":
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
            ("1. Course Management", self.action_courses),
            ("2. Record Attendance", self.action_attendance),
            ("3. View Statistics", self.action_statistics),
            ("4. Approve Leave", self.action_approve_leave),
            ("5. Export Report", self.action_export),
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

    def action_courses(self):
        courses = self.system.get_teacher_courses(self.current_user.user_id)
        display_str = "[Your Courses]\n\n"
        if not courses:
            display_str += "No courses found.\n"
        else:
            for c in courses:
                display_str += f"- Course ID: {c.course_id} | Name: {c.course_name}\n"
        
        self.update_display(display_str)
        

        if messagebox.askyesno("Create Course", "Would you like to create a new course?"):
            new_id = simpledialog.askstring("Input", "Enter new Course ID (e.g., C001):")
            new_name = simpledialog.askstring("Input", "Enter Course Name:")
            if new_id and new_name:
                success, msg = self.system.create_course(self.current_user.user_id, new_id, new_name)
                messagebox.showinfo("Result", msg)
                self.action_courses() 

    def action_attendance(self):
        courses = self.system.get_teacher_courses(self.current_user.user_id)
        if not courses:
            messagebox.showinfo("Info", "You do not teach any courses currently.")
            return
            
        if len(courses) == 1:
            c_id = courses[0].course_id
        else:
            course_ids = [c.course_id for c in courses]
            c_id = simpledialog.askstring("Input", f"Your courses: {', '.join(course_ids)}\n\nEnter Course ID:")
            if not c_id or c_id not in course_ids:
                messagebox.showerror("Error", "Invalid Course ID or you don't teach this course.")
                return
                
        students = self.system.get_enrolled_students(c_id)
        if not students:
            messagebox.showinfo("Info", f"No students enrolled in course {c_id}.")
            return
            
        for student in students:
            status = simpledialog.askstring(
                "Roll Call", 
                f"Course: {c_id}\nStudent: {student.name} ({student.user_id})\n\nEnter Status (Present/Absent/Leave):",
                initialvalue="Present" 
            )
            if status:
                self.system.edit_attendance(self.current_user.user_id, c_id, student.user_id, status)
                
        messagebox.showinfo("Result", "Roll call completed for all students in this course!")

    def action_statistics(self):
        courses = self.system.get_teacher_courses(self.current_user.user_id)
        if not courses:
            messagebox.showinfo("Info", "You do not teach any courses.")
            return
            
        if len(courses) == 1:
            c_id = courses[0].course_id
        else:
            course_ids = [c.course_id for c in courses]
            c_id = simpledialog.askstring("Input", f"Your courses: {', '.join(course_ids)}\n\nEnter Course ID:")
            if not c_id or c_id not in course_ids:
                messagebox.showerror("Error", "Invalid Course ID.")
                return

        stats = self.system.get_class_attendance_stats_sorted(self.current_user.user_id, c_id)
        if stats is None:
            messagebox.showerror("Error", "Cannot retrieve stats.")
            return
            
        display_str = f"[Attendance Stats for {c_id} (Sorted)]\n\n"
        display_str += f"{'Student ID':<15} | {'Name':<15} | {'Status'}\n"
        display_str += "-" * 50 + "\n"
        for record in stats:
            display_str += f"{record[0]:<15} | {record[1]:<15} | {record[2]:.1f}%\n"
        
        self.update_display(display_str)

    def action_export(self):
        courses = self.system.get_teacher_courses(self.current_user.user_id)
        if not courses:
            messagebox.showinfo("Info", "You do not teach any courses.")
            return
            
        if len(courses) == 1:
            c_id = courses[0].course_id
        else:
            course_ids = [c.course_id for c in courses]
            c_id = simpledialog.askstring("Input", f"Your courses: {', '.join(course_ids)}\n\nEnter Course ID:")
            if not c_id or c_id not in course_ids:
                messagebox.showerror("Error", "Invalid Course ID.")
                return

        success, msg = self.system.export_attendance_report(self.current_user.user_id, c_id)
        messagebox.showinfo("Result", msg)

    def action_approve_leave(self):
        pending_leaves = self.system.get_all_pending_leaves(self.current_user.user_id)
        
        if not pending_leaves:
            messagebox.showinfo("Info", "Great! You have no pending leave applications.")
            return
            
        for req in pending_leaves:
            msg = (f"Student: {req['student_name']} ({req['student_id']})\n"
                   f"Course: {req['course_id']}\n"
                   f"Reason: {req['reason']}\n\n"
                   f"Do you approve this leave?")
            is_approved = messagebox.askyesno("Leave Approval", msg)
            
            self.system.approve_leave_application(self.current_user.user_id, req['course_id'], req['student_id'], is_approved)
            
        messagebox.showinfo("Result", "All pending leave applications have been processed.")

    def handle_logout(self):
        self.current_user = None
        self.main_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TeacherGUI(root)
    root.mainloop()