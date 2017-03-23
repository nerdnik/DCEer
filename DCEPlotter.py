import numpy as np
import matplotlib.pyplot as pyplot
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText


def plot_dce(subplot, in_file_name):
	# print 'plotting dce...'
	dce_data = np.loadtxt(in_file_name)
	x = dce_data[:,0]
	y = dce_data[:,1]
	subplot.scatter(x, y, color='black', s=1)
	subplot.set_aspect('equal')
	subplot.axis('equal')
	subplot.set_xticks([])
	ylims = subplot.get_ylim()
	subplot.set_xticks([])
	subplot.set_yticks([])


	max_label = AnchoredText('ymax: %.2f' %ylims[1],
					  prop=dict(size=8), frameon=True,
					  loc=2)
	min_label = AnchoredText('ymin: %.2f' %ylims[0],
					  prop=dict(size=8), frameon=True,
					  loc=3)
	# at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
	subplot.add_artist(max_label)
	subplot.add_artist(min_label)


def plot_waveform(subplot, waveform_data, embed_crop):
	# print 'plotting waveform...'
	y = waveform_data
	x = np.linspace(0, len(y)/44100., len(y))

	embed_time = (len(y)/44100.) * np.array(embed_crop)

	subplot.plot(x, y, color='k', zorder=0)
	subplot.axis('tight')
	subplot.axvspan(embed_time[0], embed_time[1], facecolor='r', alpha=0.7, zorder=1)


	ylims = subplot.get_ylim()
	# subplot.set_xticks([])
	subplot.set_yticks([])


	max_label = AnchoredText('ymax: %d' %ylims[1],
					  prop=dict(size=8), frameon=True,
					  loc=2)
	min_label = AnchoredText('ymin: %d' %ylims[0],
					  prop=dict(size=8), frameon=True,
					  loc=3,
					  )

	subplot.add_artist(max_label)
	subplot.add_artist(min_label)


def plot_title(subplot, in_file_name, tau):
	subplot.axis('off')
	subplot.set_xlim([0,1])
	subplot.set_ylim([0,1])

	tau_str = r'$\tau = %d$' % tau
	subplot.text(0, .5, tau_str,
				 horizontalalignment='left',
				 verticalalignment='center',
				 size=17,
				 bbox=dict(pad=5)
				 )

	subplot.text(0, .3, in_file_name,
				 horizontalalignment='left',
				 verticalalignment='center',
				 size=8,
				 bbox=dict(facecolor='none', pad=5)
				 )


def make_window_fig(in_file_name, txt_wave_file, out_file_name, embed_crop, tau, frame_num):
	fig = pyplot.figure(figsize=(8,8), tight_layout=True)
	title_subplot = pyplot.subplot2grid((4, 4), (0, 0), rowspan=3)
	dce_subplot = pyplot.subplot2grid((4, 4), (0, 1), colspan=3, rowspan=3)
	wavform_subplot = pyplot.subplot2grid((4, 4), (3, 0), colspan=4)

	plot_dce(dce_subplot, in_file_name)
	plot_waveform(wavform_subplot, txt_wave_file, embed_crop)
	plot_title(title_subplot, in_file_name, tau)
	pyplot.savefig(out_file_name)
	pyplot.close(fig)


def make_compare_fig(out_file_name, title1, title2, frame_num, tau):
	def plot_title(subplot):
		subplot.axis('off')
		subplot.set_xlim([0, 1])
		subplot.set_ylim([0, 1])

		subplot.table(
			cellText=[[r'$\tau = %s$' % tau, 'frame: %s' % frame_num]],
			bbox=[0, 0, .25, .33],    # x0, y0, width, height))
			cellColours=[['steelblue' for x in xrange(2)]],
			rowLoc='left',
			# size=18
			)

	fig = pyplot.figure(figsize=(12, 8), tight_layout=True)
	subplot1 = pyplot.subplot2grid((5, 2), (0,0), rowspan=4)
	subplot2 = pyplot.subplot2grid((5, 2), (0,1), rowspan=4)
	subplot3 = pyplot.subplot2grid((5, 2), (4,0), colspan=2)

	plot_dce(subplot1, 'data/embedded_coords_comp1.txt')
	plot_dce(subplot2, 'data/embedded_coords_comp2.txt')
	plot_title(subplot3)

	subplot1.set_title(title1)
	subplot2.set_title(title2)
	# fig.suptitle('note number: %d' % i, bbox={'pad':5})


	pyplot.savefig(out_file_name)
	pyplot.close(fig)

