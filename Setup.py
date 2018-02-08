from setuptools import setup

setup(
    name='chronoamperometry',
    version='0.1.0a4',
    packages=['chronoamperometry'],
    url='https://github.com/Zer0Credibility/chronoamperometry',
    license='4-clause BSD',
    author='Clayton Rabideau',
    author_email='cmr57@cam.ac.uk',
    description='A toolset for analyzing chronoamperometric data',
    install_requires=[
                       'numpy',
                       'pandas',
                       'plotnine',
                       'tqdm',
                       'scipy',
                       'statsmodels',
                       'xlrd',
                     ]
)
