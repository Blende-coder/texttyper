import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import threading
import pyautogui
import webbrowser
import os
import ctypes
import sys

if sys.platform.startswith('linux'):
    os.environ["GDK_SCALE"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

if sys.platform == 'win32':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        master.title("Auto Typer")
        self.base_width = 300
        self.base_height = 140
        self.scale_factor = self.get_system_scaling()
        
        # Configure main window
        master.geometry(f"{int(self.base_width * self.scale_factor)}x{int(self.base_height * self.scale_factor)}")
        master.resizable(False, False)
        master.attributes("-topmost", True)
        self.center_window(master)

        # Create frames first
        control_frame = tk.Frame(master)
        mode_frame = tk.Frame(master)
        button_frame = tk.Frame(master)
        control_frame.pack(pady=5)
        mode_frame.pack(pady=5)
        button_frame.pack(pady=5)

        # Initialize variables
        self.transparent = False
        self.inactivity_timer = None
        self.current_command = "owo hunt"
        self.stop_event = threading.Event()
        self.command_lock = threading.Lock()
        self.delay = 12
        self.typing_mode = tk.StringVar(value="infinite")
        self.type_count = tk.IntVar(value=10)
        self.current_count = 0

        # Define font scaling
        self.default_font = ("Tahoma", int(9 * self.scale_factor))

        # Control elements
        self.command_label = tk.Label(
            control_frame, 
            text="TEXT:", 
            font=self.default_font
        )
        self.command_entry = tk.Entry(
            control_frame,
            width=20,
            font=self.default_font,
            bg="#F0F0F0",
            fg="#333333",
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.command_entry.insert(0, self.current_command)
        
        self.update_button = tk.Button(
            control_frame,
            text="OK",
            command=self.update_command,
            width=4,
            font=self.default_font,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )

        # Mode selection
        self.mode_selector = ttk.Combobox(
            mode_frame,
            textvariable=self.typing_mode,
            values=["infinite", "count"],
            state="readonly",
            width=8,
            font=self.default_font
        )
        self.count_entry = tk.Entry(
            mode_frame,
            textvariable=self.type_count,
            width=5,
            font=self.default_font,
            bg="#F0F0F0",
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.count_label = tk.Label(
            mode_frame,
            text="Times:",
            font=self.default_font
        )

        # Buttons
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_typing,
            width=8,
            font=self.default_font,
            bg="#4CAF50",
            fg="white",
            activebackground="#45A049",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_typing,
            state=tk.DISABLED,
            width=8,
            font=self.default_font,
            bg="#F44336",
            fg="white",
            activebackground="#D32F2F",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )

        # Grid layout
        self.command_label.grid(row=0, column=0, padx=2)
        self.command_entry.grid(row=0, column=1, padx=2)
        self.update_button.grid(row=0, column=2, padx=2)
        
        self.mode_selector.grid(row=0, column=0, padx=2)
        self.count_label.grid(row=0, column=1, padx=2)
        self.count_entry.grid(row=0, column=2, padx=2)
        
        self.start_button.grid(row=0, column=0, padx=5)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Hover effects
        def on_enter(e):
            e.widget['relief'] = tk.SUNKEN
            e.widget['bg'] = e.widget.cget('activebackground')
            
        def on_leave(e):
            e.widget['relief'] = tk.RAISED
            e.widget['bg'] = e.widget.cget('bg')

        for btn in [self.update_button, self.start_button, self.stop_button]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.config(cursor="hand2")

        # Menu system
        self.menu_bar = tk.Menu(master)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.open_file)
        file_menu.add_command(label="Export", command=self.export_content)
        file_menu.add_command(label="Save", command=self.open_youtube)
        
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Timer", command=self.set_timer)
        settings_menu.add_command(label="Color", command=self.change_color)
        
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        master.config(menu=self.menu_bar)

        # Transparency controls
        self.start_inactivity_timer()
        master.bind("<Button-1>", self.restore_opacity)
        master.bind("<Motion>", self.reset_inactivity_timer)
        master.bind("<KeyPress>", self.reset_inactivity_timer)
        master.bind("<ButtonPress>", self.reset_inactivity_timer)


        # Create widgets
        # Top row elements
        self.command_label = tk.Label( 
            text="TEXT:", 
            font=self.default_font
        )
        self.command_entry = tk.Entry(
            width=15,
            font=self.default_font,
            bg="#F0F0F0",
            fg="#333333",
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.command_entry.insert(0, self.current_command)
        
        self.update_button = tk.Button(
            text="OK",
            command=self.update_command,
            width=4,
            font=self.default_font,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )

        # Bottom row elements
        self.start_button = tk.Button(
            text="Start",
            command=self.start_typing,
            width=6,
            font=self.default_font,
            bg="#4CAF50",
            fg="white",
            activebackground="#45A049",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )
        self.stop_button = tk.Button(
            text="Stop",
            command=self.stop_typing,
            state=tk.DISABLED,
            width=6,
            font=self.default_font,
            bg="#F44336",
            fg="white",
            activebackground="#D32F2F",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=2
        )

        # Grid layout
        self.command_label.grid(row=0, column=0, padx=2)
        self.command_entry.grid(row=0, column=1, padx=2)
        self.update_button.grid(row=0, column=2, padx=2)
        self.start_button.grid(row=0, column=0, padx=5)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Hover effects
        def on_enter(e):
            e.widget['relief'] = tk.SUNKEN
            e.widget['bg'] = e.widget.cget('activebackground')
            
        def on_leave(e):
            e.widget['relief'] = tk.RAISED
            e.widget['bg'] = e.widget.cget('bg')

        for btn in [self.update_button, self.start_button, self.stop_button]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.config(cursor="hand2")

        # Menu system
        self.menu_bar = tk.Menu(master)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Import", command=self.open_file)
        file_menu.add_command(label="Export", command=self.export_content)
        file_menu.add_command(label="Save", command=self.open_youtube)
        
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Timer", command=self.set_timer)
        settings_menu.add_command(label="Color", command=self.change_color)
        
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        master.config(menu=self.menu_bar)

        # Transparency controls
        self.start_inactivity_timer()
        master.bind("<Button-1>", self.restore_opacity)
        master.bind("<Motion>", self.reset_inactivity_timer)
        master.bind("<KeyPress>", self.reset_inactivity_timer)
        master.bind("<ButtonPress>", self.reset_inactivity_timer)

    def get_system_scaling(self):
        if sys.platform == 'win32':
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return user32.GetDpiForSystem() / 96
        return 1.0

    def center_window(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f"+{x}+{y}")

    def start_inactivity_timer(self):
        self.inactivity_timer = self.master.after(120000, self.make_transparent)

    def reset_inactivity_timer(self, event=None):
        if self.inactivity_timer:
            self.master.after_cancel(self.inactivity_timer)
        if self.transparent:
            self.restore_opacity()
        self.start_inactivity_timer()

    def make_transparent(self):
        self.transparent = True
        self.master.attributes("-alpha", 0.5)

    def restore_opacity(self, event=None):
        self.transparent = False
        self.master.attributes("-alpha", 1.0)
        self.reset_inactivity_timer()

    def update_command(self):
        new_command = self.command_entry.get()
        with self.command_lock:
            self.current_command = new_command

    def start_typing(self):
        try:
            if self.typing_mode.get() == "count":
                if self.type_count.get() < 1:
                    messagebox.showerror("Error", "Count must be at least 1")
                    return
                self.current_count = 0
                
            self.stop_event.clear()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.mode_selector.config(state="disabled")
            self.count_entry.config(state="disabled")
            
            self.typing_thread = threading.Thread(target=self.typing_loop)
            self.typing_thread.start()
        except tk.TclError:
            messagebox.showerror("Error", "Invalid count value")

    def stop_typing(self):
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.mode_selector.config(state="readonly")
        self.count_entry.config(state="normal")

    def typing_loop(self):
        mode = self.typing_mode.get()
        max_count = self.type_count.get() if mode == "count" else None
        
        while not self.stop_event.is_set():
            if self.stop_event.wait(self.delay):
                break
            
            with self.command_lock:
                command = self.current_command
                
            pyautogui.typewrite(command)
            pyautogui.hotkey('enter')
            
            if mode == "count":
                self.current_count += 1
                if self.current_count >= max_count:
                    self.stop_typing()
                    break

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read(100)
                    self.command_entry.delete(0, tk.END)
                    self.command_entry.insert(0, content)
                    self.update_command()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def export_content(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.current_command)
                messagebox.showinfo("Success", "Content exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export content: {e}")

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com/@zarusw")

    def set_timer(self):
        self.timer_dialog = tk.Toplevel(self.master)
        self.timer_dialog.title("Set Timer")
        self.timer_dialog.attributes("-topmost", True)
        self.timer_dialog.resizable(False, False)
        
        if sys.platform == 'win32':
            self.timer_dialog.attributes("-toolwindow", 1)
        if sys.platform.startswith('linux') or sys.platform == 'darwin':
            self.timer_dialog.transient(self.master)
            self.timer_dialog.grab_set()

        self.center_child_window(self.timer_dialog)
        
        tk.Label(self.timer_dialog, text="Delay (1-60s):").pack(pady=5)
        self.delay_entry = tk.Entry(self.timer_dialog, width=10)
        self.delay_entry.pack(pady=5)
        self.delay_entry.insert(0, str(self.delay))
        
        btn_frame = tk.Frame(self.timer_dialog)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="OK", command=self.update_delay).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.timer_dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def center_child_window(self, child_window):
        self.master.update_idletasks()
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()
        
        child_window.update_idletasks()
        child_width = child_window.winfo_reqwidth()
        child_height = child_window.winfo_reqheight()
        
        x = main_x + (main_width // 2) - (child_width // 2)
        y = main_y + (main_height // 2) - (child_height // 2)
        child_window.geometry(f"+{x}+{y}")

    def update_delay(self):
        try:
            new_delay = int(self.delay_entry.get())
            if 1 <= new_delay <= 60:
                self.delay = new_delay
                messagebox.showinfo("Timer Updated", f"Delay set to {self.delay}s")
                self.timer_dialog.destroy()
            else:
                messagebox.showerror("Error", "Please enter a value between 1 and 60")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number")

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.master.config(bg=color)
            self.command_label.config(bg=color)

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("D:\\code\\texttyper\\text_typer_GUI.ico")
    app = AutoTyperApp(root)
    root.mainloop()