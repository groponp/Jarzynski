from setuptools import setup

readme = open("./README.md", "r")

setup(
    name="jarzynski", 
    version='1.0.3',
    description='A computational tool to compute PMF and Kd from non-equilibrium simulation',
    long_description=readme.read(), 
    long_description_content_type='text/markdown',
    author='Ropón-Palacios G.',
    author_email='groponp@gmail.com',
    url='https://github.com/groponp/Jarzynski',
    download_url='https://github.com/groponp/Jarzynski/tarball/1.0.3',
    keywords=['non-equilibrium md', 'jarzynski', 'PMF', 'Kd'],
    classifiers=[],
    license='GPLv3',
    include_package_data=True
)