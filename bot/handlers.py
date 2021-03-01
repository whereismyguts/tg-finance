from bot.bot_base import BaseHandler
from sheets_api import append_transaction, get_data_from_current_list
import datetime
import traceback

class ContainTestDataSource:
    # STAY IN DATABASE-LIKE PARADIGM
    _data = {
        'items': [],
    }

    # types:
    # Item = Type('Item', {'key', 'date'})
    
    @property
    def items(self):
        return self._data['items']
    

    def insert_item(self, key, date):
        self.items.append({"key": key, date: datetime.datetime.utcnow()})


    def get_items(self, key):
        result = []
        for i in self.items:
            if i['key'] == key:
                result.append(i)
        return result

class FinacialHandler(BaseHandler, ContainTestDataSource):

   
    
    # override:

    def _handle_message(self, text):
        # print(self.data)

        self.handle_key(text)
            # self.send('unknow')

        
        # self.send('texted: {}'.format(text))
        # self.send('What to do?', keys=[
        #     {'text': 'new event', 'data': 'new'},
        #     {'text': 'nah', 'data': 'nah'}
        # ])

    def _handle_press(self, buttons, button_id):
        # print(buttons[button_id]['text'])
        
        # self.send('pressed: {}'.format(buttons[button_id]))
        print('buttons[button_id]')
        print(buttons[button_id])
        self.handle_key(buttons[button_id]['callback_data'])

    def handle_key(self, text):
        
        try:
            value, *text = text.split(' ')
            value = int(value)
            text = ' '.join(text)
        except Exception as e:
            self.send('Wrong format (<int_value> <description text>).\nError: {}'.format(e))
            print(e, traceback.format_exc())
            return
        try:
            append_transaction(text, value)
        except Exception as e:
            self.send('Error while appending transaction:\n{}'.format(e))
            print(e, traceback.format_exc())
            return
        
        data = get_data_from_current_list('H29:J30')
        msg = '\n'.join([' '.join(row) for row in data])
        self.send('✔️{}р - "{}"\n{}'.format(
            value, text, msg
        ))
        # if not text.startswith("/"):
        #     self.append_item(text)
        #     self.send('{} added. Total: {}'.format(
        #         text,
        #         len(self.get_items(key=text)),
        #     ))
        
        # self.send_main_menu()

