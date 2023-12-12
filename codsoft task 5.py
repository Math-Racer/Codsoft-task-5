# Importing tkinter and sqlite3 modules
import tkinter as tk
import sqlite3 as sql

# Creating a database connection and a cursor object
conn = sql.connect("attendance.db")
cur = conn.cursor()

# Creating a table for storing student details
cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, roll_no INTEGER UNIQUE)")

# Creating a table for storing attendance records
cur.execute("CREATE TABLE IF NOT EXISTS attendance (date TEXT, roll_no INTEGER, status TEXT, FOREIGN KEY(roll_no) REFERENCES students(roll_no))")

# Committing the changes to the database
conn.commit()

# Creating a root window
root = tk.Tk()
root.title("University Attendance System")

# Creating a frame for adding new students
add_frame = tk.Frame(root)
add_frame.pack()

# Creating labels and entries for student name and roll number
name_label = tk.Label(add_frame, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

roll_label = tk.Label(add_frame, text="Roll No:")
roll_label.grid(row=1, column=0, padx=10, pady=10)
roll_entry = tk.Entry(add_frame)
roll_entry.grid(row=1, column=1, padx=10, pady=10)

# Creating a function to add a new student to the database
def add_student():
    # Getting the name and roll number from the entries
    name = name_entry.get()
    roll_no = roll_no_entry.get()

    # Checking if the name and roll number are not empty
    if name and roll_no:
        # Trying to insert the student details into the database
        try:
            cur.execute("INSERT INTO students (name, roll_no) VALUES (?, ?)", (name, roll_no))
            conn.commit()
            # Showing a success message
            tk.messagebox.showinfo("Success", "Student added successfully")
        except sql.IntegrityError:
            # Showing an error message if the roll number already exists
            tk.messagebox.showerror("Error", "Roll number already exists")
    else:
        # Showing an error message if the name or roll number is empty
        tk.messagebox.showerror("Error", "Name or roll number cannot be empty")

# Creating a button to add a new student
add_button = tk.Button(add_frame, text="Add Student", command=add_student)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Creating a frame for managing attendance
att_frame = tk.Frame(root)
att_frame.pack()

# Creating a label and an entry for the date
date_label = tk.Label(att_frame, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = tk.Entry(att_frame)
date_entry.grid(row=0, column=1, padx=10, pady=10)

# Creating a listbox to display the student names and roll numbers
student_list = tk.Listbox(att_frame)
student_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Creating a function to populate the listbox with the student details
def populate_list():
    # Deleting the previous items from the listbox
    student_list.delete(0, tk.END)
    # Querying the database for the student details
    cur.execute("SELECT name, roll_no FROM students")
    # Fetching the results
    students = cur.fetchall()
    # Looping through the results and inserting them into the listbox
    for student in students:
        student_list.insert(tk.END, f"{student[0]} ({student[1]})")

# Calling the populate_list function
populate_list()

# Creating a function to mark the attendance of the selected student
def mark_attendance(status):
    # Getting the date from the entry
    date = date_entry.get()
    # Getting the selected student from the listbox
    selection = student_list.curselection()
    # Checking if the date and selection are not empty
    if date and selection:
        # Getting the roll number from the selection
        roll_no = student_list.get(selection)[1][-2:-1]
        # Trying to insert the attendance record into the database
        try:
            cur.execute("INSERT INTO attendance (date, roll_no, status) VALUES (?, ?, ?)", (date, roll_no, status))
            conn.commit()
            # Showing a success message
            tk.messagebox.showinfo("Success", f"Attendance marked as {status} for roll number {roll_no}")
        except sql.IntegrityError:
            # Showing an error message if the attendance record already exists
            tk.messagebox.showerror("Error", f"Attendance already marked for roll number {roll_no} on {date}")
    else:
        # Showing an error message if the date or selection is empty
        tk.messagebox.showerror("Error", "Date or student selection cannot be empty")

# Creating buttons to mark the attendance as present or absent
present_button = tk.Button(att_frame, text="Present", command=lambda: mark_attendance("Present"))
present_button.grid(row=2, column=0, padx=10, pady=10)

absent_button = tk.Button(att_frame, text="Absent", command=lambda: mark_attendance("Absent"))
absent_button.grid(row=2, column=1, padx=10, pady=10)

# Creating a frame for viewing the attendance records
view_frame = tk.Frame(root)
view_frame.pack()

# Creating a label and an entry for the date
date_label = tk.Label(view_frame, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = tk.Entry(view_frame)
date_entry.grid(row=0, column=1, padx=10, pady=10)

# Creating a function to view the attendance records for a given date
def view_attendance():
    # Getting the date from the entry
    date = date_entry.get()
    # Checking if the date is not empty
    if date:
        # Querying the database for the attendance records for the given date
        cur.execute("SELECT students.name, students.roll_no, attendance.status FROM students INNER JOIN attendance ON students.roll_no = attendance.roll_no WHERE attendance.date = ?", (date,))
        # Fetching the results
        records = cur.fetchall()
        # Checking if the results are not empty
        if records:
            # Creating a new window to display the records
            record_window = tk.Toplevel()
            record_window.title(f"Attendance Records for {date}")
            # Creating a listbox to display the records
            record_list = tk.Listbox(record_window)
            record_list.pack(padx=10, pady=10)
            # Looping through the results and inserting them into the listbox
            for record in records:
                record_list.insert(tk.END, f"{record[0]} ({record[1]}) - {record[2]}")
        else:
            # Showing a message if no records are found
            tk.messagebox.showinfo("No Records", f"No attendance records found for {date}")
    else:
        # Showing an error message if the date is empty
        tk.messagebox.showerror("Error", "Date cannot be empty")

# Creating a button to view the attendance records
view_button = tk.Button(view_frame, text="View Attendance", command=view_attendance)
view_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Starting the main loop
root.mainloop()

# Closing the database connection
conn.close()
