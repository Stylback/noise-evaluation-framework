# --------------------
# External modules
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import vitaldb
import os

# Internal Modules
from data import main
from noise import artifacts
from Filters import FilterLow
#from evaluation import snr, ml

# -------------------
# Variable to store the waveform
global waveform
waveform = None



"""
NOTE: Due to how the filters work, if one wants to use the GUI past the 'DATA' and 'NOISE' sections, both timestamp and drop need to be true (checked) within the 'DATA' section. 
"""



"""
GUI methods for Data
"""
# -------------------
def open_vitaldb_page():
       # Function to handle actions when VitalDB button is clicked
    # Function to handle actions when VitalDB button is clicked
    global vitaldb_window
    vitaldb_window = tk.Toplevel(root)
    vitaldb_window.title("VitalDB Page")

    # Get the path to the track names file in the current directory
    file_path = "track_names.txt"

    # Read track names from the file and use them as lines
    with open(file_path, 'r') as file:
        track_names = [track_name.strip() for track_name in file.read().split(',')]

     # Combobox for selecting multiple track names
    combobox_label = tk.Label(vitaldb_window, text="Select Track Names:")
    combobox_label.pack(pady=10)

    combobox_var = tk.StringVar()
    combobox = ttk.Combobox(vitaldb_window, textvariable=combobox_var, values=track_names, state="readonly", width=47)
    combobox.pack(pady=10)

    # Button to plot all
    plot_all_button = tk.Button(vitaldb_window, text="Plot All", command=lambda: plot_all(combobox_var.get()))
    plot_all_button.pack(pady=10)

    # Button to select case ID
    select_case_button = tk.Button(vitaldb_window, text="Select Case ID", command=lambda: open_case_selection_page(combobox_var.get()))
    select_case_button.pack(pady=10)

    vitaldb_window.mainloop()


def plot_all(selected_track):
    # Function to handle plotting all cases for the selected track
    print(f"Plotting all cases for {selected_track}")
    main.plot_all(vitaldb.find_cases([selected_track]), selected_track, interval = None, dropna = False)

def open_case_selection_page(selected_track):
    # Function to handle actions when Case ID selection page is opened
    case_selection_window = tk.Toplevel(root)
    case_selection_window.title("Case ID Selection Page")

    # Get specific case IDs for the selected track
    case_ids = vitaldb.find_cases([selected_track])

    # Combobox for selecting a specific Case ID
    combobox_label = tk.Label(case_selection_window, text="Select Case ID:")
    combobox_label.pack(pady=10)

    combobox_var = tk.StringVar()
    combobox = ttk.Combobox(case_selection_window, textvariable=combobox_var, values=case_ids, state="readonly", width=47)
    combobox.pack(pady=10)

    # StringVar to store the selected Case ID
    selected_case_var = tk.StringVar()

    def submit_case():
        selected_case = combobox_var.get()
        selected_case_var.set(selected_case)
        case_selection_window.destroy()
        vitaldb_window.destroy()  # Destroy the vitaldb window when the case is selected
        open_parameter_selection_page(selected_case, selected_track)


    # Button to submit and close the window
    submit_button = tk.Button(case_selection_window, text="Submit", command=submit_case)
    submit_button.pack(pady=20)

    case_selection_window.mainloop()


def open_parameter_selection_page(selected_case, selected_track):
    # Function to handle actions when Parameter Selection page is opened
    parameter_selection_window = tk.Toplevel(root)
    parameter_selection_window.title("Run Get Waveform - Parameter Selection Page")

    # Label and Entry for Interval
    interval_label = tk.Label(parameter_selection_window, text="Interval:")
    interval_label.grid(row=0, column=0, padx=10, pady=10)

    interval_entry_var = tk.DoubleVar()
    interval_entry = tk.Entry(parameter_selection_window, textvariable=interval_entry_var)
    interval_entry.grid(row=0, column=1, padx=10, pady=10)

    # Label and Checkbutton for Timestamp
    timestamp_var = tk.BooleanVar()
    timestamp_checkbutton = tk.Checkbutton(parameter_selection_window, text="Timestamp", variable=timestamp_var)
    timestamp_checkbutton.grid(row=1, column=0, padx=10, pady=10)

    # Label and Checkbutton for Trim
    trim_var = tk.BooleanVar()
    trim_checkbutton = tk.Checkbutton(parameter_selection_window, text="Trim", variable=trim_var)
    trim_checkbutton.grid(row=2, column=0, padx=10, pady=10)

    # Label and Checkbutton for Dropna
    dropna_var = tk.BooleanVar()
    dropna_checkbutton = tk.Checkbutton(parameter_selection_window, text="Dropna", variable=dropna_var)
    dropna_checkbutton.grid(row=3, column=0, padx=10, pady=10)

    def run_get_waveform():

        global waveform
        
        # Function to handle actions when the "Run Get Waveform" button is clicked
        # Retrieve selected parameters and run the corresponding function (e.g., Get Waveform)
        selected_interval = interval_entry_var.get()
        selected_timestamp = timestamp_var.get()
        selected_trim = trim_var.get()
        selected_dropna = dropna_var.get()
        print(f"Pulled Waveform| Track Name: {selected_track}, Case ID: {selected_case}, Interval: {selected_interval}, Timestamp: {selected_timestamp}, Trim: {selected_trim}, Dropna: {selected_dropna}")

        waveform = main.get_waveform(int(selected_case), selected_track, selected_interval, selected_timestamp, selected_trim, selected_dropna)

    # Button to run the Get Waveform function
    run_button = tk.Button(parameter_selection_window, text="Run Get Waveform", command=run_get_waveform)
    run_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Button to plot the waveform
    plot_button = tk.Button(parameter_selection_window, text="Plot", command=lambda: plot_waveform(selected_track, selected_case, interval_entry_var.get(), timestamp_var.get(), trim_var.get(), dropna_var.get(), waveform))
    plot_button.grid(row=5, column=0, columnspan=2, pady=20)

    def plot_waveform(track_name, case_id, interval, timestamp, trim, dropna,  waveform):
        # Replace the following line with the actual logic for plotting the waveform
        print(f"Plot Waveform| Track Name: {track_name}, Case ID: {case_id}, Interval: {interval}, Timestamp: {timestamp}, Trim: {trim}, Dropna: {dropna}")

        main.plot(waveform)

    parameter_selection_window.mainloop()


def open_csv_page():
    # Function to handle actions when CSV button is clicked
    csv_window = tk.Toplevel(root)
    csv_window.title("CSV File Selector")

    # Create a StringVar to store the selected file path
    global entry_var

    # Create an Entry widget to display the selected file path
    entry = tk.Entry(csv_window, textvariable=entry_var, width=50)
    entry.grid(row=0, column=0, padx=10, pady=10)

    # Create a button to trigger file selection
    browse_button = tk.Button(csv_window, text="Browse", command=lambda: browse_file(csv_window))
    browse_button.grid(row=0, column=1, padx=10, pady=10)

    # After the file is selected and the main loop exits, you can use the selected file path
    csv_window.mainloop()
    selected_file_path = entry_var.get()
    print("Selected CSV File:", selected_file_path)

def browse_file(current_window):
    """
    Open a file dialog, allowing the user to select a file. 
    """

    global waveform

    # Open a file dialog, allowing the user to select a file and assign to varirable
    file_path = filedialog.askopenfilename()  

    # Set the value of the Tkinter StringVar variable to previous variable
    entry_var.set(file_path)

    # Close the current window after selecting a file
    current_window.destroy()

    # Open a new window for plotting
    plot_prompt_window = tk.Toplevel(root)
    plot_prompt_window.title("Plot Prompt")

    # Label and prompt for plotting
    plot_label = tk.Label(plot_prompt_window, text="Do you want to plot the waveform?")
    plot_label.pack(pady=10)

    # restructure dataframe
    df = pd.read_csv(file_path)
    if len(df.columns) > 1:
         df = df[['CardioQ/ABP', 'Time']]
    waveform = df.values.tolist()

    # Button to confirm and plot
    plot_button = tk.Button(plot_prompt_window, text="Plot", command=lambda: [main.plot(waveform), plot_prompt_window.destroy()])
    plot_button.pack(pady=10)
    plot_button.pack(pady=10)

    # Button to cancel
    cancel_button = tk.Button(plot_prompt_window, text="Cancel", command=plot_prompt_window.destroy)
    cancel_button.pack(pady=10)
# -------------------




"""
GUI Methods for Noise
"""
# -------------------
def save_noise_level(noise_value):
    try:
        noise_level = int(noise_value)
        print("Noise Level:", noise_level)
        # You can save the noise_level variable for later use
    except ValueError:
        print("Invalid input. Please enter an integer.")    

# Function to open a new window for noise level entry
def open_noise_entry_window():

    global waveform

    noise_entry_window = tk.Toplevel(noise_root)
    noise_entry_window.title("Enter Noise Level")

    # Label and Entry for inputting the noise level
    noise_label = tk.Label(noise_entry_window, text="Enter Noise Level (integer):")
    noise_label.grid(row=0, column=0, padx=10, pady=10)

    noise_entry_var = tk.StringVar()
    noise_entry = tk.Entry(noise_entry_window, textvariable=noise_entry_var)
    noise_entry.grid(row=0, column=1, padx=10, pady=10)

    # Button to save the noise level
    save_button = tk.Button(noise_entry_window, text="Save", command=lambda: save_noise_level(noise_entry_var.get()))
    save_button.grid(row=1, column=0, columnspan=2, pady=10)

    waveform_type = None

    if isinstance(waveform, list) and all(isinstance(item, list) and len(item) ==  2 for item in waveform):
        waveform_type = main.WaveformType.LIST_LISTS
    elif isinstance(waveform, list):
        waveform_type = main.WaveformType.LIST

    match waveform_type:
        case main.WaveformType.LIST_LISTS:
            # Separate the timestamps and signal values from waveform
            timestamps = [item[1] for item in waveform]
            signal_values = [item[0] for item in waveform]

            # Add artificial noise to the signal
            waveform_noisy_data = artifacts.add_random_noise(signal_values, noise_level=10)

            # Redfine waveform with noisy data
            waveform = [list(item) for item in zip(waveform_noisy_data, timestamps)]
        case main.WaveformType.LIST:
            signal_values = [item for item in waveform]
            waveform = artifacts.add_random_noise(signal_values, noise_level=10).tolist()

    # Button to plot
    plot_button = tk.Button(noise_entry_window, text="Plot", command=lambda: [main.plot(waveform), noise_entry_window.destroy()])
    plot_button.grid(row=2, column=0, columnspan=2, pady=10)

# -------------------



"""
GUI methods for filter
"""
# -------------------
def apply_low_pass_filter():
    global waveform
    _, filtered_signal = FilterLow.main(waveform)
    waveform = [[data, timestep] for data, timestep in filtered_signal]

def plot(waveform_original):
    global waveform
    original_signal = [data[0] for data in waveform_original]
    filtered_signal = [data[0] for data in waveform]
    filtered_signal = np.array(filtered_signal)
    original_signal = np.array(original_signal)
    snr_value = snr.snrCalc(original_signal, filtered_signal)
    snr.snrPlot(original_signal, filtered_signal, snr_value)
# -------------------
    


"""
GUI methods for eval
"""
# -------------------
def browse_eval_file(eval_entry_var):
    # Open a file dialog to allow the user to select a file
    file_path = filedialog.askopenfilename()

    # Set the selected file path to the StringVar variable
    eval_entry_var.set(file_path)

    # Now, you can use the selected file path stored in eval_entry_var
    selected_file_path = eval_entry_var.get()
    print("Selected File for Evaluation:", selected_file_path)

# Function to run ml.mlMain
def run_ml_main(waveform_original):
    global waveform
    original_signal = [data[0] for data in waveform_original]
    filtered_signal = [data[0] for data in waveform]
    filtered_signal = np.array(filtered_signal)
    original_signal = np.array(original_signal)

    # Retrieve the file path from the StringVar
    file_path = eval_entry_var.get()
    # Get the directory (remove the filename)
    directory_path = os.path.dirname(file_path) + '/'
    # Get the filename (remove the directory)
    filename = os.path.basename(file_path)

    print('\n')
    print(file_path)
    print(directory_path)
    print(filename)
    print('\n')

    ml.mlMain(directory_path, filename, original_signal, filtered_signal, 2500)
# -------------------


"""
Data Window
"""
# --------------------
# Data window
root = tk.Tk()
root.title("Data")

# Set the size of the main window
root.geometry("350x150")  # Adjust the dimensions as needed

# Create a menu frame
menu_frame = ttk.Frame(root, padding="10")
menu_frame.grid(row=0, column=0)

# Data heading
data_heading = ttk.Label(menu_frame, text="Data", font=("Helvetica", 14, "bold"), anchor="w")
data_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Subheading label
subheading_label = ttk.Label(menu_frame, text="Choose your data source:", font=("Helvetica", 10, "italic"), anchor="w")
subheading_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# VitalDB button
vitaldb_button = ttk.Button(menu_frame, text="Use VitalDB", command=open_vitaldb_page)
vitaldb_button.grid(row=2, column=2, columnspan=4,padx=10, pady=10, sticky="w")

# CSV button
csv_button = ttk.Button(menu_frame, text="Use CSV", command=open_csv_page)
csv_button.grid(row=2, column=4, columnspan=4, padx=10, pady=10, sticky="w")

# Create a StringVar to store the selected file path
entry_var = tk.StringVar()

root.mainloop()
# --------------------



"""
Noise Window
"""
# --------------------

# After the main loop, open a new root window called 'Noise'
noise_root = tk.Tk()
noise_root.title("Noise")

# Set the size of the main window
noise_root.geometry("350x250")  # Adjust the dimensions as needed

# Create a menu frame
menu_frame = ttk.Frame(noise_root, padding="10")
menu_frame.grid(row=0, column=0)

# Noise heading
data_heading = ttk.Label(menu_frame, text="Noise", font=("Helvetica", 14, "bold"), anchor="w")
data_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Subheading label
subheading_label = ttk.Label(menu_frame, text="Choose your Noise:", font=("Helvetica", 10, "italic"), anchor="w")
subheading_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# Button to open the window for noise level entry
open_entry_window_button = tk.Button(noise_root, text="Enter Noise", command=open_noise_entry_window)
open_entry_window_button.grid(row=2, column=2, columnspan=4,padx=10, pady=10, sticky="w")

# Button to skip and close the 'Noise' window instantly
skip_button = tk.Button(noise_root, text="Skip", command=noise_root.destroy)
skip_button.grid(row=3, column=2, columnspan=4, padx=10, pady=10, sticky="w")

# Run the main loop for the 'Noise' window
noise_root.mainloop()
# -------------------



"""
Filter Window
"""
# -------------------

# After the main loop, open a new root window called 'Noise'
filter_root = tk.Tk()
filter_root.title("Filter")

# Set the size of the main window
filter_root.geometry("350x250")  # Adjust the dimensions as needed

# Create a menu frame
menu_frame = ttk.Frame(filter_root, padding="10")
menu_frame.grid(row=0, column=0)

# Noise heading
data_heading = ttk.Label(menu_frame, text="Filter", font=("Helvetica", 14, "bold"), anchor="w")
data_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Subheading label
subheading_label = ttk.Label(menu_frame, text="Choose your Filter:", font=("Helvetica", 10, "italic"), anchor="w")
subheading_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# Button to open the window for noise level entry
open_entry_window_button = tk.Button(filter_root, text="Low Pass Filter", command=apply_low_pass_filter)
open_entry_window_button.grid(row=2, column=2, columnspan=4,padx=10, pady=10, sticky="w")

# Button to open the window for noise level entry
waveform_original = waveform
plot_filtered_button = tk.Button(filter_root, text="Plot", command=lambda:plot(waveform_original))
plot_filtered_button.grid(row=3, column=2, columnspan=4,padx=10, pady=10, sticky="w")

# Button to skip and close the 'Noise' window instantly
skip_button = tk.Button(filter_root, text="Skip", command=filter_root.destroy)
skip_button.grid(row=4, column=2, columnspan=4, padx=10, pady=10, sticky="w")

# Run the main loop for the 'Noise' window
filter_root.mainloop()
# -------------------



"""
Evaluation Window
"""
# -------------------

# After the main loop, open a new root window called 'Noise'
eval_root = tk.Tk()
eval_root.title("Eval")

# Create a StringVar to store the selected file path
eval_entry_var = tk.StringVar()

# Set the size of the main window
eval_root.geometry("350x250")  # Adjust the dimensions as needed

# Create a menu frame
menu_frame = ttk.Frame(eval_root, padding="10")
menu_frame.grid(row=0, column=0)

# Noise heading
data_heading = ttk.Label(menu_frame, text="Eval", font=("Helvetica", 14, "bold"), anchor="w")
data_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Subheading label
subheading_label = ttk.Label(menu_frame, text="Choose your Eval:", font=("Helvetica", 10, "italic"), anchor="w")
subheading_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# Button to open file dialog and select a file
browse_button = tk.Button(eval_root, text="Browse", command=lambda: browse_eval_file(eval_entry_var))
browse_button.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

# Button to run ml.mlMain
run_ml_button = tk.Button(eval_root, text="Run ML", command=lambda:run_ml_main(waveform_original))
run_ml_button.grid(row=3, column=1, columnspan=4, padx=10, pady=10)

# Button to skip and close the 'eval' window instantly
skip_button = tk.Button(eval_root, text="Skip", command=eval_root.destroy)
skip_button.grid(row=4, column=1, columnspan=4, padx=10, pady=10, sticky="w")

# Run the main loop for the 'Noise' window
eval_root.mainloop()
# -------------------