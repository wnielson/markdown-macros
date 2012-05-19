from setuptools import setup, find_packages

setup(
    name="markdown-macros",
    version="0.1.2",
    packages=find_packages(),
    author="Weston Nielson",
    author_email="wnielson@github",
    description="An extension for python-markdown that add Trac-like macro support.",
    license="MIT",
    keywords="markdown macro macros",
    url="https://github.com/wnielson/markdown-macros",
    install_requires=[
        "distribute",
        "Markdown>=2.1.1"
    ],
)