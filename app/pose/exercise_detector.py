# exercise_detector.py
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math

@dataclass
class ExerciseConfig:
    name: str
    key_points: List[int]  # Indices of key body points
    angle_ranges: Dict[str, Tuple[float, float]]  # Expected angle ranges
    feedback_messages: Dict[str, str]  # Feedback for common mistakes

# Define exercise configurations
EXERCISES = {
    'squat': ExerciseConfig(
        name='Squat',
        key_points=[23, 24, 25, 26],  # Hips and knees
        angle_ranges={
            'knee': (80, 100),  # Knee angle at bottom
            'hip': (160, 190)    # Hip angle
        },
        feedback_messages={
            'knee': 'Keep your knees behind your toes',
            'hip': 'Keep your back straight'
        }
    ),
    'pushup': ExerciseConfig(
        name='Push-up',
        key_points=[11, 12, 13, 14, 15, 16],  # Shoulders, elbows, wrists
        angle_ranges={
            'elbow': (75, 90),  # Elbow angle at bottom
        },
        feedback_messages={
            'elbow': 'Lower your body until elbows are at 90 degrees',
            'back': 'Keep your body straight'
        }
    ),
    'lunge': ExerciseConfig(
        name='Lunge',
        key_points=[23, 24, 25, 26, 27, 28],  # Hips, knees, ankles
        angle_ranges={
            'front_knee': (80, 100),  # Front knee angle
            'back_knee': (80, 100)    # Back knee angle
        },
        feedback_messages={
            'front_knee': 'Keep front knee above ankle',
            'back_knee': 'Lower back knee toward floor'
        }
    ),
    'shoulder_press': ExerciseConfig(
        name='Shoulder Press',
        key_points=[11, 12, 13, 14, 15, 16],  # Shoulders, elbows, wrists
        angle_ranges={
            'shoulder': (160, 180),  # Shoulder angle at top
            'elbow': (160, 180)      # Elbow angle at top
        },
        feedback_messages={
            'shoulder': 'Fully extend arms overhead',
            'elbow': 'Keep elbows from flaring out'
        }
    ),
    'bicep_curl': ExerciseConfig(
        name='Bicep Curl',
        key_points=[11, 12, 13, 14, 15, 16],  # Shoulders, elbows, wrists
        angle_ranges={
            'elbow': (30, 50),  # Elbow angle at top
        },
        feedback_messages={
            'elbow': 'Keep elbows close to your body',
            'shoulder': 'Keep shoulders still'
        }
    )
}

class ExerciseDetector:
    def __init__(self, exercise_name: str):
        """Initialize with a specific exercise."""
        self.exercise = EXERCISES.get(exercise_name.lower())
        if not self.exercise:
            raise ValueError(f"Exercise '{exercise_name}' not found")
        
        self.rep_count = 0
        self.current_phase = 'up'  # 'up' or 'down'
        self.feedback = []

    def calculate_angle(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        """Calculate the angle between three points."""
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
        return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    def analyze_pose(self, landmarks: np.ndarray) -> Dict:
        """Analyze the current pose and provide feedback."""
        if landmarks is None or len(landmarks) < 33:
            return {'feedback': ['No pose detected'], 'rep_count': self.rep_count}

        self.feedback = []
        results = {}
        
        # Exercise-specific analysis
        if self.exercise.name == 'Squat':
            self._analyze_squat(landmarks)
        elif self.exercise.name == 'Push-up':
            self._analyze_pushup(landmarks)
        # Add other exercise analyses...

        results['feedback'] = self.feedback
        results['rep_count'] = self.rep_count
        return results

    def _analyze_squat(self, landmarks: np.ndarray):
        """Specific analysis for squats."""
        # Get key points
        left_hip = landmarks[23][:2]
        right_hip = landmarks[24][:2]
        left_knee = landmarks[25][:2]
        right_knee = landmarks[26][:2]
        left_ankle = landmarks[27][:2]
        right_ankle = landmarks[28][:2]

        # Calculate knee angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        avg_knee_angle = (left_knee_angle + right_knee_angle) / 2

        # Check form
        if avg_knee_angle < 80:
            self.feedback.append(self.exercise.feedback_messages['knee'])
        if avg_knee_angle > 100:
            self.feedback.append('Stand up straight')

        # Count reps
        if avg_knee_angle < 90 and self.current_phase == 'up':
            self.current_phase = 'down'
        elif avg_knee_angle > 160 and self.current_phase == 'down':
            self.current_phase = 'up'
            self.rep_count += 1

    def _analyze_pushup(self, landmarks: np.ndarray):
        """Specific analysis for push-ups."""
        left_shoulder = landmarks[11][:2]
        right_shoulder = landmarks[12][:2]
        left_elbow = landmarks[13][:2]
        right_elbow = landmarks[14][:2]
        left_wrist = landmarks[15][:2]
        right_wrist = landmarks[16][:2]

        # Calculate elbow angles
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2

        # Check form
        if avg_elbow_angle > 100:
            self.feedback.append('Lower your body more')
        elif avg_elbow_angle < 80:
            self.feedback.append('Push up higher')

        # Count reps
        if avg_elbow_angle > 90 and self.current_phase == 'up':
            self.current_phase = 'down'
        elif avg_elbow_angle < 80 and self.current_phase == 'down':
            self.current_phase = 'up'
            self.rep_count += 1

# Example usage:
if __name__ == "__main__":
    detector = ExerciseDetector('squat')
    # In a real app, you would pass actual landmark data from MediaPipe
    # results = detector.analyze_pose(landmarks)
    # print(f"Reps: {results['rep_count']}, Feedback: {results['feedback']}")