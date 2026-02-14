import cv2
import numpy as np
from typing import Optional, Dict, List, Tuple

class FeedbackRenderer:
    def __init__(self, window_name: str = "Smart Mirror Mode"):
        """Initialize the feedback renderer.
        
        Args:
            window_name: Name of the display window
        """
        self.window_name = window_name
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.text_color = (255, 255, 255)  # White
        self.text_thickness = 2
        self.line_thickness = 2
        self.overlay_alpha = 0.7  # Transparency for overlay
        
        # Colors
        self.correct_color = (0, 255, 0)  # Green
        self.incorrect_color = (0, 0, 255)  # Red
        self.neutral_color = (255, 255, 255)  # White
        self.background_color = (50, 50, 50)  # Dark gray
        
    def draw_pose(self, image: np.ndarray, landmarks: np.ndarray, similarity: float = 1.0) -> np.ndarray:
        """Draw the detected pose on the image with color coding based on similarity.
        
        Args:
            image: Input image in BGR format
            landmarks: Numpy array of shape (33, 3) containing landmark coordinates
            similarity: Similarity score (0-1) to determine color coding
            
        Returns:
            Image with pose drawn
        """
        if landmarks is None:
            return image
            
        # Create a copy of the image to draw on
        img_copy = image.copy()
        
        # Define connections between landmarks (MediaPipe pose connections)
        connections = [
            # Torso
            (11, 12), (11, 23), (12, 24), (23, 24),
            # Left arm
            (11, 13), (13, 15),
            # Right arm
            (12, 14), (14, 16),
            # Left leg
            (23, 25), (25, 27),
            # Right leg
            (24, 26), (26, 28),
            # Face (simplified)
            (0, 1), (1, 2), (2, 3), (3, 7),  # Right eyebrow
            (0, 4), (4, 5), (5, 6), (6, 8),  # Left eyebrow
            (9, 10),  # Nose bridge
            (17, 18), (18, 19), (19, 20), (20, 21),  # Right eye
            (22, 23), (23, 24), (24, 25), (25, 26),  # Left eye
            (30, 31), (31, 32), (32, 33), (33, 34),  # Mouth outer
            (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 36),  # Lips
        ]
        
        # Determine color based on similarity
        if similarity > 0.8:
            color = self.correct_color
        elif similarity > 0.5:
            # Interpolate between red and green based on similarity
            ratio = (similarity - 0.5) / 0.3
            color = (
                int(self.correct_color[0] * ratio + self.incorrect_color[0] * (1 - ratio)),
                int(self.correct_color[1] * ratio + self.incorrect_color[1] * (1 - ratio)),
                int(self.correct_color[2] * ratio * 0)  # Keep red component for visibility
            )
        else:
            color = self.incorrect_color
        
        # Draw connections
        for connection in connections:
            start_idx, end_idx = connection
            if (0 <= start_idx < len(landmarks)) and (0 <= end_idx < len(landmarks)):
                start_point = (
                    int(landmarks[start_idx, 0] * img_copy.shape[1]),
                    int(landmarks[start_idx, 1] * img_copy.shape[0])
                )
                end_point = (
                    int(landmarks[end_idx, 0] * img_copy.shape[1]),
                    int(landmarks[end_idx, 1] * img_copy.shape[0])
                )
                cv2.line(img_copy, start_point, end_point, color, self.line_thickness)
        
        # Draw keypoints
        for idx, landmark in enumerate(landmarks):
            x = int(landmark[0] * img_copy.shape[1])
            y = int(landmark[1] * img_copy.shape[0])
            cv2.circle(img_copy, (x, y), 4, color, -1)
        
        return img_copy
    
    def draw_reference_overlay(self, image: np.ndarray, reference_pose: np.ndarray) -> np.ndarray:
        """Draw a semi-transparent reference pose overlay.
        
        Args:
            image: Input image in BGR format
            reference_pose: Numpy array of shape (33, 3) containing reference pose landmarks
            
        Returns:
            Image with reference pose overlay
        """
        if reference_pose is None:
            return image
            
        # Create a transparent overlay
        overlay = image.copy()
        overlay = self.draw_pose(overlay, reference_pose, 1.0)
        
        # Blend the overlay with the original image
        return cv2.addWeighted(overlay, 0.3, image, 0.7, 0)
    
    def draw_feedback_panel(self, image: np.ndarray, feedback: Dict) -> np.ndarray:
        """Draw a feedback panel with similarity score and instructions.
        
        Args:
            image: Input image in BGR format
            feedback: Dictionary containing feedback information
            
        Returns:
            Image with feedback panel
        """
        img_copy = image.copy()
        height, width = img_copy.shape[:2]
        
        # Create a semi-transparent overlay for the panel
        overlay = np.zeros_like(img_copy, dtype=np.uint8)
        
        # Panel dimensions and position (right side of the screen)
        panel_width = 300
        panel_x = width - panel_width - 20
        panel_y = 20
        panel_height = height - 40
        
        # Draw panel background
        cv2.rectangle(overlay, 
                     (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height),
                     self.background_color, -1)
        
        # Add title
        title = "Smart Mirror Feedback"
        (text_width, text_height), _ = cv2.getTextSize(title, self.font, self.font_scale + 0.3, self.text_thickness + 1)
        cv2.putText(overlay, title,
                   (panel_x + (panel_width - text_width) // 2, panel_y + 40),
                   self.font, self.font_scale + 0.3, self.text_color, self.text_thickness + 1, cv2.LINE_AA)
        
        # Add similarity score
        similarity = feedback.get('similarity', 0)
        similarity_text = f"Similarity: {similarity*100:.1f}%"
        
        # Determine color based on similarity
        if similarity > 0.8:
            color = self.correct_color
            status = "Excellent!"
        elif similarity > 0.6:
            color = (0, 200, 255)  # Orange
            status = "Good"
        elif similarity > 0.4:
            color = (0, 165, 255)  # Orange-Red
            status = "Needs Work"
        else:
            color = self.incorrect_color
            status = "Needs Improvement"
        
        # Draw similarity bar
        bar_width = 200
        bar_height = 20
        bar_x = panel_x + (panel_width - bar_width) // 2
        bar_y = panel_y + 80
        
        # Background bar
        cv2.rectangle(overlay, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                     (100, 100, 100), -1)
        # Filled bar based on similarity
        fill_width = int(bar_width * min(max(similarity, 0), 1))
        cv2.rectangle(overlay, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height),
                     color, -1)
        # Border
        cv2.rectangle(overlay, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                     (200, 200, 200), 1)
        
        # Add similarity text
        cv2.putText(overlay, status,
                   (bar_x + (bar_width - cv2.getTextSize(status, self.font, self.font_scale, self.text_thickness)[0][0]) // 2,
                    bar_y - 10),
                   self.font, self.font_scale, self.text_color, self.text_thickness, cv2.LINE_AA)
        
        # Add feedback messages
        feedback_messages = feedback.get('feedback', [])
        y_offset = bar_y + bar_height + 40
        
        if feedback_messages:
            cv2.putText(overlay, "Feedback:",
                       (panel_x + 10, y_offset),
                       self.font, self.font_scale, self.text_color, self.text_thickness, cv2.LINE_AA)
            y_offset += 30
            
            for i, message in enumerate(feedback_messages[:4]):  # Show up to 4 messages
                cv2.putText(overlay, f"• {message}",
                           (panel_x + 20, y_offset + i * 30),
                           self.font, self.font_scale * 0.8, self.text_color, self.text_thickness, cv2.LINE_AA)
        else:
            cv2.putText(overlay, "No specific feedback",
                       (panel_x + 10, y_offset),
                       self.font, self.font_scale * 0.8, self.text_color, self.text_thickness, cv2.LINE_AA)
        
        # Add help text at the bottom
        help_text = [
            "Press 'r' to set reference pose",
            "Press 'q' to quit"
        ]
        
        for i, text in enumerate(help_text):
            cv2.putText(overlay, text,
                       (panel_x + 10, height - 60 + i * 25),
                       self.font, self.font_scale * 0.7, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Blend the overlay with the original image
        return cv2.addWeighted(overlay, 0.7, img_copy, 0.3, 0)
    
    def show_image(self, image: np.ndarray, window_name: str = None):
        """Display the image in a window.
        
        Args:
            image: Image to display
            window_name: Optional window name (uses default if None)
        """
        cv2.imshow(window_name or self.window_name, image)
    
    def destroy_windows(self):
        """Destroy all OpenCV windows."""
        cv2.destroyAllWindows()
