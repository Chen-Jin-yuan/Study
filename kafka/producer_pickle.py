from kafka import KafkaProducer
from PIL import Image
import pickle

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
for i in range(10):
    # 发送消息，指定键和值
    producer.send('test_topic', key=f"hello-{i}", value=message_dict)

print('Message sent to Kafka!')
producer.close() # 关闭生产者
