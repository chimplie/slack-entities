from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="slack_entities",
    version="0.0.16",
    author="Oleh Zorenko",
    author_email="oleh@chimplie.com",
    description="Package for more convenient work with Slack API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chimplie/slack_entities",
    packages=find_packages(exclude=['slack_entities.tests']),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'slackclient==1.2.1',
    ]
)
