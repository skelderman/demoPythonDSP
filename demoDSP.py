import numpy as np
import wave
import struct
import matplotlib.pyplot as plt

frequency = 1000

num_samples = 48000
# The sampling rate of the analog to digital convert
sampling_rate = 48000.0

amplitude = 16000

file = "test.wav"

sine_wave = [np.sin(2 * np.pi * frequency * x / sampling_rate) for x in range(num_samples)]

print ("This program is gonna test some DSP stuff")
