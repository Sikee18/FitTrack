# exercise_app.py
import cv2
import mediapipe as mp
import numpy as np
from exercise_detector import ExerciseDetector, EXERCISES

class ExerciseApp:
    def __init__(self, exercise_name='squat'):
        """Initialize the exercise application."""
        self.exercise_name = exercise_name
        self.detector = ExerciseDetector(exercise_name)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        
        # Set up display window
        self.window_name = f"Exercise: {exercise_name.capitalize()}"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
    def run(self):
        """Run the main application loop."""
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
                
            # Flip the frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process the frame with MediaPipe
            results = self.process_frame(frame)
            
            # If pose is detected, analyze it
            if results.pose_landmarks:
                landmarks = self.get_landmarks(results)
                analysis = self.detector.analyze_pose(landmarks)
                
                # Draw landmarks and feedback
                self.draw_landmarks(frame, results)
                self.draw_feedback(frame, analysis)
                
            # Display the frame
            cv2.imshow(self.window_name, frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cleanup()
        
    def process_frame(self, frame):
        """Process a frame with MediaPipe Pose."""
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.pose.process(frame_rgb)
        
    def get_landmarks(self, results):
        """Extract landmarks in a numpy array format."""
        landmarks = results.pose_landmarks.landmark
        return np.array([[lm.x, lm.y, lm.visibility] for lm in landmarks])
        
    def draw_landmarks(self, frame, results):
        """Draw pose landmarks on the frame."""
        self.mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )
        
    def draw_feedback(self, frame, analysis):
        """Draw feedback on the frame."""
        # Display rep count
        cv2.putText(frame, f"Reps: {analysis['rep_count']}", 
                   (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display feedback messages
        for i, message in enumerate(analysis['feedback'][:3]):  # Show up to 3 messages
            cv2.putText(frame, message, 
                       (20, 80 + i * 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    def cleanup(self):
        """Release resources."""
        self.cap.release()
        cv2.destroyAllWindows()

def show_exercise_menu():
    """Show a menu to select an exercise."""
    print("\nAvailable Exercises:")
    for i, ex_name in enumerate(EXERCISES.keys(), 1):
        print(f"{i}. {ex_name.replace('_', ' ').title()}")
    
    while True:
        try:
            choice = int(input("\nSelect an exercise (number): ")) - 1
            if 0 <= choice < len(EXERCISES):
                return list(EXERCISES.keys())[choice]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    # Select exercise
    exercise_name = show_exercise_menu()
    
    # Start the application
    app = ExerciseApp(exercise_name)
    print(f"\nStarting {exercise_name} detection...")
    print("Press 'q' to quit")
    app.run()