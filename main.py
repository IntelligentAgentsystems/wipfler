from Units.conveyor_belt import *

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

# pinger = PingActor.start()
# ponger = PongActor.start()
#
# ponger.ask('Ping')
#
# sleep(5)
#
# pinger.stop()
# ponger.stop()
#
# sleep(2)
#
c1 = ConveyorBelt((0, 0))
print(c1.direction)
for i in range(0, 10):
    c1.turn_counter_clockwise()
    print(c1.direction)


print('Terminate main')

