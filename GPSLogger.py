# References:
# https://www.gpsinformation.org/dale/nmea.htm
# https://sites.google.com/site/vmacgpsgsm/understanding-nmea
# Baud is 4800
# Data bits: 8bit (bit 7 set to 0)
# stop bits: 1 or 2
# Parity: None
# Each sentence begins with a '$' and ends with a carriage return/line feed sequence and can be no longer than 80 characters of visible text (plus the line terminators)
# data = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n" \
#        "$HCHDG,101.1,,,7.1,W*3C\r\n"

from sys import exit
import socket
from time import gmtime, strftime
import operator
import functools

# Configurable Parameters
HOST = "127.0.0.1"
PORT = 14551

# Do not change this parameter
# Note: Protocol states to use \r\n however Mission Planner with Ardupilot firmware 
# formats messages beginning with $ and ending only with \n
# CRLF = "\r\n"
CRLF = "\n"

def init(host="127.0.0.1", port=14551):
    sock = socket.socket()
    sock.connect((host, port))
    return sock


def socket_receive_one_sentence(socket):
    sentence = ""
    
    # recieve until we get an entire sentence
    while sentence[-len(CRLF):] != CRLF:
        char = socket.recv(1).decode()
        sentence += char
    print("Message Rec: {}".format(repr(sentence)))
    return sentence

# the checksum is exclusive or of all chars between $ and *
def split_and_check_crc(sentence):
    # remove $ at the front and \r\n at the back
    data = sentence[1:-1]
    # get data vs CRC delimited with *
    data, crc_hex = data.split("*")
    print("data: {}".format(data))
    print("crc: {}".format(crc_hex))
    # check if XOR of data given is equal to crc hex
    isValid = compute_crc(data, crc_hex)
    return isValid, data


def compute_crc(data, crc_hex_string):
    # Source: http://code.activestate.com/recipes/576789-nmea-sentence-checksum/
    crc_result = functools.reduce(operator.xor, (ord(s) for s in data), 0)

    # convert our hex to dec for comparison
    print("Hex String: {}".format(crc_hex_string))
    crc = int(crc_hex_string, 16)
    
    print("CRC: {} == {}: {}".format(crc, crc_result,(crc == crc_result)))

    if crc == crc_result:
        return True
    else:
        return False


def decode(sentence):
    print("Time: " + strftime("%H:%M:%S", gmtime()))
    valid_crc, d = split_and_check_crc(sentence)

    if not valid_crc:
        print("Bad message: CRC Error")
        return

    # print(repr(d))
    d = d.split(',')
    # print(repr(d))

    if "GGA" in sentence:
        gps_time = d[1]     # fixed time taken
        lat = d[2]          # in deg
        lat_dir = d[3]      # North or south
        lon = d[4]          # in deg
        lon_dir = d[5]      # East or west
        quality = d[6]      # fix quality
        satellites = d[5]   # number of satellites
        alt = d[9]          # in AMSL
        alt_units = d[10]
        alt_geoid = d[11]   # in AMSL

        print("GGA: Time: {}, Lat: {}deg {}, Lon {}deg {}, Quality: {}, Satellites: {}, Alt: {}{}".format(gps_time, lat,
                                                                                                          lat_dir, lon,
                                                                                                          lon_dir,
                                                                                                          quality,
                                                                                                          satellites,
                                                                                                          alt,
                                                                                                          alt_units))
        return gps_time, lat, lat_dir, lon, lon_dir, quality, satellites, alt, alt_units

    # magnetic heading deviation variation
    elif "HDG" in sentence:
        heading = d[1]
        variation = d[4]
        variation_dir = d[5]
        print("HDG: Heading: {} Variation: {}{}".format(heading, variation, variation_dir))
        
        return heading, variation, variation_dir
        
    else:
        print("Unsupported Message: {}".format(sentence))


def run():
    # setup port
    if HOST == "127.0.0.1":
        hostname = "localhost"

    try:
        s = init(host=HOST, port=PORT)
        print("Connected to {}.".format(hostname))
        
    except ConnectionRefusedError:
        hostname = HOST
        print("No connection could be made to {}.".format(hostname))
        exit()

    while True:
        sentence = socket_receive_one_sentence(s)
        decode(sentence)
            

if __name__ == "__main__":
    run()
