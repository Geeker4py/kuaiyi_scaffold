x=open("aaa.php")
xxx=x.readlines()[0:-2]
x.close()
#xxx.append('\n')
x=open("aaa.php","wb")
x.writelines(xxx)
x.close()
