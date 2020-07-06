import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="web-framework-ullyzian",
    version="0.0.1",
    author="Viktor Ashcheulov",
    author_email="victor.ashcheulov@gmail.com",
    description="Personal framework for educational purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ullyzian/web-framework",
    packages=setuptools.find_packages(),
    install_requires=[
        'gunicorn',
        'jinja2',
        'MarkupSafe',
        'parse',
        'WebOb',
        'whitenoise'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.6'
)
