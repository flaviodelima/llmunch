from setuptools import setup, find_packages

setup(
    name="llmunch",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'llmunch=llmunch.__main__:main',
        ],
    },
    python_requires='>=3.7',
    install_requires=[
        # Add your dependencies here
    ],
)
