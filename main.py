import socket
import dns.resolver
import dns.e164

def handler(context, inputs):
    print('Action started.')
    msAddr = inputs["msisdn"]
    dnsMX = inputs["dnsMX"]

    # Log Input Entries
    #print (inputs)
    #print (msAddr)
    #print (dnsMX)

    # Converts E164 Address to ENUM with propietary library dnspython
    n = dns.e164.from_e164(msAddr)
    print ('My MSISDN:', dns.e164.to_e164(n), 'ENUM NAME Conversion:', n)

    # Resolve DNS MX Query with propietary library dnspython
    answers = dns.resolver.query(dnsMX, 'MX')
    print ('Resolving MX Records for:', dnsMX)
    for rdata in answers:
        print ('Host', rdata.exchange, 'has preference', rdata.preference)

    # Resolve AAA with prebuilt socket library 
    addr1 = socket.gethostbyname(dnsMX)
    print('Resolving AAA Record:', addr1)

    return addr1 

