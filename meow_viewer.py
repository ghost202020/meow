"""
MEOW File Viewer - Simple image viewer for MEOW format files
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from meow_format import MeowFormat


class MeowViewer:
    """Simple viewer for MEOW format images"""
    
    def __init__(self, file_path: str = None):
        self.root = tk.Tk()
        self.root.title("MEOW Image Viewer")
        self.root.geometry("800x600")
        
        self.meow = MeowFormat()
        self.current_image = None
        self.photo_image = None
        
        self.setup_ui()
        
        if file_path:
            self.load_image(file_path)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create info frame
        info_frame = ttk.LabelFrame(main_frame, text="Image Information", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=4, state=tk.DISABLED)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create image frame
        image_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars for image display
        canvas_frame = ttk.Frame(image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Open MEOW File", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save as PNG", command=self.save_as_png).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset Zoom", command=self.reset_zoom).pack(side=tk.LEFT, padx=5)
        
        self.zoom_level = 1.0
        self.zoom_label = ttk.Label(button_frame, text="100%")
        self.zoom_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Initially show placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder text when no image is loaded"""
        self.update_info("No image loaded. Click 'Open MEOW File' to load an image.")
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() // 2, 
            self.canvas.winfo_height() // 2,
            text="No image loaded", 
            font=("Arial", 24), 
            fill="gray"
        )
    
    def open_file(self):
        """Open file dialog and load selected MEOW file"""
        from tkinter.filedialog import askopenfilename
        
        file_path = askopenfilename(
            title="Open MEOW File",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path: str):
        """Load and display a MEOW image file"""
        try:
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {file_path}")
                return
            
            # Load the image
            self.current_image = self.meow.meow_to_image(file_path)
            
            if self.current_image is None:
                messagebox.showerror("Error", f"Failed to load MEOW file: {file_path}")
                return
            
            # Update window title
            self.root.title(f"MEOW Image Viewer - {os.path.basename(file_path)}")
            
            # Display image information
            info = self.meow.get_file_info(file_path)
            info_text = f"File: {os.path.basename(file_path)}\n"
            info_text += f"Dimensions: {info['width']} x {info['height']} pixels\n"
            info_text += f"File size: {info['file_size']:,} bytes\n"
            info_text += f"Format: {info['format']}"
            
            if self.meow.metadata:
                info_text += "\n\nMetadata:\n"
                for key, value in self.meow.metadata.items():
                    info_text += f"  {key}: {value}\n"
            
            self.update_info(info_text)
            
            # Reset zoom and display image
            self.zoom_level = 1.0
            self.display_image()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
    
    def display_image(self):
        """Display the current image on the canvas"""
        if self.current_image is None:
            return
        
        # Calculate display size
        display_width = int(self.current_image.width * self.zoom_level)
        display_height = int(self.current_image.height * self.zoom_level)
        
        # Resize image for display
        if self.zoom_level != 1.0:
            resized_image = self.current_image.resize((display_width, display_height), Image.NEAREST)
        else:
            resized_image = self.current_image
        
        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized_image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Update zoom label
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
    
    def update_info(self, text: str):
        """Update the information text area"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state=tk.DISABLED)
    
    def zoom_in(self):
        """Zoom in on the image"""
        if self.current_image:
            self.zoom_level = min(self.zoom_level * 1.25, 10.0)
            self.display_image()
    
    def zoom_out(self):
        """Zoom out on the image"""
        if self.current_image:
            self.zoom_level = max(self.zoom_level * 0.8, 0.1)
            self.display_image()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        if self.current_image:
            self.zoom_level = 1.0
            self.display_image()
    
    def save_as_png(self):
        """Save current image as PNG"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded to save")
            return
        
        from tkinter.filedialog import asksaveasfilename
        
        file_path = asksaveasfilename(
            title="Save as PNG",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.current_image.save(file_path, 'PNG')
                messagebox.showinfo("Success", f"Image saved as: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def run(self):
        """Start the viewer application"""
        self.root.mainloop()


def main():
    """Main entry point for the viewer"""
    file_path = None
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        # Validate file exists and has correct extension
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            return
        
        if not file_path.lower().endswith('.meow'):
            print("Error: File must have .meow extension")
            return
    
    # Create and run viewer
    viewer = MeowViewer(file_path)
    viewer.run()


if __name__ == "__main__":
    main()
