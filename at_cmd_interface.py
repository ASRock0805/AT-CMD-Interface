import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import time

class SerialCommunicator:
    """
    Handles serial communication with a device.

    Attributes:
        port (str): The serial port to connect to.
        baud_rate (int): The baud rate for serial communication (default: 115200).
        timeout (int): Timeout value for serial read operations (default: 1).
        ser (serial.Serial): The serial object.

    Author: Starke Wang
    """
    def __init__(self, port, baud_rate=115200, timeout=1):
        """
        Initializes SerialCommunicator with the specified parameters.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        """
        Establishes a serial connection to the specified port.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")
            return False

    def disconnect(self):
        """
        Closes the serial connection.
        """
        if self.ser:
            self.ser.close()
            self.ser = None

    def send_command(self, command):
        """
        Sends an AT command to the device.

        Args:
            command (str): The AT command to send.

        Returns:
            str: The response from the device.
        """
        if self.ser:
            self.ser.write(command.encode())
            time.sleep(0.1)  # Adjust sleep time as needed
            response = self.ser.read_all().decode()
            return response
        else:
            return "Not connected to serial port."

class ATCommandInterface:
    """
    Provides a graphical user interface for sending AT commands to a device.

    Attributes:
        baud_rate (int): The baud rate for serial communication (default: 115200).
        serial_communicator (SerialCommunicator): The serial communicator object.

    Author: Starke Wang
    """
    def __init__(self, baud_rate=115200):
        """
        Initializes ATCommandInterface with the specified baud rate.
        """
        self.baud_rate = baud_rate
        self.serial_communicator = None
        self.create_gui()

    def create_gui(self):
        """
        Creates the graphical user interface elements.
        """
        self.root = tk.Tk()
        self.root.title("AT Command Interface")

        # Configure styles
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TCombobox", padding=5)
        style.configure("TEntry", padding=5)

        # --- COM Port Selection ---
        port_frame = ttk.Frame(self.root)
        port_frame.pack(pady=10)

        port_label = ttk.Label(port_frame, text="COM Port:")
        port_label.pack(side=tk.LEFT, padx=5)

        self.com_port_var = tk.StringVar()
        self.com_port_combo = ttk.Combobox(port_frame, textvariable=self.com_port_var, state="readonly", width=15)
        self.com_port_combo.pack(side=tk.LEFT, padx=5)
        self.update_com_ports()

        connect_button = ttk.Button(port_frame, text="Connect", command=self.connect_to_port)
        connect_button.pack(side=tk.LEFT, padx=5)

        disconnect_button = ttk.Button(port_frame, text="Disconnect", command=self.disconnect_from_port)
        disconnect_button.pack(side=tk.LEFT, padx=5)

        # --- Device Info ---
        device_info_label = ttk.Label(self.root, text="Device Info:")
        device_info_label.pack(pady=5)

        self.device_info_var = tk.StringVar(value="No device detected")
        device_info_display = ttk.Label(self.root, textvariable=self.device_info_var, font=("Helvetica", 12, "bold"))
        device_info_display.pack(pady=5)

        # --- Command Input ---
        command_frame = ttk.Frame(self.root)
        command_frame.pack(pady=10)

        command_label = ttk.Label(command_frame, text="AT Command:")
        command_label.pack(side=tk.LEFT, padx=5)

        self.command_entry = ttk.Entry(command_frame, width=50)
        self.command_entry.pack(side=tk.LEFT, padx=5)

        send_button = ttk.Button(command_frame, text="Send", command=self.send_at_command)
        send_button.pack(side=tk.LEFT, padx=5)

        # --- Output Display ---
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=70, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        clear_button = ttk.Button(self.root, text="Clear Output", command=self.clear_output)
        clear_button.pack(pady=5)

        # Center the window
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")

        # Closing Event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_com_ports(self):
        """
        Updates the list of available COM ports in the GUI.
        """
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.com_port_combo['values'] = ports
        if ports:
            self.com_port_combo.current(0)  # Select the first port by default

    def connect_to_port(self):
        """
        Connects to the selected COM port.
        """
        selected_port = self.com_port_var.get()
        self.serial_communicator = SerialCommunicator(selected_port, baud_rate=self.baud_rate)
        if self.serial_communicator.connect():
            self.output_text.insert(tk.END, f"Connected to {selected_port}\n")
            self.get_device_info()
        else:
            messagebox.showerror("Error", f"Failed to connect to {selected_port}")

    def disconnect_from_port(self):
        """
        Disconnects from the current COM port.
        """
        if self.serial_communicator:
            self.serial_communicator.disconnect()
            self.output_text.insert(tk.END, "Disconnected from serial port\n")
            self.device_info_var.set("No device detected")

    def get_device_info(self):
        """
        Retrieves device information (DSN and Battery Level) using ADB in a separate thread.
        """
        def get_info_thread():
            try:
                # Check if a device is connected
                adb_check = subprocess.run(["adb", "devices"], capture_output=True, text=True)
                if "device" in adb_check.stdout:
                    # Use ADB command to get device serial number
                    serial_process = subprocess.run(
                        ["adb", "get-serialno"],
                        capture_output=True, text=True
                    )
                    serial_number = serial_process.stdout.strip()

                    # Use ADB command to get battery level
                    battery_process = subprocess.run(
                        ["adb", "shell", "cat /sys/class/power_supply/battery/capacity"],
                        capture_output=True, text=True
                    )
                    battery_level = battery_process.stdout.strip()

                    if serial_number and battery_level:
                        self.device_info_var.set(f"Serial Number: {serial_number}, Battery: {battery_level}%")
                    else:
                        self.device_info_var.set("Unable to retrieve device information.")
                else:
                    self.device_info_var.set("No ADB device connected.")
            except Exception as e:
                self.device_info_var.set(f"ADB error: {e}")
        threading.Thread(target=get_info_thread).start()

    def send_at_command(self):
        """
        Sends the AT command entered by the user.
        """
        command = self.command_entry.get().strip().upper()
        if not command.startswith("AT"):
            self.output_text.insert(tk.END, "Invalid AT Command format.\n")
            return

        if not command.endswith('\r'):
            command += '\r'

        if self.serial_communicator:
            response = self.serial_communicator.send_command(command)
            self.output_text.insert(tk.END, f"Command: {command.strip()}\nResponse: {response}\n")
            self.output_text.see(tk.END)
        else:
            self.output_text.insert(tk.END, "Not connected to serial port.\n")

    def clear_output(self):
        """
        Clears the output text area.
        """
        self.output_text.delete(1.0, tk.END)

    def on_closing(self):
        """
        Handles the window closing event.
        """
        if self.serial_communicator:
            self.serial_communicator.disconnect()
        self.root.destroy()

    def run(self):
        """
        Starts the Tkinter main loop.
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = ATCommandInterface(baud_rate=115200)
    app.run()