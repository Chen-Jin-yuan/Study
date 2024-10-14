from kafka.admin import KafkaAdminClient, NewTopic

# 创建Kafka AdminClient
admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092', client_id='test')

def create_topic():
    # 定义要创建的主题及其分区和副本因子
    topic_name = "test_topic"
    num_partitions = 1
    replication_factor = 1

    # 创建新的主题
    new_topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    # 创建主题
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)

    print(f"Topic '{topic_name}' created with {num_partitions} partitions.")

def delete_topic():
    topic_name = "test_topic"
    admin_client.delete_topics(topics=[topic_name])
    print("delete", topic_name)

create_topic()
# delete_topic()

admin_client.close()