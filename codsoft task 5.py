import tkinter as tk
import sqlite3 as sql
from tkinter import messagebox
import re

conn = sql.connect("attendance.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, roll_no INTEGER UNIQUE)")

cur.execute("CREATE TABLE IF NOT EXISTS attendance (date TEXT, roll_no INTEGER, status TEXT, FOREIGN KEY(roll_no) REFERENCES students(roll_no))")

conn.commit()

root = tk.Tk()
root.title("Attendance")


add_frame = tk.Frame(root)
add_frame.pack()

name_label = tk.Label(add_frame, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

roll_label = tk.Label(add_frame, text="Roll No:")
roll_label.grid(row=1, column=0, padx=10, pady=10)
roll_entry = tk.Entry(add_frame)
roll_entry.grid(row=1, column=1, padx=10, pady=10)

def add_student():

    name = name_entry.get()
    roll_no = roll_entry.get()

    if name and roll_no:

        try:
            cur.execute("INSERT INTO students (name, roll_no) VALUES (?, ?)", (name, roll_no))
            conn.commit()

            messagebox.showinfo("Success", "Student added successfully")
        except sql.IntegrityError:

            messagebox.showerror("Error", "Roll number already exists")
    else:

        messagebox.showerror("Error", "Name or roll number cannot be empty")

    populate_list()

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)



add_button = tk.Button(add_frame, text="Add Student", command=add_student)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

att_frame = tk.Frame(root)
att_frame.pack()

date_label = tk.Label(att_frame, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry_attput = tk.Entry(att_frame)
date_entry_attput.grid(row=0, column=1, padx=10, pady=10)

studentList = tk.Listbox(att_frame)
studentList.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def populate_list():

    studentList.delete(0, tk.END)

    cur.execute("SELECT name, roll_no FROM students")

    students = cur.fetchall()

    for student in students:
        studentList.insert(tk.END, f"{student[0]} ({student[1]})")

populate_list()


def mark_attendance(status):

    date = date_entry_attput.get()

    selection = studentList.curselection()

    if date and selection:

        tempname = (studentList.get(selection))
        match = re.search(r"\d+",tempname)
        roll_no = int(match.group())


        messagebox.showerror("Error", roll_no)
        try:
            cur.execute("INSERT INTO attendance (date, roll_no, status) VALUES (?, ?, ?)", (date, roll_no, status))
            conn.commit()
            messagebox.showinfo("Success", "Attendance marked as {} for roll number {}".format(status,roll_no))
        except sql.IntegrityError:

            messagebox.showerror("Error", f"Attendance already marked for roll number {roll_no} on {date}")
    else:

        messagebox.showerror("Error", "Date or student selection cannot be empty")




present_button = tk.Button(att_frame, text="Present", command=lambda: mark_attendance("Present"))
present_button.grid(row=2, column=0, padx=10, pady=10)

absent_button = tk.Button(att_frame, text="Absent", command=lambda: mark_attendance("Absent"))
absent_button.grid(row=2, column=1, padx=10, pady=10)

view_frame = tk.Frame(root)
view_frame.pack()


date_label = tk.Label(view_frame, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = tk.Entry(view_frame)
date_entry.grid(row=0, column=1, padx=10, pady=10)

def view_attendance():

    date = date_entry.get()

    if date:

        cur.execute("SELECT students.name, students.roll_no, attendance.status FROM students INNER JOIN attendance ON students.roll_no = attendance.roll_no WHERE attendance.date = ?", (date,))

        records = cur.fetchall()

        if records:

            record_window = tk.Toplevel()
            record_window.title(f"Attendance Records for {date}")

            record_list = tk.Listbox(record_window)
            record_list.pack(padx=10, pady=10)

            for record in records:
                record_list.insert(tk.END, f"{record[0]} ({record[1]}) - {record[2]}")
        else:

            messagebox.showinfo("No Records", f"No attendance records found for {date}")
    else:

        messagebox.showerror("Error", "Date cannot be empty")

view_button = tk.Button(view_frame, text="View Attendance", command=view_attendance)
view_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

conn.close()
