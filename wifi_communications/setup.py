from setuptools import find_packages, setup

package_name = 'wifi_communications'

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
    maintainer='pi',
    maintainer_email='h.nasir@leeds.ac.uk',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 'file_publisher=wifi_communications.file_publisher:main',
             'my_wifi_communication_node=wifi_communications.my_wifi_communication_node:main',
        ],
    },
)
