import time
from DCETools import wav_to_txt, batch_wav_to_txt
from DCEPlotter import make_window_fig
from DCEMovies import frames_to_movie
from DCEMovies import vary_tau, slide_window, compare_multi, compare_vary_tau


test = 0
start_time = time.time()

if test == 0:
    batch_wav_to_txt('C:\Users\PROGRAMMING\Documents\CU_research\DCEer\input\piano_data\C134C')
    batch_wav_to_txt('C:\Users\PROGRAMMING\Documents\CU_research\DCEer\input\piano_data\C135B')

if test == 1:
    vary_tau('input/34-C135B.txt', tau_lims=(1, 100), tau_inc=5, embed_crop=(.27, .275))
    frames_to_movie('output/vary_tau_test.mp4', framerate=1)

if test == 2:
    slide_window('input/34-C135B.txt')
    frames_to_movie('output/slide_window_test.mp4', framerate=1)

if test == 3:
    compare_vary_tau('input/34-C135B.txt', 'input/34-C134C.txt', tau_lims=(1, 50))
    frames_to_movie('output/compare_tau_test.mp4', framerate=1)

if test == 4:
    dir1 = "C:/Users/PROGRAMMING/Documents/CU_research/piano_data/C134C"
    dir2 = "C:/Users/PROGRAMMING/Documents/CU_research/piano_data/C135B"
    tau = 20
    compare_multi(dir1,'-C134C.txt', dir2, '-C135B.txt', tau, max_frames=15, embed_crop=(0, .2))
    frames_to_movie('output/compare_multi_test.mp4', framerate=1)




print("time elapsed: %d seconds" % (time.time() - start_time))
