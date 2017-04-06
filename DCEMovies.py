import DCETools
import DCEPlotter
import sys
import os
import math
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


def slide_window(txt_wave_file,
                 window_size=.5,    # seconds
                 step_size=.1,      # seconds
                 tau=10,
                 ds_rate=1,
                 max_frames=0,      # 0 for disabled
                 wav_sample_rate=44100):

    remove_old_frames()

    worm_length = sum(1 for line in open(txt_wave_file))/wav_sample_rate
    num_frames = worm_length/step_size

    for i, start in enumerate(np.arange(0, worm_length, step_size)):
        print 'building frame %i of %i' % (i, num_frames)

        embed_crop = [start, start + window_size]
        DCETools.embed(txt_wave_file, 'data/embedded_coords.txt',
                       embed_crop, tau, 2, wav_sample_rate, ds_rate=ds_rate)

        DCEPlotter.make_window_frame('data/embedded_coords.txt', txt_wave_file,
                                   'frames/frame%03d.png' % i, embed_crop, tau, i)

        if  max_frames != 0 and i > max_frames: break


def vary_tau(txt_wave_file,
             tau_lims=(1, 15),
             tau_inc=1,
             m = 2,
             embed_crop=(1, 2),
             wav_sample_rate=44100,
             ds_rate=1):

    remove_old_frames()

    for i, tau in enumerate(np.arange(tau_lims[0], tau_lims[1], tau_inc)):
        print 'frame %i of %i' % (i + 1, int((tau_lims[1] - tau_lims[0]) / tau_inc))
        DCETools.embed(txt_wave_file, 'data/embedded_coords.txt', embed_crop, tau, m, wav_sample_rate, ds_rate=ds_rate)
        DCEPlotter.make_window_frame('data/embedded_coords.txt', txt_wave_file,
                                   'frames/frame%03d.png' % i, embed_crop, tau, i)


def compare_vary_tau(txt_wave_file1,
                     txt_wave_file2,
                     tau_lims,
                     tau_inc=1,
                     embed_crop=(1, 2),
                     ds_rate=1,
                     m=2,
                     wav_sample_rate=44100):

    remove_old_frames()

    for i, tau in enumerate(np.arange(tau_lims[0], tau_lims[1], tau_inc)):
        print 'building frame %i of %i' % (i + 1, int((tau_lims[1] - tau_lims[0]) / tau_inc))
        DCETools.embed(txt_wave_file1, 'data/embedded_coords_comp1.txt', embed_crop, tau, m, wav_sample_rate, ds_rate=ds_rate)
        DCETools.embed(txt_wave_file2, 'data/embedded_coords_comp2.txt', embed_crop, tau, m, wav_sample_rate, ds_rate=ds_rate)
        DCEPlotter.compare_vary_tau_frame('frames/frame%03d.png' % i, txt_wave_file1, txt_wave_file2, i, tau, embed_crop)



def compare_multi(dir1, dir1_base,
                  dir2, dir2_base,
                  tau,
                  embed_crop=(1, 2),
                  max_frames=89,
                  m=2,
                  ds_rate=1,
                  wav_sample_rate=44100):
    """makes frames for comparison movie: constant tau, constant, vary in files"""

    remove_old_frames()
    frame_idx = 0
    for i in xrange(1, max_frames):
        frame_idx += 1
        print 'frame', frame_idx
        filename1 = dir1 + "/%02d" % i + dir1_base
        filename2 = dir2 + "/%02d" % i + dir2_base
        DCETools.embed(filename1, 'data/embedded_coords_comp1.txt', embed_crop, tau, m, wav_sample_rate, ds_rate=ds_rate)
        DCETools.embed(filename2, 'data/embedded_coords_comp2.txt', embed_crop, tau, m, wav_sample_rate, ds_rate=ds_rate)
        DCEPlotter.compare_multi_frame('frames/frame%03d.png' % frame_idx, filename1, filename2, i, tau, embed_crop)


def compare_multi_auto_tau(dir1, dir1_base,
                           dir2, dir2_base,
                           tau_T,
                           embed_crop=(1, 2),
                           i_lims=(1, 89),
                           m=2,
                           ds_rate=1,
                           wav_sample_rate=44100,
                           dpi=200):
    """makes frames for comparison movie: proportional tau, constant, vary in files"""
    from DCETools import get_fund_freq
    remove_old_frames()
    frame_idx = 0
    for i in xrange(i_lims[0], i_lims[1]):
        frame_idx +=1
        print 'frame', frame_idx
        filename1 = dir1 + "/%02d" % i + dir1_base
        filename2 = dir2 + "/%02d" % i + dir2_base

        # freq = math.pow(2, (i - 49)/12) * 440    # Hz, ascending index
        freq = math.pow(2, (40 - float(i))/12) * 440    # Hz, descending index
        period = 1 / freq
        tau_sec = period * tau_T
        sample_rate = 44100
        tau_samp = int(tau_sec * sample_rate)

        info_main = [
            ['tau (samples)', '{:d}'.format(tau_samp)],
            ['tau (sec)', '{:.4f}'.format(tau_sec)],
            ['period (sec)', '{:.4f}'.format(period)],
            ['f (Hz) [ideal]', '{:.1f}'.format(freq)]
        ]

        info_1 = [
            filename1,
            ['f (Hz) [detected]', '{:.1f}'.format(embed_crop[0], embed_crop[1])],
            ['embed lims (s)', '({:.2f}, {:.2f})'.format(embed_crop[0], embed_crop[1])]

        ]

        info_2 = [
            filename2,
            ['f (Hz) [detected]', '{:.1f}'.format(embed_crop[0], embed_crop[1])],
            ['embed lims (s)', '({:.2f}, {:.2f})'.format(embed_crop[0], embed_crop[1])]
        ]

        title_info = [info_main, info_1, info_2]


        DCETools.embed(filename1, 'data/embedded_coords_comp1.txt', embed_crop, tau_samp, m, wav_sample_rate, ds_rate=ds_rate)
        DCETools.embed(filename2, 'data/embedded_coords_comp2.txt', embed_crop, tau_samp, m, wav_sample_rate, ds_rate=ds_rate)
        DCEPlotter.compare_multi_frame_new('frames/frame%03d.png' % frame_idx, filename1, filename2, i, tau_samp, embed_crop, title_info, dpi)


