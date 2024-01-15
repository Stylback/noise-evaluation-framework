# --------------------
# External modules

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import vitaldb
# -------------------

# Main window
root = tk.Tk()
root.title("Filter File Selector")

entry_var = tk.StringVar()
function = tk.StringVar()


def browse_file():
    """
    Open a file dialog, allowing the user to select a file. 
    """

    # Open a file dialog, allowing the user to select a file and assign to varirable
    file_path = filedialog.askopenfilename()  

    # Set the value of the Tkinter StringVar variable to previous variable
    entry_var.set(file_path)

def submit():
    """
    Close all of the windows
    """

    root.destroy()

def show():

    # Create a menu
    menu_frame = ttk.Frame(root, padding="10")
    menu_frame.grid(row=0, column=0)

    # Create a StringVar to store the selected file path

    # creating a lable for the file location
    file_label = tk.Label(root, text = 'File Path', font=('calibre',10, 'bold'))

    # creating a lable for the function name
    function_label = tk.Label(root, text = 'Function Name', font=('calibre',10, 'bold'))

    # Create an Entry widget to display the selected file path
    entry = tk.Entry(root, textvariable=entry_var, width=50)

    # Create a button to trigger file selection
    browse_button = tk.Button(root, text="Browse", command=browse_file)

    #The function name selection
    function_name = tk.Entry(root, textvariable=function, font=('calibre',10,'normal'))

    # Create a button to trigger file selection
    submit_button = tk.Button(root, text="submit", command=submit)

    #Place thins in the right place
    file_label.grid(row=0, column=0, padx=10, pady=10)
    entry.grid(row=1, column=0, padx=10, pady=10)
    browse_button.grid(row=1, column=1, padx=10, pady=10)
    function_label.grid(row=2, column=0, padx=10, pady=10)
    function_name.grid(row=3, column=0, padx=10, pady=10)
    submit_button.grid(row=4, column=0, padx=10, pady=10)

    root.mainloop()

    selected_file_path = entry_var.get()
    print("Selected Filter File:", selected_file_path)
    function_name = function.get()
    print("Selected Function Name:", function_name)

    return selected_file_path, function_name