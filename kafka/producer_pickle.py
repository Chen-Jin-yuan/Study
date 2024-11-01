from kafka import KafkaProducer
from PIL import Image
import pickle
from msg import Msg

# 创建Kafka生产者
producer = KafkaProducer(
    bootstrap_servers='10.2.64.75:9092',
    key_serializer=lambda k: k.encode('utf-8'),  # 将字符串编码为字节
    value_serializer=lambda v: pickle.dumps(v)  # 序列化
)


image = Image.open("test_image.jpg").convert("RGB")
# 创建要发送的字典
message_dict = {
    'text': 'This is a sample message',
    'image': image, # pickle不用序列化
    'image_format': "PNG"
}
# 不需要序列化字典，可以直接序列化对象
msg = Msg()
msg.input_data = message_dict
msg.key = "this is key"
for i in range(10):
    # 发送消息，指定键和值
    producer.send('test_topic', key=f"hello-{i}", value=msg)

print('Message sent to Kafka!')
producer.close() # 关闭生产者
