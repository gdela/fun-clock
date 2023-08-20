from os import listdir
from shutil import copyfile

for file in listdir('f:'):
    if file.endswith('.py'):
        copyfile('f:/' + file, file)
