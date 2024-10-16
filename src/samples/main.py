import requests

def main():
  url = "https://api.binance.com/sapi/v1/capital/deposit/hisrec?timestamp=1656775551286&signature=71ee09f19d348bea59c7bd0adec813f9850283990f4ef9610f2f4ff5dabbc49e"
  payload = {}
  headers = {
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': 'w706rQMj7OUPAtMHuZtCv02odP8faed5AsZVABsRZd8OmXHdQWOLXrqcSopUXRDj'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  print(response.text)


if __name__ == '__main__':
  main()
