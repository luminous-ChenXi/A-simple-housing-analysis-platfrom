from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chengdu-housing-analysis",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="成都二手房房价数据分析与可视化平台",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/chengdu-housing-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dash>=2.0.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "plotly>=5.0.0",
        "flask>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "isort>=5.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "housing-analysis=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.csv", "plots/*.html", "plots/*.png"],
    },
)