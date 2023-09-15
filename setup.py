from setuptools import setup

__package__ = "ntp-amplification"
__version__ = "1.5.4"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name=__package__,
    version=__version__,
    author="cavoq",
    author_email="cavoq@proton.me",
    license="BSD 2-Clause simplified License",
    description="NTP-Amplification Attack Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cavoq/ntp-amplification",
    python_requires=">=3",
    py_modules=["ntp_amplification"],
    scripts=["ntp_amplification.py"],
    entry_points={
        "console_scripts": [
            "ntp-amplification = ntp_amplification:main",
        ],
    },
    install_requires=requirements,
)
