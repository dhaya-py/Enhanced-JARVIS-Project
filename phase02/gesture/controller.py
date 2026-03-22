"""
Phase 02 - Gesture Control Module
Hand gesture recognition for system control
"""

import cv2
import mediapipe as mp
import pyautogui
from typing import Tuple, Optional
import numpy as np

class GestureController:
    """Hand gesture recognition and control"""
    
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Hand detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Gesture state
        self.prev_x, self.prev_y = 0, 0
        self.smoothing_factor = 0.5
        
        print("✓ Gesture Controller initialized")
    
    def _count_fingers(self, landmarks) -> int:
        """Count number of fingers raised"""
        finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky
        thumb_tip = 4
        
        count = 0
        
        # Check thumb
        if landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x:
            count += 1
        
        # Check other fingers
        for tip in finger_tips:
            if landmarks[tip].y < landmarks[tip - 2].y:
                count += 1
        
        return count
    
    def _is_pinching(self, landmarks) -> bool:
        """Check if thumb and index finger are pinching"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = np.sqrt(
            (thumb_tip.x - index_tip.x) ** 2 +
            (thumb_tip.y - index_tip.y) ** 2
        )
        
        return distance < 0.05
    
    def start_gesture_control(self) -> Tuple[bool, str]:
        """
        Start gesture-based cursor control
        
        Returns:
            Tuple of (success, message)
        """
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return False, "Could not access camera"
            
            print("Gesture control started")
            print("Controls:")
            print("  - Move hand to control cursor")
            print("  - Pinch to click")
            print("  - 5 fingers to scroll up")
            print("  - Fist to scroll down")
            print("  - Press ESC to exit")
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                frame_height, frame_width, _ = frame.shape
                
                # Convert to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect hands
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw hand landmarks
                        self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS
                        )
                        
                        # Get index finger tip position
                        index_tip = hand_landmarks.landmark[8]
                        
                        # Convert to screen coordinates
                        x = int(index_tip.x * self.screen_width)
                        y = int(index_tip.y * self.screen_height)
                        
                        # Smooth movement
                        x = int(self.prev_x + (x - self.prev_x) * self.smoothing_factor)
                        y = int(self.prev_y + (y - self.prev_y) * self.smoothing_factor)
                        
                        self.prev_x, self.prev_y = x, y
                        
                        # Move cursor
                        pyautogui.moveTo(x, y, duration=0)
                        
                        # Check gestures
                        finger_count = self._count_fingers(hand_landmarks.landmark)
                        
                        # Pinch to click
                        if self._is_pinching(hand_landmarks.landmark):
                            pyautogui.click()
                            cv2.putText(
                                frame, "CLICK", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                            )
                        
                        # 5 fingers - scroll up
                        elif finger_count == 5:
                            pyautogui.scroll(10)
                            cv2.putText(
                                frame, "SCROLL UP", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
                            )
                        
                        # Fist - scroll down
                        elif finger_count == 0:
                            pyautogui.scroll(-10)
                            cv2.putText(
                                frame, "SCROLL DOWN", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2
                            )
                        
                        # Display finger count
                        cv2.putText(
                            frame, f"Fingers: {finger_count}", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
                        )
                
                # Display frame
                cv2.imshow('Gesture Control', frame)
                
                # Exit on ESC
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            return True, "Gesture control stopped"
            
        except Exception as e:
            return False, f"Error in gesture control: {e}"
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.hands.close()
        except:
            pass

# Global gesture controller instance
gesture_controller = GestureController()
