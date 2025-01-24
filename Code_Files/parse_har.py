import json

def parse_har_file(har_file_path):
    
    with open(har_file_path, 'r') as f:
        har_data = json.load(f)
        
    status_2xx = 0
    status_4xx = 0
    status_5xx = 0
    total_status_code_count = 0
    
    for entry in har_data['log']['entries']:
        status_code = entry['response']['status']
        
        
        if 200 <= status_code < 300:
            status_2xx += 1
        elif 400 <= status_code < 500:
            status_4xx += 1
        elif 500 <= status_code < 600:
            status_5xx += 1
        
        total_status_code_count += 1
    
    return total_status_code_count, status_2xx, status_4xx, status_5xx

def save_output(total, status_2xx, status_4xx, status_5xx):
    
    with open("status_code_output.txt", "w") as output_file:
        output_file.write(f"Total status code count: {total}\n")
        output_file.write(f"2XX status code count: {status_2xx}\n")
        output_file.write(f"4XX status code count: {status_4xx}\n")
        output_file.write(f"5XX status code count: {status_5xx}\n")


har_file_path = "output.har"


total, status_2xx, status_4xx, status_5xx = parse_har_file(har_file_path)


save_output(total, status_2xx, status_4xx, status_5xx)


print(f"Total status code count: {total}")
print(f"2XX status code count: {status_2xx}")
print(f"4XX status code count: {status_4xx}")
print(f"5XX status code count: {status_5xx}")
