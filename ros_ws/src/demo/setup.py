from setuptools import setup

from glob import glob

package_name = 'demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=['demo', 'demo/obj'],
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rareslemnariu',
    maintainer_email='rares.lemnariu@ro.bosch.com',
    description='Package that shows a GUI demo for controlling the car',
    license='BSD-3-Clause License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = demo.main:main',
        ],
    },
)
