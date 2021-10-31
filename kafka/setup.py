from setuptools import find_packages, setup

setup(
	name='kafkalib',
	version='0.1.0',
	description='A Python library for writing/reading <topic, key, value> to/from Kafka.',
	author='Mehmet Aktas',
	author_email='mfatihaktas@gmail.com',
	license='MIT',
	install_requires=['confluent-kafka'],
	packages=find_packages(include=['kafkalib']),
	include_package_data=True)
