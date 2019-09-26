import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kcrawler",
    version="0.0.18",
    author="ken",
    author_email="kenbliky@gmail.com",
    description="A python crawler authored by Ken.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/kcrawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'kcrawler = kcrawler.cli:main',
            'kcjuejin = kcrawler.cli:juejin',
            'kcanjuke = kcrawler.cli:anjuke',
            'kcargs = kcrawler.cli:args'
        ]
    },
    python_requires='>=3.6',
)
