# M3U IPTV Player

This repository contains a Python script that implements a simple M3U IPTV player with a graphical user interface (GUI) using the Tkinter library. The player allows you to parse an M3U playlist from a given URL and play the channels using the mpv media player.

## Features

- Fetches and parses an M3U file from a provided URL.
- Displays channel names in a listbox.
- Plays the selected channel using the mpv media player.
- Supports playing the previous and next channels.
- Provides error handling for invalid URLs and missing mpv executable.

## Usage

To use the M3U IPTV Player:

1. Clone the repository or download the `iptv_player.py` file.
2. Ensure you have Python 3 installed on your system.
3. Install the required dependencies by running `pip install tkinter`.
4. Place the `mpv.exe` file next to the `iptv_player.py` script, ensuring it is the executable for the mpv media player.
5. Run the script using `python iptv_player.py`.
6. The GUI window will appear.
7. Enter the M3U URL in the provided entry field and click "Parse M3U URL" to fetch and parse the channels.
8. Select a channel from the listbox and click "Watch Selected Channel" to play it.
9. Use the "<< Channel" and "Channel >>" buttons to navigate through the channels.
10. To exit, close the GUI window or press `Ctrl+C` in the terminal.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize and enhance the code to suit your specific needs. Contributions are also welcome.

**Note:** Ensure that you have the necessary rights and permissions to access and play the channels from the provided M3U URL.
