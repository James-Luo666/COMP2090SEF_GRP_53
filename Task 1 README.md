# COMP2090SEF_GRP_53
The group work for HKMU COMP2090SEF[Group53]

Project name：student attendance management system

Developer：LUO Dongfan 罗栋藩；LAI WingYat 黎穎㇐；CHAN Tsz Him 陳梓謙

Development Background：

Hope that this system can help schools manage attendance more conveniently and solve the problems of traditional attendance management.

Core Objective：

Developing a lightweight attendance system based on Python OOP, covering student-side check-in and leave application functions and teacher-side statistics functions

File Structure：

（1）core.py：Core server, handles storage data + provides interfaces

（2）student.py：Student terminal, including all student functions (login, punching, leave, etc.)

（3）teacher.py：Teacher terminal, including all teacher functions (login, course management, attendance statistics, etc.)

（4）student_GUI.py：Visual interface for students

（5）teacher_GUI.py：Visual interface for teachers

（6）README.md：Project Description Document

Development Status：

--1.0--- Time：2026.3.8 ----Status：Pre-submission
--2.0--- Time：2026.4.17 ---Status：Final-submission

Project Introduction Video: 
https://youtu.be/i6Jv8D5gtms?si=nrToLBCEtLfSe6qZ

How to use：

                                              Step 1: Download the Code from GitHub
Go to our GitHub repository page.
Click the green "Code" button and select "foler" to download (or use git clone if you know how).
Open the folder in VS Code or your computer's Terminal/Command Prompt.

                                              Step 2: Default Test Accounts
When you run the system for the first time, it will automatically create a database (system_data.json) with some default test accounts. You can use these to test the system:

Teacher Account:
Teacher ID: T001
Password: admin123

Student Account:
Student ID: S001 (You can also use S002, S003, etc.)
Password: hkmu1234

                                              Step 3: How to Use the Teacher GUI
Open your terminal and run this command: python teacher_GUI.py
Login: Type T001 and admin123, then click Login.

Course Management (Feature 1): Click this to see the courses you teach. When you first time use it，you need to type COMP2090SEF.
Record Attendance (Feature 2): Click this to do a manual roll call. You can change a specific student's status to "Present", "Absent", or "Leave".
View Statistics (Feature 3): Click this to see the class ranking. The system will calculate the attendance rate and sort students from highest to lowest using the Bubble Sort algorithm.
Approve Leave (Feature 4): Click this to check all pending leave requests from students. You can click "Yes" to approve or "No" to reject them.
Export Report (Feature 5): Click this to save all the attendance data into a .txt file on your computer.

                                              Step 4: How to Use the Student GUI
Open a new terminal window and run this command: python student_GUI.py
Login: Type S001 and hkmu1234, then click Login. (Note: If the password box shows numbers, change it to hkmu1234)

Course Attendance (Feature 1): Click this and type your Course ID (e.g., COMP2090SEF) to check into the class.
Attendance Record (Feature 2): Click this to see your past check-in history and your current status.
Attendance Rate (Feature 3): Click this and type the Course ID. The system will show your attendance percentage. If it is below 80%, it will give you a "FAILED" warning.
Leave Application (Feature 4): Click this if you are sick. Type the Course ID and your reason (e.g., "Fever"), then wait for the teacher to approve it.

                                              Step 5: How to Use the Console (Terminal) Version
If you prefer a text-only interface without the graphical windows, we also built a console version!
For Teachers: Run python teacher.py
For Students: Run python student.py
Just type a number (from 0 to 5) based on the menu on the screen, and press Enter to use the exact same features!

Module Function Description:

【1】Student terminal

1.1 User Login

1.2 Student Menu

1.3 Attend the course

1.4 Check the attendance record

1.5 Check the attendance rate(Determine if failed)

1.6 Leave application

1.7 Exit System

【2】Teacher terminal

2.1 User Login

2.2 Teacher menu

2.3 Course Management

2.4 Record attendance

2.5 Edit Attendance

2.6 Statistics of class attendance rate

2.7 Check student attendance status

2.8 Leave Application Approval

2.9 Export Attendance Report

2.10 Exit System

【3】Core Server

3.1 Data Initialization

3.2 Login verification interface

3.3 Course-related interfaces

3.4 Attendance record interface

3.5 Statistics Interface

3.6 Leave Application Interface
