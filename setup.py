from setuptools import setup

__package__ = "ntp-amplification"
__version__ = "1.2"


setup(
    name=__package__,
    version=__version__,
    author="cavoq",
    author_email="cavoq@proton.me",
    license="MIT",
    description="NTP-Amplification Attack Tool",
    url="https://github.com/cavoq/ntp-amplification",
    python_requires=">=3",
    scripts=["ntp_amplification.py"],
    entry_points={
        'console_scripts': [
            'ntp-amplification = ntp_amplification:main',
        ],
    },
)