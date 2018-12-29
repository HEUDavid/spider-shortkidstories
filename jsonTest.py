## jsonTest.py

import json



def main():
    
    data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
    }

    json_str = json.dumps(data)
    return ""

main()
