import pika
import marshal


def start_server(queue, callback):
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()


def request_reply(key, callback, _id, command):
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    reply_queue = channel.queue_declare(queue='', exclusive=True)
    callback_queue = reply_queue.method.queue

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.basic_publish(
        exchange='',
        routing_key=key,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=_id
        ),
        body=command
    )
    print("WAITING FOR RESPONSE...")
    connection.process_data_events(time_limit=10)


def publish_message(channel, reply_queue, _id, msg):
    channel.basic_publish(
        exchange='',
        routing_key=reply_queue,
        properties=pika.BasicProperties(
            correlation_id=_id
        ),
        body=marshal.dumps(msg)
    )


def receive_template(response):
    status = response[0]

    if status == "SUCCESS":
        print("Response: SUCCESS")
        return True

    print("Response: FAILED")
    print("Error:", response[1])
    return False


def display_choices(server_list):
    keys = []
    for index, server in enumerate(server_list):
        keys.append(server)
        print(f'\t{index + 1}) {server}')

    if len(keys) == 0:
        return None

    if len(keys) == 1:
        print("AUTO SELECTING", keys[0], "AS ONLY ONE CHOICE")
        return keys[0]

    choice = int(input("Enter choice: "))
    return keys[choice - 1]


def check_publish_format(article_type, author, time, content):
    categories = ["SPORTS", "FASHION", "POLITICS"]

    if article_type not in categories or \
            time != '' or \
            author == '' or \
            content == '' or \
            len(content) > 200:
        return False

    return True
