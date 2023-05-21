import subprocess
import tkinter as tk
from tkinter import messagebox
import urllib.request
import os

channels = []  # List to store channel URLs
current_channel_index = -1  # Index of the currently selected channel
mpv_process = None  # Process instance of the running mpv


def parse_m3u_url():
    # Get the M3U URL from the entry widget
    m3u_url = entry.get()

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
    if not os.path.isfile(mpv_path):
        messagebox.showerror("Error", "mpv.exe not found. Please place the 'mpv.exe' file next to the script file.")
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


def play_next_channel():
    global current_channel_index
    current_channel_index = (current_channel_index + 1) % len(channels)
    listbox.select_clear(0, tk.END)
    listbox.select_set(current_channel_index)
    listbox.activate(current_channel_index)
    listbox.see(current_channel_index)

    embed_mpv_window()


def play_previous_channel():
    global current_channel_index
    current_channel_index = (current_channel_index - 1) % len(channels)
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
window_height = 350  # adjust as needed
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a label and entry for the M3U URL
label = tk.Label(window, text="M3U URL:")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Set the initial text of the entry widget
entry.insert(0, "")  # Replace with the actual M3U URL

# Create a right-click menu for the entry widget
entry_menu = tk.Menu(window, tearoff=0)
entry_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: window.focus_get().event_generate("<<Cut>>"))
entry_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: window.focus_get().event_generate("<<Copy>>"))
entry_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: window.focus_get().event_generate("<<Paste>>"))

# Bind the right-click menu to the entry widget
entry.bind("<Button-3>", lambda e: entry_menu.post(e.x_root, e.y_root))

# Create a button to parse the M3U URL
parse_button = tk.Button(window, text="Parse M3U URL", command=parse_m3u_url)
parse_button.pack()

# Create a listbox to display channel names
listbox = tk.Listbox(window, width=50)
listbox.pack()

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack()

# Create a button to embed the mpv window
embed_button = tk.Button(button_frame, text="Watch Selected Channel", command=embed_mpv_window)
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

