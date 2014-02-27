import pypandoc
import os

rst = pypandoc.convert('README.md', 'rst')

with open('README.txt', 'w+') as f:
    f.write(rst)

os.system("python setup.py register sdist bdist upload")
os.remove('README.txt')