import os
import hashlib

class code():
    def __init__(self):
        pass
    def hashfile(path, blocksize = 65536):
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()

    def findDup(parentFolder):
        dups = {}
        for dirName, subdirs, fileList in os.walk(parentFolder):
            for filename in fileList:
                path = os.path.join(dirName, filename)#  Полный путь к файлу
                file_hash = code.hashfile(path)#    Вычисление хэша
                if file_hash in dups:
                    dups[file_hash].append(path)# добавление дубликата
                    os.remove(path)
                else:
                    dups[file_hash] = [path]#   добавление нового типа дубликата
        return dups

    def joinDicts(dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]

    def printResults(dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            print('Duplicates Found:')
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print(subresult)
                print('___________________')
        else:
            print('No duplicate files found.')

def main1(data1):
    dups = {}
    code.joinDicts(dups, code.findDup(data1))
    code.printResults(dups)

