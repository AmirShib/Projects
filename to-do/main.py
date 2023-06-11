# a Simple to do app, with add, delete load and save functions

import tkinter as tk
import tkinter.messagebox
from datetime import date
root = tk.Tk()
root.title('simple To-Do App')


def add_function():
    task = entry_space.get()
    # only add a task when there is a text in the Entry space
    if task != "":
        Tasks_listbox.insert(tk.END, task)
        entry_space.delete(0, tk.END)
    else:
        tk.messagebox.showerror(message='Please Enter A Task', title='Error')


def delete_function():
    # if the user is trying to delete nothing, raise an error.
    try:
        task_to_delete = Tasks_listbox.curselection()
        Tasks_listbox.delete(task_to_delete)
    except:
        tk.messagebox.showerror(message='Please Choose A Task to Delete', title='Error')


def save_function():
    if Tasks_listbox.size() > 0:
        today = str(date.today()) # string with current date
        saved_list = Tasks_listbox.get(0, tk.END)
        saved_list = [line + "\n" for line in saved_list] # create a new line for each item in listbox
        saved_file = open("tasks-to-do" + "-" + today + ".txt", "w") # save the file with the current date as txt file
        saved_file.writelines(saved_list)
        saved_file.close()
        tk.messagebox.showinfo(message='file has been saved')
    else:
        tk.messagebox.showerror(title='Error', message='No Tasks to be saved')


"""" GUI : 1. A Button for adding, deleting and saving.
            2. a scrollbar for tasks."""


frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

Tasks_listbox = tk.Listbox(frame, width=52, height=15)
Tasks_listbox.pack()
Tasks_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=Tasks_listbox.yview)

entry_space = tk.Entry(root, width=50)
entry_space.pack()

add_button = tk.Button(root, text='Add Task', width=26, command=add_function)
add_button.pack()
add_button.config(command=add_function)
root.bind('<Return>', lambda event=None: add_button.invoke()) # bind the Enter key so it will add tasks to the list

delete_button = tk.Button(root, text='Delete Task', width=26, command=delete_function)
delete_button.pack()
delete_button.config(command=delete_function)
root.bind('<Delete>', lambda event=None: delete_button.invoke()) # bind the delete key to delete selected tasks

save_button = tk.Button(root, text='Save Tasks', width=26, command=save_function)
save_button.pack()


root.mainloop()