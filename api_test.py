import requests


def api_test_get(url, method):
    print(f"Test api GET using {method}")
    response = requests.get(url)
    print(f"status get request: {response.status_code}")
    print(response.text)


def api_test_post(url, method, data):
    print(f"Test api POST using {method}")
    response = requests.post(url, json=data)
    print(f"status post request: {response.status_code}")
    print(response.text)


if __name__ == '__main__':
    data = {'a': 1, 'b': 2}
    try:
        method = 'uvicorn'
        url_uvi = "http://127.0.0.1:8000/"
        api_test_get(url_uvi, method)
        api_test_post(url_uvi + 'predict', method, data)
    except requests.exceptions.ConnectionError:
        print('Activate uvicorn in command line to test API with uvicorn')

    print('\n')
    url = 'https://dvc-aws-app.herokuapp.com/'
    method = 'Heroku'
    api_test_get(url, method)
    api_test_post(url + 'predict', method, data)
