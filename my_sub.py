# coding=utf-8
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /Users/macbook/opt/anaconda3/lib/python3.7/site-packages/pyspark/jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.6.jar pyspark-shell'
import cv2
import json
import numpy as np
import config as cfg
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
from pyspark import SparkContext, SparkConf
import pyspark
import dlib
#from emotion_detection import f_emotion_detection
from utils import *
from darknet import Darknet

#------------------------------------------------------------------------------------------------------------------------------------------
#                                               obtener frames del mensaje
def deserializer(im_byte):
    # bytes --> jpg
    decoByte = np.frombuffer(im_byte, dtype=np.uint8)
    # Jpg --> unit8
    decoJpg = cv2.imdecode(decoByte, cv2.IMREAD_COLOR)
    return decoJpg
#------------------------------------------------------------------------------------------------------------------------------------------
#                                           Obtener bounding box rostros
def get_objects(m):
    iou_thresh = 0.4
    nms_thresh = 0.6
    d = Darknet(cfg.f)
    d.load_weights(cfg.wts)
    class_names = load_class_names(cfg.classes)
    im = m[1]
    gray =  cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(gray, (d.width, d.height))
    boxes = detect_objects(d, resized_image, iou_thresh, nms_thresh)
    plot_boxes(gray, boxes, class_names, plot_labels = True)
    result = print_objects(boxes, class_names)
    return result
        
  
from kafka import KafkaProducer
my_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def message_sender(m):
    """Send (key, value) to a Kafka producer"""
    my_producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    my_producer.send(cfg.end_topic,m)
    return m

# ------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    conf = SparkConf()
    sc = SparkContext(master="local", appName='video_streaming_job', conf=conf)
    sc.setLogLevel('WARN')
    n_secs = 0.5  # en segundos
    ssc = StreamingContext(sparkContext=sc, batchDuration=n_secs)

    kafkaParams = {'bootstrap.servers':'localhost:9092', 
                    'fetch.message.max.bytes':'15728640',
                    'auto.offset.reset':'largest'}
    stream = KafkaUtils.createDirectStream(ssc=ssc,
                    topics=[cfg.topic],
                    kafkaParams=kafkaParams,
                    valueDecoder=lambda v: deserializer(v))  
    
    # inicio pipeline                                     
    stream.map(
            get_objects
        ).map(
          message_sender
        ).pprint()

    # comienza la computación de streaming
    ssc.start()
    # espera que la transmisión termine
    ssc.awaitTermination()
