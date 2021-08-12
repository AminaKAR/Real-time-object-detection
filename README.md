# Real-time-object-detection
This is a project originally made for emotion detection in real time, you find the original work here  through this link: https://github.com/juan-csv/Architecture-for-real-time-video-streaming-analytics.



This was a very helpful and clear repository, it helped me learn how to work with spark and kafka.
What i did is i changed the emotion detection into object detection with YOLO V3
So the final output can be found in the two images output-frame.png and output.png

Start Zookeeper and kafka
To simplify the tedious task of building a kafka server, we will use Docker with Kafka and Zookeeper out of the box: Go to the kafka-docker folder

$ cd kafka-docker 
Start Kafka and Zookeeper with Docker Compose

$ docker-compose -f docker-compose_local.yml up 
In the docker-compose_local.yml configuration file, the topics are defined, the url and the port through which our publisher and subscribers connected.

To stop Kafka uses

$ docker-compose stop 
for more information Apache Kafka: Docker Container refer to this post

Send frames in real time with Kafka:

spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.7  my_pub.py

Get frames in real time with Kafka:


spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.7  my_sub.py

If you have come this far you should be able to see something like this:
x-special/nautilus-clipboard
copy
https://github.com/AminaKAR/Real-time-object-detection/blob/main/output.png
