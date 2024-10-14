from kafka import KafkaProducer
from PIL import Image
from io import BytesIO
import json
import base64

# 将PIL.Image对象序列化为Base64字符串
def serialize_image_to_binary(image):
    image_format = image.format if image.format else 'png'
    with BytesIO() as output:
        image.save(output, format=image_format)  # 将图像保存为字节流
        image_data = output.getvalue()  # 获取字节数据
        return base64.b64encode(image_data).decode('utf-8'), image_format  # 编码为Base64并转为字符串


# 创建Kafka生产者
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=lambda k: k.encode('utf-8'),  # 将字符串编码为字节
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 序列化为JSON格式
)


image = Image.open("test_image.jpg").convert("RGB")
image_base64_data, image_format = serialize_image_to_binary(image)
# 创建要发送的字典
message_dict = {
    'text': 'This is a sample message',
    'image_base64_data': image_base64_data,  # 将图像序列化为Base64字符串
    'image_format': image_format
}

# 发送消息，指定键和值
producer.send('test_topic', key="hello", value=message_dict)

print('Message sent to Kafka!')
producer.close() # 关闭生产者
