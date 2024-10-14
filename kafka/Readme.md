# env
python=3.10.14
* pip install kafka-python
# run
* docker-compose up -d
* docker-compose down 
# check
* docker exec -it {container id} /bin/bash
* kafka-topics.sh --describe --bootstrap-server localhost:9092