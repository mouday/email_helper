import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="email_helper",
    version="0.0.2",
    author="Pengshiyu",
    author_email="pengshiyuyx@gmail.com",
    description="email helper for simple send email and receive email of python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mouday/email_helper",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)