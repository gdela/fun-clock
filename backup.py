from os import listdir
from shutil import copyfile

for file in listdir('e:'):
    if file.endswith('.py'):
        copyfile('e:/' + file, file)
