from setuptools import find_packages, setup

package_name = 'nav_pose_follower'

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
    maintainer='jerome',
    maintainer_email='jeromekemper@florinco.nl',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_follower = nav_pose_follower.pose_follower:main',  # Existing entry
            'pose_estimator = nav_pose_follower.pose_estimator:main',  # New entry for pose_estimator
        ],
    },
)

