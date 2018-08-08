from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='freud',
    version='0.0.1',
    author='Stephen Martin',
    author_email='lockwood@opperline.com',
    description='TUI REST client to analyze API endpoints',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stloma/freud',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cli tui http rest request api',
    packages=find_packages(),
    install_requires=['requests', 'prompt_toolkit==2.0.3', 'pygments'],
    tests_require=['pytest', 'pytest_asyncio', 'pytest_httpbin'],
    entry_points={
        'console_scripts': [
            'freud=freud.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/stloma/freud/issues',
        'Source': 'https://github.com/stloma/freud',
    },
)
