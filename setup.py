import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arxiv-pdf-summary-helper",
    version="0.0.2",
    author="Jessica Tanon",
    author_email="jessica.tanon@gmail.com",
    description="A small package to help the note-taking process for arxiv papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xhattam/arxiv-pdf-summary-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Text Processing :: Markup :: LaTeX"
    ],
)