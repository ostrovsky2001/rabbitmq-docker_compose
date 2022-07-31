import pika
import json
import os 
print(os.getcwd())
with open('./data/data.json','r') as input:
    data = json.load(input)
print(data)
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq')
    )
    channel = connection.channel()
    channel.queue_declare(queue='y_pred')
    channel.queue_declare(queue='y_true')
    def callback(ch, method, properties, body):
        dict_queue = json.loads(body)
        if dict_queue['timestamp'] in data.keys():
            data[dict_queue['timestamp']].update({method.routing_key:dict_queue[method.routing_key]})
            if len(data)>1:
                data[dict_queue['timestamp']]['RMSE'] = (((list(data.values())[-2]['RMSE']**2*(len(data)-1))+(data[dict_queue['timestamp']]['y_pred'] - data[dict_queue['timestamp']]['y_true'])**2)/len(data))**0.5
            else:
                data[dict_queue['timestamp']]['RMSE'] = abs(data[dict_queue['timestamp']]['y_pred'] - data[dict_queue['timestamp']]['y_true'])
        else:
            data[dict_queue['timestamp']]={}
            data[dict_queue['timestamp']].update({method.routing_key:dict_queue[method.routing_key]})
        with open('./data/data.json','w') as output:
            json.dump(data,output,indent=4)
        print(f'Из очереди {method.routing_key} получено значение {method.routing_key}={dict_queue[method.routing_key]} с id={dict_queue["timestamp"]}')
    channel.basic_consume(
        queue='y_pred', on_message_callback=callback, auto_ack=True
    )
    channel.basic_consume(
        queue='y_true', on_message_callback=callback, auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди в metric.py')