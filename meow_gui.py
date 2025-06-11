"""
Steganographic MEOW GUI - AI-Optimized Image Viewer
Showcases AI features and true cross-compatibility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import json
from meow_format import MeowFormat, smart_fallback_loader


class MeowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganographic MEOW Viewer - True Cross-Compatibility")
        self.root.geometry("1200x800")
        
        # Variables
        self.current_image = None
        self.current_meow = None
        self.ai_metadata = None
        self.viewer_capabilities = {'supports_meow': True, 'universal_compatibility': True}
        
        # Setup GUI
        self.setup_menu()
        self.setup_main_interface()
        self.setup_ai_panel()
        self.update_status()
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Other Image...", command=self.open_image)
        file_menu.add_command(label="Open MEOW...", command=self.open_meow)
        file_menu.add_separator()
        file_menu.add_command(label="Convert to Steganographic MEOW...", command=self.convert_to_meow)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Show AI Features", command=self.toggle_ai_panel)
        view_menu.add_command(label="Viewer Capabilities", command=self.show_capabilities)
        
        # AI menu
        ai_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="AI", menu=ai_menu)
        ai_menu.add_command(label="Export Features...", command=self.export_ai_features)
        ai_menu.add_command(label="Import Annotations...", command=self.import_annotations)
    
    def setup_main_interface(self):
        """Setup main interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for image
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Image canvas with scrollbars
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas = tk.Canvas(canvas_frame, bg='white')
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        
        self.image_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(left_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Control buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Open Other Image", command=self.open_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Open MEOW", command=self.open_meow).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Convert to MEOW", command=self.convert_to_meow).pack(side=tk.LEFT, padx=2)
        
        # Separator
        separator = ttk.Separator(main_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
    
    def setup_ai_panel(self):
        """Setup AI features panel"""
        # Right panel for AI features
        self.ai_frame = ttk.Frame(self.root)
        self.ai_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # AI Features label
        ai_title = ttk.Label(self.ai_frame, text="AI Features", font=('Arial', 12, 'bold'))
        ai_title.pack(pady=(0, 10))
        
        # Notebook for tabbed AI info
        self.ai_notebook = ttk.Notebook(self.ai_frame)
        self.ai_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Metadata tab
        self.setup_metadata_tab()
        
        # Objects tab
        self.setup_objects_tab()
        
        # Features tab
        self.setup_features_tab()
        
        # Performance tab
        self.setup_performance_tab()
    
    def setup_metadata_tab(self):
        """Setup metadata display tab"""
        metadata_frame = ttk.Frame(self.ai_notebook)
        self.ai_notebook.add(metadata_frame, text="Metadata")
        
        # Scrollable text widget for metadata
        text_frame = ttk.Frame(metadata_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.metadata_text = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)
        metadata_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.metadata_text.yview)
        self.metadata_text.configure(yscrollcommand=metadata_scroll.set)
        
        self.metadata_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        metadata_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_objects_tab(self):
        """Setup object detection display tab"""
        objects_frame = ttk.Frame(self.ai_notebook)
        self.ai_notebook.add(objects_frame, text="Objects")
        
        # Objects treeview
        self.objects_tree = ttk.Treeview(objects_frame, columns=('Class', 'Confidence', 'BBox'), show='tree headings')
        self.objects_tree.heading('#0', text='ID')
        self.objects_tree.heading('Class', text='Class')
        self.objects_tree.heading('Confidence', text='Confidence')
        self.objects_tree.heading('BBox', text='Bounding Box')
        
        self.objects_tree.column('#0', width=50)
        self.objects_tree.column('Class', width=100)
        self.objects_tree.column('Confidence', width=80)
        self.objects_tree.column('BBox', width=120)
        
        objects_scroll = ttk.Scrollbar(objects_frame, orient=tk.VERTICAL, command=self.objects_tree.yview)
        self.objects_tree.configure(yscrollcommand=objects_scroll.set)
        
        self.objects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        objects_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.objects_tree.bind('<<TreeviewSelect>>', self.on_object_select)
    
    def setup_features_tab(self):
        """Setup features display tab"""
        features_frame = ttk.Frame(self.ai_notebook)
        self.ai_notebook.add(features_frame, text="Features")
        
        # Feature maps info
        feature_info = ttk.LabelFrame(features_frame, text="Available Features")
        feature_info.pack(fill=tk.X, pady=5)
        
        self.features_var = tk.StringVar()
        features_label = ttk.Label(feature_info, textvariable=self.features_var, wraplength=250)
        features_label.pack(padx=5, pady=5)
        
        # Preprocessing params
        preprocessing_info = ttk.LabelFrame(features_frame, text="Preprocessing Parameters")
        preprocessing_info.pack(fill=tk.X, pady=5)
        
        self.preprocessing_text = tk.Text(preprocessing_info, height=8, wrap=tk.WORD)
        self.preprocessing_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Attention regions
        attention_info = ttk.LabelFrame(features_frame, text="Attention Regions")
        attention_info.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.attention_tree = ttk.Treeview(attention_info, columns=('Area', 'Saliency'), show='tree headings')
        self.attention_tree.heading('#0', text='Region')
        self.attention_tree.heading('Area', text='Area')
        self.attention_tree.heading('Saliency', text='Avg Saliency')
        
        self.attention_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_performance_tab(self):
        """Setup performance info tab"""
        perf_frame = ttk.Frame(self.ai_notebook)
        self.ai_notebook.add(perf_frame, text="Performance")
        
        # File size comparison
        size_info = ttk.LabelFrame(perf_frame, text="File Size Analysis")
        size_info.pack(fill=tk.X, pady=5)
        
        self.size_text = tk.Text(size_info, height=6, wrap=tk.WORD)
        self.size_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Chunks information
        chunks_info = ttk.LabelFrame(perf_frame, text="MEOW Chunks")
        chunks_info.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.chunks_tree = ttk.Treeview(chunks_info, columns=('Size', 'Description'), show='tree headings')
        self.chunks_tree.heading('#0', text='Chunk Type')
        self.chunks_tree.heading('Size', text='Size (bytes)')
        self.chunks_tree.heading('Description', text='Description')
        
        self.chunks_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # AI benefits
        benefits_info = ttk.LabelFrame(perf_frame, text="AI Benefits")
        benefits_info.pack(fill=tk.X, pady=5)
        
        benefits_text = tk.Text(benefits_info, height=4, wrap=tk.WORD)
        benefits_text.pack(fill=tk.X, padx=5, pady=5)
        benefits_text.insert(tk.END, "• Pre-computed features reduce processing time\n")
        benefits_text.insert(tk.END, "• Multi-resolution pyramid supports various models\n")
        benefits_text.insert(tk.END, "• Embedded attention guides model focus\n")
        benefits_text.insert(tk.END, "• Cross-compatible with standard viewers")
        benefits_text.config(state=tk.DISABLED)
    
    def open_image(self):
        """Open standard image file"""
        file_path = filedialog.askopenfilename(
            title="Open Other Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.current_image = Image.open(file_path)
                self.display_image(self.current_image)
                self.current_meow = None
                self.ai_metadata = None
                self.update_ai_display()
                self.update_status(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
    
    def open_meow(self):
        """Open MEOW file"""
        file_path = filedialog.askopenfilename(
            title="Open MEOW File",
            filetypes=[
                ("MEOW files", "*.meow"),
                ("All files", "*.*")
            ]        )
        
        if file_path:
            try:
                # Use smart fallback loader
                self.current_image = smart_fallback_loader(file_path)
                  # Try to load MEOW data if it's a MEOW file
                if file_path.lower().endswith('.meow'):
                    self.current_meow = MeowFormat()
                    img, meow_data = self.current_meow.load_steganographic_meow(file_path)
                    if meow_data:
                        # Store the extracted MEOW data for display
                        self.extracted_meow_data = meow_data
                        
                        # Populate AI metadata from extracted data
                        from meow_format import AIMetadata
                        self.ai_metadata = AIMetadata()
                        
                        # Extract AI annotations if present
                        if 'ai_annotations' in meow_data:
                            annotations = meow_data['ai_annotations']
                            if 'object_classes' in annotations:
                                self.ai_metadata.object_classes = annotations['object_classes']
                            if 'bounding_boxes' in annotations:
                                self.ai_metadata.bounding_boxes = annotations['bounding_boxes']
                            if 'preprocessing_params' in annotations:
                                self.ai_metadata.preprocessing_params = annotations['preprocessing_params']
                        
                        # Extract features if present
                        if 'features' in meow_data:
                            features = meow_data['features']
                            self.ai_metadata.edge_density = features.get('edge_density')
                            self.ai_metadata.complexity_map = {'brightness': features.get('brightness')}
                    else:
                        self.extracted_meow_data = None
                
                self.display_image(self.current_image)
                self.update_ai_display()
                self.update_status(f"Loaded MEOW: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open MEOW file: {e}")
    
    def convert_to_meow(self):
        """Convert current image to Enhanced MEOW"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="Save Enhanced MEOW File",
            defaultextension=".meow",
            filetypes=[("MEOW files", "*.meow"), ("All files", "*.*")]
        )
        
        if output_path:
            try:                # Create enhanced MEOW with sample AI annotations
                meow = MeowFormat()
                
                # Generate sample annotations based on image
                ai_annotations = self.generate_sample_annotations()
                
                # Save temporary PNG for conversion
                temp_png = "temp_convert.png"
                self.current_image.save(temp_png, "PNG")
                
                success = meow.create_steganographic_meow(temp_png, output_path, 
                                                        ai_annotations=ai_annotations)
                
                # Clean up temp file
                if os.path.exists(temp_png):
                    os.remove(temp_png)
                
                if success:
                    messagebox.showinfo("Success", f"Steganographic MEOW saved: {output_path}")
                    
                    # Reload to show AI features
                    self.current_meow = meow
                    self.ai_metadata = meow.get_ai_metadata()
                    self.update_ai_display()
                else:
                    messagebox.showerror("Error", "Failed to create Steganographic MEOW file")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Conversion failed: {e}")
    
    def generate_sample_annotations(self):
        """Generate sample AI annotations for demonstration"""
        if not self.current_image:
            return {}
        
        width, height = self.current_image.size
        
        return {
            'object_classes': ['background', 'foreground'],
            'bounding_boxes': [
                {
                    'class': 'region_of_interest',
                    'bbox': [width//4, height//4, 3*width//4, 3*height//4],
                    'confidence': 0.85
                }
            ],
            'preprocessing_params': {
                'mean_rgb': [0.485, 0.456, 0.406],
                'std_rgb': [0.229, 0.224, 0.225],
                'input_size': [224, 224],
                'normalization': 'imagenet'
            }
        }
    
    def display_image(self, image):
        """Display image on canvas"""
        if image:
            # Resize image if too large
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                img_width, img_height = image.size
                
                # Calculate scale to fit canvas
                scale_x = canvas_width / img_width
                scale_y = canvas_height / img_height
                scale = min(scale_x, scale_y, 1.0)  # Don't scale up
                
                if scale < 1.0:
                    new_size = (int(img_width * scale), int(img_height * scale))
                    display_image = image.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    display_image = image
            else:
                display_image = image
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and display image
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
              # Update scroll region
            self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
    
    def update_ai_display(self):
        """Update AI features display"""
        # Clear all displays
        self.metadata_text.delete(1.0, tk.END)
        self.objects_tree.delete(*self.objects_tree.get_children())
        self.attention_tree.delete(*self.attention_tree.get_children())
        self.preprocessing_text.delete(1.0, tk.END)
        self.chunks_tree.delete(*self.chunks_tree.get_children())
        self.size_text.delete(1.0, tk.END)
        
        # Check if we have steganographic MEOW data
        if not hasattr(self, 'extracted_meow_data') or not self.extracted_meow_data:
            self.metadata_text.insert(tk.END, "No AI metadata available.\nLoad a Steganographic MEOW file to see AI features.")
            self.features_var.set("No features available")
            return
        
        meow_data = self.extracted_meow_data
        
        # Update metadata
        metadata_info = f"Steganographic MEOW Data\n{'='*25}\n"
        metadata_info += f"Format Version: {meow_data.get('version', 'Unknown')}\n"
        metadata_info += f"Creation Date: {meow_data.get('creation_date', 'Unknown')}\n"
        
        if 'ai_annotations' in meow_data:
            annotations = meow_data['ai_annotations']
            if 'object_classes' in annotations:
                metadata_info += f"Object Classes: {', '.join(annotations['object_classes'])}\n"
            if 'source' in annotations:
                metadata_info += f"Source: {annotations['source']}\n"
            if 'ai_enhanced' in annotations:
                metadata_info += f"AI Enhanced: {annotations['ai_enhanced']}\n"
        
        if 'features' in meow_data:
            features = meow_data['features']
            metadata_info += f"Features Available: {len(features)} types\n"
            
        self.metadata_text.insert(tk.END, metadata_info)
        
        # Update objects (from AI annotations)
        if 'ai_annotations' in meow_data and 'bounding_boxes' in meow_data['ai_annotations']:
            for i, bbox_info in enumerate(meow_data['ai_annotations']['bounding_boxes']):
                obj_class = bbox_info.get('class', 'Unknown')
                confidence = bbox_info.get('confidence', 0.0)
                bbox = bbox_info.get('bbox', [])
                bbox_str = f"[{', '.join(map(str, bbox))}]" if bbox else "N/A"
                
                self.objects_tree.insert('', tk.END, text=str(i+1),
                                       values=(obj_class, f"{confidence:.2f}", bbox_str))
        
        # Update features
        features_list = []
        if 'features' in meow_data:
            features_list = list(meow_data['features'].keys())
        
        self.features_var.set(f"Available: {', '.join(features_list) if features_list else 'None'}")
        
        # Update preprocessing parameters
        if 'ai_annotations' in meow_data and 'preprocessing_params' in meow_data['ai_annotations']:
            preprocessing_info = json.dumps(meow_data['ai_annotations']['preprocessing_params'], indent=2)
            self.preprocessing_text.insert(tk.END, preprocessing_info)
        
        # Update attention data
        if 'attention_maps' in meow_data:
            attention_data = meow_data['attention_maps']
            for key, value in attention_data.items():
                if isinstance(value, (int, float)):
                    self.attention_tree.insert('', tk.END, text=key,
                                             values=("N/A", f"{value:.3f}"))
          # Update steganographic information instead of chunks
        stego_info = "Steganographic Storage\n" + "="*25 + "\n\n"
        
        # Calculate hidden data size
        hidden_data_size = len(json.dumps(meow_data).encode())
        stego_info += f"Hidden Data Size: {hidden_data_size:,} bytes\n"
        stego_info += f"Storage Method: LSB Steganography\n"
        stego_info += f"Channels Used: RGB (2 bits each)\n"
        stego_info += f"Capacity Used: {hidden_data_size} bytes\n"
          # Add data breakdown
        self.chunks_tree.insert('', tk.END, text="Features",
                               values=(f"{len(str(meow_data.get('features', {})))} chars", "AI feature data"))
        self.chunks_tree.insert('', tk.END, text="Attention",
                               values=(f"{len(str(meow_data.get('attention_maps', {})))} chars", "Attention maps"))
        self.chunks_tree.insert('', tk.END, text="Annotations",
                               values=(f"{len(str(meow_data.get('ai_annotations', {})))} chars", "AI annotations"))
        
        self.size_text.insert(tk.END, stego_info)
    
    def on_object_select(self, event):
        """Handle object selection in treeview"""
        selection = self.objects_tree.selection()
        if selection:
            # In a full implementation, this could highlight the bounding box on the image
            pass
    
    def toggle_ai_panel(self):
        """Toggle AI panel visibility"""
        if self.ai_frame.winfo_viewable():
            self.ai_frame.pack_forget()
        else:
            self.ai_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    
    def show_capabilities(self):
        """Show viewer capabilities dialog"""
        cap_window = tk.Toplevel(self.root)
        cap_window.title("Viewer Capabilities")
        cap_window.geometry("400x300")
        
        cap_text = tk.Text(cap_window, wrap=tk.WORD)
        cap_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        cap_info = "Enhanced MEOW Viewer Capabilities\n"
        cap_info += "="*40 + "\n\n"
        
        for capability, supported in self.viewer_capabilities.items():
            status = "✓ Supported" if supported else "✗ Not Supported"
            cap_info += f"{capability}: {status}\n"
        
        cap_info += "\nFeatures:\n"
        cap_info += "• Cross-compatible fallback loading\n"
        cap_info += "• AI metadata visualization\n"
        cap_info += "• Object detection display\n"
        cap_info += "• Feature map information\n"
        cap_info += "• Performance analysis\n"
        cap_info += "• Chunk-based architecture\n"
        
        cap_text.insert(tk.END, cap_info)
        cap_text.config(state=tk.DISABLED)
    
    def export_ai_features(self):
        """Export AI features to JSON"""
        if not self.ai_metadata:
            messagebox.showwarning("Warning", "No AI metadata to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export AI Features",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                ai_data = {
                    'object_classes': self.ai_metadata.object_classes,
                    'bounding_boxes': self.ai_metadata.bounding_boxes,
                    'preprocessing_params': self.ai_metadata.preprocessing_params
                }
                
                with open(file_path, 'w') as f:
                    json.dump(ai_data, f, indent=2)
                
                messagebox.showinfo("Success", f"AI features exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def import_annotations(self):
        """Import AI annotations from JSON"""
        file_path = filedialog.askopenfilename(
            title="Import AI Annotations",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    annotations = json.load(f)
                
                messagebox.showinfo("Info", "AI annotation import not yet implemented in this demo")
                
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")
    
    def update_status(self, message="Ready"):
        """Update status bar"""
        if self.current_image:
            width, height = self.current_image.size
            mode = self.current_image.mode
            ai_status = " | AI Enhanced" if self.current_meow else " | Standard Format"
            self.status_var.set(f"{message} | {width}x{height} {mode}{ai_status}")
        else:
            self.status_var.set(message)


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        if os.path.exists("assets/logos/logo.png"):
            icon_img = tk.PhotoImage(file="assets/logos/logo.png")
            root.iconphoto(True, icon_img)
    except:
        pass
    
    app = MeowGUI(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
