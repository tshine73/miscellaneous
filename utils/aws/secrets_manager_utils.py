import boto3


def get_secret(secret_name: str, region_name: str, profile_name=None):
    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name=profile_name)
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']
    return secret
