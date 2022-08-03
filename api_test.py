import requests


def api_test(url, method):
    print(f"Test api using {method}")
    response = requests.get(url)
    print(f"status get request: {response.status_code}")
    print(response.text)


if __name__ == '__main__':
    try:
        method = 'uvicorn'
        url_uvi = "http://127.0.0.1:8000/"
        api_test(url_uvi, method)
    except requests.exceptions.ConnectionError:
        print('Activate uvicorn in command line to test API with uvicorn')
    print('\n')
    url = 'https://dvc-aws-app.herokuapp.com/'
    method = 'Heroku'
    api_test(url, method)

