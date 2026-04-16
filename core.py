import json
import os

class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.__password = password  

    def verify_password(self, input_password):
        return self.__password == input_password

    def get_role(self):
        pass

class Student(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)  
        self.courses_enrolled = []  
        self.leave_requests = {}  

    def get_role(self):
        return "Student"

class Teacher(User):

    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)  
        self.courses_taught = []  

    def get_role(self):
        return "Teacher"

class Course:

    def __init__(self, course_id, course_name, teacher_id):
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_id = teacher_id

        self.attendance_records = {}

# Controller Class

class AttendanceSystemCore:
    def __init__(self):
        self.users = {}    
        self.courses = {}  
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(current_dir, "system_data.json")
        
        self.load_data()   

    def save_data(self):
        data_to_save = {
            "users": {},
            "courses": {}
        }

        for uid, user_obj in self.users.items():
            if user_obj.get_role() == "Student":
                data_to_save["users"][uid] = {
                    "role": "Student",
                    "name": user_obj.name,
                    "password": user_obj._User__password, 
                    "courses_enrolled": user_obj.courses_enrolled,
                    "leave_requests": user_obj.leave_requests
                }
            elif user_obj.get_role() == "Teacher":
                data_to_save["users"][uid] = {
                    "role": "Teacher",
                    "name": user_obj.name,
                    "password": user_obj._User__password,
                    "courses_taught": user_obj.courses_taught
                }

        for cid, course_obj in self.courses.items():
            data_to_save["courses"][cid] = {
                "course_name": course_obj.course_name,
                "teacher_id": course_obj.teacher_id,
                "attendance_records": course_obj.attendance_records
            }

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if not os.path.exists(self.data_file):
            self.init_test_data()
            return

        with open(self.data_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                self.init_test_data() 
                return 

        for uid, user_data in data.get("users", {}).items():
            if user_data["role"] == "Student":
                student = Student(uid, user_data["name"], user_data["password"])
                student.courses_enrolled = user_data.get("courses_enrolled", [])
                student.leave_requests = user_data.get("leave_requests", {})
                self.users[uid] = student
            elif user_data["role"] == "Teacher":
                teacher = Teacher(uid, user_data["name"], user_data["password"])
                teacher.courses_taught = user_data.get("courses_taught", [])
                self.users[uid] = teacher

        for cid, course_data in data.get("courses", {}).items():
            course = Course(cid, course_data["course_name"], course_data["teacher_id"])
            course.attendance_records = course_data.get("attendance_records", {})
            self.courses[cid] = course

    def init_test_data(self):

        test_teacher = Teacher("T001", "Dr.James", "admin123")
        self.users["T001"] = test_teacher
        
        test_student = Student("S001", "JamesLuo", "14132449")
        self.users["S001"] = test_student
        
        self.save_data()

#student function
    def login(self, user_id, password):
        if user_id in self.users: 
            user_obj = self.users[user_id]
            if user_obj.verify_password(password): 
                return user_obj
        return None

    def student_check_in(self, student_id, course_id):
        if course_id not in self.courses:
            return False, "Course not found."
        course = self.courses[course_id]
        student = self.users.get(student_id)
        if not student or course_id not in student.courses_enrolled:
            return False, "You are not enrolled in this course."
            
        if student_id not in course.attendance_records:
            course.attendance_records[student_id] = []
        course.attendance_records[student_id].append("Present")
        self.save_data() 
        return True, "Check-in successful!"

    def get_student_attendance_rate(self, student_id, course_id):
        if course_id not in self.courses:
            return 0.0, False
            
        records_list = self.courses[course_id].attendance_records.get(student_id, [])
        if not records_list:
            return 0.0, False 
        
        total_classes = len(records_list)
        attended = records_list.count("Present") + records_list.count("Leave (Approved)")
        rate = (attended / total_classes) * 100
        
        is_failed = rate < 80.0 
        return rate, is_failed

    def get_class_attendance_stats_sorted(self, teacher_id, course_id):
        course = self.courses.get(course_id)
        if not course or course.teacher_id != teacher_id:
            return None

        stats_list = []
        for sid, records in course.attendance_records.items():
            s_name = self.users[sid].name if sid in self.users else "Unknown"
            if not records:
                rate = 0.0
            else:
                attended = records.count("Present") + records.count("Leave (Approved)")
                rate = (attended / len(records)) * 100
            stats_list.append([sid, s_name, rate])

        n = len(stats_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if stats_list[j][2] < stats_list[j+1][2]:
                    stats_list[j], stats_list[j+1] = stats_list[j+1], stats_list[j]
        return stats_list
    
    def student_apply_leave(self, student_id, course_id, reason):
        student = self.users.get(student_id)
        if not student:
            return False, "Student not found."
            
        if course_id not in student.courses_enrolled:
            return False, "You are not enrolled in this course."
            
        student.leave_requests[course_id] = reason
        if course_id in self.courses:
            self.courses[course_id].attendance_records[student_id] = "Leave (Pending)"
            
        self.save_data()
        return True, "Leave application submitted."
    
    def get_student_attendance_record(self, student_id):
        student = self.users.get(student_id)
        if not student:
            return None
            
        records = []
        for course_id in student.courses_enrolled:
            if course_id in self.courses:
                course = self.courses[course_id]
                status = course.attendance_records.get(student_id, "Not Recorded")
                records.append({
                    "course_id": course_id,
                    "course_name": course.course_name,
                    "status": status
                })
        return records

    def get_student_attendance_rate(self, student_id, course_id):

        if course_id not in self.courses:
            return None
        status = self.courses[course_id].attendance_records.get(student_id, "Not Recorded")
        return status

#teacher function
    def create_course(self, teacher_id, course_id, course_name):

        if course_id in self.courses:
            return False, "Course ID already exists."
        
        teacher = self.users.get(teacher_id)
        if not teacher or teacher.get_role() != "Teacher":
            return False, "Invalid teacher ID."
            
        new_course = Course(course_id, course_name, teacher_id)
        self.courses[course_id] = new_course
        teacher.courses_taught.append(course_id)
        self.save_data()
        return True, "Course created successfully."

    def get_teacher_courses(self, teacher_id):
        teacher = self.users.get(teacher_id)
        if not teacher:
            return []
        
        course_list = []
        for cid in teacher.courses_taught:
            if cid in self.courses:
                course_list.append(self.courses[cid])
        return course_list

    def edit_attendance(self, teacher_id, course_id, student_id, new_status):
        course = self.courses.get(course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Course not found or permission denied."
            
        course.attendance_records[student_id] = new_status
        self.save_data()
        return True, f"Attendance updated to {new_status}."

    def approve_leave_application(self, teacher_id, course_id, student_id, is_approved):
        course = self.courses.get(course_id)
        student = self.users.get(student_id)
        
        if not course or course.teacher_id != teacher_id or not student:
            return False, "Invalid request."
            
        if course_id in student.leave_requests:
            if is_approved:
                course.attendance_records[student_id] = "Leave (Approved)"
            else:
                course.attendance_records[student_id] = "Absent (Leave Rejected)"

            del student.leave_requests[course_id]
            self.save_data()
            return True, "Leave application processed."
        return False, "No leave request found."

    def export_attendance_report(self, teacher_id, course_id):
        course = self.courses.get(course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Permission denied."
            
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f"Report_{course_id}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Attendance Report for Course: {course.course_name} ({course_id})\n")
            f.write("-" * 40 + "\n")
            for sid, status in course.attendance_records.items():
                student_name = self.users[sid].name if sid in self.users else "Unknown"
                f.write(f"Student ID: {sid} | Name: {student_name} | Status: {status}\n")
                
        return True, f"Report exported to {file_path}"

    def get_class_attendance_stats_sorted(self, teacher_id, course_id):
        course = self.courses.get(course_id)
        if not course or course.teacher_id != teacher_id:
            return None

        stats_list = []
        for sid, status in course.attendance_records.items():
            s_name = self.users[sid].name if sid in self.users else "Unknown"
            stats_list.append([sid, s_name, status])
            

        def get_status_weight(status_str):
            if "Present" in status_str: return 3
            if "Leave" in status_str: return 2
            if "Absent" in status_str: return 1
            return 0 

        n = len(stats_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                weight_j = get_status_weight(stats_list[j][2])
                weight_j_next = get_status_weight(stats_list[j+1][2])
                
                if weight_j < weight_j_next:
                    stats_list[j], stats_list[j+1] = stats_list[j+1], stats_list[j]
                    
        return stats_list
    
if __name__ == "__main__":
    core = AttendanceSystemCore()
    print("success!!!you are so smart")