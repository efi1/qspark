from collections import defaultdict

data = [{'client': 'client1', 'sym': 'TTT', 'allocates': 100}, {'client': 'client2', 'sym': 'TTT', 'allocates': 200},
      {'client': 'client3', 'sym': 'TTT', 'allocates': 100}, {'client': 'client4', 'sym': 'TTT', 'allocates': 100},
      {'client': 'client1', 'sym': 'QQQ', 'allocates': 100}, {'client': 'client2', 'sym': 'QQQ', 'allocates': 200},
      {'client': 'client3', 'sym': 'QQQ', 'allocates': 100}, {'client': 'client4', 'sym': 'QQQ', 'allocates': 100},
      {'client': 'client1', 'sym': 'WWW', 'allocates': 100}, {'client': 'client2', 'sym': 'WWW', 'allocates': 200},
      {'client': 'client3', 'sym': 'WWW', 'allocates': 100}, {'client': 'client4', 'sym': 'WWW', 'allocates': 100}
      ]

approved_locates =  {"WWW" : 499.9956, "QQQ" : 499.95, "TTT" : 499.3256}

quantom_unit = 100 # round-robin unit

d_out = defaultdict(int)


def group_by_field(data, field_name: str):
    grouped_by_data = defaultdict(list)
    sorted_data = sorted(data, key=lambda x: x.get(field_name))
    for i in sorted_data:
        grouped_by_data[i['sym']].append(i)
    return grouped_by_data

data_grouped_by_sym = group_by_field(data, 'sym')

for sym in data_grouped_by_sym:
    stack = data_grouped_by_sym[sym]
    while stack and approved_locates[sym]:
        if approved_locates[sym] >= quantom_unit:
            subtractor = quantom_unit
        else:
            subtractor = approved_locates[sym]
        test = stack.pop()
        if test['allocates'] >= subtractor:
            test['allocates'] -= subtractor
            d_out[F"{test['client']}-{sym}"] += subtractor
            approved_locates[test['sym']] -= subtractor
        if test['allocates'] > 0:
            stack.insert(0, test)
        else:
            d_out[F"{test['client']}-{sym}"] += test['allocates']


print(d_out)

