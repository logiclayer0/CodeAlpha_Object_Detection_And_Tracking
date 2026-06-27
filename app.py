import cv2
import time
from ultralytics import YOLO

class ProductionTrackerEngine:
    def __init__(self):
        print("[INFO] Loading Core AI Framework...")
        # Industry standard YOLOv8 nano deployment
        self.model = YOLO('yolov8n.pt') 
        
    def execute_live_pipeline(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("[ERROR] Critical Error: Camera driver peripheral failed.")
            return

        print("[INFO] Matrix stream running. Tap 'q' key to release resources.")
        
        # Initializing core time tracking buffers for FPS computation
        prev_time = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Frame geometry extraction
            height, width, _ = frame.shape

            # Executing deep feature tracking pipeline
            results = self.model.track(frame, persist=True, verbose=False)
            
            # Rendering baseline detections arrays
            annotated_frame = results[0].plot()

            # Dynamic Object Counting Logic
            detected_boxes = results[0].boxes
            target_count = len(detected_boxes) if detected_boxes is not None else 0

            # Real-Time FPS Performance Computation
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time

            # --- CYBERPUNK INDUSTRIAL SYSTEM OVERLAY DESIGN ---
            # Top Header HUD bar background
            cv2.rectangle(annotated_frame, (0, 0), (width, 55), (22, 17, 13), -1)
            cv2.line(annotated_frame, (0, 55), (width, 55), (88, 166, 248), 1)

            # Telemetry Metadata Overlays (FPS, Targets Count, Dimensions)
            cv2.putText(annotated_frame, f"ENGINE: NEXUS-VISION v1.0", (20, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139, 148, 158), 1, cv2.LINE_AA)
            
            cv2.putText(annotated_frame, f"FPS: {int(fps)}", (width - 260, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (126, 231, 135) if fps > 20 else (248, 81, 73), 2, cv2.LINE_AA)
            
            cv2.putText(annotated_frame, f"LIVE TARGETS: {target_count}", (width - 150, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (88, 166, 248), 2, cv2.LINE_AA)

            # Bottom Status Matrix Bar
            cv2.rectangle(annotated_frame, (0, height - 30), (width, height), (22, 17, 13), -1)
            cv2.line(annotated_frame, (0, height - 30), (width, height - 30), (48, 54, 61), 1)
            cv2.putText(annotated_frame, f"RESOLUTION: {width}x{height} | STREAM: ACTIVE | CODEALPHA AIML ENGINE", (20, height - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (139, 148, 158), 1, cv2.LINE_AA)

            # Display updated graphic frames matrix
            cv2.imshow("CodeAlpha AI Object Tracker Hub", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] System architecture offline.")

if __name__ == "__main__":
    engine = ProductionTrackerEngine()
    engine.execute_live_pipeline()