from setuptools import setup, find_packages

with open('utils/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="utils-73",
    version="0.1",
    include_package_data=True,
    python_requires='>=3.11',
    packages=find_packages(),
    setup_requires=['setuptools-git-versioning'],
    install_requires=requirements,
    author="tshine73",
    author_email="fan.steven.chiang@gmail.com",
    description="no description",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    version_config={
       "dirty_template": "{tag}",
    }
)