import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as ecf:
        c = ecf.read()

        # remove all comments
        rc = re.sub(r'[#].*[\n]', '', c)

        sc = re.findall(r'\s*(\S+)\s*[{](.+)[}]', rc, re.DOTALL)

        if len(sc) != 1:
            print("one .ec file can only contains one top element")
            exit(1)
        
        top, topc = sc[0]

        sc = re.findall(r'\s*(\S+)\s*[{]([^{}]+)[}]', topc, re.DOTALL)

        if len(sc) == 0:
            print("one .ec file at least has level-3 architecture")
            exit(1)

        print(sc)

        macros = []
        macid = 1    

        for stop, stopc in sc:
            stc = re.sub(r'\s+', '', stopc).split(',')

            for stcc in stc:
                if not re.match(r'[0-9a-zA-Z]+', stcc):
                    print("error name in .ec file must not contain special characters")
                    exit(1)
                
                macros.append("#define {} {}\n".format(top + stop + stcc, macid))
                macid += 1

        with open(argv[2], "w") as echf:
            echf.writelines(macros)