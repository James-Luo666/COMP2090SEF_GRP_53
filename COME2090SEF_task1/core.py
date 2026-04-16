import json
import os
#Base class
#all useer under class have 3 elements：ID;name;password
class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.__password = password  

    def verify_password(self, input_password):
        return self.__password == input_password 
    #This is Encapsulation, only can use "verify_password to check"

    def get_role(self):
        pass
#Sub class
#They inheritance the basic elements from User
class Student(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)  
        self.courses_enrolled = []  
        self.leave_requests = {}  
#Use the polymorphism, in one same way, if you are student you will get student, if you are teacher you will get teacher
    def get_role(self):
        return "Student"

class Teacher(User):

    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)  
        self.courses_taught = []  

    def get_role(self):
        return "Teacher"
#A moudle to take course information, have 4 elements: course id;course name;teacher id;dictionary of attendance record
class Course:

    def __init__(self, course_id, course_name, teacher_id):
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_id = teacher_id

        self.attendance_records = {}

# Controller Class

class AttendanceSystemCore:
    #when the system start, will run these codes, prepare two empty dictionary"self.users"and"self.courses"
    #then find JSON file which load data
    def __init__(self):
        self.users = {}    
        self.courses = {}  
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(current_dir, "system_data.json")
        
        self.load_data()   
    #translate the OOP(student;teacher;course) to the dictionary
    #write inside the json file
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
    #transfer the normal date inside the JSON file to Student; teacher; course
    #when find the file broke or not here, use "init_teat_data" to create new JSON file
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

    #test data
    #we create some teacher student and course for test
    def init_test_data(self):
        self.users["T001"] = Teacher("T001", "Dr. Jimmy", "admin123")
        self.users["T002"] = Teacher("T002", "Dr. Patrick", "admin123")
        self.users["T003"] = Teacher("T003", "Dr. JamesLuo", "admin123")
        
        students_info = [
            ("S001", "Wyatt", "hkmu1234"),
            ("S002", "Oscarctho", "hkmu1234"),
            ("S003", "James", "hkmu1234"), 
            ("S004", "David", "hkmu1234"),
            ("S005", "Eve", "hkmu1234")      
        ]
        for sid, name, pwd in students_info:
            student = Student(sid, name, pwd)
            student.courses_enrolled = ["COMP2090SEF", "IT1030SEF","STAT1510SEF"]
            self.users[sid] = student
            
        self.courses["COMP2090SEF"] = Course("COMP2090SEF", "Data Structures,Algorithms And Problem Solving", "T001")
        self.courses["IT1030SEF"] = Course("IT1030SEF", "Introduction To Internet Application Development", "T002")
        self.courses["STAT1510SEF"] = Course("STAT1510SEF", "Probability And Distributions", "T003")

        self.courses["COMP2090SEF"].attendance_records["S001"] = ["Present", "Present", "Present", "Present"]
        
        self.courses["COMP2090SEF"].attendance_records["S002"] = ["Present", "Present", "Present", "Absent"]
        
        self.courses["COMP2090SEF"].attendance_records["S003"] = ["Present", "Absent", "Present", "Absent"]
        
        self.courses["COMP2090SEF"].attendance_records["S004"] = ["Present", "Present", "Leave (Approved)", "Present"]
        
        self.courses["COMP2090SEF"].attendance_records["S005"] = ["Present", "Present", "Present", "Leave (Pending)"]
        self.users["S005"].leave_requests["COMP2090SEF"] = "Fever and cough"

        self.save_data()

#student function
#function1: login
#use ID to find people from dictionary
    def login(self, user_id, password):
        if user_id in self.users: 
            user_obj = self.users[user_id]
            #when find, check the password
            if user_obj.verify_password(password): 
                return user_obj
        return None
#function2: take attendance
#check the coures, then check the student in this course or not
#if yes, write the "present"
#if never check in before, will create list first
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
#function3: calculate the attendance rate
#get all the attendance history from the list
    def get_student_attendance_rate(self, student_id, course_id):
        if course_id not in self.courses:
            return 0.0, False
            
        records_list = self.courses[course_id].attendance_records.get(student_id, [])
        if not records_list:
            return 0.0, False 
#calculate the "present"and"leave"
#calculate the rate        
        total_classes = len(records_list)
        attended = records_list.count("Present") + records_list.count("Leave (Approved)")
        rate = (attended / total_classes) * 100
#judge with the passing standards       
        is_failed = rate < 80.0 
        return rate, is_failed
#function4: ask for leave
#add the status and keep the leave reason
    def student_apply_leave(self, student_id, course_id, reason):
        student = self.users.get(student_id)
        if not student:
            return False, "Student not found."
            
        if course_id not in student.courses_enrolled:
            return False, "You are not enrolled in this course."
            
        student.leave_requests[course_id] = reason
        if course_id in self.courses:
            if student_id not in self.courses[course_id].attendance_records:
                self.courses[course_id].attendance_records[student_id] = []
            self.courses[course_id].attendance_records[student_id].append("Leave (Pending)")
            
        self.save_data()
        return True, "Leave application submitted."
#transfer the list to the string，easy for studentGUI to print
    def get_student_attendance_record(self, student_id):
        student = self.users.get(student_id)
        if not student:
            return None
            
        records = {}
        for course_id in student.courses_enrolled:
            if course_id in self.courses:
                course = self.courses[course_id]
                rec_list = course.attendance_records.get(student_id, [])
                status_str = ", ".join(rec_list) if rec_list else "Not Recorded"
                records[course_id] = {
                    "course_name": course.course_name,
                    "status": status_str
                }
        return records

#teacher function
#funtion1: create course
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
#function2: change attendance
#when teacher want to change some student's attendance status,they can use this
    def edit_attendance(self, teacher_id, course_id, student_id, new_status):
        course = self.courses.get(course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Course not found or permission denied."
            
        if student_id not in course.attendance_records:
            course.attendance_records[student_id] = []
        course.attendance_records[student_id].append(new_status)
        
        self.save_data()
        return True, f"Attendance updated to {new_status}."
#function3: approve Leave
#find all the leave(pending),if teacher agree, change to approved, disageree change to rejected
#delate the leave reason
    def approve_leave_application(self, teacher_id, course_id, student_id, is_approved):
        course = self.courses.get(course_id)
        student = self.users.get(student_id)
        
        if not course or course.teacher_id != teacher_id or not student:
            return False, "Invalid request."
            
        if course_id in student.leave_requests:
            records = course.attendance_records.get(student_id, [])
            for i in range(len(records)-1, -1, -1):
                if records[i] == "Leave (Pending)":
                    records[i] = "Leave (Approved)" if is_approved else "Absent (Leave Rejected)"
                    break

            del student.leave_requests[course_id]
            self.save_data()
            return True, "Leave application processed."
        return False, "No leave request found."
#function4: export the report
#change the data to the sentence, write to one txt file
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
#funtion5: attendance rate
#this is the rank for class attendance
#calculate the rate and bring all the rate inside the list    
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
#use bubble sort
#compare the 2 people's rate, if front is less than the back, change their list
        n = len(stats_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if stats_list[j][2] < stats_list[j+1][2]:
                    stats_list[j], stats_list[j+1] = stats_list[j+1], stats_list[j]
        return stats_list
#find all student in one class for teacher    
    def get_enrolled_students(self, course_id):
        enrolled = []
        for uid, user_obj in self.users.items():
            if user_obj.get_role() == "Student" and course_id in user_obj.courses_enrolled:
                enrolled.append(user_obj)
        return enrolled
#find all leave(pending) for teacher to agree or disagree
    def get_all_pending_leaves(self, teacher_id):
        pending_leaves = []
        teacher = self.users.get(teacher_id)
        if not teacher: return pending_leaves
        
        for cid in teacher.courses_taught:
            for uid, user_obj in self.users.items():
                if user_obj.get_role() == "Student" and cid in user_obj.leave_requests:
                    pending_leaves.append({
                        "student_id": uid,
                        "student_name": user_obj.name,
                        "course_id": cid,
                        "reason": user_obj.leave_requests[cid]
                    })
        return pending_leaves


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
#use for test the code   
if __name__ == "__main__":
    core = AttendanceSystemCore()
    print("success!!!you are so smart")