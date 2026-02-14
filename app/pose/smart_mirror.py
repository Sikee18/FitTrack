import cv2
import numpy as np
import time
from pose_detector import PoseDetector
from pose_comparator import PoseComparator
from feedback_renderer import FeedbackRenderer

def main():
    # Initialize components
    detector = PoseDetector(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    comparator = PoseComparator()
    renderer = FeedbackRenderer("Smart Mirror Mode")
    
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # 0 for default camera
    
    # Set camera resolution (adjust based on your camera's capabilities)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Variables for FPS calculation
    prev_time = 0
    fps = 0
    
    # Main loop
    reference_pose = None
    show_reference = False
    
    print("Smart Mirror Mode started!")
    print("Press 'r' to set reference pose")
    print("Press 't' to toggle reference overlay")
    print("Press 'q' to quit")
    
    try:
        while True:
            # Read frame from camera
            success, frame = cap.read()
            if not success:
                print("Failed to capture frame")
                break
            
            # Mirror the frame for more natural interaction
            frame = cv2.flip(frame, 1)
            
            # Detect pose
            landmarks = detector.detect_landmarks(frame)
            
            # Process frame based on current state
            display_frame = frame.copy()
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time
            
            # Draw FPS
            cv2.putText(display_frame, f"FPS: {int(fps)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # If we have a reference pose and landmarks are detected, compare them
            feedback = {}
            if reference_pose is not None and landmarks is not None:
                # Compare current pose with reference
                comparison = comparator.compare_with_reference(landmarks)
                
                # Draw pose with color coding based on similarity
                display_frame = renderer.draw_pose(
                    display_frame, landmarks, comparison['similarity']
                )
                
                # Add feedback to display
                feedback = {
                    'similarity': comparison['similarity'],
                    'feedback': comparison['feedback']
                }
                
                # Toggle reference overlay if enabled
                if show_reference:
                    display_frame = renderer.draw_reference_overlay(display_frame, reference_pose)
            elif landmarks is not None:
                # Just draw the detected pose in neutral color if no reference
                display_frame = renderer.draw_pose(display_frame, landmarks, 1.0)
            
            # Draw feedback panel
            display_frame = renderer.draw_feedback_panel(display_frame, feedback)
            
            # Show the frame
            renderer.show_image(display_frame)
            
            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            
            # Set reference pose with 'r' key
            if key == ord('r') and landmarks is not None:
                reference_pose = landmarks
                comparator.set_reference_pose(reference_pose)
                print("Reference pose set!")
            
            # Toggle reference overlay with 't' key
            elif key == ord('t'):
                show_reference = not show_reference
                print(f"Reference overlay: {'ON' if show_reference else 'OFF'}")
            
            # Quit on 'q' key
            elif key == ord('q'):
                print("Exiting...")
                break
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    finally:
        # Release resources
        cap.release()
        detector.release()
        renderer.destroy_windows()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
