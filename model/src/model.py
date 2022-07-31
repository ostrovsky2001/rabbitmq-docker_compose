import pika
import pickle
import numpy as np
import json
import os
import sklearn
print(os.getcwd())
with open('./src/myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)
print(type(regressor))
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='Features')
    channel.queue_declare(queue='y_pred')


    def callback(ch, method, properties, body):
        dict_queue = json.loads(body)
        array = dict_queue['features']
        y_pred = regressor.predict(np.array(array).reshape(1,len(array)))[0]
        dict_y_pred = {'timestamp':dict_queue['timestamp'],
                        'y_pred':y_pred.tolist()}
        channel.basic_publish(exchange='',
                                routing_key='y_pred',
                                body=json.dumps(dict_y_pred))
        print(f'Получено предсказание для признаков с id={dict_queue["timestamp"]}')
        print(dict_y_pred)

    channel.basic_consume(
        queue='Features', on_message_callback=callback, auto_ack=True)


    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди в model.py')