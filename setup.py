import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='matlabhub',
    version='2022.7.0',
    author='Wim Pomp @ Lenstra lab NKI',
    author_email='w.pomp@nki.nl',
    description='matlabhub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wimpomp/matlabhub',
    packages=['matlabhub'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=['matlab-proxy', 'flask'],
    entry_points={'console_scripts': ['matlabhub=matlabhub:main'], },
    package_data={'': ['templates/*', 'config.yml']},
    include_package_data=True,
)
