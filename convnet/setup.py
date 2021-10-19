from setuptools import find_packages, setup

setup(
	name='convnetlib',
	version='0.1.0',
	description='A Python library for training a basic CNN model for multi-class prediction.',
	author='Mehmet Aktas',
	author_email="mfatihaktas@gmail.com",
	license='MIT',
	install_requires=['tensorflow >= 2.1', 'numpy'],
	packages=find_packages(include=['convnetlib']),
	include_package_data=True)
