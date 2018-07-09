import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slack-entities",
    version="0.0.1",
    author="Oleh Zorenko",
    author_email="oleh@chimplie.com",
    description="Package for more convenient work with Slack API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chimplie/slack-entities",
    packages=[
        'slack-entities',
        'slack-entities.entities'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'slackclient==1.1.2',
    ]
)
