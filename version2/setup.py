from setuptools import setup

setup(
    name="main",
    packages = ['Inputs','PipelineMessageBroker', 'Pipes'],
    install_requires = ['python-magic', 'libmagic'],
    license = 'MIT'
    )
