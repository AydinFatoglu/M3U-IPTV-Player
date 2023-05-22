**M3U IPTV Player**

This is a Python application that provides a graphical user interface (GUI) for an M3U IPTV player. It allows you to watch streaming channels using an M3U playlist file.

## Features

- Enter the server, port, username, and password for your IPTV service.
- Fetch the M3U playlist file from the specified URL.
- Parse the playlist file to extract channel names and URLs.
- Display the channel names in a list on the GUI.
- Select a channel from the list to watch it.
- Launch the associated media player (mpv) to play the selected channel.
- Navigate through the channel list using the previous and next buttons.
- Save the server, port, username, and password in a configuration file for future use.
- Terminate the media player process and close the application window.

## Usage

1. Clone the repository or download the source code.
2. Install the required dependencies (`tkinter`, `urllib`, `subprocess`, `configparser`, `sys`, `shutil`) if needed.
3. Run the `m3u_iptv_player.py` script using Python 3.
4. Enter the server, port, username, and password for your IPTV service in the respective fields.
5. Click the "Get/Update Channels" button to fetch and parse the M3U playlist.
6. The channel names will be displayed in a list on the left side of the GUI.
7. Select a channel from the list by clicking on it.
8. Click the "Watch Now!" button to launch the media player and start playing the selected channel.
9. Use the previous and next buttons to navigate through the channel list.
10. Close the application window to exit the program.

Note: Make sure to have the `mpv.exe` file in the same folder as the script or include it in the bundled resources if you are using a distribution package.

## Dependencies

The application relies on the following Python packages:

- `tkinter`: GUI library for Python.
- `urllib`: Library for URL handling.
- `subprocess`: Module for managing subprocesses.
- `configparser`: Module for working with configuration files.
- `sys`: Module providing access to system-specific parameters and functions.
- `shutil`: Module for file operations.

You can install these dependencies using `pip`:

```shell
pip install tkinter urllib subprocess configparser
