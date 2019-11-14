from producer_actor import ProducerActor
from consumer_actor import ConsumerActor
from time import sleep

from ping_actor import PingActor
from pong_actor import PongActor

# consumer = ConsumerActor()
# producer = ProducerActor(consumer=consumer)
#
# producer.start()
# consumer.start()
#
# sleep(2)
#
# print('stopping')
# producer.stop()
# consumer.stop()
# print('done')

pinger = PingActor.start()
ponger = PongActor.start()

ponger.ask('Ping')


sleep(5)

pinger.stop()
ponger.stop()

sleep(2)

print('Terminate main')