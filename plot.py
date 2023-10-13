import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
# from mpl_toolkits.axes_grid1.colorbar import colorbar
from copy import copy

def determine_cut_time(a):    
    if np.all(a >= 0):
        cut_time = 0
        
    else:
        cut_time = 0
        while all(a[:,cut_time] >= 0):
            cut_time += 1
    
    return cut_time
    
def fill_removed_portion(number_of_cells, cut_time, a_ax, b_ax, c_ax, v_ax, a, a_ymax, b_ymax, c_ymax, v_ymax):
    x_fill = np.arange(0, number_of_cells, 1)
    fill_bool = a[:,cut_time] < 0
    fill_alpha = 0.35
    a_ax.fill_between(x_fill, a_ymax, where=fill_bool, color="tab:gray", alpha=fill_alpha, step='mid')
    b_ax.fill_between(x_fill, b_ymax, where=fill_bool, color="tab:gray", alpha=fill_alpha, step='mid')
    c_ax.fill_between(x_fill, c_ymax, where=fill_bool, color="tab:gray", alpha=fill_alpha, step='mid')
    v_ax.fill_between(x_fill, v_ymax, where=fill_bool, color="tab:gray", alpha=fill_alpha, step='mid')
    
    return a_ax, b_ax, c_ax, v_ax, 

def create_animated_output(number_of_cells, t, a, b, v, c, params, save_directory):
    
    a_over_time = a
    
    timepoints_N = a.shape[1]
    streak_count = np.zeros((timepoints_N,),dtype=int)
    for col_idx in range(timepoints_N):
        unique, counts = np.unique(a[:,col_idx], return_counts=True)
        count_dict = dict(zip(unique, counts))
        try:
            one_count = count_dict[1.0]
        except KeyError:
            one_count = 0
        streak_count[col_idx] = one_count
    
    number_of_frames = timepoints_N
    
    sample_rate = int(round(len(t) / timepoints_N))
    
    # print('sample_rate = ' + str(sample_rate))
    # print('t shape = ' + str(t.shape))
    # print('a shape = ' + str(a.shape))

    # fig = plt.figure(figsize=(4,8))
 #
 #    ax_a = fig.add_subplot(4,1,1)
 #    ax_v = fig.add_subplot(4,1,2)
 #    ax_b = fig.add_subplot(4,1,3)
 #    ax_c = fig.add_subplot(4,1,4)
    
    fig, (ax_a, ax_v, ax_b, ax_c) = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(4,8))

    # ax.plot(a[:,100])

    # ax_a.set_title('streak')
    # ax_b.set_title('bmp')
    # ax_c.set_title('calcium')

    a_ymax = np.max(a)*1.5 # 0.01
    c_ymax = 10
    ant_c_ymax = (10/11) * c_ymax

    ax_a.set_ylim([0,a_ymax])
    ax_b.set_ylim([0,np.max(b)*1.1])
    ax_c.set_ylim([0,c_ymax])
    # ax_c.set_ylim([0,np.max(c)*1.1])
    ax_v.set_ylim([0,np.max(v)*1.1])
    
    ax_a.set_yticks([0,1])
    ax_a.set_yticklabels(['OFF','ON'])
    
    anterior_cell = (number_of_cells - 1) / 2

    ax_a.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_b.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_c.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_v.set_xticks([0,anterior_cell, number_of_cells - 1])

    ax_a.set_xticklabels([])
    ax_b.set_xticklabels([])
    ax_v.set_xticklabels([])
    ax_c.set_xticklabels(['pos.', 'ant.', 'pos.'])

    ax_c.set_xlabel("Cell position")
    
    ant_x = [anterior_cell, anterior_cell]
    
    threshold_streak = [params["c_b_threshold"], params["c_b_threshold"]]
    threshold_vg1 = [params["v_b_threshold"], params["v_b_threshold"]]
    
    ant_a, = ax_a.plot( ant_x, [0,np.max(a)], lw=1, c='k', linestyle='dashed')
    ant_b, = ax_b.plot( ant_x, [0,np.max(b)], lw=1, c='k', linestyle='dashed')
    ant_c, = ax_c.plot( ant_x, [0,ant_c_ymax], lw=1, c='k', linestyle='dashed')
    ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=1, c='k', linestyle='dashed')
    
    threshold_streak_line, = ax_b.plot( [0, number_of_cells - 1],threshold_streak, lw=1, c='C0', linestyle='dashed')
    threshold_vg1_line, = ax_b.plot( [0, number_of_cells - 1], threshold_vg1, lw=1, c='C9', linestyle='dashed')

    line_a, = ax_a.plot( a_over_time[:,0], lw=3, c='C0', label="'Streak'")
    line_b, = ax_b.plot( b[:,0], lw=3, c='C3', label='BMP4')
    line_c, = ax_c.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_v, = ax_v.plot( v[:,0], lw=3, c='C9',label='cVG1')

    time_x_loc = number_of_cells/3
    time_y_loc = 0.87*a_ymax
    time_text = ax_a.text(time_x_loc, time_y_loc,'t = ', fontsize=16)
    streak_x_loc = (number_of_cells/3) - (number_of_cells * 0.03)
    streak_y_loc = 0.73*a_ymax
    # streak_text = ax_a.text(streak_x_loc, streak_y_loc,'Streak cells: ', fontsize=12)

    ax_a.legend(loc=2)
    ax_b.legend(loc=2)
    ax_c.legend(loc=2)
    ax_v.legend(loc=2)
    
    cut_time = determine_cut_time(a)

    plt.tight_layout()

    # plt.show()

    def init():
        line_a, = ax_a.plot([],[], lw=3, c='C0', label="'Streak'")
        line_b, = ax_b.plot([],[], lw=3, c='C3', label='BMP4')
        line_c, = ax_c.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_v, = ax_v.plot([],[],lw=3, c='C9',label='cVG1')
        time_text.set_text('t = ')
        # streak_text.set_text('Streak cells: ')
        return line_a, line_b, line_c, line_v, time_text, # streak text,
    def animate(i):
        line_a.set_data(range(number_of_cells), a_over_time[:,i])
        line_b.set_data(range(number_of_cells), b[:,i])
        line_c.set_data(range(number_of_cells), c[:,i])
        line_v.set_data(range(number_of_cells), v[:,i])
        
        if i == cut_time:
            out = fill_removed_portion(number_of_cells, cut_time, ax_a, ax_b, ax_c, ax_v, a, np.max(a), np.max(b), ant_c_ymax, np.max(v))
        
        # time_text.set_text('t = ' + "{:.1f}".format(t[i]) +'h')
        time_text.set_text('t = ' + "{:.2f}".format(t[i*sample_rate]) +'h')
        # streak_text.set_text('Streak cells: ' + str(int(streak_count[i])))
        return line_a, line_b, line_c, line_v, time_text, # streak text,

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_frames, blit=False)

    anim.save(save_directory + 'hello.mp4', writer='ffmpeg', fps=10)
    
    return
    
def create_animated_output_extra_calcium(number_of_cells, sample_rate, t, a, b, v, c, params, save_directory):
    
    a_over_time = a
    
    streak_count = np.sum(a, axis=0)
    
    number_of_frames = int(len(t) / sample_rate)
    
    fig, (ax_a, ax_v, ax_b, ax_c_low, ax_c_high) = plt.subplots(nrows=5, ncols=1, sharex=True, figsize=(3.5,8))

    a_ymax = np.max(a)*1.5 # 0.01
    
    c_low_max = 10
    c_high_max = 110

    ax_a.set_ylim([0,a_ymax])
    ax_b.set_ylim([0,np.max(b)*1.1])
    ax_c_low.set_ylim([0,c_low_max])
    ax_c_high.set_ylim([0,c_high_max])
    ax_v.set_ylim([0,np.max(v)*1.1])
    
    ax_a.set_yticks([0,1])
    ax_a.set_yticklabels(['OFF','ON'])
    
    anterior_cell = (number_of_cells - 1) / 2

    ax_a.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_b.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_c_low.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_c_high.set_xticks([0,anterior_cell, number_of_cells - 1])
    ax_v.set_xticks([0,anterior_cell, number_of_cells - 1])

    ax_a.set_xticklabels([])
    ax_b.set_xticklabels([])
    ax_v.set_xticklabels([])
    ax_c_low.set_xticklabels([])
    ax_c_high.set_xticklabels(['pos.', 'ant.', 'pos.'])

    ax_c_high.set_xlabel("Cell position")
    
    ant_x = [anterior_cell, anterior_cell]
    
    threshold_streak = [params["c_b_threshold"], params["c_b_threshold"]]
    threshold_vg1 = [params["v_b_threshold"], params["v_b_threshold"]]
    
    ant_a, = ax_a.plot( ant_x, [0,np.max(a)], lw=1, c='k', linestyle='dashed')
    ant_b, = ax_b.plot( ant_x, [0,np.max(b)], lw=1, c='k', linestyle='dashed')
    ant_c_low, = ax_c_low.plot( ant_x, [0,c_low_max], lw=1, c='k', linestyle='dashed')
    ant_c_high, = ax_c_high.plot( ant_x, [0,c_high_max], lw=1, c='k', linestyle='dashed')
    ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=1, c='k', linestyle='dashed')
    
    threshold_streak_line, = ax_b.plot( [0, number_of_cells - 1],threshold_streak, lw=1, c='C0', linestyle='dashed')
    threshold_vg1_line, = ax_b.plot( [0, number_of_cells - 1], threshold_vg1, lw=1, c='C9', linestyle='dashed')

    line_a, = ax_a.plot( a_over_time[:,0], lw=3, c='C0', label="'Streak'")
    line_b, = ax_b.plot( b[:,0], lw=3, c='C3', label='BMP4')
    line_c_low, = ax_c_low.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_c_high, = ax_c_high.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_v, = ax_v.plot( v[:,0], lw=3, c='C9',label='cVG1')

    text_x_loc = number_of_cells * 0.68
    # text_x_loc = number_of_cells * 0.33
    time_x_loc = text_x_loc
    time_y_loc = 0.85*a_ymax
    time_text = ax_a.text(time_x_loc, time_y_loc,'t = ', fontsize=14)
    streak_x_loc = text_x_loc - number_of_cells*0.05
    streak_y_loc = 0.74*a_ymax
    streak_text = ax_a.text(streak_x_loc, streak_y_loc,'Streak cells: ', fontsize=10)

    ax_a.legend(loc=2)
    ax_b.legend(loc=2)
    # ax_c_low.legend(loc=2)
    ax_c_high.legend(loc=2)
    ax_v.legend(loc=2)

    plt.tight_layout()

    # plt.show()

    def init():
        line_a, = ax_a.plot([],[], lw=3, c='C0', label="'Streak'")
        line_b, = ax_b.plot([],[], lw=3, c='C3', label='BMP4')
        line_c_low, = ax_c_low.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_c_high, = ax_c_high.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_v, = ax_v.plot([],[],lw=3, c='C9',label='cVG1')
        time_text.set_text('t = ')
        streak_text.set_text('Streak cells: ')
        return line_a, line_b, line_c_low, line_c_high, line_v, time_text, streak_text,
    def animate(i):
        line_a.set_data(range(number_of_cells), a_over_time[:,i * sample_rate])
        line_b.set_data(range(number_of_cells), b[:,i * sample_rate])
        line_c_low.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_c_high.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_v.set_data(range(number_of_cells), v[:,i * sample_rate])
        time_text.set_text('t = ' + "{:.1f}".format(t[i * sample_rate]) +'h')
        streak_text.set_text('Streak cells: ' + str(int(streak_count[i * sample_rate])))
        return line_a, line_b, line_c_low,line_c_high, line_v, time_text, streak_text,

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_frames, blit=False)

    anim.save(save_directory + 'hello.mp4', writer='ffmpeg', fps=10)
    
    return

def create_stills_array(time_indices, number_of_cells, t, a, b, v, c, params, filename):
    
    matplotlib.rcParams['font.family'] = 'sans-serif'
    # matplotlib.rcParams['font.sans-serif'] = ['Arial']
    matplotlib.rcParams['font.sans-serif'] = ['Clear Sans']
    
    timepointsN = len(time_indices)

    streak_count = np.sum(a, axis=0)
    
    a_ymax = np.max(a)*1.1
    b_ymax = np.max(b)*1.1
    c_ymax = np.max(c)*1.1
    v_ymax = np.max(v)*1.1
    
    anterior_cell = (number_of_cells - 1) / 2
    
    cut_time = determine_cut_time(a)

    fig = plt.figure(figsize=(8,4))
    
    for col_idx, time_idx in enumerate(time_indices):

        ax_a = fig.add_subplot(4, timepointsN, 1 + col_idx)
        ax_v = fig.add_subplot(4, timepointsN, 1 + timepointsN + col_idx)
        ax_b = fig.add_subplot(4, timepointsN, 1 + (2*timepointsN) + col_idx)
        ax_c = fig.add_subplot(4, timepointsN, 1 + (3*timepointsN) + col_idx)

        ax_a.set_ylim([0,a_ymax])
        ax_b.set_ylim([0,b_ymax])
        ax_c.set_ylim([0,c_ymax])
        ax_v.set_ylim([0,v_ymax])

        ax_a.set_yticks([0,1])

        ax_a.set_xticks([0,anterior_cell, number_of_cells - 1])
        ax_b.set_xticks([0,anterior_cell, number_of_cells - 1])
        ax_c.set_xticks([0,anterior_cell, number_of_cells - 1])
        ax_v.set_xticks([0,anterior_cell, number_of_cells - 1])

        ax_a.set_xticklabels([])
        ax_b.set_xticklabels([])
        ax_v.set_xticklabels([])
        ax_c.set_xticklabels(['P', 'A', 'P'])
        
        b_x_min, b_x_max = ax_b.get_xlim()

        ax_c.set_xlabel("Cell position")

        ant_x = [anterior_cell, anterior_cell]
        thresh_v_b = [params["v_b_threshold"], params["v_b_threshold"]]
        thresh_c_b = [params["c_b_threshold"], params["c_b_threshold"]]

        ant_a, = ax_a.plot( ant_x, [0,np.max(a)], lw=0.5, c='k', linestyle='dashed')
        ant_b, = ax_b.plot( ant_x, [0,np.max(b)], lw=0.5, c='k', linestyle='dashed')
        ant_c, = ax_c.plot( ant_x, [0,np.max(c)], lw=0.5, c='k', linestyle='dashed')
        ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=0.5, c='k', linestyle='dashed')
        
        line_thresh_v_b, = ax_b.plot( [b_x_min,b_x_max], thresh_v_b, lw=1, c='C9', linestyle='dashed')
        line_thresh_c_b, = ax_b.plot( [b_x_min,b_x_max], thresh_c_b, lw=1, c='C0', linestyle='dashed')

        line_a, = ax_a.plot( a[:,time_idx], lw=2, c='C0', label="'Streak'")
        line_b, = ax_b.plot( b[:,time_idx], lw=2, c='C3', label='cBMP4')
        line_c, = ax_c.plot( c[:,time_idx], lw=2, c='C1',label='Ca2+')
        line_v, = ax_v.plot( v[:,time_idx], lw=2, c='C9',label='cVG1')
        
        time_str = str(t[time_idx])
        ax_a.set_title('t = ' + time_str + 'h', fontweight='bold')
        
        if col_idx == 0:
            ax_a.set_yticklabels(['OFF','ON'])
            
            ax_a.set_ylabel("'Streak'", fontweight='bold')
            ax_b.set_ylabel('BMP4\n', fontweight='bold')
            ax_c.set_ylabel('Ca2+\nactivity', fontweight='bold')
            ax_v.set_ylabel('cVG1\n', fontweight='bold')
            
        else:
            ax_a.set_yticklabels([])
            ax_b.set_yticklabels([])
            ax_c.set_yticklabels([])
            ax_v.set_yticklabels([])
            
        if time_idx >= cut_time:
            out = fill_removed_portion(number_of_cells, cut_time, ax_a, ax_b, ax_c, ax_v, a, np.max(a), np.max(b), np.max(c), np.max(v))
            
        # if col_idx == timepointsN - 1:
        #     ax_a.legend(loc=2)
        #     ax_b.legend(loc=2)
        #     ax_c.legend(loc=2)
        #     ax_v.legend(loc=2)

    plt.tight_layout()
    
    fig.savefig(filename, dpi=300, orientation='portrait', format='png') #, transparent=True)

def create_circle_animation(var, save_directory):

    number_of_cells = var.shape[0]
    number_of_steps = var.shape[1] # timesteps

    b_max = np.amax(var)
    b_min = np.amin(var)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_ylim([1,-1])
    ax.set_xlim([1,-1])

    ax.set_aspect('equal')
    ax.axis('off')

    theta_list = np.linspace(90 , 450, 101)
    b_patches = []
    for i in range(len(theta_list) - 1):
        b_patches.append(Wedge((0,0), 0.8, theta_list[i], theta_list[i+1], width=0.1))

    b_patch_col = PatchCollection(b_patches)
    b_colors = var[:,0]
    b_patch_col.set_array(np.array(b_colors))
    b_patch_col.set_clim(vmin=b_min, vmax=b_max)
    b_patch_col.set_cmap('viridis')
    ax.add_collection(b_patch_col)
    fig.colorbar(b_patch_col, ax=ax)

    # ax.text(-0.9, 0.5, label_string, fontsize=20)
    #
    # current_time = 0
    # time_string = 't = ' + str(current_time) + 's'
    # time_text = ax.text(-0.9, -0.5,[],fontsize=16)
    # time_text.set_text(time_string)

    def init():
        b_colors = var[:,0]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        return b_patch_col, 

    sample_rate = 1
    def animate(i):
        sample_rate = 1
        b_colors = var[:,sample_rate * i]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        return b_patch_col, 


    number_of_frames = int(np.ceil(number_of_steps / sample_rate))
    frames_per_second = 24
    interval = np.ceil(1000/frames_per_second)

    anim = FuncAnimation(fig, animate, init_func=init, interval=interval, frames=number_of_frames, blit=True)

    anim.save(save_directory + 'circle' + '.mp4', fps=frames_per_second, extra_args=['-vcodec', 'libx264'])

# def add_colormaps(var):
#
#     grey_proportion = 1 / (np.max(var) + 1)
#     color_proportion = np.max(var) / (np.max(var) + 1)
#
#     cmap_pointsN = 256
#
#     grey_pointsN = np.floor(grey_proportion * cmap_pointsN)
#     color_pointsN = np.ceil(color_proportion * cmap_pointsN)
#
#     grey_points = numpy.linspace(-1, 0, num=50, endpoint=False)
#     color_points = numpy.linspace(0, 1, num=50, endpoint=True) # not sure 1 here is what you want
#
#     # sample the colormaps that you want to use. Use 128 from each so we get 256
#     # colors in total
#     colors1 = plt.cm.binary(np.linspace(0., 1, 128))
#     colors2 = plt.cm.gist_heat_r(np.linspace(0, 1, 128))
#
#     # combine them and build a new colormap
#     colors = np.vstack((colors1, colors2))
#     mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
#
#     plt.pcolor(data, cmap=mymap)
#     plt.colorbar()
#     plt.show()

def concentric_circle_animation(t, a, b, c, v, save_directory):

    number_of_cells = a.shape[0]
    number_of_steps = a.shape[1] # timesteps
    
    a_max = np.amax(a)
    a_min = 0

    b_max = np.amax(b)
    b_min = 0
    
    c_max = np.amax(c)
    c_min = 0
    
    v_max = np.amax(v)
    v_min = 0

    fig = plt.figure()
    ax = fig.add_subplot(122)
    ax_bmp = fig.add_subplot(121)

    ax.set_ylim([1,-1])
    ax.set_xlim([1,-1])

    ax.set_aspect('equal')
    # ax.axis('off')
    ax.set_facecolor('C7')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([-1,1],[0,0],linestyle='dashed', linewidth=0.5, c='k')
    ax.plot([0,0],[-1,1],linestyle='dashed', linewidth=0.5, c='k')
    
    ax_bmp.set_ylim([1,-1])
    ax_bmp.set_xlim([1,-1])

    ax_bmp.set_aspect('equal')
    # ax.axis('off')
    ax_bmp.set_facecolor('C7')
    ax_bmp.set_xticks([])
    ax_bmp.set_yticks([])
    ax_bmp.plot([-1,1],[0,0],linestyle='dashed', linewidth=0.5, c='k')
    ax_bmp.plot([0,0],[-1,1],linestyle='dashed', linewidth=0.5, c='k')

    theta_list = np.linspace(90 , 450, 101)
    a_patches = []
    b_patches = []
    c_patches = []
    v_patches = []
    for i in range(len(theta_list) - 1):
        a_patches.append(Wedge((0,0), 0.75, theta_list[i], theta_list[i+1], width=0.08))
        b_patches.append(Wedge((0,0), 0.85, theta_list[i], theta_list[i+1], width=0.25))
        c_patches.append(Wedge((0,0), 0.65, theta_list[i], theta_list[i+1], width=0.08))
        v_patches.append(Wedge((0,0), 0.85, theta_list[i], theta_list[i+1], width=0.08))

    a_patch_col = PatchCollection(a_patches)
    a_colors = a[:,0]
    a_patch_col.set_array(np.array(a_colors))
    a_patch_col.set_clim(vmin=a_min, vmax=a_max)
    a_patch_col.set_cmap('Purples')
    a_cm = copy(a_patch_col.get_cmap())
    a_cm.set_under('C7')
    a_patch_col.set_cmap(a_cm)
    
    b_patch_col = PatchCollection(b_patches)
    b_colors = b[:,0]
    b_patch_col.set_array(np.array(b_colors))
    b_patch_col.set_clim(vmin=b_min, vmax=b_max)
    b_patch_col.set_cmap('viridis')
    b_cm = copy(b_patch_col.get_cmap())
    b_cm.set_under('C7')
    b_patch_col.set_cmap(b_cm)
    
    c_patch_col = PatchCollection(c_patches)
    c_colors = c[:,0]
    c_patch_col.set_array(np.array(c_colors))
    c_patch_col.set_clim(vmin=c_min, vmax=c_max)
    c_patch_col.set_cmap('Oranges')
    c_cm = copy(c_patch_col.get_cmap())
    c_cm.set_under('C7')
    c_patch_col.set_cmap(c_cm)
    
    v_patch_col = PatchCollection(v_patches)
    v_colors = v[:,0]
    v_patch_col.set_array(np.array(v_colors))
    v_patch_col.set_clim(vmin=v_min, vmax=v_max)
    v_patch_col.set_cmap('Blues')
    v_cm = copy(v_patch_col.get_cmap())
    v_cm.set_under('C7')
    v_patch_col.set_cmap(v_cm)
    
    ax.add_collection(a_patch_col)
    ax.add_collection(c_patch_col)
    ax.add_collection(v_patch_col)
    
    ax_bmp.add_collection(b_patch_col)
    
    """ colorbars """
    # divider = make_axes_locatable(ax)
    # b_cax = divider.append_axes("right", size="5%", pad=0.05)
    # b_cb = fig.colorbar(b_patch_col, cax=b_cax, orientation='vertical', label='BMP4')
    #
    # c_cax = divider.append_axes("left", size="5%", pad=0.05)
    # c_cb = colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    # # c_cb = plt.colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    # # c_cb = fig.colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    # c_cax.yaxis.set_ticks_position("left")
    
    """ time string """
    # ax.text(-0.9, 0.5, label_string, fontsize=20)
    #
    # current_time = 0
    # time_string = 't = ' + str(current_time) + 's'
    # time_text = ax.text(-0.9, -0.5,[],fontsize=16)
    # time_text.set_text(time_string)

    def init():
        a_colors = a[:,0]
        a_patch_col.set_array(np.array(a_colors))
        a_patch_col.set_clim(vmin=a_min, vmax=a_max)
        
        b_colors = b[:,0]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        
        c_colors = c[:,0]
        c_patch_col.set_array(np.array(c_colors))
        c_patch_col.set_clim(vmin=c_min, vmax=c_max)
        
        v_colors = c[:,0]
        v_patch_col.set_array(np.array(v_colors))
        v_patch_col.set_clim(vmin=v_min, vmax=v_max)
        return a_patch_col, b_patch_col, c_patch_col, v_patch_col, 

    sample_rate = 2
    def animate(i):
        sample_rate = 2
        a_colors = a[:,sample_rate * i]
        a_patch_col.set_array(np.array(a_colors))
        a_patch_col.set_clim(vmin=a_min, vmax=a_max)
        
        b_colors = b[:,sample_rate * i]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        
        c_colors = c[:,sample_rate * i]
        c_patch_col.set_array(np.array(c_colors))
        c_patch_col.set_clim(vmin=c_min, vmax=c_max)
        
        v_colors = v[:,sample_rate * i]
        v_patch_col.set_array(np.array(v_colors))
        v_patch_col.set_clim(vmin=v_min, vmax=v_max)
        return a_patch_col, b_patch_col, c_patch_col, v_patch_col, 


    number_of_frames = int(np.ceil(number_of_steps / sample_rate))
    frames_per_second = 10
    interval = np.ceil(1000/frames_per_second)

    anim = FuncAnimation(fig, animate, init_func=init, interval=interval, frames=number_of_frames, blit=True)

    anim.save(save_directory + 'circle' + '.mp4', fps=frames_per_second, extra_args=['-vcodec', 'libx264'])

    # plt.savefig(save_directory + 'circle' + '.jpg')

    # plt.show()
