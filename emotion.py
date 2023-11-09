import cv2
from deepface import DeepFace
from twilio.rest import Client
import threading



def send_notifications():

    account_sid = 'AC678944e9b523a086ee25760e241cfc2f'
    auth_token = '58edb44f0c4022039e38186296fe9e1d'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+12028833925',
    body='The children are crying',
    to='+254794505881'
    )



def emotion_recognition():
    # Load the pre-trained emotion detection model
    model = DeepFace.build_model("Emotion")

    # Define emotion labels
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start capturing video
    cap = cv2.VideoCapture(0)

    no_times_sad=0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


        for (x, y, w, h) in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = gray_frame[y:y + h, x:x + w]

            # Resize the face ROI to match the input shape of the model
            resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)

            # Normalize the resized face image
            normalized_face = resized_face / 255.0

            # Reshape the image to match the input shape of the model
            reshaped_face = normalized_face.reshape(1, 48, 48, 1)

            # Predict emotions using the pre-trained model
            preds = model.predict(reshaped_face)[0]
            emotion_idx = preds.argmax()
            emotion = emotion_labels[emotion_idx]

            # test sending notifications

            if emotion == "sad":
                no_times_sad = no_times_sad + 1

            if no_times_sad == 10:
                print("hello")
                send_notifications()


            # Draw rectangle around face and label with predicted emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Real-time Emotion Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

thread1 = threading.Thread(target=emotion_recognition)
thread1.start()
