#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import nrzi4b5b
import dividing
import bitarray
import struct
import writetofile


def encode(src, dst, msg, filename):
    # Reprezentacja src, dst, msg na bitach
    # src, dst: int (rzutowanie na 6 bajtów)
    srcb = bitarray.bitarray()
    srcb.frombytes(struct.pack('!LH', src // (2 ** 15), src % (2 ** 15)))
    dstb = bitarray.bitarray()
    dstb.frombytes(struct.pack('!LH', dst // (2 ** 15), dst % (2 ** 15)))


    # msg: bytes (jeżeli str, to rzutowanie na bajty)
    if isinstance(msg, str):
        msg = bytes(msg, 'utf8')
    msgb = bitarray.bitarray()
    if len(msg) < 46:
        msg = bytes(46 - len(msg)) + msg
    msgb.frombytes(msg)

    # Poskładać ramkę Ethernet
    # ramka = dst + src + len(msg) + msg
    lenb = bitarray.bitarray()
    lenb.frombytes(struct.pack('!H', len(msg)))
    ramka = dstb + srcb + lenb + msgb

    # suma = src32(ramka)
    # reszta z dzielenia wielomianu (ramka z dopisanymi 32 zerami na końcu) przez 100000100110000010001110110110111
    suma = dividing.divide(ramka + bitarray.bitarray([0] * 32), bitarray.bitarray('100000100110000010001110110110111'))[
        1]
    suma = bitarray.bitarray([0] * (32 - len(suma))) + suma

    # ramka = ramka + suma
    ramka = ramka + suma

    # preamble = '10101010' * 7 + '10101011'
    # bity = preamble + nrzi(4b5b(ramka))
    # założyć, że poprzedni bit był 1
    bity = bitarray.bitarray('10101010' * 7 + '10101011') + nrzi4b5b.nrzi4b5b(ramka)
    print(bity)


    # Wygenerować tony reprezantujące wiadomość
    writetofile.writetofile(0.05, 440, 880, bity, filename)

    # glosnik(0.1, 440, 880, bity)

if __name__ == "__main__":
    encode(7, 3, 'Nazarii Denha', 'denha05.wav')


# 10101010101010101010101010101010101010101010101010101010101010110101101011010110101101011010110101101011010110101101011001101010010100101001010010100101001010010100101001010010100010101010010100110001011101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101110011010000101110001101010010001011100011010100111101001110110100111010011101011100111001110100011011010010111101001110001011100010100101011010011001100101001000111001011
# 101010101010101010101010101010101010101010101010101010101010101101011010110101101011010110101101011010110101101011010110011010100101001010010100101001010010100101001010010100101000101010100101001100010111010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011010110101101011100110100001011100011010100100010111000110101001111010011101101001110100111010111001110011101000110110100101111010011100010111000101001010110100110011001010010001110010111