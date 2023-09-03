from setuptools import setup

__package__ = "ntp-amplification"
__version__ = "1.3"

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name=__package__,
    version=__version__,
    author="cavoq",
    author_email="cavoq@proton.me",
    license="BSD 2-Clause simplified License",
    description="NTP-Amplification Attack Tool",
    url="https://github.com/cavoq/ntp-amplification",
    python_requires=">=3",
    scripts=["ntp_amplification.py"],
    entry_points={
        'console_scripts': [
            'ntp-amplification = ntp_amplification:main',
        ],
    },
    install_requires=requirements,
)
