from setuptools import find_packages, setup

package_name = 'my_ros2_package'

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
    maintainer='ties',
    maintainer_email='ties@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'listener_csv = my_ros2_package.csv_listener:main',
            'sender_csv = my_ros2_package.csv_sender:main',
            'location_server = my_ros2_package.next_location_server:main',
            'location_pi = my_ros2_package.next_location_pi:main'
        ],
    },
)
