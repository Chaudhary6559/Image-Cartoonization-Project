import cv2
import numpy as np

class Cartoonizer:
    """
    A class that implements image cartoonization using classical computer vision techniques.
    """
    
    def __init__(self):
        """Initialize the Cartoonizer with default parameters."""
        # Default parameters
        self.line_size = 7
        self.blur_value = 7
        self.bilateral_filter_d = 9
        self.bilateral_sigma_color = 75
        self.bilateral_sigma_space = 75
        self.edge_threshold1 = 50
        self.edge_threshold2 = 150
        self.total_color_levels = 8
        
    def edge_detection(self, img):
        """
        Detect edges in the image using Canny edge detector.
        
        Args:
            img: Input image
            
        Returns:
            Edge mask
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur to reduce noise
        gray_blur = cv2.medianBlur(gray, self.line_size)
        
        # Apply Canny edge detector
        edges = cv2.Canny(gray_blur, self.edge_threshold1, self.edge_threshold2)
        
        # Dilate edges to make them more visible
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Invert edges to get black lines on white background
        edges = cv2.bitwise_not(edges)
        
        # Convert back to 3-channel image
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        return edges
    
    def color_quantization(self, img):
        """
        Reduce the number of colors in the image.
        
        Args:
            img: Input image
            
        Returns:
            Image with reduced colors
        """
        # Convert to float32 for processing
        data = np.float32(img).reshape((-1, 3))
        
        # Define criteria for K-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        
        # Apply K-means clustering
        ret, label, center = cv2.kmeans(data, self.total_color_levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        
        # Map back to original image dimensions
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        
        return result
    
    def apply_bilateral_filter(self, img):
        """
        Apply bilateral filter to smooth the image while preserving edges.
        
        Args:
            img: Input image
            
        Returns:
            Filtered image
        """
        # Apply bilateral filter
        filtered = cv2.bilateralFilter(img, self.bilateral_filter_d, 
                                      self.bilateral_sigma_color, 
                                      self.bilateral_sigma_space)
        return filtered
    
    def cartoonize(self, img):
        """
        Apply cartoonization effect to the image.
        
        Args:
            img: Input image
            
        Returns:
            Cartoonized image
        """
        # Apply bilateral filter for smoothing
        filtered = self.apply_bilateral_filter(img)
        
        # Apply color quantization
        color_quantized = self.color_quantization(filtered)
        
        # Detect edges
        edges = self.edge_detection(img)
        
        # Combine edges with color quantized image
        cartoon = cv2.bitwise_and(color_quantized, edges)
        
        return cartoon
    
    def update_parameters(self, line_size=None, blur_value=None, bilateral_filter_d=None,
                         bilateral_sigma_color=None, bilateral_sigma_space=None,
                         edge_threshold1=None, edge_threshold2=None, total_color_levels=None):
        """
        Update the cartoonization parameters.
        
        Args:
            line_size: Size of the median blur kernel for edge detection
            blur_value: Blur value for smoothing
            bilateral_filter_d: Diameter of each pixel neighborhood in bilateral filter
            bilateral_sigma_color: Filter sigma in the color space
            bilateral_sigma_space: Filter sigma in the coordinate space
            edge_threshold1: First threshold for Canny edge detector
            edge_threshold2: Second threshold for Canny edge detector
            total_color_levels: Number of color levels for quantization
        """
        if line_size is not None:
            self.line_size = line_size
        if blur_value is not None:
            self.blur_value = blur_value
        if bilateral_filter_d is not None:
            self.bilateral_filter_d = bilateral_filter_d
        if bilateral_sigma_color is not None:
            self.bilateral_sigma_color = bilateral_sigma_color
        if bilateral_sigma_space is not None:
            self.bilateral_sigma_space = bilateral_sigma_space
        if edge_threshold1 is not None:
            self.edge_threshold1 = edge_threshold1
        if edge_threshold2 is not None:
            self.edge_threshold2 = edge_threshold2
        if total_color_levels is not None:
            self.total_color_levels = total_color_levels
