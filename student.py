from core import AttendanceSystemCore

def student_main():
    
    system = AttendanceSystemCore()

    print("="*50)
    print("   Attendance Management System (Student Terminal)   ")
    print("="*50)

# student User Login
# default test account: S001 / 14132449
    student_id = input("Enter Student ID (e.g., S001): ")
    password = input("Enter Password (e.g., 14132449): ")
    
    user_obj = system.login(student_id, password)
    
    if not user_obj or user_obj.get_role() != "Teacher":
        print("[Error] Login failed. Invalid ID/Password or insufficient permissions.")
        return
    
    print(f"\nLogin successful! Welcome, {user_obj.name}")

# student menu 
    while True:
        print("\n" + "-"*18 + " Student Menu " + "-"*18)
        print("1. Course Attendance [Feature 1.3]")
        print("2. Attendence Record[Feature 1.4 ]")
        print("3. Attendance rate [Feature 1.5]")
        print("4. Leave Application Approval [Feature 1.6]")
        print("0. Exit System [Feature 1.7]")
        
        choice = input("Select an option (0-4): ")

        if choice == '1':

            #Course Attendance
            c_id = input("Enter Course ID you would like to check in:")
            success, msg = system.student_check_in(student_id, c_id)
            print(f"[System Message] {msg}")

        if choice == '2':
            records = system.get_student_attendance_record(student_id)

            if not records :
                print("[Error] Cannot retrieve record. You have no current attendance record in this semster.")
            else:
                print(f"\n[Attendance record of {student_id} ]:")
                for r in records.values():
                    print(f"- Course name: {r["course_name"]} | Status: {r["status"]}")

        if choice == '3':
            c_id = input("Enter Course ID you would like to check:")
            att_rate = system.get_student_attendance_rate(student_id, c_id)

            if att_rate is None:
                print("[Error]You are not enrolled in this course.")
            else:
                print (att_rate)

        if choice == '4':
            c_id = input("Enter Course ID you would like to take leave :")
            reason_text = input("Enter the reason why you would like to take leave :")
            success, msg = system.student_apply_leave(student_id, c_id, reason_text)
            print(f"[System Message] {msg}")

        elif choice == '0':
            # Exit System
            print("Exiting system. Goodbye!")
            break

        else:
            print("[Error] Invalid input. Please select a number between 0 and 5.")




if __name__ == "__main__":
    student_main()