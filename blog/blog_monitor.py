import boto3
import requests


def check_blog_status():
    url = "https://tshine73.blog"

    resp = requests.get(url)

    return resp.status_code != 200


def notify_error():
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:482117386475:blog',
        Message='tshine73 blog is unhealthy, please check it as soon as possible',
        Subject='【Alert】tshine73 blog is unhealthy'
    )

    print("notify error to topic blog")


def lambda_handler(event, context):
    if check_blog_status():
        notify_error()
    else:
        print("blog is healthy")

if __name__ == '__main__':
    lambda_handler(None, None)
