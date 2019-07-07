import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pytest-rt",
	version="0.4.0",
	author="Andrey Smirnov",
	author_email="and.inbx@gmail.com",
	description="pytest data collector plugin for Testgr",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/and-sm/pytest-rt",
	py_modules=["pytest_rt"],
	# the following makes a plugin available to pytest
	entry_points={"pytest11": ["pytest_rt = pytest_rt"]},
	classifiers=[
		"Framework :: Pytest",
		"Programming Language :: Python :: 3.6"],
)
