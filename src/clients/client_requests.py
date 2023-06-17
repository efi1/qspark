import copy
import csv
import itertools
import json
import logging
from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from typing import Iterator

logging.getLogger()


class RequestesLocatesClient:

    def __init__(self, rsrc_path):
        self.rsrc_path = rsrc_path
        self.data = []

    def load_data(self, csv_file: str):
        """
        loading data from csv into this client
        :param csv_file:
        """
        csv_file_path = Path(self.rsrc_path).joinpath(csv_file)
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            for row in csv_reader:
                row['number_of_locates_requested'] = int(row['number_of_locates_requested'])
                self.data.append(row)
            logging.info(F'data from {csv_file} was loaded successfully')

    def request_locates(self, requested_locates: dict[str, int]) -> dict[str, int]:
        """
        gets a customer's locates request of a specific symbol and return the approved located
        :param requested_locates: e.g. {"client_name": "Client1", 'symbol': "TTT", "number_of_locates_requested": 100}
        :return: e.g. {'client_name': 'Client1', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100}
        """
        requested_locates = json.loads(requested_locates) if not isinstance(requested_locates, dict) else requested_locates
        if self.calc_approved_error:
            res = {"Error": self.calc_approved_error, "error": 0}
            logging.error(F'request: {requested_locates}, ended with error: {res}')
            return res
        req_per_client = self.dist_loc_by_client.get(requested_locates['client_name'])
        if req_per_client:
            for i in req_per_client:
                symbol = i.get('symbol')
                if symbol == requested_locates['symbol']:
                    res = {"client_name": requested_locates['client_name'], "symbol": symbol,
                            "req_locates": requested_locates['number_of_locates_requested'],
                            "approved_locates": i['approved_locates']}
                    logging.info(F'request: {requested_locates}, has this approved locates: {res}')
                    return res
        res = {"Error": F"no approved locates found for {requested_locates['client_name']}-symbol-{requested_locates['symbol']}", "error": 1}
        logging.error(F'request: {requested_locates}, ended with error: {res}')
        return res

    @classmethod
    def sort_by_field(cls, field_name: str, data: list[dict]) -> list[dict]:
        """
        Sort the data the field which is given (field=symbol)
        :param field_name: can be Symbol, client_name or number_of_locates_requested
        :param data: the loaded data from csv
        :return: sorted data
        """
        return sorted(data, key=lambda x: x.get(field_name))

    def group_by_field(self, field_name: str) -> Iterator[tuple[str, list[dict]]]:
        """
        gatheres the data by the symbol request (or any other field which is given).
        :param field_name: the field to be gathered from - in our scope we used field=symbol
        :return: generator (of which the data can be retrieved)
        """
        data = copy.deepcopy(self.data)
        sorted_data = RequestesLocatesClient.sort_by_field(field_name, data)
        for key, value in itertools.groupby(sorted_data, key=itemgetter(field_name)):
            yield key, list(value)

    def calc_approved_locates_by_client(self, field_name: str, approved_locates: [str, dict]):
        """
        Calculates the approved locates for each client.
        :param field_name: the field for the data to accumulated by - the symbol field.
        :param approved_locates: the approved locate per each symbol.  e.g. {"ABC" : 480, "QQQ" : 445, "TTT" : 210.12}
        """
        # the following param is updated with the approved locates made by each client. it is initiated at the init
        self.dist_loc_by_client = defaultdict(list)
        approved_locates = approved_locates if isinstance(approved_locates, dict) else json.loads(approved_locates)
        self.calc_approved_error = None
        for symbol, locates in self.group_by_field(field_name):
            approved_sum = approved_locates.get(symbol)
            total_reques_sum = sum([int(k.get('number_of_locates_requested')) for k in locates])
            if approved_sum > total_reques_sum:
                msg = F"the total approved sum is bigger than requested for symbol: {symbol}"
                logging.info(msg)
                self.calc_approved_error = msg
                break
            remain_sum = approved_sum
            client_sum = defaultdict(int)
            while remain_sum > 0:
                for i in locates:
                    number_of_locates_requested = int(i.get('number_of_locates_requested'))
                    if total_reques_sum <= approved_sum and approved_sum % 100 == 0:
                        prop_sum = number_of_locates_requested / total_reques_sum * approved_sum
                        client_sum[i['client_name']] += int(prop_sum)
                        remain_sum -= prop_sum
                    elif remain_sum < 100 and i['number_of_locates_requested'] >= 100:
                        client_sum[i['client_name']] += remain_sum
                        remain_sum = 0
                        continue
                    elif i['number_of_locates_requested'] >= 100:
                        i['number_of_locates_requested'] -= 100
                        client_sum[i['client_name']] += 100
                        remain_sum -= 100
            for i in locates:
                self.dist_loc_by_client[i['client_name']].append({"symbol": i['symbol'],
                                                        "approved_locates": round(client_sum[i['client_name']], 3)})


if __name__ == '__main__':
    csv_file = 'locates.csv'
    csv_path = Path(__file__).parent.parent.joinpath('resources', csv_file)
    inst = RequestesLocatesClient(csv_path)
    inst.load_data('locates.csv')
    approved_locates = {"ABC": 580, "QQQ": 445, "TTT": 299.9956}
    inst.calc_approved_locates_by_client('symbol', approved_locates)
    res = inst.request_locates({"client_name": "Client1", 'symbol': "ABC", "number_of_locates_requested": 100})
    print(res)

