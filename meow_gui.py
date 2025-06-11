"""
MEOW GUI Application - Complete graphical interface for MEOW file operations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from meow_format import MeowFormat
from PIL import Image, ImageTk


class MeowGUI:
    """Complete GUI application for MEOW file format operations"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEOW File Format Manager")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        
        self.meow = MeowFormat()
        self.current_image = None
        self.photo_image = None
        self.zoom_level = 1.0
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Convert PNG to MEOW", command=self.convert_png_to_meow)
        file_menu.add_command(label="Convert MEOW to PNG", command=self.convert_meow_to_png)
        file_menu.add_separator()
        file_menu.add_command(label="Open MEOW File", command=self.open_meow_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About MEOW Format", command=self.show_about)
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Converter
        self.setup_converter_tab()
        
        # Tab 2: Viewer
        self.setup_viewer_tab()
        
        # Tab 3: File Info
        self.setup_info_tab()
    
    def setup_converter_tab(self):
        """Setup the converter tab"""
        converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(converter_frame, text="Converter")
        
        # Title
        title_label = ttk.Label(converter_frame, text="MEOW File Converter", font=("Arial", 16, "bold"))
        title_label.pack(pady=(20, 30))
        
        # PNG to MEOW section
        png_frame = ttk.LabelFrame(converter_frame, text="Convert PNG to MEOW", padding=20)
        png_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.png_input_var = tk.StringVar()
        self.png_output_var = tk.StringVar()
        
        ttk.Label(png_frame, text="Input PNG file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(png_frame, textvariable=self.png_input_var, width=50).grid(row=0, column=1, padx=(10, 5), pady=5)
        ttk.Button(png_frame, text="Browse", command=self.browse_png_input).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(png_frame, text="Output MEOW file:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(png_frame, textvariable=self.png_output_var, width=50).grid(row=1, column=1, padx=(10, 5), pady=5)
        ttk.Button(png_frame, text="Browse", command=self.browse_png_output).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Button(png_frame, text="Convert to MEOW", command=self.do_png_to_meow).grid(row=2, column=1, pady=20)
        
        # MEOW to PNG section
        meow_frame = ttk.LabelFrame(converter_frame, text="Convert MEOW to PNG", padding=20)
        meow_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.meow_input_var = tk.StringVar()
        self.meow_output_var = tk.StringVar()
        
        ttk.Label(meow_frame, text="Input MEOW file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(meow_frame, textvariable=self.meow_input_var, width=50).grid(row=0, column=1, padx=(10, 5), pady=5)
        ttk.Button(meow_frame, text="Browse", command=self.browse_meow_input).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(meow_frame, text="Output PNG file:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(meow_frame, textvariable=self.meow_output_var, width=50).grid(row=1, column=1, padx=(10, 5), pady=5)
        ttk.Button(meow_frame, text="Browse", command=self.browse_meow_output).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Button(meow_frame, text="Convert to PNG", command=self.do_meow_to_png).grid(row=2, column=1, pady=20)
        
        # Status text
        status_frame = ttk.LabelFrame(converter_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.status_text = tk.Text(status_frame, height=6, state=tk.DISABLED)
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_viewer_tab(self):
        """Setup the viewer tab"""
        viewer_frame = ttk.Frame(self.notebook)
        self.notebook.add(viewer_frame, text="Viewer")
        
        # Controls frame
        controls_frame = ttk.Frame(viewer_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="Open MEOW File", command=self.open_meow_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Reset Zoom", command=self.reset_zoom).pack(side=tk.LEFT, padx=5)
        
        self.zoom_label = ttk.Label(controls_frame, text="100%")
        self.zoom_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Image display area
        image_frame = ttk.LabelFrame(viewer_frame, text="Image Preview", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Canvas with scrollbars
        canvas_frame = ttk.Frame(image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.viewer_canvas = tk.Canvas(canvas_frame, bg='white')
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.viewer_canvas.yview)
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.viewer_canvas.xview)
        
        self.viewer_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.viewer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Show placeholder
        self.show_viewer_placeholder()
    
    def setup_info_tab(self):
        """Setup the file info tab"""
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="File Info")
        
        # File selection
        file_frame = ttk.Frame(info_frame)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(file_frame, text="MEOW File:").pack(side=tk.LEFT)
        self.info_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.info_file_var, width=50).pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_info_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Analyze", command=self.analyze_file).pack(side=tk.LEFT, padx=5)
        
        # Info display
        info_display_frame = ttk.LabelFrame(info_frame, text="File Information", padding=10)
        info_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.info_text = tk.Text(info_display_frame, state=tk.DISABLED)
        info_scroll = ttk.Scrollbar(info_display_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scroll.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Converter methods
    def browse_png_input(self):
        file_path = filedialog.askopenfilename(
            title="Select PNG file",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.png_input_var.set(file_path)
            # Auto-suggest output filename
            output_path = str(Path(file_path).with_suffix('.meow'))
            self.png_output_var.set(output_path)
    
    def browse_png_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Save MEOW file as",
            defaultextension=".meow",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        if file_path:
            self.png_output_var.set(file_path)
    
    def browse_meow_input(self):
        file_path = filedialog.askopenfilename(
            title="Select MEOW file",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        if file_path:
            self.meow_input_var.set(file_path)
            # Auto-suggest output filename
            output_path = str(Path(file_path).with_suffix('.png'))
            self.meow_output_var.set(output_path)
    
    def browse_meow_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Save PNG file as",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.meow_output_var.set(file_path)
    
    def do_png_to_meow(self):
        input_file = self.png_input_var.get().strip()
        output_file = self.png_output_var.get().strip()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input PNG file")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output MEOW file")
            return
        
        try:
            self.log_status(f"Converting {input_file} to MEOW format...")
            
            success = self.meow.png_to_meow(input_file, output_file)
            
            if success:
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                ratio = output_size / input_size if input_size > 0 else 0
                
                self.log_status("Conversion successful!")
                self.log_status(f"Original PNG: {input_size:,} bytes")
                self.log_status(f"MEOW file: {output_size:,} bytes")
                self.log_status(f"Size ratio: {ratio:.2f}x")
                self.log_status("-" * 40)
                
                messagebox.showinfo("Success", f"Successfully converted to {output_file}")
            else:
                self.log_status("Conversion failed!")
                messagebox.showerror("Error", "Conversion failed")
                
        except Exception as e:
            self.log_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def do_meow_to_png(self):
        input_file = self.meow_input_var.get().strip()
        output_file = self.meow_output_var.get().strip()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input MEOW file")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output PNG file")
            return
        
        try:
            self.log_status(f"Converting {input_file} to PNG format...")
            
            img = self.meow.meow_to_image(input_file)
            if img:
                img.save(output_file, 'PNG')
                
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                
                self.log_status("Conversion successful!")
                self.log_status(f"MEOW file: {input_size:,} bytes")
                self.log_status(f"PNG file: {output_size:,} bytes")
                self.log_status("-" * 40)
                
                messagebox.showinfo("Success", f"Successfully converted to {output_file}")
            else:
                self.log_status("Conversion failed!")
                messagebox.showerror("Error", "Failed to load MEOW file")
                
        except Exception as e:
            self.log_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def log_status(self, message):
        """Add a message to the status log"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    # Viewer methods
    def open_meow_file(self):
        file_path = filedialog.askopenfilename(
            title="Open MEOW file",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        if file_path:
            self.load_image_in_viewer(file_path)
    
    def load_image_in_viewer(self, file_path):
        try:
            self.current_image = self.meow.meow_to_image(file_path)
            if self.current_image:
                self.zoom_level = 1.0
                self.display_image_in_viewer()
                # Switch to viewer tab
                self.notebook.select(1)
            else:
                messagebox.showerror("Error", "Failed to load MEOW file")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
    
    def display_image_in_viewer(self):
        if self.current_image is None:
            return
        
        # Calculate display size
        display_width = int(self.current_image.width * self.zoom_level)
        display_height = int(self.current_image.height * self.zoom_level)
        
        # Resize image
        if self.zoom_level != 1.0:
            resized_image = self.current_image.resize((display_width, display_height), Image.NEAREST)
        else:
            resized_image = self.current_image
        
        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized_image)
        
        # Display on canvas
        self.viewer_canvas.delete("all")
        self.viewer_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.viewer_canvas.configure(scrollregion=self.viewer_canvas.bbox("all"))
        
        # Update zoom label
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
    
    def show_viewer_placeholder(self):
        self.viewer_canvas.delete("all")
        self.viewer_canvas.create_text(
            400, 300, text="No image loaded\nClick 'Open MEOW File' to load an image",
            font=("Arial", 16), fill="gray", justify=tk.CENTER
        )
    
    def zoom_in(self):
        if self.current_image:
            self.zoom_level = min(self.zoom_level * 1.25, 10.0)
            self.display_image_in_viewer()
    
    def zoom_out(self):
        if self.current_image:
            self.zoom_level = max(self.zoom_level * 0.8, 0.1)
            self.display_image_in_viewer()
    
    def reset_zoom(self):
        if self.current_image:
            self.zoom_level = 1.0
            self.display_image_in_viewer()
    
    # File info methods
    def browse_info_file(self):
        file_path = filedialog.askopenfilename(
            title="Select MEOW file to analyze",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        if file_path:
            self.info_file_var.set(file_path)
    
    def analyze_file(self):
        file_path = self.info_file_var.get().strip()
        if not file_path:
            messagebox.showerror("Error", "Please select a MEOW file to analyze")
            return
        
        try:
            info = self.meow.get_file_info(file_path)
            if info is None:
                messagebox.showerror("Error", "Not a valid MEOW file")
                return
            
            # Load metadata
            img = self.meow.meow_to_image(file_path)
            
            info_text = f"File: {os.path.basename(file_path)}\n"
            info_text += f"Full path: {file_path}\n\n"
            info_text += f"Format: {info['format']}\n"
            info_text += f"Dimensions: {info['width']} x {info['height']} pixels\n"
            info_text += f"Total pixels: {info['pixels']:,}\n"
            info_text += f"File size: {info['file_size']:,} bytes\n"
            info_text += f"Pixel data: {info['pixel_data_size']:,} bytes\n"
            info_text += f"Metadata: {info['metadata_size']:,} bytes\n\n"
            
            if self.meow.metadata:
                info_text += "Metadata:\n"
                info_text += "-" * 20 + "\n"
                for key, value in self.meow.metadata.items():
                    info_text += f"{key}: {value}\n"
            else:
                info_text += "No metadata found\n"
            
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            self.info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing file: {str(e)}")
    
    # Menu methods
    def convert_png_to_meow(self):
        self.notebook.select(0)  # Switch to converter tab
    
    def convert_meow_to_png(self):
        self.notebook.select(0)  # Switch to converter tab
    
    def show_about(self):
        about_text = """MEOW Image File Format

A Python implementation of a simple image file format.

Features:
• Cross-platform compatibility
• RGBA support with transparency
• Metadata support
• Binary storage for efficiency
• Simple and readable format specification

Created as an improved alternative to the BRUHIFF format.

Version 1.0"""
        
        messagebox.showinfo("About MEOW Format", about_text)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = MeowGUI()
    app.run()


if __name__ == "__main__":
    main()
