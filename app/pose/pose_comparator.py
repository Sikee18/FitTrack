import numpy as np
from typing import List, Tuple, Optional, Dict
import cv2

class PoseComparator:
    def __init__(self, reference_pose: np.ndarray = None):
        """Initialize the PoseComparator with an optional reference pose.
        
        Args:
            reference_pose: Numpy array of shape (33, 3) containing the reference pose landmarks
        """
        self.reference_pose = reference_pose
        
        # Define important joint connections for angle calculations
        self.joint_connections = {
            'left_arm': [11, 13, 15],      # Shoulder, Elbow, Wrist
            'right_arm': [12, 14, 16],     # Shoulder, Elbow, Wrist
            'left_leg': [23, 25, 27],      # Hip, Knee, Ankle
            'right_leg': [24, 26, 28],     # Hip, Knee, Ankle
            'torso': [11, 23, 24, 12]      # Shoulders and Hips
        }
    
    def set_reference_pose(self, reference_pose: np.ndarray):
        """Set the reference pose for comparison.
        
        Args:
            reference_pose: Numpy array of shape (33, 3) containing the reference pose landmarks
        """
        self.reference_pose = reference_pose
    
    def normalize_pose(self, landmarks: np.ndarray) -> np.ndarray:
        """Normalize pose landmarks to be scale and position invariant.
        
        Args:
            landmarks: Numpy array of shape (33, 3) containing landmark coordinates
            
        Returns:
            Normalized landmarks
        """
        if landmarks is None or len(landmarks) == 0:
            return None
            
        # Convert to numpy array if not already
        landmarks = np.array(landmarks)
        
        # Get torso size as a scale factor
        left_shoulder = landmarks[11, :2]  # Left shoulder
        right_shoulder = landmarks[12, :2]  # Right shoulder
        left_hip = landmarks[23, :2]  # Left hip
        right_hip = landmarks[24, :2]  # Right hip
        
        # Calculate center of torso
        center_x = (left_shoulder[0] + right_shoulder[0] + left_hip[0] + right_hip[0]) / 4
        center_y = (left_shoulder[1] + right_shoulder[1] + left_hip[1] + right_hip[1]) / 4
        center = np.array([center_x, center_y])
        
        # Calculate scale factor using distance between shoulders (or hips if shoulders not visible)
        shoulder_dist = np.linalg.norm(left_shoulder - right_shoulder)
        hip_dist = np.linalg.norm(left_hip - right_hip)
        
        # Use the average of shoulder and hip distances if both are valid
        if shoulder_dist > 0 and hip_dist > 0:
            scale = (shoulder_dist + hip_dist) / 2
        else:
            scale = max(shoulder_dist, hip_dist)
        
        # If scale is still 0 (unlikely), set a default small value to avoid division by zero
        if scale == 0:
            scale = 0.1
        
        # Normalize landmarks
        normalized_landmarks = landmarks.copy()
        normalized_landmarks[:, :2] = (landmarks[:, :2] - center) / scale
        
        return normalized_landmarks
    
    def calculate_pose_similarity(self, pose1: np.ndarray, pose2: np.ndarray) -> float:
        """Calculate similarity score between two poses.
        
        Args:
            pose1: First pose landmarks (33, 3)
            pose2: Second pose landmarks (33, 3)
            
        Returns:
            Similarity score (0-1, where 1 is identical)
        """
        if pose1 is None or pose2 is None:
            return 0.0
            
        # Normalize both poses
        norm_pose1 = self.normalize_pose(pose1)
        norm_pose2 = self.normalize_pose(pose2)
        
        # Calculate Euclidean distances between corresponding landmarks
        distances = np.linalg.norm(norm_pose1[:, :2] - norm_pose2[:, :2], axis=1)
        
        # Calculate weighted average distance (weight by landmark visibility if available)
        if pose1.shape[1] > 2 and pose2.shape[1] > 2:  # Check if visibility is available
            weights = (pose1[:, 2] + pose2[:, 2]) / 2  # Average visibility
            avg_distance = np.average(distances, weights=weights)
        else:
            avg_distance = np.mean(distances)
        
        # Convert distance to similarity score (lower distance = higher similarity)
        # Using exponential decay to map distance to [0, 1] range
        similarity = np.exp(-5 * avg_distance)
        
        return float(similarity)
    
    def calculate_joint_angles(self, landmarks: np.ndarray) -> Dict[str, float]:
        """Calculate joint angles for important body parts.
        
        Args:
            landmarks: Numpy array of shape (33, 3) containing landmark coordinates
            
        Returns:
            Dictionary of joint angles in degrees
        """
        if landmarks is None:
            return {}
            
        angles = {}
        
        # Calculate angles for each joint connection
        for joint_name, indices in self.joint_connections.items():
            if len(indices) == 3:  # Three points form an angle
                a, b, c = [landmarks[i, :2] for i in indices]  # Get (x,y) coordinates
                
                # Calculate vectors
                ba = a - b
                bc = c - b
                
                # Calculate angle in radians
                cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
                # Clamp to valid range to avoid numerical errors
                cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
                angle_rad = np.arccos(cosine_angle)
                
                # Convert to degrees
                angle_deg = np.degrees(angle_rad)
                angles[joint_name] = angle_deg
            
        return angles
    
    def compare_with_reference(self, current_pose: np.ndarray) -> Dict:
        """Compare current pose with the reference pose.
        
        Args:
            current_pose: Numpy array of shape (33, 3) containing current pose landmarks
            
        Returns:
            Dictionary containing comparison results:
            - similarity: Overall similarity score (0-1)
            - angle_differences: Dictionary of angle differences
            - feedback: List of feedback messages
        """
        if self.reference_pose is None or current_pose is None:
            return {
                'similarity': 0.0,
                'angle_differences': {},
                'feedback': ['No reference pose available for comparison']
            }
        
        # Calculate similarity score
        similarity = self.calculate_pose_similarity(self.reference_pose, current_pose)
        
        # Calculate joint angles for both poses
        ref_angles = self.calculate_joint_angles(self.reference_pose)
        current_angles = self.calculate_joint_angles(current_pose)
        
        # Calculate angle differences
        angle_differences = {}
        feedback = []
        
        for joint in ref_angles:
            if joint in current_angles:
                diff = abs(ref_angles[joint] - current_angles[joint])
                angle_differences[joint] = diff
                
                # Generate feedback based on angle differences
                if 'arm' in joint and diff > 15:  # 15 degrees threshold for arms
                    side = 'left' if 'left' in joint else 'right'
                    feedback.append(f"Adjust your {side} arm position")
                elif 'leg' in joint and diff > 10:  # 10 degrees threshold for legs
                    side = 'left' if 'left' in joint else 'right'
                    feedback.append(f"Adjust your {side} leg position")
        
        # If no specific feedback, but similarity is low, provide general feedback
        if not feedback and similarity < 0.7:
            feedback.append("Try to match the reference pose more closely")
        
        return {
            'similarity': similarity,
            'angle_differences': angle_differences,
            'feedback': feedback
        }
