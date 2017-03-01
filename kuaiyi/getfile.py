import os
import types
def getFileList(p):
        p = str(p)
        if p=="":
            return []
        #p = p.replace( "/","\\")
        if p[ -1] != "/":
            p = p+"/"
        a = os.listdir(p)
        b = [ x  for x in a if os.path.isfile( p + x ) ]
        return b

def getDirList(p):
        p = str( p )
        if p=="":
              return []
        #p = p.replace( "/","\\")
        if p[ -1] != "/":
            p = p+"/"
        a = os.listdir(p)
        b = [ x for x in a if os.path.isdir( p + x ) ]
        return b


def createAllFolder(path):
    dir_list=getDirList(path)
    for i in xrange(len(dir_list)):
        if dir_list[i]:
            current_path=path+'/'+dir_list[i] 
            print path+'/'+dir_list[i]  
            file_list=getFileList(current_path) 
            for f in xrange(len(file_list)):
                print current_path+'/'+file_list[f]

            createAllFolder(current_path)


                          	

print createAllFolder('/Users/dingzhipeng/Desktop/leyue/kuaiyi/library/Adapter/Platform/GZHUAQIAO')
print getFileList('/Users/dingzhipeng/Desktop/leyue/kuaiyi/library/Adapter/Platform/GZHUAQIAO')
#print getFileList('/Users/dingzhipeng/Desktop/leyue/kuaiyi')
#print copyAllFile('/Users/dingzhipeng/Desktop/leyue/kuaiyi/library/Adapter/Platform/GZHUAQIAO')

