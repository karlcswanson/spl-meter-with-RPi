#!/usr/bin/env python
import os, errno
import pyaudio
import spl_lib as spl
from scipy.signal import lfilter
import numpy

# dB Fast ~.125 seconds
SAMPLE = .125
RATE = 48000
CHUNK = int(RATE * SAMPLE)
FORMAT = pyaudio.paInt16
CHANNEL = 1

NUMERATOR, DENOMINATOR = spl.A_weighting(RATE)

pa = pyaudio.PyAudio()

stream = pa.open(format = FORMAT,
                channels = CHANNEL,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)


def is_meaningful(old, new):
    return abs(old - new) > 3

def update_max_if_new_is_larger_than_max(new, max):
    print("update_max_if_new_is_larger_than_max called")
    if new > max:
        print("max observed")
        return new
    else:
        return max

def listen(old=0, error_count=0, min_decibel=100, max_decibel=0):
    print("Listening")
    while True:
        try:
            ## read() returns string. You need to decode it into an array later.
            block = stream.read(CHUNK)
        except IOError as e:
            error_count += 1
            print(" (%d) Error recording: %s" % (error_count, e))
        else:
            ## Int16 is a numpy data type which is Integer (-32768 to 32767)
            ## If you put Int8 or Int32, the result numbers will be ridiculous
            decoded_block = numpy.fromstring(block, 'Int16')
            ## This is where you apply A-weighted filter
            y = lfilter(NUMERATOR, DENOMINATOR, decoded_block)
            new_decibel = 20*numpy.log10(spl.rms_flat(y))
            if is_meaningful(old, new_decibel):
                old = new_decibel
                print('A-weighted: {:+.2f} dB'.format(new_decibel))

    stream.stop_stream()
    stream.close()
    pa.terminate()

if __name__ == '__main__':
    listen()
