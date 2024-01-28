import cv2
from flask import Flask, render_template, Response, request
from openai import OpenAI
import os
import requests

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

# OpenAI API Key
API_KEY = "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"


def generate_story(selected_item):
    client = OpenAI(api_key=API_KEY)
    prompt = f"Write a 200 word fairy tale story about a {selected_item}. The primary audience of this story is for children."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
    )

    ai_response = response.choices[0].message.content
    return ai_response


def generate_text_to_speech(prompt):
    def generateTextToSpeech(prompt):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/oWAxZDx7w5VEj9dCyTzz"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": "be02680fb61d7c65edb047fde0b7a3cb"
        }

        data = {
            "text": prompt,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)
        with open('audio/speechoutput.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
    pass


def generate_frames(selected_item):
    while True:
        success, frame = cap.read()

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                class_id = int(detections[0, 0, i, 1])
                label = classes[class_id]
                box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                (startX, startY, endX, endY) = box.astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ai_response = generate_story(selected_item)
        generate_text_to_speech(ai_response)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template('ai&cam.html')


@app.route('/video')
def video():
    selected_item = request.args.get('items', 'background')  # Default to 'background' if not selected
    return Response(generate_frames(selected_item), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

