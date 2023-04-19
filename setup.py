from setuptools import setup, find_packages


setup(
    name='qtp',
    version='0.1.0',
    description='Graphical Interface for Multi-Omics Visualisation',
    url='',
    author='Thibaut Peyric',
    author_email='thibaut.peyric@proton.me',
    license='BSD 2-clause',
    packages=find_packages(),
    package_data={'guimov': ['assets/*']},
    install_requires=['dash',
                      'dash_daq',
                      'plotly',
                      'dash_bootstrap_components',
                      'pandas',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],

    entry_points={
        'console_scripts': [
            'guimov_launch = guimov._commands:_commands_guimov_launch',
        ],
    },

)
