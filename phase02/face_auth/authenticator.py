"""
Phase 02 - Face Authentication Module
Face capture and recognition for user authentication
"""

import cv2
import face_recognition
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import pickle

class FaceAuthenticator:
    """Face recognition authentication system"""
    
    def __init__(self):
        self.faces_dir = Path(__file__).parent / "faces_data"
        self.faces_dir.mkdir(exist_ok=True)
        
        self.encodings_file = self.faces_dir / "encodings.pkl"
        self.known_encodings = []
        self.known_names = []
        
        self._load_encodings()
    
    def _load_encodings(self):
        """Load saved face encodings"""
        try:
            if self.encodings_file.exists():
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data['encodings']
                    self.known_names = data['names']
                print(f"✓ Loaded {len(self.known_encodings)} face encodings")
        except Exception as e:
            print(f"✗ Error loading encodings: {e}")
    
    def _save_encodings(self):
        """Save face encodings"""
        try:
            data = {
                'encodings': self.known_encodings,
                'names': self.known_names
            }
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(data, f)
            print("✓ Face encodings saved")
        except Exception as e:
            print(f"✗ Error saving encodings: {e}")
    
    def capture_face(self, name: str, num_samples: int = 5) -> Tuple[bool, str]:
        """
        Capture face samples for a user
        
        Args:
            name: User's name
            num_samples: Number of samples to capture
            
        Returns:
            Tuple of (success, message)
        """
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return False, "Could not access camera"
            
            samples_captured = 0
            encodings = []
            
            print(f"Capturing face samples for {name}...")
            print("Look at the camera and press SPACE to capture")
            
            while samples_captured < num_samples:
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Display frame
                cv2.imshow(f'Capturing {name} - Sample {samples_captured + 1}/{num_samples}', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                # Press SPACE to capture
                if key == ord(' '):
                    # Find faces in frame
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_frame)
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    
                    if len(face_encodings) > 0:
                        encodings.append(face_encodings[0])
                        samples_captured += 1
                        print(f"✓ Captured sample {samples_captured}/{num_samples}")
                    else:
                        print("✗ No face detected, try again")
                
                # Press ESC to cancel
                elif key == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    return False, "Capture cancelled"
            
            cap.release()
            cv2.destroyAllWindows()
            
            # Save encodings
            for encoding in encodings:
                self.known_encodings.append(encoding)
                self.known_names.append(name)
            
            self._save_encodings()
            
            return True, f"Successfully captured {num_samples} samples for {name}"
            
        except Exception as e:
            return False, f"Error capturing face: {e}"
    
    def authenticate(self, tolerance: float = 0.6) -> Tuple[bool, Optional[str]]:
        """
        Authenticate user via face recognition
        
        Args:
            tolerance: Face matching tolerance (lower = stricter)
            
        Returns:
            Tuple of (authenticated, username)
        """
        try:
            if not self.known_encodings:
                return False, None
            
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return False, None
            
            print("Looking for face...")
            authenticated = False
            recognized_name = None
            
            for _ in range(30):  # Try for 3 seconds (assuming 10 fps)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Find faces
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                for face_encoding in face_encodings:
                    # Compare with known faces
                    matches = face_recognition.compare_faces(
                        self.known_encodings,
                        face_encoding,
                        tolerance=tolerance
                    )
                    
                    if True in matches:
                        # Get the best match
                        face_distances = face_recognition.face_distance(
                            self.known_encodings,
                            face_encoding
                        )
                        best_match_index = np.argmin(face_distances)
                        
                        if matches[best_match_index]:
                            recognized_name = self.known_names[best_match_index]
                            authenticated = True
                            break
                
                if authenticated:
                    break
                
                cv2.imshow('Authentication', frame)
                cv2.waitKey(100)
            
            cap.release()
            cv2.destroyAllWindows()
            
            return authenticated, recognized_name
            
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False, None
    
    def list_users(self) -> list:
        """Get list of registered users"""
        return list(set(self.known_names))
    
    def remove_user(self, name: str) -> Tuple[bool, str]:
        """Remove a user from the system"""
        try:
            indices_to_remove = [i for i, n in enumerate(self.known_names) if n == name]
            
            if not indices_to_remove:
                return False, f"User {name} not found"
            
            # Remove encodings
            for idx in sorted(indices_to_remove, reverse=True):
                del self.known_encodings[idx]
                del self.known_names[idx]
            
            self._save_encodings()
            
            return True, f"Removed {len(indices_to_remove)} samples for {name}"
            
        except Exception as e:
            return False, f"Error removing user: {e}"

# Global face authenticator instance
face_auth = FaceAuthenticator()
