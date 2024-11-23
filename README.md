# AT Command Interface

This repository contains a Python-based AT command interface application with a graphical user interface (GUI) for sending AT commands to a device over a serial connection. It also includes a batch script to easily launch the application.

## Features

* **GUI for AT Commands:** Provides a user-friendly interface for sending AT commands to a device.
* **Serial Communication:** Establishes a serial connection with the device.
* **COM Port Selection:** Allows users to select the desired COM port from a list of available ports.
* **Device Information:** Displays device information, including serial number (DSN) and battery level (if supported by the device).
* **Clear Output:** Allows users to clear the output display.
* **Automatic Centering:** The application window is automatically centered on the screen.

## Requirements

* **Python 3.x:** Make sure you have Python 3 installed on your system.
* **Tkinter:** This is usually included with Python installations.
* **pyserial:** Install this library using `pip install pyserial`.
* **ADB (Optional):** If you want to retrieve device information like serial number and battery level, you'll need to have ADB (Android Debug Bridge) installed and configured.

## Usage

1.  **Install dependencies:**

    ```bash
    pip install pyserial
    ```

2.  **Run the application:**

    *   Execute the `start_at_interface.bat` batch script. This will check for Python installation and launch the `at_cmd_interface.py` script.

3.  **Connect to a device:**

    *   Select the appropriate COM port from the dropdown menu.
    *   Click the **"Connect"** button.

4.  **Send AT commands:**

    *   Type an AT command in the input field (e.g., `ATI` to get device information).
    *   Click the **"Send"** button.
    *   The response from the device will be displayed in the output area.

5.  **Clear the output:**

    *   Click the **"Clear Output"** button to clear the output display area.

6.  **Disconnect from the device:**

    *   Click the **"Disconnect"** button to close the serial connection.

## Author

Starke Wang
