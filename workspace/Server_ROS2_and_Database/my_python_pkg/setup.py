from setuptools import find_packages, setup

package_name = 'my_python_pkg'

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
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'receive_data = my_python_pkg.data_sender:main',
            'send_data = my_python_pkg.data_reciever:main',
            'raspberry_main = my_python_pkg.raspberry_main:main',
            'server_main = my_python_pkg.server_main:main',
            'pi_test = my_python_pkg.pi_test:main'
        ],
    },
)
