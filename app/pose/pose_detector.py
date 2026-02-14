import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional

class PoseDetector:
    def __init__(self, min_detection_confidence: float = 0.5, min_tracking_confidence: float = 0.5):
        """Initialize the MediaPipe Pose detector.
        
        Args:
            min_detection_confidence: Minimum confidence value for detection
            min_tracking_confidence: Minimum confidence value for tracking
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # Balance between speed and accuracy
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def detect_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Detect pose landmarks in the given image.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Numpy array of shape (33, 3) containing landmark coordinates (x, y, visibility) or None if no pose is detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
            
        # Extract landmarks to numpy array (33 landmarks with x, y, visibility)
        landmarks = np.array([[lm.x, lm.y, lm.visibility] 
                            for lm in results.pose_landmarks.landmark])
        return landmarks
    
    def draw_landmarks(self, image: np.ndarray, landmarks: np.ndarray) -> np.ndarray:
        """Draw pose landmarks on the image.
        
        Args:
            image: Input image in BGR format
            landmarks: Numpy array of shape (33, 3) containing landmark coordinates
            
        Returns:
            Image with landmarks drawn
        """
        # Create a copy of the image to draw on
        img_copy = image.copy()
        
        # Convert landmarks to MediaPipe format
        pose_landmarks = self.mp_pose.PoseLandmark
        landmark_list = []
        
        for idx in range(landmarks.shape[0]):
            landmark = self.mp_pose.PoseLandmark(idx)
            landmark_list.append(landmark)
            
            # Draw circles for each landmark
            x = int(landmarks[idx, 0] * img_copy.shape[1])
            y = int(landmarks[idx, 1] * img_copy.shape[0])
            cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
        
        # Draw connections between landmarks
        connections = self.mp_pose.POSE_CONNECTIONS
        for connection in connections:
            start_idx, end_idx = connection
            if (0 <= start_idx < len(landmark_list)) and (0 <= end_idx < len(landmark_list)):
                start_point = (
                    int(landmarks[start_idx, 0] * img_copy.shape[1]),
                    int(landmarks[start_idx, 1] * img_copy.shape[0])
                )
                end_point = (
                    int(landmarks[end_idx, 0] * img_copy.shape[1]),
                    int(landmarks[end_idx, 1] * img_copy.shape[0])
                )
                cv2.line(img_copy, start_point, end_point, (0, 255, 0), 2)
        
        return img_copy
    
    def get_landmark_coordinates(self, landmarks: np.ndarray, landmark_indices: List[int]) -> List[Tuple[float, float]]:
        """Get the (x, y) coordinates of specified landmarks.
        
        Args:
            landmarks: Numpy array of shape (33, 3) containing landmark coordinates
            landmark_indices: List of landmark indices to retrieve
            
        Returns:
            List of (x, y) coordinate tuples for the specified landmarks
        """
        coordinates = []
        for idx in landmark_indices:
            if 0 <= idx < landmarks.shape[0]:
                x, y, _ = landmarks[idx]
                coordinates.append((x, y))
        return coordinates
    
    def release(self):
        """Release resources."""
        self.pose.close()
