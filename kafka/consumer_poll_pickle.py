from kafka import KafkaConsumer
from PIL import Image
import time
import pickle
from msg import Msg

# 创建Kafka消费者
consumer = KafkaConsumer(
    'test_topic',  # 主题名称
    bootstrap_servers='10.2.64.75:9092',
    group_id='my_group',  # 设置消费者组
    key_deserializer=lambda k: k.decode('utf-8'),  # 解码字节为字符串
    value_deserializer=lambda v: pickle.loads(v)  # 反序列化值
)

# 消费消息的非阻塞模式
while True:
    # poll 方法用于尝试从 Kafka 中获取消息，timeout_ms 设置为 10 毫秒，轮询开销约0.03个核
    # timeout_ms 参数用于指定等待消息的超时时间，单位为毫秒。在超时时长内，如果没有消息可用， consumer.poll()将返回一个空的消息集合。

    messages = consumer.poll(timeout_ms=10)
    if not messages:
        # 没有消息时可以执行其他任务
        print("No messages, doing other tasks...")
        time.sleep(1)  # 模拟其他任务的处理时间
        continue
    
    # 处理获取到的消息
    for topic_partition, records in messages.items():
        for message in records:
            # 获取键值
            key = message.key
            value = message.value  # 反序列化后的值
            print(value)
            # 获取文本信息
            text_message = value.input_data['text']
            print(f'Received text: {text_message} with key: {key}')

            image = value.input_data['image']
            image_format = value.input_data['image_format']
            image.save(f'received_image.{image_format}')  # 保存到文件
            print(f'Image received {image_format} from Kafka!')
            print(value.key)

    # 手动提交偏移量
    # Kafka 默认会使用自动提交的机制（如果配置了 enable.auto.commit=true），在设置的时间间隔后自动提交偏移量。
    # 自动提交偏移量时，如果消息还未被处理，消费者崩溃或重启后会从新的偏移量继续读取，这可能导致部分消息没有被处理就标记为已消费。
    consumer.commit()
