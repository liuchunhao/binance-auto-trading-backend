from setuptools import setup

setup(
    name="example_project",
    version="1.0.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="An example Python project",
    url="https://github.com/your-username/example-project",
    packages=["example_project"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "matplotlib"
    ]
)
