#! /usr/bin/python
import re, sys, getopt

from operator import itemgetter

def receiving(file):
    f = open(file, 'r')

    receiving = []
    uniqueDict = {}
    double_list = []
    # Creating the regex template
    receivingRegex = re.compile(r'(\d\d\.\d(\d)?(\d)?\.\d(\d)?(\d)?\.\d(\d)?(\d)?)(\.2424)')
    # Reading the file line by line and appending the IP's (regex) to the Array
    for i in f:
        mo2 = receivingRegex.search(i)
        receiving.append(mo2.group(1))
    f.close()

    # The set function remove duplicates from array. Iterating over this array and creating dictionary with IP's
    # as keys and setting the initial packet number as 0
    for ip in set(receiving):
        uniqueDict[ip] = 0

    # Checking how many times each unique IP can be found in all receiving IP array. Increasing the values in
    # the dictionary with 1, for each IP found
    for allip in receiving:
        if allip in uniqueDict.keys():
            uniqueDict[allip] += 1
    # This is something strange which I have done. Two dimensional array with the KEYS and VALUES. This is done so
    # I can actually SORT the list/dictionary by the VALUES.
    for uip, packet in uniqueDict.items():
        double_list.append([uip, packet])

    # The actual sorting is happening here. Itemgetter (read more about it) is sorting by the second value.
    sorted_by_second = sorted(double_list, key=itemgetter(1), reverse = True)

    print('Top 10 IP\'s receiving the most packets\nand the corresponding number of packets')
    for final, final2 in sorted_by_second[:10]:

        print(' ' + final + ' - ' + str(final2))

def small_large(file):
    f = open(file, 'r')

    packetRegex = re.compile(r'length\s(\d*)')
    size = 0
    counter_small = 0
    counter_large = 0

    for i in f:
        mo3 = packetRegex.search(i)
        if int(mo3.group(1)) < 512:
            counter_small += 1
        else:
            counter_large += 1
        size += 1
    f.close()
    print('The percentage of small packets is' + ' ' + str(round((counter_small / size) * 100, 2)) + ' %')
    print('The percentage of large packets is' + ' ' + str(round((counter_large / size) * 100, 2)) + ' %')

def sending(file):
    f = open(file, 'r')

    sending = []
    uniqueIP = {}
    double_list = []
    packet_list = []

    # Creating the regex template
    sendingRegex = re.compile(r'\d\d\.\d(\d)?(\d)?\.\d(\d)?(\d)?\.\d(\d)?(\d)?')
    packetRegex = re.compile(r'length\s(\d*)')

    # Reading the file line by line and appending the IP's (regex) and packet size (regex) to the 2 Arrays
    for i in f:
        mo1 = packetRegex.search(i)
        packet_list.append(mo1.group(1))
        mo2 = sendingRegex.search(i)
        sending.append(mo2.group())
    f.close()

    # The set function remove duplicates from array. Iterating over this array and creating dictionary with IP's
    # as keys and setting the initial packet overall size as 0
    for ip in set(sending):
        uniqueIP[ip] = 0


    for c in range(len(packet_list)):
        if sending[c] in uniqueIP.keys():
            uniqueIP[sending[c]] += int(packet_list[c])

    # This is something strange which I have done. Two dimensional array with the KEYS and VALUES. This is done so
    # I can actually SORT the list/dictionary by the VALUES.
    for uip, packet in uniqueIP.items():
        double_list.append([uip, packet])

    # The actual sorting is happening here. Itemgetter (read more about it) is sorting by the second value.
    sorted_by_second = sorted(double_list, key=itemgetter(1), reverse=True)

    print('Top 10 clients sending the most bytes. Showing the IP address and the number of bytes sent for each:')
    for send in (sorted_by_second[0:10]):
        print(send[0] + ' --> ' + str(send[1]))

def usage():
    usage = """
    -h --help                 Prints this
    -r --receive (file)       Top 10 servers receiving the most packets. Showing the amount of packets received by each
    -l --large (file)         Percentage of "small packets" (maximum 512 bytes) and Percentage of "large packets" (over 512 bytes)
    -s --send (file)          Top 10 clients sending the most bytes. Showing the IP address and the number of bytes sent for each
    """
    print(usage)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:l:s:h', ['receive=', 'large=', 'send=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-r', '--receive'):
        receiving(arg)
    elif opt in ('-l', '--large'):
        small_large(arg)
    elif opt in ('-s', '--send'):
        sending(arg)
    else:
        usage()
        sys.exit(2)

