import subprocess
import tkinter as tk
from tkinter import messagebox
import urllib.request
import os
import configparser
import sys
import shutil

channels = []  # List to store channel URLs
current_channel_index = -1  # Index of the currently selected channel
mpv_process = None  # Process instance of the running mpv
config_file = "config.ini"  # Name of the INI file

# Create a configparser instance
config = configparser.ConfigParser()


def save_config(server, port, username, password):
    # Create the config file if it doesn't exist
    if not os.path.exists(config_file):
        config.add_section("Settings")

    # Set the options in the config file
    config.set("Settings", "server", server)
    config.set("Settings", "port", port)
    config.set("Settings", "username", username)
    config.set("Settings", "password", password)

    # Save the config to the INI file
    with open(config_file, "w") as configfile:
        config.write(configfile)


def read_config():
    # Read the config file
    config.read(config_file)

    # Check if the options are present in the config file
    if "Settings" in config:
        server = config.get("Settings", "server", fallback="")
        port = config.get("Settings", "port", fallback="")
        username = config.get("Settings", "username", fallback="")
        password = config.get("Settings", "password", fallback="")

        return server, port, username, password

    return "", "", "", ""


def extract_mpv_exe():
    # Get the temp directory where the script is running
    temp_dir = sys._MEIPASS

    # Specify the path to the bundled mpv.exe file
    bundled_mpv_path = os.path.join(temp_dir, "mpv.exe")

    # Specify the destination path to extract mpv.exe
    extracted_mpv_path = os.path.join(os.path.dirname(__file__), "mpv.exe")

    # Extract the mpv.exe file from the bundled resource
    shutil.copy2(bundled_mpv_path, extracted_mpv_path)


def parse_m3u_url():
    # Get the server, port, username, and password from the entry widgets
    server = server_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Construct the M3U URL using the provided information
    m3u_url = f"{server}:{port}/get.php?username={username}&password={password}&type=m3u&output=ts"

    try:
        # Fetch the M3U file from the URL
        response = urllib.request.urlopen(m3u_url)
        m3u_content = response.read().decode("utf-8")

        # Extract channel names and URLs from the M3U content
        channel_names = []
        channel_urls = []
        lines = m3u_content.split("\n")
        for line in lines:
            if line.startswith("#EXTINF"):
                name = line.split(",")[1]
                channel_names.append(name)
            elif line.startswith("http"):
                channel_urls.append(line.strip())  # Remove leading/trailing whitespace

        # Clear existing items in the listbox and channels list
        listbox.delete(0, tk.END)
        channels.clear()

        # Add channel names to the listbox and URLs to the channels list
        for name, url in zip(channel_names, channel_urls):
            listbox.insert(tk.END, name)
            channels.append(url)

        # Reset the current channel index
        global current_channel_index
        current_channel_index = -1

        # Save the server, port, username, and password to the INI file
        save_config(server, port, username, password)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def embed_mpv_window():
    # Get the selected channel from the listbox
    selected_index = listbox.curselection()
    if len(selected_index) == 0:
        messagebox.showerror("Error", "No channel selected.")
        return

    # Check if mpv.exe file exists in the same folder as the script
    mpv_path = os.path.join(os.path.dirname(__file__), "mpv.exe")

    # If mpv.exe doesn't exist, extract it from the bundled resource
    if not os.path.isfile(mpv_path):
        extract_mpv_exe()

    # Check again if mpv.exe file exists after extraction
    if not os.path.isfile(mpv_path):
        messagebox.showerror("Error", "mpv.exe not found. Please ensure it is bundled or place it next to the script file.")
        return

    # Terminate the existing mpv process if it is running
    global mpv_process
    if mpv_process:
        mpv_process.terminate()
        mpv_process = None

    # Get the URL of the selected channel
    selected_url = channels[selected_index[0]]

    # Launch "mpv" with command-line arguments using subprocess
    mpv_args = [mpv_path, selected_url]  # Pass the selected URL as a command-line argument
    mpv_process = subprocess.Popen(mpv_args)


def play_previous_channel():
    global current_channel_index
    current_channel_index = (current_channel_index - 1) % len(channels)
    listbox.select_clear(0, tk.END)
    listbox.select_set(current_channel_index)
    listbox.activate(current_channel_index)
    listbox.see(current_channel_index)

    embed_mpv_window()


def play_next_channel():
    global current_channel_index
    current_channel_index = (current_channel_index + 1) % len(channels)
    listbox.select_clear(0, tk.END)
    listbox.select_set(current_channel_index)
    listbox.activate(current_channel_index)
    listbox.see(current_channel_index)

    embed_mpv_window()


def exit_application():
    # Terminate the mpv process if it is running
    global mpv_process
    if mpv_process:
        mpv_process.terminate()

    # Close the Tkinter window
    window.destroy()


# Create the GUI window
window = tk.Tk()

# this removes the maximize button
window.resizable(0, 0)

window.title("M3U IPTV Player")
window.attributes('-topmost', 1)

# Calculate the center position of the window
window_width = 400  # adjust as needed
window_height = 450  # adjust as needed
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a frame to hold the labels and entry widgets
entry_frame = tk.Frame(window)
entry_frame.pack()

# Create labels and entry widgets for server, port, username, and password
server_label = tk.Label(entry_frame, text="Server:")
server_label.pack()
server_entry = tk.Entry(entry_frame)
server_entry.pack()

port_label = tk.Label(entry_frame, text="Port:")
port_label.pack()
port_entry = tk.Entry(entry_frame)
port_entry.pack()

username_label = tk.Label(entry_frame, text="Username:")
username_label.pack()
username_entry = tk.Entry(entry_frame)
username_entry.pack()

password_label = tk.Label(entry_frame, text="Password:")
password_label.pack()
password_entry = tk.Entry(entry_frame, show="*")
password_entry.pack()

# Read the server, port, username, and password from the INI file, if available
server, port, username, password = read_config()
server_entry.insert(0, server)
port_entry.insert(0, port)
username_entry.insert(0, username)
password_entry.insert(0, password)

# Create a button to parse the M3U URL
parse_button = tk.Button(window, text="Get/Update Channels", command=parse_m3u_url)
parse_button.pack()

# Create a frame to hold the listbox and scrollbar
listbox_frame = tk.Frame(window)
listbox_frame.pack(fill=tk.BOTH, expand=True)

# Create a listbox to display channel names
listbox = tk.Listbox(listbox_frame, width=50)

# Create a vertical scrollbar and associate it with the listbox
scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.pack(fill=tk.BOTH, expand=True)

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack()

# Create a button to embed the mpv window
embed_button = tk.Button(button_frame, text="Watch Now!", command=embed_mpv_window)
embed_button.pack(side="left")

# Create a button to play the previous channel
previous_button = tk.Button(button_frame, text="<< Channel", command=play_previous_channel)
previous_button.pack(side="left")

# Create a button to play the next channel
next_button = tk.Button(button_frame, text="Channel >>", command=play_next_channel)
next_button.pack(side="left")

# Center the button frame horizontally
button_frame.pack(anchor="center")

# Register exit_application function to be called when the window is closed
window.protocol("WM_DELETE_WINDOW", exit_application)

# Start the Tkinter event loop
window.mainloop()

