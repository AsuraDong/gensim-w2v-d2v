fin = open('倚天屠龙记.Txt','br')

fout = open('倚天屠龙记_utf8.txt','w')

num = 0
for line in fin.readlines():
    try:
        newline = line.decode('gbk')
    except Exception as error:
        print(num)
        newline = "\n"
    else:
        print(newline,file=fout,end='')
    finally:

        num= num+1


fin.close()
fout.close()