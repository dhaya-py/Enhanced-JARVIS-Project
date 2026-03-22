"""
Jarvis GUI - Graphical User Interface
Tkinter-based desktop interface for Jarvis AI Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from core.engine import engine
from core.database import db
from config.settings import config

class JarvisGUI:
    """Main GUI for Jarvis AI Assistant"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS - AI Personal Assistant")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Color scheme
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eaeaea"
        self.accent_color = "#0f3460"
        self.button_color = "#16213e"
        self.active_color = "#00ff41"
        self.inactive_color = "#ff0000"
        
        # Configure root
        self.root.configure(bg=self.bg_color)
        
        # Setup GUI
        self._setup_gui()
        
        # Set engine callback
        engine.set_status_callback(self.update_status)
        
        # Update clock
        self._update_clock()
    
    def _setup_gui(self):
        """Setup all GUI components"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Title
        title_label = tk.Label(
            title_frame,
            text="J A R V I S",
            font=("Arial", 32, "bold"),
            bg=self.accent_color,
            fg=self.active_color
        )
        title_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="AI-Based Personal Assistant System",
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.fg_color
        )
        subtitle_label.pack()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status Frame
        status_frame = tk.Frame(main_container, bg=self.button_color, relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status Indicator
        self.status_indicator = tk.Canvas(
            status_frame,
            width=20,
            height=20,
            bg=self.button_color,
            highlightthickness=0
        )
        self.status_indicator.pack(side=tk.LEFT, padx=10, pady=10)
        self.status_circle = self.status_indicator.create_oval(2, 2, 18, 18, fill=self.inactive_color)
        
        # Status Label
        self.status_label = tk.Label(
            status_frame,
            text="Status: Stopped",
            font=("Arial", 14, "bold"),
            bg=self.button_color,
            fg=self.fg_color
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Clock Label
        self.clock_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 12),
            bg=self.button_color,
            fg=self.fg_color
        )
        self.clock_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Control Buttons Frame
        control_frame = tk.Frame(main_container, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Start Button
        self.start_button = tk.Button(
            control_frame,
            text="▶ START",
            font=("Arial", 14, "bold"),
            bg=self.active_color,
            fg="#000000",
            activebackground="#00cc33",
            width=15,
            height=2,
            command=self.start_jarvis,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop Button
        self.stop_button = tk.Button(
            control_frame,
            text="■ STOP",
            font=("Arial", 14, "bold"),
            bg=self.inactive_color,
            fg="#ffffff",
            activebackground="#cc0000",
            width=15,
            height=2,
            command=self.stop_jarvis,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Clear Logs Button
        self.clear_button = tk.Button(
            control_frame,
            text="🗑 Clear Logs",
            font=("Arial", 12),
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.accent_color,
            width=15,
            height=2,
            command=self.clear_logs,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.RIGHT, padx=10)
        
        # Log Frame
        log_frame = tk.LabelFrame(
            main_container,
            text="Activity Log",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.RAISED,
            bd=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log Text Area
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 10),
            bg="#0a0a0a",
            fg=self.active_color,
            insertbackground=self.active_color,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info Frame
        info_frame = tk.Frame(main_container, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Info Label
        info_label = tk.Label(
            info_frame,
            text="💡 Speak clearly into your microphone after clicking START",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        info_label.pack()
        
        # Initial log message
        self.log_message("Jarvis AI Assistant initialized")
        self.log_message("Click START to begin voice interaction")
    
    def _update_clock(self):
        """Update clock display"""
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%B %d, %Y")
        self.clock_label.config(text=f"{date_str} | {time_str}")
        self.root.after(1000, self._update_clock)
    
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_status(self, status: str):
        """Update status label and indicator"""
        if "Listening" in status:
            self.status_label.config(text=f"Status: {status}")
            self.status_indicator.itemconfig(self.status_circle, fill="#ffaa00")
        elif "Processing" in status:
            self.status_label.config(text=f"Status: {status}")
            self.status_indicator.itemconfig(self.status_circle, fill="#00aaff")
        elif "Responding" in status:
            self.status_label.config(text=f"Status: {status}")
            self.status_indicator.itemconfig(self.status_circle, fill="#aa00ff")
        elif "Started" in status or "Running" in status:
            self.status_label.config(text="Status: Active")
            self.status_indicator.itemconfig(self.status_circle, fill=self.active_color)
        elif "Stopped" in status:
            self.status_label.config(text="Status: Stopped")
            self.status_indicator.itemconfig(self.status_circle, fill=self.inactive_color)
        
        self.log_message(status)
    
    def start_jarvis(self):
        """Start Jarvis engine"""
        try:
            self.log_message("Starting Jarvis engine...")
            engine.start()
            
            # Update button states
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            self.log_message("✓ Jarvis is now active")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Jarvis: {e}")
            self.log_message(f"✗ Error: {e}")
    
    def stop_jarvis(self):
        """Stop Jarvis engine"""
        try:
            self.log_message("Stopping Jarvis engine...")
            engine.stop()
            
            # Update button states
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            self.log_message("✓ Jarvis stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop Jarvis: {e}")
            self.log_message(f"✗ Error: {e}")
    
    def clear_logs(self):
        """Clear activity logs"""
        response = messagebox.askyesno(
            "Clear Logs",
            "Are you sure you want to clear all activity logs?"
        )
        
        if response:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.log_message("Logs cleared")
    
    def on_closing(self):
        """Handle window closing"""
        if engine.is_active():
            response = messagebox.askyesno(
                "Confirm Exit",
                "Jarvis is still running. Do you want to stop it and exit?"
            )
            
            if response:
                engine.stop()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
