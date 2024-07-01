from setuptools import setup, find_packages

setup(
    name='ninmpl',
    version='0.0.0',
    install_requires=['matplotlib'],
    package_dir={'ninmpl': 'ninmpl'},
    packages=find_packages(),
    description='Wrapper of matplotlib using inheritance.',
    long_description='''This small package wraps matplotlib.
Inheritting, which is feature of OOP, may makes drawing more easily.
However, I did not know the best practice.''',
    url='https://github.com/uesseu/ninmpl',
    author='Shoichiro Nakanishi',
    author_email='sheepwing@kyudai.jp',
    license='MIT',
    zip_safe=False,
)
