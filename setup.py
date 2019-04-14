from setuptools import setup, find_packages
try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements
setup(
    name = 'reversiTool',
    version='1.0.16',
    url = 'https://github.com/reversiWebApp/reversiTools.git',
    license = 'Free',
    author = 'Hiroya Iyori',
    author_email = 'vp054az116@gmail.com',
    description='Reversi API for machine learning and web api',
    install_requires = ['setuptools', 'numpy', 'toml'],
    packages=find_packages(),
    include_package_data = True
)
