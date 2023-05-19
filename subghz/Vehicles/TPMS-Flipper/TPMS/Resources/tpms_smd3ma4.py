import time
import os

home_directory = os.path.expanduser( '~' )

MODEL='Schrader'

PREAMBLE=int('F5555555E',16)
PRESSURE=int(10*20)


def main():
        
    id = input('What is the 6 digit hex ID?\n')
    id = int(id, 16)

    start = format((PREAMBLE), '036b')
    flag= format(7, '03b')
    device= format((id), '024b')
    psi = format((PRESSURE), '010b')
    
    payload= flag + device + psi
    
    print('Payload = %s' % payload)
    
    #Lazy Manchester
    payload=payload.replace("0", "0_")
    payload=payload.replace("1", "1 ")
    payload=payload.replace(" ", "0")
    payload=payload.replace("_", "1")
    
    print('Manchester payload = %s' % payload)
    
    finished = start + payload
    
    print('Finished = %s' % finished)
    
    
    f = open(os.path.join( home_directory, 'TPMS', 'Output', 'smd3ma4.txt'),"w")
    f.write("[_ (8000us) ]\n[0 (120us) ]\n[1 (40kHz 120us) ]\n\n\n_ _ _\n%s\n_ _ _" % finished) 
  
if __name__ == '__main__':
    exit(main())
