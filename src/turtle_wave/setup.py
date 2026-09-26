from setuptools import find_packages, setup

package_name = 'turtle_wave'

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
    description='Turtlesim cosine-wave driver for HW1 Problem 2(f)',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cosine_wave = turtle_wave.cosine_wave:main',
        ],
    },
)
