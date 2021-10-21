from setuptools import setup

setup(
    name='TSP-Framework',
    version='0.5',
    description='Framework para resolver el problema del vendedor viajero aplicando metaheristicas como Simulated Annealing y Genetic Algorithm',
    long_description=open('README.md').read(),
    author='Javier del Canto, Jorge Polanco',
    author_email='javier.delcanto.m@mail.pucv.cl, jorge.polanco.sanmartin@gmail.com',
    url='https://github.com/Javernaver/TSP-Framework',
    scripts=['tspf.py'],
    packages=['src', 'src.Algorithms'],
    install_requires=['matplotlib'], 
    zip_safe=False,
    classifiers=[
        'License :: MIT License',
        'Programming Language :: Python :: 3.9.7',
    ],
    include_package_data=True,
    package_data={
        'instances': ['instances/*.tsp'],
        'trajectory': ['trajectory/*']
    },
)