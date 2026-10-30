from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8') if (here / 'README.md').exists() else None

setup(
    name='plasx',
    version='0.1.0',
    description='A plasmid sequence classifier',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/michaelkyu/plasx',
    author='Michael Ku Yu', 
    author_email='michaelkuyu@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='plasmid, metagenomics',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'numba',
        'blosc',
    ], 
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'plasx=plasx.plasx_script:run',
        ],
    },
    project_urls={
        'Source': 'https://github.com/michaelkyu/plasx/',
    },
)
