from distutils.core import setup

setup(
    name='pychain',
    version='0.1.0',
    author='Lev Rubel',
    author_email='rubel.lev@gmail.com',
    packages=['pychain'],
    url='http://pypi.python.org/pypi/pychain/',
    license='LICENSE',
    description='Python library for Chain API.',
    long_description="""
        Python library for Chain API
        It is built on top of excellent Requests library, has its own exceptions and follows PEP8!
        Please feel free to contribute and send pull requests.
        If you've committed, feel free to include your name in contributors list.
    """,
    install_requires=[
        "requests >= 2.3.0"
    ],
)
