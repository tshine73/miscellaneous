import pandas as pd


def lambda_handler(event, context):
    data = [["Orange", "fruit", 500],
            ["PS5", "console", 300],
            ["Grape", "fruit", 200]]
    df = pd.DataFrame(data, columns=['name', 'category', 'price'])

    print(df)


if __name__ == '__main__':
    # event = {
    #     "type": "specific",
    #     "period": "2024-12",
    #     "process_status": StatusEnum.success.value,
    #     "codes": ["51"]
    # }

    event = {
        "period": "2024-12"
    }

    lambda_handler(event, None)
