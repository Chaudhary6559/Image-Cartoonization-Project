import tkinter as tk
from tkinter import filedialog, ttk, Scale, HORIZONTAL
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from cartoonizer import Cartoonizer

class CartoonGUI:
    """
    GUI application for image cartoonization.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Image Cartoonizer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Set application icon
        # self.root.iconbitmap("icon.ico")  # Uncomment if you have an icon file
        
        # Initialize cartoonizer
        self.cartoonizer = Cartoonizer()
        
        # Initialize variables
        self.original_image = None
        self.cartoon_image = None
        self.current_image_path = None
        self.tk_original = None
        self.tk_cartoon = None
        
        # Create main frames
        self.create_frames()
        
        # Create widgets
        self.create_menu()
        self.create_image_display()
        self.create_controls()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                  bg="#34495e", fg="white")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_frames(self):
        """Create the main frames for the GUI."""
        # Top frame for menu and buttons
        self.top_frame = tk.Frame(self.root, bg="#2c3e50")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Middle frame for images
        self.middle_frame = tk.Frame(self.root, bg="#2c3e50")
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for original image
        self.left_frame = tk.LabelFrame(self.middle_frame, text="Original Image", 
                                       bg="#34495e", fg="white", font=("Arial", 12))
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right frame for cartoon image
        self.right_frame = tk.LabelFrame(self.middle_frame, text="Cartoonized Image", 
                                        bg="#34495e", fg="white", font=("Arial", 12))
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom frame for controls
        self.bottom_frame = tk.LabelFrame(self.root, text="Cartoonization Controls", 
                                         bg="#34495e", fg="white", font=("Arial", 12))
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
    def create_menu(self):
        """Create the menu bar."""
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Image", command=self.open_image)
        self.file_menu.add_command(label="Save Cartoon", command=self.save_cartoon)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        self.root.config(menu=self.menu_bar)
        
        # Quick access buttons
        self.open_button = tk.Button(self.top_frame, text="Open Image", 
                                    command=self.open_image, bg="#3498db", fg="white",
                                    font=("Arial", 10, "bold"), padx=10, pady=5)
        self.open_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(self.top_frame, text="Save Cartoon", 
                                    command=self.save_cartoon, bg="#2ecc71", fg="white",
                                    font=("Arial", 10, "bold"), padx=10, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(self.top_frame, text="Reset Parameters", 
                                     command=self.reset_parameters, bg="#e74c3c", fg="white",
                                     font=("Arial", 10, "bold"), padx=10, pady=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
    def create_image_display(self):
        """Create the image display areas."""
        # Original image display
        self.original_canvas = tk.Canvas(self.left_frame, bg="#2c3e50", 
                                        highlightthickness=0)
        self.original_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Cartoon image display
        self.cartoon_canvas = tk.Canvas(self.right_frame, bg="#2c3e50", 
                                       highlightthickness=0)
        self.cartoon_canvas.pack(fill=tk.BOTH, expand=True)
        
    def create_controls(self):
        """Create the control panel with sliders."""
        # Create a frame for each row of controls
        control_frames = []
        for i in range(3):
            frame = tk.Frame(self.bottom_frame, bg="#34495e")
            frame.pack(fill=tk.X, padx=10, pady=5)
            control_frames.append(frame)
        
        # Line size slider
        tk.Label(control_frames[0], text="Edge Thickness:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.line_size_var = tk.IntVar(value=self.cartoonizer.line_size)
        self.line_size_slider = Scale(control_frames[0], from_=1, to=15, 
                                     orient=HORIZONTAL, variable=self.line_size_var,
                                     command=self.update_cartoon, length=200,
                                     bg="#34495e", fg="white", troughcolor="#2c3e50",
                                     highlightthickness=0)
        self.line_size_slider.pack(side=tk.LEFT, padx=5)
        
        # Bilateral filter diameter
        tk.Label(control_frames[0], text="Smoothing:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.bilateral_d_var = tk.IntVar(value=self.cartoonizer.bilateral_filter_d)
        self.bilateral_d_slider = Scale(control_frames[0], from_=5, to=15, 
                                       orient=HORIZONTAL, variable=self.bilateral_d_var,
                                       command=self.update_cartoon, length=200,
                                       bg="#34495e", fg="white", troughcolor="#2c3e50",
                                       highlightthickness=0)
        self.bilateral_d_slider.pack(side=tk.LEFT, padx=5)
        
        # Bilateral sigma color
        tk.Label(control_frames[1], text="Color Smoothing:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.bilateral_color_var = tk.IntVar(value=self.cartoonizer.bilateral_sigma_color)
        self.bilateral_color_slider = Scale(control_frames[1], from_=10, to=150, 
                                          orient=HORIZONTAL, variable=self.bilateral_color_var,
                                          command=self.update_cartoon, length=200,
                                          bg="#34495e", fg="white", troughcolor="#2c3e50",
                                          highlightthickness=0)
        self.bilateral_color_slider.pack(side=tk.LEFT, padx=5)
        
        # Bilateral sigma space
        tk.Label(control_frames[1], text="Spatial Smoothing:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.bilateral_space_var = tk.IntVar(value=self.cartoonizer.bilateral_sigma_space)
        self.bilateral_space_slider = Scale(control_frames[1], from_=10, to=150, 
                                          orient=HORIZONTAL, variable=self.bilateral_space_var,
                                          command=self.update_cartoon, length=200,
                                          bg="#34495e", fg="white", troughcolor="#2c3e50",
                                          highlightthickness=0)
        self.bilateral_space_slider.pack(side=tk.LEFT, padx=5)
        
        # Edge threshold1
        tk.Label(control_frames[2], text="Edge Threshold 1:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.edge_t1_var = tk.IntVar(value=self.cartoonizer.edge_threshold1)
        self.edge_t1_slider = Scale(control_frames[2], from_=10, to=100, 
                                   orient=HORIZONTAL, variable=self.edge_t1_var,
                                   command=self.update_cartoon, length=200,
                                   bg="#34495e", fg="white", troughcolor="#2c3e50",
                                   highlightthickness=0)
        self.edge_t1_slider.pack(side=tk.LEFT, padx=5)
        
        # Edge threshold2
        tk.Label(control_frames[2], text="Edge Threshold 2:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.edge_t2_var = tk.IntVar(value=self.cartoonizer.edge_threshold2)
        self.edge_t2_slider = Scale(control_frames[2], from_=50, to=200, 
                                   orient=HORIZONTAL, variable=self.edge_t2_var,
                                   command=self.update_cartoon, length=200,
                                   bg="#34495e", fg="white", troughcolor="#2c3e50",
                                   highlightthickness=0)
        self.edge_t2_slider.pack(side=tk.LEFT, padx=5)
        
        # Color levels
        tk.Label(control_frames[0], text="Color Levels:", 
                bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.color_levels_var = tk.IntVar(value=self.cartoonizer.total_color_levels)
        self.color_levels_slider = Scale(control_frames[0], from_=2, to=16, 
                                        orient=HORIZONTAL, variable=self.color_levels_var,
                                        command=self.update_cartoon, length=200,
                                        bg="#34495e", fg="white", troughcolor="#2c3e50",
                                        highlightthickness=0)
        self.color_levels_slider.pack(side=tk.LEFT, padx=5)
        
    def open_image(self):
        """Open an image file and display it."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        
        if file_path:
            self.current_image_path = file_path
            self.status_var.set(f"Opened: {os.path.basename(file_path)}")
            
            # Load the image
            self.original_image = cv2.imread(file_path)
            
            # Display the original image
            self.display_original()
            
            # Process and display the cartoon image
            self.process_cartoon()
            
    def display_original(self):
        """Display the original image on the canvas."""
        if self.original_image is not None:
            # Convert from BGR to RGB
            img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # Resize to fit the canvas
            img_resized = self.resize_image(img_rgb)
            
            # Convert to PhotoImage
            self.tk_original = ImageTk.PhotoImage(image=Image.fromarray(img_resized))
            
            # Update canvas
            self.original_canvas.config(width=self.tk_original.width(), height=self.tk_original.height())
            self.original_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_original)
            
    def process_cartoon(self):
        """Process the image with cartoonization and display it."""
        if self.original_image is not None:
            # Update cartoonizer parameters
            self.update_cartoonizer_params()
            
            # Apply cartoonization
            self.cartoon_image = self.cartoonizer.cartoonize(self.original_image)
            
            # Display the cartoon image
            self.display_cartoon()
            
    def display_cartoon(self):
        """Display the cartoon image on the canvas."""
        if self.cartoon_image is not None:
            # Convert from BGR to RGB
            img_rgb = cv2.cvtColor(self.cartoon_image, cv2.COLOR_BGR2RGB)
            
            # Resize to fit the canvas
            img_resized = self.resize_image(img_rgb)
            
            # Convert to PhotoImage
            self.tk_cartoon = ImageTk.PhotoImage(image=Image.fromarray(img_resized))
            
            # Update canvas
            self.cartoon_canvas.config(width=self.tk_cartoon.width(), height=self.tk_cartoon.height())
            self.cartoon_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_cartoon)
            
    def resize_image(self, img, max_width=500, max_height=400):
        """
        Resize the image to fit within the specified dimensions while maintaining aspect ratio.
        
        Args:
            img: Input image
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Resized image
        """
        height, width = img.shape[:2]
        
        # Calculate the scaling factor
        scale = min(max_width / width, max_height / height)
        
        # Resize the image
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return resized
    
    def update_cartoonizer_params(self):
        """Update the cartoonizer parameters from the sliders."""
        self.cartoonizer.update_parameters(
            line_size=self.line_size_var.get(),
            bilateral_filter_d=self.bilateral_d_var.get(),
            bilateral_sigma_color=self.bilateral_color_var.get(),
            bilateral_sigma_space=self.bilateral_space_var.get(),
            edge_threshold1=self.edge_t1_var.get(),
            edge_threshold2=self.edge_t2_var.get(),
            total_color_levels=self.color_levels_var.get()
        )
        
    def update_cartoon(self, event=None):
        """Update the cartoon image when sliders are adjusted."""
        if self.original_image is not None:
            self.status_var.set("Processing...")
            self.root.update_idletasks()  # Update the GUI
            
            # Process and display the cartoon image
            self.process_cartoon()
            
            self.status_var.set("Ready")
            
    def save_cartoon(self):
        """Save the cartoon image to a file."""
        if self.cartoon_image is not None:
            # Get the file path
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), 
                          ("All files", "*.*")])
            
            if file_path:
                # Save the image
                cv2.imwrite(file_path, self.cartoon_image)
                self.status_var.set(f"Saved: {os.path.basename(file_path)}")
                
    def reset_parameters(self):
        """Reset all parameters to default values."""
        # Reset cartoonizer
        self.cartoonizer = Cartoonizer()
        
        # Reset sliders
        self.line_size_var.set(self.cartoonizer.line_size)
        self.bilateral_d_var.set(self.cartoonizer.bilateral_filter_d)
        self.bilateral_color_var.set(self.cartoonizer.bilateral_sigma_color)
        self.bilateral_space_var.set(self.cartoonizer.bilateral_sigma_space)
        self.edge_t1_var.set(self.cartoonizer.edge_threshold1)
        self.edge_t2_var.set(self.cartoonizer.edge_threshold2)
        self.color_levels_var.set(self.cartoonizer.total_color_levels)
        
        # Update the cartoon image
        if self.original_image is not None:
            self.process_cartoon()
            
        self.status_var.set("Parameters reset to default values")
        
    def show_about(self):
        """Show the about dialog."""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Image Cartoonizer")
        about_window.geometry("400x300")
        about_window.configure(bg="#2c3e50")
        about_window.resizable(False, False)
        
        # Add some padding
        frame = tk.Frame(about_window, bg="#2c3e50", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(frame, text="Image Cartoonizer", font=("Arial", 16, "bold"),
                bg="#2c3e50", fg="white").pack(pady=10)
        
        # Description
        description = """
        This application converts images into cartoon-style sketches 
        using classical digital image processing techniques:
        
        • Edge Detection
        • Bilateral Filtering
        • Color Quantization
        
        Adjust the sliders to customize the cartoon effect.
        """
        
        tk.Label(frame, text=description, justify=tk.LEFT, 
                bg="#2c3e50", fg="white", font=("Arial", 10)).pack(pady=10)
        
        # Version
        tk.Label(frame, text="Version 1.0", font=("Arial", 10),
                bg="#2c3e50", fg="white").pack(pady=5)
        
        # Close button
        tk.Button(frame, text="Close", command=about_window.destroy,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 padx=10, pady=5).pack(pady=10)


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = CartoonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
