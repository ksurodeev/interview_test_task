import json
from pprint import pprint

class Seeker:
    '''
    Class for seeking interfaces and cards. 
    '''
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as file:
            self._sample = json.load(file)  
        self.sample = self._sample           ### dictionary loaded from file

    def int_seek(self, parameter, value):
        '''
        Function for seeking interface parameters in file. Doesn't seek in Loopback|MGMT|Null interfaces. 
        Returns dictionary.
        '''
        #pprint(sample['task_result']['content']['network-element'][0]['interface'])
        result = {}
        interfaces_dict = self.sample['task_result']['content']['network-element'][0]['interface']
        for int in interfaces_dict:
            if int[parameter] == value and 'Mgmt' not in int['name'] and 'Null' not in int['name'] and 'Loopback' not in int['name']:
                result.setdefault(int['name']) 
                result[int['name']] = [int['name'], int['oper-status'], int['id'], int['hw-component-reference']]
        return result
    
    def hw_seek(self, hw_component):
        '''
        Function for seeking card from hw-component-reference-id. Returns dictionary.
        '''
        result = {}
        hw_dict = self.sample['task_result']['content']['network-element'][0]['hw-component']
        for hw in hw_dict:
            if hw['id'] == hw_component:
                result.setdefault(hw['model-name'])
                result[hw['model-name']] = ', '.join([hw['model-name'], ''.join(hw['parent-slot-ref-name'])])
        return result

    def write(self, filename, value):
        '''
        Function for writing result to file.
        '''
        with open(filename, 'a') as f:
            f.write(value)


if __name__ == "__main__":
    uniq_cards_id = []
    seek = Seeker('ne-data-sample.txt')
    interfaces = seek.int_seek('oper-status', 'up')
    for key in interfaces.keys():
        uniq_cards_id.append(interfaces[key][3])
    uniq_cards_id = set(uniq_cards_id)              ### find an unique cards
    for card_id in list(uniq_cards_id):
        seek.write('test.txt', ''.join(list(seek.hw_seek(card_id).values())) + '\n')    ### write card info
        for key in interfaces.keys():
            if interfaces[key][3] == card_id:
                seek.write('test.txt', '\t' + ' '.join(interfaces[key][0:3]) + '\n')    ### write interface info

    