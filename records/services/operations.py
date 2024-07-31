import requests
import math

def calculate(operation, first_input, second_input):
    match(operation):
        case 'addition':
            return first_input + second_input
        case 'subtraction':
            return first_input - second_input
        case 'multiplication':
            return first_input * second_input
        case 'division':
            if(second_input == 0):
                return 0
            return first_input / second_input
        case 'square_root':
            return math.sqrt(first_input)
        case 'random_string':
            url = "https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
            response = requests.get(url)
            if response.status_code == 200:
                return response.text.strip()
            else:
                return f"Failed to fetch data. Status code: {response.status_code}"
