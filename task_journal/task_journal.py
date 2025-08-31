import tkinter as tk
from tkinter import ttk
from datetime import datetime
from journal_processor import JournalProcessor

class TaskJournal:
    def __init__(self, root):
        self.root = root
        self.root.title("✍️ Daily Task Journal")
        self.root.geometry("680x930")
        
        # Set main window background color
        self.root.configure(bg='#1a1a2e')  # Deep blue background
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors and styles with dark theme
        self.style.configure('TFrame', background='#1a1a2e')
        self.style.configure('TLabelframe', background='#1a1a2e', bordercolor='#4a4e69')
        self.style.configure('TLabelframe.Label', 
                           font=('Helvetica', 12, 'bold'), 
                           background='#1a1a2e',
                           foreground='#e6e6e6')  # Light gray text
        
        # Button styling
        self.style.configure('TButton', 
                           font=('Helvetica', 11),
                           padding=10,
                           background='#4a4e69',
                           foreground='#ffffff')
        
        # Header styling
        self.style.configure('Header.TLabel', 
                           font=('Helvetica', 16, 'bold'),
                           background='#1a1a2e',
                           foreground='#ffffff')  # White text
        
        # Create a canvas with scrollbar - dark themed
        self.canvas = tk.Canvas(root, 
                              bg='#1a1a2e',
                              highlightthickness=0)  # Remove canvas border
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        
        # Configure scrollbar style
        self.style.configure('Vertical.TScrollbar',
                           background='#4a4e69',
                           troughcolor='#1a1a2e',
                           bordercolor='#4a4e69')
        
        # Create main container with padding
        container = ttk.Frame(self.canvas, padding="20")
        
        # Configure scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout for scrollbar and canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weight
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create window in canvas
        self.canvas.create_window((0, 0), window=container, anchor="nw")
        
        # Configure container
        container.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=container.winfo_width()
        ))
        
        # Rest of your code remains the same, just make sure it's all inside the container
        container.columnconfigure(0, weight=1)
        
        # Header first
        header = ttk.Label(container, text="Daily Productivity Journal", style='Header.TLabel')
        header.grid(row=0, column=0, pady=(0, 10))
        
        # Buttons frame - Below header
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=1, column=0, pady=(0, 20))
        
        # Center the buttons
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        
        # Add empty label for spacing on left
        ttk.Label(btn_frame, text="").grid(row=0, column=0)
        
        # Save and Clear buttons in the middle
        save_btn = ttk.Button(btn_frame, text="💾 Save Journal", command=self.save_journal)
        save_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="🗑️ Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=2, padx=5)
        
        # Add empty label for spacing on right
        ttk.Label(btn_frame, text="").grid(row=0, column=3)

        # Time blocks - Updated row numbers to start from 2
        self.time_blocks = [
            ("🌅 Morning Tasks", 2, '#16213e'),    # Dark navy blue
            ("☀️ Mid-day Tasks", 3, '#1b2430'),    # Dark slate blue
            ("🌙 Evening Tasks", 4, '#1f1d36')     # Dark purple blue
        ]
        self.entries = []
        self.entry_widgets = {}

        # Entry widget style
        self.style.configure('Dark.TEntry',
                           fieldbackground='#2a2a3e',
                           foreground='#ffffff',
                           insertcolor='#ffffff')

        for block, idx, color in self.time_blocks:
            # Block frame
            frame = ttk.LabelFrame(container, text=block, padding="15")
            frame.grid(row=idx, column=0, pady=10, sticky=(tk.W, tk.E))
            
            # Time selection frame styling
            time_frame = ttk.Frame(frame)
            time_frame.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
            
            # Time labels with light text
            ttk.Label(time_frame, 
                     text="Start Time:", 
                     font=('Helvetica', 10),
                     background='#1a1a2e',
                     foreground='#e6e6e6').grid(row=0, column=0, padx=(0, 5))
            
            # Style the time entry widgets
            start_time = ttk.Entry(time_frame, 
                                 width=10,
                                 font=('Helvetica', 10),
                                 style='Dark.TEntry')
            start_time.grid(row=0, column=1, padx=5, sticky=tk.W)
            start_time.insert(0, "00:00")
            
            ttk.Label(time_frame, 
                     text="End Time:",
                     font=('Helvetica', 10),
                     background='#1a1a2e',
                     foreground='#e6e6e6').grid(row=0, column=2, padx=(20, 5))
            
            end_time = ttk.Entry(time_frame,
                               width=10,
                               font=('Helvetica', 10),
                               style='Dark.TEntry')
            end_time.grid(row=0, column=3, padx=5, sticky=tk.W)
            end_time.insert(0, "00:00")
            
            # Text area with dark theme
            text_area = tk.Text(frame, 
                              height=8,
                              width=70,
                              font=('Helvetica', 11),
                              wrap=tk.WORD,
                              padx=10,
                              pady=10,
                              bg=color,              # Dark background
                              fg='#e6e6e6',          # Light gray text
                              insertbackground='#ffffff',  # White cursor
                              relief="flat")
            text_area.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
            
            # Add placeholder text and store widget references
            placeholder = f"Enter your {block.split(' ')[1].lower()} tasks here..."
            text_area.insert('1.0', placeholder)
            self.entry_widgets[block.split(" ")[1].lower()] = {
                "start": start_time,
                "end": end_time,
                "text": text_area
            }
            text_area.bind('<FocusIn>', lambda e, t=text_area, p=placeholder: self.on_focus_in(e, t, p))
            text_area.bind('<FocusOut>', lambda e, t=text_area, p=placeholder: self.on_focus_out(e, t, p))

        # Status bar - Update row number
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(container,
                             textvariable=self.status_var,
                             font=('Helvetica', 9),
                             background='#1a1a2e',
                             foreground='#b8b8b8')  # Light gray text
        status_bar.grid(row=6, column=0, pady=(0, 10))
        self.status_var.set("Ready to record your day! ✨")

        # Initialize the processor
        self.processor = JournalProcessor()

    def on_focus_in(self, event, text_widget, placeholder):
        if text_widget.get('1.0', 'end-1c') == placeholder:
            text_widget.delete('1.0', tk.END)

    def on_focus_out(self, event, text_widget, placeholder):
        if text_widget.get('1.0', 'end-1c').strip() == '':
            text_widget.insert('1.0', placeholder)

    def save_journal(self):
        """Save and process journal entries, then clear inputs if successful."""
        success, message = self.processor.process_and_save_journal(self)
        if success:
            self.clear_all()
            self.status_var.set(message + " ✅")
        else:
            self.status_var.set(message + " ❌")
        
    def clear_all(self):
        for child in self.root.winfo_children():
            if isinstance(child, tk.Text):
                child.delete('1.0', tk.END)
        self.status_var.set("All entries cleared! 🗑️")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskJournal(root)
    root.mainloop()
