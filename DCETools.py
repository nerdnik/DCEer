import os
import numpy as np
from scipy.io import wavfile

def wav_to_txt(wav_file_name, output_file_name, crop=[0, 1]):
    print "converting wav to txt..."
    sampFreq, snd = wavfile.read(wav_file_name)
    bounds = len(snd) * np.array(crop)
    snd = snd[int(bounds[0]):int(bounds[1])]
    np.savetxt(output_file_name, snd)


def embed(input_file_name, output_file_name, embed_crop, tau, m, channel=0):
    # print 'embedding...'
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")
    output_file.truncate()  # ??
    lines = input_file.read().split("\n")

    bounds = len(lines) * np.array(embed_crop)
    lines = lines[int(bounds[0]):int(bounds[1])]

    series = []
    for line in lines:
        if line != "":
            channels = [x for x in line.split(" ") if x != ""]
            series.append(float(channels[channel]))
    end = len(lines) - (tau*(m - 1)) - 1
    for i in xrange(end):
        for j in xrange(m):
            output_file.write("%f " % series[i + (j*tau)])
        if i < end:
            output_file.write("\n")
    input_file.close()
    output_file.close()

def rename_files():
    os.chdir('C:\Users\PROGRAMMING\Documents\CU_research\piano_data\C134C')
    [os.rename(f, f.replace('-consolidated', '')) for f in os.listdir('.') if f.endswith('.wav') or f.endswith('.txt')]

def batch_wav_to_txt(dir_name):
    os.chdir(dir_name)
    [wav_to_txt(f, f.replace('.wav', '.txt')) for f in os.listdir('.') if f.endswith('.wav')]



if __name__ == '__main__':
    rename_files()
    # batch_wav_to_txt('C:\Users\PROGRAMMING\Documents\CU_research\piano_data\C134C')
    # batch_wav_to_txt('C:\Users\PROGRAMMING\Documents\CU_research\piano_data\C135B')