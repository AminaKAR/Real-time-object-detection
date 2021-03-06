#!pip install kafka-python

import sys
import time
import cv2
import imutils
from kafka import KafkaProducer
import config as cfg
import json

def publish_video(producer,topic,video_file="vid.mp4"):
    """
    Publish given video file to a specified Kafka topic. 
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """
    # Open file
    video = cv2.VideoCapture(video_file)
    print('publishing video...')
    while(video.isOpened()):
        success, frame = video.read()
        frame = imutils.resize(frame,width=720)
        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)
        print(type(buffer))
        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())
        time.sleep(0.2)
    video.release()
    print('publish complete')

    
def publish_camera(producer,topic):
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()

            if not success:
                print("bad read!")
                break
            frame = imutils.resize(frame,width=720)
            """
            im_bytes = encoding_img(frame)
            producer.send(topic, im_bytes)
            """
            producer.send(topic, value=frame)
            cv2.imshow('publisher preview',frame)
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
            # Choppier stream, reduced load on processor
            time.sleep(0.2)
    except:
        print("\nExiting.")
    camera.release()


def encoding_img(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    im_bytes = buffer.tobytes()
    return im_bytes

if __name__ == "__main__":
    topic = 'vid'
    kafkaBrokers = ['wn1-*************'] #TODO: Replace with your Kafak broker endpoint (including port)


    producer=KafkaProducer(bootstrap_servers=kafkaBrokers,api_version=(0,10,1),
                        batch_size=15728640,
                        linger_ms=100,
                        max_request_size=15728640)

    input_type = "video"
    if input_type == "video":
        print("sending frames...")
        publish_video(producer,topic)
    elif input_type == "webcam":
        print("sending frames...")
        publish_camera(producer,topic)





