import time
import os
import numpy as np
import cv2
from picamera2 import Picamera2
from picamera2.devices.imx500 import IMX500

# 1. Force Display for SSH (Ensures window opens on Pi Desktop)
os.environ["DISPLAY"] = ":0"

# 2. Path to the IMX500 AI Model
model_file = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"

# 3. Initialize Hardware
imx500 = IMX500(model_file)
picam2 = Picamera2()

# Configure for 640x480 RGB (Fastest for OpenCV processing)
config = picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# --- 4. SCANNING & HYSTERESIS SETTINGS ---
CENTER_X = 320         # Middle of the 640px frame
TOLERANCE = 120        # Detection zone width (adjust based on table size)
ENTRY_BUFFER = 5       # Consecutive frames to confirm a person entered
EXIT_BUFFER = 25       # Consecutive empty frames to confirm a person left

# State Variables
is_detecting = False
in_zone_count = 0
out_of_zone_count = 0
first_step = 0
last_seen_step = 0
player_locations = []

print("\n" + "="*40)
print("CARD DEALER AI: ACTIVE SCANNING")
print("Press 'q' in the camera window to stop.")
print("="*40 + "\n")

try:
    # Run for a set duration (e.g., 5000 frames) or until interrupted
    for current_step in range(500):
        # A. Capture AI Metadata and Image Frame
        request = picam2.capture_metadata()
        frame = picam2.capture_array()
        
        # B. Extract AI detections from the IMX500 chip
        outputs = imx500.get_outputs(request)
        person_currently_visible = False
        
        if outputs and len(outputs) >= 3:
            boxes = np.atleast_2d(outputs[0][0])
            scores = np.atleast_1d(outputs[1][0])
            classes = np.atleast_1d(outputs[2][0])
            
            for i in range(len(scores)):
                # Class 0 = Person (MobileNet SSD)
                if int(classes[i]) == 0 and scores[i] > 0.50:
                    # Convert AI normalized coordinates to pixel coordinates
                    scaled_box = imx500.convert_inference_coords(boxes[i], request, picam2)
                    box_center = scaled_box[0] + (scaled_box[2] / 2)
                    
                    # VISUAL FEEDBACK: Draw on the frame
                    # Blue circle for any detected person
                    cv2.circle(frame, (int(box_center), 240), 10, (255, 0, 0), 2)
                    
                    # Check if person is within the dealer's "Action Zone"
                    if abs(box_center - CENTER_X) < TOLERANCE:
                        person_currently_visible = True
                        last_seen_step = current_step # Mark the literal last frame seen
                        # Green circle for person in the action zone
                        cv2.circle(frame, (int(box_center), 240), 20, (0, 255, 0), 3)
                        break

        # --- 5. TRUE MIDPOINT LOGIC ---
        if person_currently_visible:
            out_of_zone_count = 0 # Reset exit timer
            if not is_detecting:
                in_zone_count += 1
                if in_zone_count >= ENTRY_BUFFER:
                    is_detecting = True
                    # Set start to the literal first frame of the buffer
                    first_step = current_step - (ENTRY_BUFFER - 1)
                    print(f"PLAYER SPOTTED  (Start Step: {first_step})")
        else:
            in_zone_count = 0 # Reset entry timer
            if is_detecting:
                out_of_zone_count += 1
                if out_of_zone_count >= EXIT_BUFFER:
                    is_detecting = False
                    
                    # Calculate midpoint using the literal last frame seen
                    # This ignores the "cooldown" frames for 100% accuracy
                    midpoint = (first_step + last_seen_step) // 2
                    player_locations.append(midpoint)
                    
                    print(f"PLAYER SAVED    (Midpoint: {midpoint}, End Step: {last_seen_step})")
                    out_of_zone_count = 0

        # --- 6. DISPLAY ---
        # Draw the "Action Zone" boundaries for calibration
        cv2.line(frame, (CENTER_X - TOLERANCE, 0), (CENTER_X - TOLERANCE, 480), (0, 0, 255), 1)
        cv2.line(frame, (CENTER_X + TOLERANCE, 0), (CENTER_X + TOLERANCE, 480), (0, 0, 255), 1)
        
        cv2.imshow("Dealer AI Viewfinder", frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        # Small sleep to keep timing consistent (approx 60-100 FPS total)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping manual scan...")
finally:
    # Cleanup
    cv2.destroyAllWindows()
    picam2.stop()
    
    print("\n" + "="*40)
    print(f"FINAL PLAYER POSITIONS: {player_locations}")
    print(f"TOTAL PLAYERS FOUND: {len(player_locations)}")
    print("="*40)