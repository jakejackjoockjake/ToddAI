import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load pre-trained MobileNet SSD model
net = cv2.dnn.readNetFromCaffe(
    'MobileNetSSD_deploy.prototxt',
    'MobileNetSSD_deploy.caffemodel'
)

# Labels for the 21 classes used by MobileNet SSD
classes = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]

# Open a video capture object (0 corresponds to the default camera)
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Capture a frame
        success, frame = cap.read()

        # Resize frame to 300x300 pixels (required input size for MobileNet SSD)
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

        # Set the input to the network
        net.setInput(blob)

        # Forward pass through the network
        detections = net.forward()

        # Loop over the detections and draw bounding boxes
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:  # Confidence threshold
                class_id = int(detections[0, 0, i, 1])
                label = classes[class_id]
                box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Provide the frame to the browser

@app.route('/')
def home():
    return render_template('ai&cam.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)