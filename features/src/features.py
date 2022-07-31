import pika
import numpy as np
import json
import time
from sklearn.datasets import load_diabetes

X,y = load_diabetes(return_X_y=True)

while True:
    try:
        random_row = np.random.randint(0, X.shape[0]-1)
        timestamp = time.time()
        dict_y_true = {'timestamp':timestamp,
                        'y_true':y[random_row].tolist()}
        dict_features = {'timestamp':timestamp,
                        'features':X[random_row].tolist()}

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='Features')

        channel.basic_publish(exchange='',
                                routing_key='y_true',
                                body=json.dumps(dict_y_true))
        channel.basic_publish(exchange='',
                                routing_key='Features',
                                body=json.dumps(dict_features))
                                
        print(f'Сообщения отправлены в очередь с id={timestamp}')
        connection.close()
        time.sleep(5)
    except:
        print('Не удалось подключиться к очереди в features.py')