from kafka import KafkaConsumer
from PIL import Image
from io import BytesIO
import json
import base64

def decode_base64_to_image(base64_str):
    image_bytes = base64.b64decode(base64_str)  # 解码为字节数据
    image = Image.open(BytesIO(image_bytes))  # 反序列化为PIL.Image对象
    return image

"""
如果两个消费者（比如 Consumer A 和 Consumer B）订阅了同一个主题（topic），并且它们属于同一个消费者组（同一个 group_id），那么 Kafka 会确保每条消息只会被组中的一个消费者消费。
这意味着 Consumer A 和 Consumer B 共享消息，只有其中一个消费者会收到某条消息，具体由 Kafka 根据分区的分配策略来决定。

如果这两个消费者属于不同的消费者组（例如 Consumer A 在 group_id_1 中，Consumer B 在 group_id_2 中），那么每个消费者组都会收到主题中的所有消息。
这意味着 Consumer A 会收到消息，Consumer B 也会收到相同的消息，各自处理各自的副本。
"""
# 创建Kafka消费者
consumer = KafkaConsumer(
    'test_topic',  # 主题名称
    bootstrap_servers='10.2.64.91:9092',
    group_id='my_group', # 设置消费者组
    key_deserializer=lambda k: k.decode('utf-8'),  # 解码字节为字符串
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # 反序列化值
)

# 消费消息
for message in consumer:
    # 获取键值
    key = message.key
    value = message.value  # 反序列化后的值
    # 获取文本信息
    text_message = value['text']
    print(f'Received text: {text_message} with key: {key}')
    
    # 从Base64字符串反序列化为PIL.Image对象
    image = decode_base64_to_image(value['image_base64_data'])
    image_format = value['image_format']

    image.save(f'received_image.{image_format}') # 保存到文件
    print(f'Image received {image_format} from Kafka!')
