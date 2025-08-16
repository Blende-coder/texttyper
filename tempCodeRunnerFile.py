        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            self.settings_window.config(bg=bg_color)
            for widget in self.settings_window.winfo_children():
                if isinstance(widget, tk.Label) or isinstance(widget, tk.Checkbutton):
                    widget.config(bg=bg_color, fg=fg_color)
                elif isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                    widget.config(background=bg_color, foreground=fg_color)
            combostyle = ttk.Style()
            combostyle.theme_use("default")
            combostyle.configure("TCombobox", background=bg_color, foreground=fg_color)