from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PMSP_ml',
    version='0.1.2',
    packages=find_packages(),
    description='Example Python package',
    long_description=long_description,
    author='MAPS',
    author_email='cjf4674@naver.com',
    url='https://github.com/Dongguk-MAPS/PMSP_ml',
    license='MIT',
    install_requires=[
        'docplex','pickle','numpy'
        # 사용하는 패키지 추가
    ],
)