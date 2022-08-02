import pandas as pd


def create_data():
    df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    df.to_csv('data.csv')


if __name__ == '__main__':
    create_data()
