from setuptools import setup

setup(
    name='TSP-Framework',
    version='1.27',
    description='Framework para resolver el problema del vendedor viajero aplicando métodos de búsqueda como Simulated Annealing, Genetic Algorithm, Local Search o Iterated Local Search',
    long_description=open('README.md').read(),
    author='Javier del Canto, Jorge Polanco',
    author_email='javier.delcanto.m@mail.pucv.cl, jorge.polanco.sanmartin@gmail.com',
    url='https://github.com/Javernaver/TSP-Framework',
    scripts=['tspf.py'],
    packages=['src.tspf','src.tspf.Algorithms', 'src.tspf.Tools'],
    install_requires=['matplotlib', 'prettytable', 'tkinter'], 
    zip_safe=False,
    classifiers=[
        'License :: Freeware',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    package_data={
        '': ['instances/*.tsp']
    },
    entry_points={
        'console_scripts':[
            'tspf = tspf:main'
        ]
    },
)