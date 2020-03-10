from setuptools import setup, find_packages

setup(
    name='flaskr',  #: 包名称
    version='alpha',
    long_descripyion=__doc__,  #: 项目详细描述
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  #: 防止创建zip压缩包
    install_requires=['Flask'],  #: 安装依赖
)
