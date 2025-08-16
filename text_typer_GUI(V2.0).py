import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pyautogui
import os
import ctypes
import sys

def set_dpi_awareness():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except (AttributeError, OSError):
            pass
    elif sys.platform.startswith('linux'):
        os.environ["GDK_SCALE"] = "1"
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

set_dpi_awareness()

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        master.title("Auto Typer Pro")
        self.scale_factor = self.get_system_scaling()
        master.geometry(f"{int(320 * self.scale_factor)}x{int(150 * self.scale_factor)}")
        master.resizable(False, False)
        self.center_window(master)
        
        self.current_command = "owo hunt"
        self.stop_event = threading.Event()
        self.command_lock = threading.Lock()
        self.delay = tk.DoubleVar(value=12.0)
        self.typing_mode = tk.StringVar(value="infinite")
        self.type_count = tk.IntVar(value=10)
        self.current_count = 0
        self.theme = tk.StringVar(value="Light")
        
        self.style = ttk.Style()
        self.configure_styles()
        self.setup_ui()
        self.master.attributes("-topmost", True)

    def get_system_scaling(self):
        if sys.platform == 'win32':
            try:
                user32 = ctypes.windll.user32
                return user32.GetDpiForSystem() / 96
            except AttributeError:
                return 1.0
        return 1.0

    def center_window(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"+{x}+{y}")

    def configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure('.', font=('Segoe UI', int(9 * self.scale_factor)))
        
        # Light theme
        self.style.configure('light.TFrame', background='#FFFFFF')
        self.style.configure('light.TButton', 
                        background='#4CAF50', 
                        foreground='white',
                        bordercolor='#4CAF50',
                        focuscolor='#4CAF50')
        self.style.map('light.TButton',
                    background=[('active', '#45a049')])
        
        # Dark theme
        self.style.configure('dark.TFrame', background='#2d2d2d')
        self.style.configure('dark.TButton',
                        background='#2196F3',
                        foreground='white',
                        bordercolor='#2196F3',
                        focuscolor='#2196F3')
        self.style.map('dark.TButton',
                    background=[('active', '#1976D2')])

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Settings button
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        self.settings_icon = tk.PhotoImage(file="texttyper/settings.png")  # Updated path
        self.settings_icon = self.resize_image(self.settings_icon, (20, 20))  # Resize image
        ttk.Button(settings_frame, text="Settings", command=self.open_settings, style=f'{self.theme.get().lower()}.TButton', image=self.settings_icon, compound=tk.LEFT).pack(side=tk.RIGHT)

        # Command entry
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entry_frame, text="Command:").pack(side=tk.LEFT, padx=2)
        self.command_entry = ttk.Entry(entry_frame, width=25)
        self.command_entry.insert(0, self.current_command)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.update_icon = tk.PhotoImage(file="texttyper/updated.png")  # Updated path
        self.update_icon = self.resize_image(self.update_icon, (20, 20))  # Resize image
        ttk.Button(entry_frame, text="Update", command=self.update_command, style=f'{self.theme.get().lower()}.TButton', width=8, image=self.update_icon, compound=tk.LEFT).pack(side=tk.LEFT, padx=2)


        # Control buttons


        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.start_icon = tk.PhotoImage(file="texttyper/play.png")  # Updated path
        self.start_icon = self.resize_image(self.start_icon, (20, 20))  # Resize image
        self.start_button = ttk.Button(
            button_frame, 
            text="Start", 
            command=self.start_typing,
            style=f'{self.theme.get().lower()}.TButton',
            width=10,
            image=self.start_icon,
            compound=tk.LEFT
        )
        self.start_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.stop_icon = tk.PhotoImage(file="texttyper/stop-button.png")  # Updated path
        self.stop_icon = self.resize_image(self.stop_icon, (20, 20))  # Resize image
        self.stop_button = ttk.Button(
            button_frame, 
            text="Stop", 
            command=self.stop_typing,
            style=f'{self.theme.get().lower()}.TButton',
            width=10,
            state=tk.DISABLED,
            image=self.stop_icon,
            compound=tk.LEFT
        )
        self.stop_button.pack(side=tk.LEFT, expand=True, padx=2)

        self.update_theme()

    def open_settings(self):
        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.attributes("-topmost", True)

        self.settings_window.title("Settings")
        self.settings_window.geometry(f"{int(300 * self.scale_factor)}x{int(200 * self.scale_factor)}")
        self.settings_window.resizable(False, False)
        self.center_window(self.settings_window)
        
        container = ttk.Frame(self.settings_window)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Count Mode
        count_frame = ttk.Frame(container)
        count_frame.pack(fill=tk.X, pady=5)
        self.count_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            count_frame, 
            text="Enable Count Mode", 
            variable=self.count_mode,
            command=self.toggle_count_mode
        ).pack(side=tk.LEFT)
        
        # Count Entry
        count_entry_frame = ttk.Frame(container)
        count_entry_frame.pack(fill=tk.X, pady=5)
        ttk.Label(count_entry_frame, text="Repeat Count:").pack(side=tk.LEFT)
        self.count_entry = ttk.Entry(count_entry_frame, textvariable=self.type_count, width=8)
        self.count_entry.pack(side=tk.RIGHT)
        self.count_entry.state(['disabled'])

        # Delay Settings
        delay_frame = ttk.Frame(container)
        delay_frame.pack(fill=tk.X, pady=5)
        ttk.Label(delay_frame, text="Delay (seconds):").pack(side=tk.LEFT)
        ttk.Spinbox(delay_frame, from_=1, to=60, textvariable=self.delay, width=8).pack(side=tk.RIGHT)

        # Theme Selector
        theme_frame = ttk.Frame(container)
        theme_frame.pack(fill=tk.X, pady=5)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        theme_combo = ttk.Combobox(
            theme_frame, 
            textvariable=self.theme, 
            values=["Light", "Dark"],
            state="readonly",
            width=10
        )
        theme_combo.pack(side=tk.RIGHT)
        theme_combo.bind("<<ComboboxSelected>>", self.update_theme)

        self.update_theme()

    def toggle_count_mode(self):
        if self.count_mode.get():
            self.typing_mode.set("count")
            self.count_entry.state(['!disabled'])
        else:
            self.typing_mode.set("infinite")
            self.count_entry.state(['disabled'])

    def update_theme(self, event=None):
        theme = self.theme.get().lower()
        bg = '#FFFFFF' if theme == 'light' else '#2d2d2d'
        fg = '#000000' if theme == 'light' else '#FFFFFF'
        
        # Update main window
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style=f'{theme}.TFrame')
        
        # Update settings window
        if hasattr(self, 'settings_window') and self.settings_window.winfo_exists():
            for widget in self.settings_window.winfo_children():
                if isinstance(widget, ttk.Frame):
                    widget.configure(style=f'{theme}.TFrame')

        # Update button styles
        self.style.configure(f'{theme}.TButton', font=('Segoe UI', int(9 * self.scale_factor)), padding=4, relief=tk.RAISED)
        
        # Update entry field colors
        self.style.configure(f'{theme}.TEntry', fieldbackground='#f0f0f0' if theme == 'light' else '#404040', foreground=fg)

    def update_command(self):
        with self.command_lock:
            self.current_command = self.command_entry.get()
        messagebox.showinfo("Updated", "Command updated successfully!")

    def start_typing(self):
        try:
            delay = float(self.delay.get())
            count = int(self.type_count.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
            return

        if self.typing_mode.get() == "count" and count < 1:
            messagebox.showerror("Error", "Count must be at least 1")
            return

        self.current_count = 0
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        threading.Thread(
            target=self.typing_loop,
            args=(delay, self.typing_mode.get(), count),
            daemon=True
        ).start()

    def typing_loop(self, delay, mode, count_limit):
        while not self.stop_event.is_set():
            with self.command_lock:
                command = self.current_command
            
            try:
                pyautogui.typewrite(command)
                pyautogui.press("enter")
            except Exception as e:
                messagebox.showerror("Typing Error", str(e))
                break
            
            self.current_count += 1

            if mode == "count" and self.current_count >= count_limit:
                self.stop_typing()
                break

            self.stop_event.wait(delay)

    def stop_typing(self):
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Stopped", "Auto typing has been stopped")

    def resize_image(self, image, size):
        return image.subsample(int(image.width() / size[0]), int(image.height() / size[1]))

def main():
    root = tk.Tk()
    AutoTyperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
