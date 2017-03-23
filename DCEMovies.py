import DCETools
import DCEPlotter
import sys
import os
import numpy as np

def remove_old_frames():
    os.chdir('frames')
    for f in os.listdir("."):
        if f.endswith(".png"):
            os.remove(f)
    os.chdir('..')


def frames_to_movie(out_file_name, framerate=2):
    print 'building movie...'
    if os.path.exists(out_file_name):
        overwrite = raw_input(out_file_name + " already exists. Overwrite? (y/n)\n")
        if overwrite == "y":
            pass
        else:
            sys.exit()

    in_str = ('ffmpeg -y -framerate %i ' % framerate) + '-i frames/frame%03d.png'
    out_str = (' -r %d ' % 24) + out_file_name
    os.system(in_str + out_str)
    print os.getcwd() + ('\\' if os.name == 'nt' else '/') + out_file_name


def slide_window(txt_wave_file, window_size=.01, num_frames=10, tau=10):
    # TODO: add window start/stop arguments so wav_crop can show larger waveform
    remove_old_frames()
    for i, start in enumerate(np.linspace(0, 1, num_frames, endpoint=False)):
        print 'building frame %i of %i' % (i + 1, num_frames)
        embed_crop = [start, start + window_size]
        DCETools.embed(txt_wave_file, 'data/embedded_coords.txt', embed_crop, tau, 2)

        wave_data = np.loadtxt(txt_wave_file)
        # wave_data = np.loadtxt(txt_wave_file)[:, 0]


        DCEPlotter.make_window_fig('data/embedded_coords.txt', wave_data, 'frames/frame%03d.png' % i, embed_crop, tau, i)


def vary_tau(txt_wave_file, tau_lims=(1, 5), tau_inc=1, embed_crop=(.5, .52)):
    remove_old_frames()
    for i, tau in enumerate(np.arange(tau_lims[0], tau_lims[1], tau_inc)):
        print 'frame %i of %i' % (i + 1, int((tau_lims[1] - tau_lims[0]) / tau_inc))
        DCETools.embed(txt_wave_file, 'data/embedded_coords.txt', embed_crop, tau, 2)
        # wave_data = np.loadtxt(txt_wave_file)[:, 0]
        wave_data = np.loadtxt(txt_wave_file)

        DCEPlotter.make_window_fig('data/embedded_coords.txt', wave_data,
                                   'frames/frame%03d.png' % i, embed_crop, tau, i)

def compare_vary_tau(txt_wave_file1, txt_wave_file2, tau_lims, tau_inc=1, embed_crop=(.5, .51)):
    remove_old_frames()
    for i, tau in enumerate(np.arange(tau_lims[0], tau_lims[1], tau_inc)):
        print 'building frame %i of %i' % (i + 1, int((tau_lims[1] - tau_lims[0]) / tau_inc))
        DCETools.embed(txt_wave_file1, 'data/embedded_coords_comp1.txt', embed_crop, tau, 2)
        DCETools.embed(txt_wave_file2, 'data/embedded_coords_comp2.txt', embed_crop, tau, 2)
        DCEPlotter.make_compare_fig('frames/frame%03d.png' % i, txt_wave_file1, txt_wave_file2, i, tau)



def compare_multi(dir1, dir1_base, dir2, dir2_base, tau, embed_crop=(.05, .1), max_frames=89):
    """makes frames for comparison movie"""
    remove_old_frames()
    for i in xrange(1, max_frames):
        print 'frame', i
        filename1 = dir1 + "/%02d" % i + dir1_base
        filename2 = dir2 + "/%02d" % i + dir2_base
        DCETools.embed(filename1, 'data/embedded_coords_comp1.txt', embed_crop, tau, 2)
        DCETools.embed(filename2, 'data/embedded_coords_comp2.txt', embed_crop, tau, 2)
        DCEPlotter.make_compare_fig('frames/frame%03d.png' % i, dir1_base, dir2_base, i, tau)


