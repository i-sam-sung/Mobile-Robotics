from setuptools import find_packages, setup

package_name = 'char_talk'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='samee',
    maintainer_email='todo@todo.todo',
    description='Char publisher and subscriber for HW1 Problem 2(c)',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'char_publisher = char_talk.char_publisher:main',
            'char_subscriber = char_talk.char_subscriber:main',
        ],
    },
)
