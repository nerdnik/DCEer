import sys
import time
from DCETools import wav_to_txt, batch_wav_to_txt
from DCEPlotter import make_window_frame
from DCEMovies import frames_to_movie
from DCEMovies import vary_tau, slide_window, compare_multi, compare_vary_tau


#test = 1
test = int(sys.argv[1])

start_time = time.time()

if test == 0:
    batch_wav_to_txt('input\piano_data\C134C')
    batch_wav_to_txt('input\piano_data\C135B')


if test == 1:
	note = 67
	piano = 'C135B' 
	vary_tau('input/piano_data/%s/%s-%s.txt' % (piano, str(note), piano),
             tau_lims=(1, 100),
             tau_inc=10,
             embed_crop=(.3, .6),  # aka window position, in seconds
             ds_rate=20)             # downsample rate (takes every third sample)

	frames_to_movie('output/vary_tau_%s_%s.mp4' % (str(note), piano), framerate=1)


if test == 2:
	note = 67
	piano = 'C135B' 
	slide_window('input/piano_data/%s/%s-%s.txt' % (piano, str(note), piano),
                 window_size=.5,    # seconds
                 ds_rate=50,
                 tau=80,
                 step_size=.5)      # how much to move window each frame

	frames_to_movie('output/slide_window_%s_%s.mp4' % (str(note),piano), framerate=1)


if test == 3:
	note = 67 
	compare_vary_tau('input/piano_data/C135B/%s-C135B.txt' % str(note), 'input/piano_data/C134C/%s-C134C.txt' % str(note),
                     tau_lims=(1, 200),
                     tau_inc=10,
                     embed_crop=(3, 4),
                     ds_rate = 50)

	frames_to_movie('output/compare_tau_%s.mp4' % str(note), framerate=1)


if test == 4:
    dir1 = "input/piano_data/C134C"
    dir2 = "input/piano_data/C135B"
    tau = 20
    compare_multi(dir1,'-C134C.txt',
                  dir2, '-C135B.txt',
                  tau,
                  embed_crop=(0, .2))
    frames_to_movie('output/compare_multi_test.mp4', framerate=1)


print("time elapsed: %d seconds" % (time.time() - start_time))
