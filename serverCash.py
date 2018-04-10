import json

import time


class Cash:
    def __init__(self):
        self.name_to_data = {}
        self.data_to_name = {}
    
    def register_entry(self, record):
        self.name_to_data[record.name] = record
        self.data_to_name[record.data] = record
    
    def refresh_cash(self):
        for record in list(self.name_to_data.values()):
            if record.ttl < time.time():
                self.name_to_data.pop(record.name)
                self.data_to_name.pop(record.data)
    
    def save(self, file='server_cash.json'):
        with open(file, 'w') as f:
            f.write(json.dumps([self.name_to_data, self.data_to_name]))
    
    def load(self, file='server_cash.json'):
        try:
            with open(file, 'r') as f:
                self.name_to_data, self.data_to_name = json.loads(f.read())
        except FileNotFoundError:
            pass
    
    def register_package(self, package):
        for record in package.answers:
            self.register_entry(record)
        for record in package.authority_records:
            self.register_entry(record)
        for record in package.additional_records:
            self.register_entry(record)
    
    def assure_consistency(self):
        print('Assuring consistency')
        while True:
            self.refresh_cash()
            time.sleep(60)
