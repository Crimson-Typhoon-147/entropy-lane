import cv2

def preprocess_frames(frames):
    processed_frames = []

    for frame in frames:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize to fixed resolution
        resized = cv2.resize(gray, (320, 240))

        # Light Gaussian blur to suppress camera/compression artifacts
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)

        processed_frames.append(blurred)

    return processed_frames
