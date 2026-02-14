from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np

@dataclass
class ExerciseConfig:
    name: str
    description: str
    key_points: List[int]  # Indices of key body points used for this exercise
    angle_thresholds: Dict[str, Tuple[float, float]]  # Joint angle ranges for correct form
    feedback_messages: Dict[str, str]  # Feedback messages for common form errors
    rep_phase_threshold: float  # Threshold to count a repetition

# Define exercise configurations
EXERCISES = {
    'squat': ExerciseConfig(
        name="Squat",
        description="Stand with feet shoulder-width apart, lower your body by bending your knees.",
        key_points=[23, 24, 25, 26, 27, 28],  # Hips, knees, ankles
        angle_thresholds={
            'knee': (80, 100),  # Knee angle at bottom of squat
            'torso': (160, 190)  # Torso angle (relative to vertical)
        },
        feedback_messages={
            'knee_too_far': "Keep your knees behind your toes",
            'knee_collapse': "Push your knees outward",
            'back_bent': "Keep your back straight"
        },
        rep_phase_threshold=0.7
    ),
    'pushup': ExerciseConfig(
        name="Push-up",
        description="Keep your body straight, lower until your chest nearly touches the floor.",
        key_points=[11, 12, 13, 14, 15, 16, 23, 24],  # Shoulders, elbows, wrists, hips
        angle_thresholds={
            'elbow': (75, 90),  # Elbow angle at bottom
            'shoulder': (0, 30)  # Shoulder angle
        },
        feedback_messages={
            'hips_too_low': "Keep your body straight",
            'hips_too_high': "Lower your hips",
            'depth_insufficient': "Go lower"
        },
        rep_phase_threshold=0.6
    ),
    'lunge': ExerciseConfig(
        name="Lunge",
        description="Step forward and lower your hips until both knees are bent at 90 degrees.",
        key_points=[23, 24, 25, 26, 27, 28],  # Hips, knees, ankles
        angle_thresholds={
            'front_knee': (80, 100),  # Front knee angle at bottom
            'back_knee': (80, 100),   # Back knee angle at bottom
        },
        feedback_messages={
            'front_knee_over': "Don't let your front knee go past your toes",
            'torso_lean': "Keep your torso upright",
            'knee_collapse': "Keep your front knee in line with your foot"
        },
        rep_phase_threshold=0.7
    ),
    'shoulder_press': ExerciseConfig(
        name="Shoulder Press",
        description="Press weights overhead until arms are fully extended.",
        key_points=[11, 12, 13, 14, 15, 16],  # Shoulders, elbows, wrists
        angle_thresholds={
            'elbow': (160, 180),  # Elbow angle at top
            'shoulder': (160, 180)  # Shoulder angle at top
        },
        feedback_messages={
            'elbows_low': "Raise your elbows higher",
            'arms_not_straight': "Fully extend your arms",
            'back_arch': "Don't arch your back"
        },
        rep_phase_threshold=0.8
    ),
    'bicep_curl': ExerciseConfig(
        name="Bicep Curl",
        description="Keep elbows close to your torso, curl the weights up to shoulder level.",
        key_points=[11, 12, 13, 14, 15, 16],  # Shoulders, elbows, wrists
        angle_thresholds={
            'elbow': (30, 50),    # Elbow angle at top of curl
            'shoulder': (0, 20)   # Shoulder stability
        },
        feedback_messages={
            'elbows_moving': "Keep your elbows still",
            'range_insufficient': "Complete the full range of motion",
            'shoulders_rising': "Keep your shoulders down"
        },
        rep_phase_threshold=0.7
    )
}

def get_exercise_config(exercise_name: str) -> Optional[ExerciseConfig]:
    """Get configuration for a specific exercise."""
    return EXERCISES.get(exercise_name.lower())

def list_available_exercises() -> List[str]:
    """Return list of available exercise names."""
    return list(EXERCISES.keys())
