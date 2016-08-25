from setuptools import setup

setup(
    name='alep_za_entities',
    entry_points={
        'aleph.analyzers': [
            'za_entities = aleph_za_entities.entities:Company'
        ]
    },
    version='0.1',
    description='Aleph Analyzer to identify South African entities',
    url='http://github.com/code4sa/za_entities',
    author='Code For South Africa',
    author_email='info@code4sa.org',
    license='MIT',
    packages=["aleph_za_entities"],
    zip_safe=False
)
