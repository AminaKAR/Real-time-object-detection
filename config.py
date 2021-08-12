# --------------------------------------------- Kafka --------------------------------------------
   topic = 'vid'
    kafkaBrokers = [''] #TODO: Replace with your Kafka broker endpoint (including port)
# -------------------------------------- profile_detection ---------------------------------------
detect_frontal_face = 'profile_detection/haarcascades/haarcascade_frontalface_alt.xml'
detect_perfil_face = 'profile_detection/haarcascades/haarcascade_profileface.xml'

 ---------------------------------------
=
path_model = 'emotion_detection/Modelos/model_dropout.hdf5'
wts = './weights/yolov3.weights'
classes = './yolov4.txt'
f = './cfg/yolov3.cfg'
=
w,h = 48,48
rgb = False
labels = ['angry','disgust','fear','happy','neutral','sad','surprise']

