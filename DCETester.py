import sys
import time
from DCETools import wav_to_txt, batch_wav_to_txt
from DCEPlotter import make_window_frame
from DCEMovies import frames_to_movie
from DCEMovies import vary_tau, slide_window, compare_multi, compare_vary_tau, compare_multi_auto_tau


# test = 6
test = int(sys.argv[1])

start_time = time.time()

if test == 0:
    batch_wav_to_txt('input\piano_data\C134C')
    batch_wav_to_txt('input\piano_data\C135B')


if test == 1:
    for i in xrange(10):
        print 'Hello'
        note = i + 10
        piano = 'C134C'
        vary_tau('input/piano_data/%s/%s-%s.txt' % (piano, str(note), piano),
                 tau_lims=(1, 100),
                 tau_inc=5,
                 embed_crop=(.5*i, .5*(i+1)),  # aka window position, in seconds
                 ds_rate=20)             # downsample rate (takes every third sample)
        print 'hi'
        frames_to_movie('output/vary_tau_%s_%s.mp4' % (str(note), piano), framerate=1)


if test == 2:
    for i in xrange(7):
        note = i*10+10
        piano = 'C134C'
        slide_window('input/piano_data/%s/%s-%s.txt' % (piano, str(note), piano),
                     window_size=.05*(i+1),    # seconds
                     ds_rate=1,
                     tau= 10,
                     step_size=.5)      # how much to move window each frame
        frames_to_movie('output/slide_window_scale_tau_%s_%s.mp4' % (str(note),piano), framerate=1)


if test == 3:
    for i in xrange(7):
        note = (i+1)*10
        print 'note is %s ' % str(note)
        compare_vary_tau('input/piano_data/C135B/%s-C135B.txt' % str(note), 'input/piano_data/C134C/%s-C134C.txt' % str(note),
                         tau_lims=(1,40),
                         tau_inc=2,
                         embed_crop=(.5,.7),
                         ds_rate = 5)
        print 'note is still %s ' % str(note)
        frames_to_movie('output/compare_tau_%s.mp4' % str(note), framerate=1)


if test == 4:
    dir1 = "input/piano_data/C134C"
    dir2 = "input/piano_data/C135B"
    tau = 10
    compare_multi(dir1,'-C134C.txt',
                  dir2, '-C135B.txt',
                  tau,
                  embed_crop=(.5, .7))
    frames_to_movie('output/compare_multi_test.mp4', framerate=1)

import math

if test == 5:
    dir1 = "input/piano_data/C134C"
    dir2 = "input/piano_data/C135B"
    tau_T = 1/math.pi
    compare_multi_auto_tau(dir1, '-C134C.txt',
                           dir2, '-C135B.txt',
                           tau_T,
                           embed_crop=(1, 1.1),
                           ds_rate=5,
                           i_lims=(20, 35))

    frames_to_movie('output/compare_auto_tau__1_pi_t5.mp4', framerate=1)

if test == 6:
    dir1 = "input/piano_data/C134C"
    dir2 = "input/viol_data"
    tau_T = 1 / math.pi
    compare_multi_auto_tau(dir1, '-C134C.txt',
                           dir2, '-viol.txt',
                           tau_T,
                           embed_crop=(1, 1.2),
                           ds_rate=1,
                           i_lims=(36, 64)  # specify note range
                           )

    frames_to_movie('output/viol_test_align.mp4', framerate=1)

print("time elapsed: %d seconds" % (time.time() - start_time))
