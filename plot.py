import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar

def create_animated_output(number_of_cells, sample_rate, t, a, b, v, c, params, save_directory):
    
    a_over_time = a
    
    nodal_count = np.sum(a, axis=0)
    
    number_of_frames = int(len(t) / sample_rate)

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

    ax_a.set_ylim([0,a_ymax])
    ax_b.set_ylim([0,np.max(b)*1.1])
    ax_c.set_ylim([0,10])
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
    ant_c, = ax_c.plot( ant_x, [0,10], lw=1, c='k', linestyle='dashed')
    # ant_c, = ax_c.plot( ant_x, [0,np.max(c)], lw=1, c='k', linestyle='dashed')
    ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=1, c='k', linestyle='dashed')
    
    threshold_streak_line, = ax_b.plot( [0, number_of_cells - 1],threshold_streak, lw=1, c='C0', linestyle='dashed')
    threshold_vg1_line, = ax_b.plot( [0, number_of_cells - 1], threshold_vg1, lw=1, c='C9', linestyle='dashed')

    line_a, = ax_a.plot( a_over_time[:,0], lw=3, c='C0', label='NODAL')
    line_b, = ax_b.plot( b[:,0], lw=3, c='C3', label='BMP4')
    line_c, = ax_c.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_v, = ax_v.plot( v[:,0], lw=3, c='C9',label='cVG1')

    time_x_loc = number_of_cells/3
    time_y_loc = 0.87*a_ymax
    time_text = ax_a.text(time_x_loc, time_y_loc,'t = ', fontsize=16)
    nodal_x_loc = (number_of_cells/3) - (number_of_cells * 0.03)
    nodal_y_loc = 0.73*a_ymax
    nodal_text = ax_a.text(nodal_x_loc, nodal_y_loc,'NODAL cells: ', fontsize=12)

    ax_a.legend(loc=2)
    ax_b.legend(loc=2)
    ax_c.legend(loc=2)
    ax_v.legend(loc=2)

    plt.tight_layout()

    # plt.show()

    def init():
        line_a, = ax_a.plot([],[], lw=3, c='C0', label='NODAL')
        line_b, = ax_b.plot([],[], lw=3, c='C3', label='BMP4')
        line_c, = ax_c.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_v, = ax_v.plot([],[],lw=3, c='C9',label='cVG1')
        time_text.set_text('t = ')
        nodal_text.set_text('Nodal cells: ')
        return line_a, line_b, line_c, line_v, time_text, nodal_text,
    def animate(i):
        line_a.set_data(range(number_of_cells), a_over_time[:,i * sample_rate])
        line_b.set_data(range(number_of_cells), b[:,i * sample_rate])
        line_c.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_v.set_data(range(number_of_cells), v[:,i * sample_rate])
        time_text.set_text('t = ' + "{:.1f}".format(t[i * sample_rate]) +'h')
        nodal_text.set_text('Nodal cells: ' + str(int(nodal_count[i * sample_rate])))
        return line_a, line_b, line_c, line_v, time_text, nodal_text,

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_frames, blit=False)

    anim.save(save_directory + 'hello.mp4', writer='ffmpeg', fps=10)
    
    return
    
def create_animated_output_extra_calcium(number_of_cells, sample_rate, t, a, b, v, c, params, save_directory):
    
    a_over_time = a
    
    nodal_count = np.sum(a, axis=0)
    
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

    line_a, = ax_a.plot( a_over_time[:,0], lw=3, c='C0', label='NODAL')
    line_b, = ax_b.plot( b[:,0], lw=3, c='C3', label='BMP4')
    line_c_low, = ax_c_low.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_c_high, = ax_c_high.plot( c[:,0], lw=3, c='C1',label='Ca2+\nactivity')
    line_v, = ax_v.plot( v[:,0], lw=3, c='C9',label='cVG1')

    text_x_loc = number_of_cells * 0.68
    # text_x_loc = number_of_cells * 0.33
    time_x_loc = text_x_loc
    time_y_loc = 0.85*a_ymax
    time_text = ax_a.text(time_x_loc, time_y_loc,'t = ', fontsize=14)
    nodal_x_loc = text_x_loc - number_of_cells*0.05
    nodal_y_loc = 0.74*a_ymax
    nodal_text = ax_a.text(nodal_x_loc, nodal_y_loc,'NODAL cells: ', fontsize=10)

    ax_a.legend(loc=2)
    ax_b.legend(loc=2)
    # ax_c_low.legend(loc=2)
    ax_c_high.legend(loc=2)
    ax_v.legend(loc=2)

    plt.tight_layout()

    # plt.show()

    def init():
        line_a, = ax_a.plot([],[], lw=3, c='C0', label='NODAL')
        line_b, = ax_b.plot([],[], lw=3, c='C3', label='BMP4')
        line_c_low, = ax_c_low.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_c_high, = ax_c_high.plot([],[],lw=3, c='C1',label='Ca2+\nactivity')
        line_v, = ax_v.plot([],[],lw=3, c='C9',label='cVG1')
        time_text.set_text('t = ')
        nodal_text.set_text('Nodal cells: ')
        return line_a, line_b, line_c_low, line_c_high, line_v, time_text, nodal_text,
    def animate(i):
        line_a.set_data(range(number_of_cells), a_over_time[:,i * sample_rate])
        line_b.set_data(range(number_of_cells), b[:,i * sample_rate])
        line_c_low.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_c_high.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_v.set_data(range(number_of_cells), v[:,i * sample_rate])
        time_text.set_text('t = ' + "{:.1f}".format(t[i * sample_rate]) +'h')
        nodal_text.set_text('Nodal cells: ' + str(int(nodal_count[i * sample_rate])))
        return line_a, line_b, line_c_low,line_c_high, line_v, time_text, nodal_text,

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_frames, blit=False)

    anim.save(save_directory + 'hello.mp4', writer='ffmpeg', fps=10)
    
    return

def create_stills_array(time_indices, number_of_cells, t, a, b, v, c, filename):
    
    timepointsN = len(time_indices)

    nodal_count = np.sum(a, axis=0)
    
    a_ymax = np.max(a)*1.1
    b_ymax = np.max(b)*1.1
    c_ymax = np.max(c)*1.1
    v_ymax = np.max(v)*1.1
    
    anterior_cell = (number_of_cells - 1) / 2

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

        ax_c.set_xlabel("Cell position")

        ant_x = [anterior_cell, anterior_cell]

        ant_a, = ax_a.plot( ant_x, [0,np.max(a)], lw=0.5, c='k', linestyle='dashed')
        ant_b, = ax_b.plot( ant_x, [0,np.max(b)], lw=0.5, c='k', linestyle='dashed')
        ant_c, = ax_c.plot( ant_x, [0,np.max(c)], lw=0.5, c='k', linestyle='dashed')
        ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=0.5, c='k', linestyle='dashed')

        line_a, = ax_a.plot( a[:,time_idx], lw=2, c='C0', label='NODAL')
        line_b, = ax_b.plot( b[:,time_idx], lw=2, c='C3', label='BMP4')
        line_c, = ax_c.plot( c[:,time_idx], lw=2, c='C1',label='Ca2+')
        line_v, = ax_v.plot( v[:,time_idx], lw=2, c='C9',label='cVG1')
        
        time_str = str(t[time_idx])
        ax_a.set_title('t = ' + time_str + 'h', fontweight='bold')
        
        if col_idx == 0:
            ax_a.set_yticklabels(['OFF','ON'])
            
            ax_a.set_ylabel('NODAL', fontweight='bold')
            ax_b.set_ylabel('BMP4\n', fontweight='bold')
            ax_c.set_ylabel('Ca2+\nactivity', fontweight='bold')
            ax_v.set_ylabel('cVG1\n', fontweight='bold')
            
        else:
            ax_a.set_yticklabels([])
            ax_b.set_yticklabels([])
            ax_c.set_yticklabels([])
            ax_v.set_yticklabels([])
            
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

def concentric_circle_animation(t, a, b, c, v, save_directory):

    number_of_cells = a.shape[0]
    number_of_steps = a.shape[1] # timesteps
    
    a_max = np.amax(a)
    a_min = np.amin(a)

    b_max = np.amax(b)
    b_min = np.amin(b)
    
    c_max = np.amax(c)
    c_min = np.amin(c)
    
    v_max = np.amax(v)
    v_min = np.amin(v)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_ylim([1,-1])
    ax.set_xlim([1,-1])

    ax.set_aspect('equal')
    # ax.axis('off')
    ax.set_facecolor('C7')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([-1,1],[0,0],linestyle='dashed', linewidth=0.5, c='k')
    ax.plot([0,0],[-1,1],linestyle='dashed', linewidth=0.5, c='k')

    theta_list = np.linspace(90 , 450, 101)
    a_patches = []
    b_patches = []
    c_patches = []
    v_patches = []
    for i in range(len(theta_list) - 1):
        a_patches.append(Wedge((0,0), 0.8, theta_list[i], theta_list[i+1], width=0.1))
        b_patches.append(Wedge((0,0), 0.65, theta_list[i], theta_list[i+1], width=0.1))
        c_patches.append(Wedge((0,0), 0.8, theta_list[i], theta_list[i+1], width=0.1))
        v_patches.append(Wedge((0,0), 0.8, theta_list[i], theta_list[i+1], width=0.1))

    a_patch_col = PatchCollection(a_patches)
    a_colors = a[:,0]
    a_patch_col.set_array(np.array(a_colors))
    a_patch_col.set_clim(vmin=a_min, vmax=a_max)
    a_patch_col.set_cmap('viridis')
    
    b_patch_col = PatchCollection(b_patches)
    b_colors = b[:,0]
    b_patch_col.set_array(np.array(b_colors))
    b_patch_col.set_clim(vmin=b_min, vmax=b_max)
    b_patch_col.set_cmap('viridis')
    
    c_patch_col = PatchCollection(c_patches)
    c_colors = c[:,0]
    c_patch_col.set_array(np.array(c_colors))
    c_patch_col.set_clim(vmin=c_min, vmax=c_max)
    c_patch_col.set_cmap('inferno')
    
    v_patch_col = PatchCollection(v_patches)
    v_colors = v[:,0]
    v_patch_col.set_array(np.array(v_colors))
    v_patch_col.set_clim(vmin=v_min, vmax=v_max)
    v_patch_col.set_cmap('viridis')
    
    ax.add_collection(c_patch_col)
    ax.add_collection(b_patch_col)
    
    divider = make_axes_locatable(ax)
    b_cax = divider.append_axes("right", size="5%", pad=0.05)
    b_cb = fig.colorbar(b_patch_col, cax=b_cax, orientation='vertical')
    
    c_cax = divider.append_axes("left", size="5%", pad=0.05)
    c_cb = colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    # c_cb = plt.colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    # c_cb = fig.colorbar(c_patch_col, cax=c_cax, orientation="vertical")
    c_cax.yaxis.set_ticks_position("left")
    
    # ax.text(-0.9, 0.5, label_string, fontsize=20)
    #
    # current_time = 0
    # time_string = 't = ' + str(current_time) + 's'
    # time_text = ax.text(-0.9, -0.5,[],fontsize=16)
    # time_text.set_text(time_string)

    def init():
        b_colors = b[:,0]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        
        c_colors = c[:,0]
        c_patch_col.set_array(np.array(c_colors))
        c_patch_col.set_clim(vmin=c_min, vmax=c_max)
        return b_patch_col, c_patch_col, 

    sample_rate = 2
    def animate(i):
        sample_rate = 2
        b_colors = b[:,sample_rate * i]
        b_patch_col.set_array(np.array(b_colors))
        b_patch_col.set_clim(vmin=b_min, vmax=b_max)
        
        c_colors = c[:,sample_rate * i]
        c_patch_col.set_array(np.array(c_colors))
        c_patch_col.set_clim(vmin=c_min, vmax=c_max)
        return b_patch_col, c_patch_col, 


    number_of_frames = int(np.ceil(number_of_steps / sample_rate))
    frames_per_second = 10
    interval = np.ceil(1000/frames_per_second)

    anim = FuncAnimation(fig, animate, init_func=init, interval=interval, frames=number_of_frames, blit=True)

    anim.save(save_directory + 'circle' + '.mp4', fps=frames_per_second, extra_args=['-vcodec', 'libx264'])

    # plt.savefig(save_directory + 'circle' + '.jpg')

    # plt.show()
