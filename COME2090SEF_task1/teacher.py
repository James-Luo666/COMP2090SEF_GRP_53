#import the core logic
from core import AttendanceSystemCore

def teacher_main():

    system = AttendanceSystemCore()

    print("="*50)
    print("   Attendance Management System (Teacher Terminal)   ")
    print("="*50)
    
#User Login
#user enter the password then check from"system.login"
#default test account: T001 / admin123
    teacher_id = input("Enter Teacher ID (e.g., T001): ")
    password = input("Enter Password (e.g., admin123): ")
    
    user_obj = system.login(teacher_id, password)
#check the user is teacher not a student     
    if not user_obj or user_obj.get_role() != "Teacher":
        print("[Error] Login failed. Invalid ID/Password or insufficient permissions.")
        return

    print(f"\nLogin successful! Welcome, {user_obj.name}")

#Teacher menu
##use infinite loop to keep teacher menu until user choose 
    while True:
        print("\n" + "-"*18 + " Teacher Menu " + "-"*18)
        print("1. Course Management [Feature 2.3]")
        print("2. Record / Edit Attendance [Feature 2.4 & 2.5]")
        print("3. Attendance Statistics & Status [Feature 2.6 & 2.7]")
        print("4. Leave Application Approval [Feature 2.8]")
        print("5. Export Attendance Report [Feature 2.9]")
        print("0. Exit System [Feature 2.10]")
        
        choice = input("Select an option (0-5): ")
        
        if choice == '1':
            #course Management
            #teacher can create new course
            courses = system.get_teacher_courses(teacher_id)
            print("\n[Your Courses]:")
            if not courses:
                print("You are not teaching any courses currently.")
            for c in courses:
                print(f"- Course ID: {c.course_id} | Course Name: {c.course_name}")
            
            do_create = input("\nWould you like to create a new course? (y/n): ")
            if do_create.lower() == 'y':
                new_c_id = input("Enter new Course ID (e.g., C001): ")
                new_c_name = input("Enter new Course Name (e.g., Python OOP): ")
                success, msg = system.create_course(teacher_id, new_c_id, new_c_name)
                print(f"[System Message] {msg}")

        elif choice == '2':
            # Record & Edit Attendance
            #teacher can change the attendance status
            c_id = input("Enter Course ID (e.g., C001): ")
            s_id = input("Enter Student ID (e.g., S001): ")
            status = input("Enter Attendance Status (Present/Absent/Leave): ")
            success, msg = system.edit_attendance(teacher_id, c_id, s_id, status)
            print(f"[System Message] {msg}")

        elif choice == '3':
            # Statistics of class attendance rate & Check status
            #use :<15 and :.1f}% to make page clear
            c_id = input("Enter Course ID for statistics: ")
            stats = system.get_class_attendance_stats_sorted(teacher_id, c_id)
            
            if stats is None:
                print("[Error] Cannot retrieve stats. Check Course ID or your permissions.")
            else:
                print(f"\n[Attendance Stats for {c_id} (Sorted by Performance)]:")
                print(f"{'Student ID':<15} | {'Name':<15} | {'Status'}")
                print("-" * 50)
                for record in stats:
                    print(f"{record[0]:<15} | {record[1]:<15} | {record[2]:.1f}%")

        elif choice == '4':
            # Leave Application Approval
            #teacher agree or disagree
            c_id = input("Enter Course ID: ")
            s_id = input("Enter Student ID requesting leave: ")
            approve_str = input("Approve this leave application? (y/n): ")
            is_approved = True if approve_str.lower() == 'y' else False
            success, msg = system.approve_leave_application(teacher_id, c_id, s_id, is_approved)
            print(f"[System Message] {msg}")

        elif choice == '5':
            # Export Attendance Report
            c_id = input("Enter Course ID to export report: ")
            success, msg = system.export_attendance_report(teacher_id, c_id)
            print(f"[System Message] {msg}")

        elif choice == '0':
            # Exit System
            print("Exiting system. Goodbye!")
            break
            
        else:
            print("[Error] Invalid input. Please select a number between 0 and 5.")
#test code
if __name__ == "__main__":
    teacher_main()