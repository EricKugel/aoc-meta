import setuptools

setuptools.setup(
    name="aoc-meta",
    version="0.1.0",
    author="erickugel",
    author_email="erickugel713@gmail.com",
    description="AOC meta tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'requests',
    ]
)