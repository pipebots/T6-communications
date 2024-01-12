from setuptools import find_packages, setup

package_name = 'lora_wifi_communications'

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
        'console_scripts': [
        'integrated_node=lora_wifi_communications.integrated_node:main',
            'file_publisher=lora_wifi_communications.file_publisher:main',
            'lora_node=lora_wifi_communications.lora_node:main',
        ],
    },
)
