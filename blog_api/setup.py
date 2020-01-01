from setuptools import setup, find_packages

setup(
    name='blog_app',
    version='1.0.0',
    license='GNU General Public License v3',
    long_description=__doc__,
    author='Wale',
    author_email='adekoya.wale@yahoo.com',
    description='webapp for blog_posts',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blog_app = blog_app.wsgi:main']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask', 'pymongo',
        'flask_bootstrap',
        'flask_debugtoolbar',
        'mysql-connector-python', 'requests', 'werkzeug', 'redis'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
