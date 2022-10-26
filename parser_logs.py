import re
import json

path_logs = "access.log"
path_result = "result.json"
regex = r"(?P<ip>\S*).*\[(?P<date>\S*)\s+(?P<timezone>\S*)]\s+\"(?P<request_type>\S*)\s+(?P<url>\S*)\s+" \
        r"(?P<protocol>\S*)\"\s+(?P<status_code>\d*)\s+(?P<byte>[\d\-]*)\s\"(?P<referer_url>.*)\"\s+\"" \
        r"(?P<headers>.*)\"\s+(?P<duration>\d*)"

result_json = {}
result_requests = {}
result_ip = {}
result_time_max = []


def read_file(path):
    with open(file=path, mode="r", newline="\n") as file:
        for f in file:
            yield f


def write_file_json(path, json_file):
    with open(path, "w", encoding='utf8') as file:
        json.dump(json_file, file, indent=4, ensure_ascii=False)


a = read_file(path_logs)

for c, i in enumerate(a, start=1):
    count_requests = c

    matches = re.search(regex, i)

    ip = matches.group(1)
    date = matches.group(2)
    request_type = matches.group(4)
    url = matches.group(5)
    duration = int(matches.group(11))

    result_requests.update({request_type: result_requests.get(request_type, 0) + 1})

    result_ip.update({ip: result_ip.get(ip, 0) + 1})

    value_for_max_duration = (duration, request_type, url, ip, date)
    if len(result_time_max) < 3:
        result_time_max.append(value_for_max_duration)
    elif min_value_in_result_time_max[0] < duration:
        result_time_max[index_min_value] = value_for_max_duration

    result_time_max = sorted(result_time_max, key=lambda x: x[0], reverse=True)
    min_value_in_result_time_max = min(result_time_max, key=lambda x: x[0])
    index_min_value = result_time_max.index(min_value_in_result_time_max)

    if count_requests == 50000:
        break

top_3_ip = dict(sorted(result_ip.items(), key=lambda x: x[1], reverse=True)[:3])

result_json = {"count_requests": {"name": "Общее количество выполненных запросов",
                                  "value": count_requests
                                  },
               "result_requests": {"name": "Количество запросов по HTTP-методам",
                                   "value": result_requests
                                   },
               "top_3_ip": {"name": "Топ 3 IP адресов, с которых были сделаны запросы",
                            "value": top_3_ip
                            },
               "result_time_max": {"name": "Топ 3 IP адресов, с которых были сделаны запросы",
                                   "value": result_time_max
                                   },

               }

write_file_json(path_result, result_json)

result = f"{result_json['count_requests']['name']}: {result_json['count_requests']['value']}\n" \
         f"{result_json['result_requests']['name']}:\n" \
         f"{'new_line'.join(map(lambda x: f'{x[0]}: {x[1]}', dict(result_json['result_requests']['value']).items()))}\n" \
         f"{result_json['top_3_ip']['name']}:\n" \
         f"{'new_line'.join(map(lambda x: f'{x[0]}: {x[1]}', dict(result_json['top_3_ip']['value']).items()))}\n" \
         f"{result_json['result_time_max']['name']}:\n" \
         f"{'new_line'.join(map(str, result_json['result_time_max']['value']))}\n" \
         f" ".replace("new_line", "\n")

print(result)
