import logging
import asyncio
import random
from signalwire.relay.consumer import Consumer

#+1 (201) 277-7289

global simon_sequence
global input_list

class CustomConsumer(Consumer):
    def setup(self):
        self.project = ''
        self.token = ''
        self.contexts = ['office']

    async def ready(self):
        logging.info('CustomConsumer is ready!')

    async def on_incoming_call(self, call):
        async def on_digit(data):
            digit = data["params"]["event"]
            input_list.append(digit)

        def pick_number():
            randnum = random.choice(list(range(1,10)))
            simon_sequence.append(str(randnum))
            print(simon_sequence)
                

        result = await call.answer()            
        if result.successful:
            await asyncio.sleep(1)
            await call.play_tts(text='Welcome to simon. Memorize the sequence and repeat it back.', gender = 'male')
            call.on('detect.update', on_digit)
            action = await call.detect_digit_async(digits = '123456789', timeout = 900)
            simon_sequence = []
            input_list = []
            while(call.active and not action.completed):
                if len(input_list) == len(simon_sequence):
                    if(input_list == simon_sequence):
                        pick_number()      
                        for x in range(len(simon_sequence)):
                            simon_string = str(simon_sequence[x])
                            await call.play_tts(text = simon_string, gender = 'male')
                    else:
                        print(input_list)
                        await call.play_tts(text='Epic fail, you suck! Starting Over', gender = 'male')
                        simon_sequence = []
                    input_list = []         
                await asyncio.sleep(0)
            await action.stop()
        logging.info('Hanging up..')
        await call.hangup()

consumer = CustomConsumer()
consumer.run()
