import cv2

def preprocess_frames(frames):
    processed = []

    for frame in frames:
        # Handle both grayscale and color frames
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        # Optional: resize (if you had it earlier)
        gray = cv2.resize(gray, (64, 64))

        processed.append(gray)

    return processed