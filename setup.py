from glob import glob
from setuptools import setup

setup(
    name='lidar_drone', version='0.1.0', packages=['lidar_drone'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/lidar_drone']),
        ('share/lidar_drone', ['package.xml']),
        ('share/lidar_drone/launch', glob('launch/*.py')),
        ('share/lidar_drone/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    description='Reconstructed ROS 2 support nodes for a LiDAR UAV research project',
    license='LicenseRef-Pending-Author-Decision',
    entry_points={'console_scripts': [
        f'{name} = lidar_drone.nodes:{name}'
        for name in ['odom_to_tf', 'goal_relay', 'laser_safety_stop', 'cmd_vel_mux']
    ]},
)
