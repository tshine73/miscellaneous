from setuptools import setup, find_packages

setup(
    name="tshine73-utils",
    version="0.2",
    author="tshine73",
    author_email="fan.steven.chiang@gmail.com",
    description="tshine73 utils",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    include_package_data=True,
    install_requires=[
        "psycopg2-binary==2.9.9", 'boto3==1.36.3', 'requests==2.32.3'
    ]
)
