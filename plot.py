import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_animated_output(number_of_cells, sample_rate, t, a, b, v, c, save_directory):
    
    a_over_time = a
    
    nodal_count = np.sum(a, axis=0)
    
    number_of_frames = int(len(t) / sample_rate)

    fig = plt.figure(figsize=(4,8))

    ax_a = fig.add_subplot(4,1,1)
    ax_v = fig.add_subplot(4,1,2)
    ax_b = fig.add_subplot(4,1,3)
    ax_c = fig.add_subplot(4,1,4)

    # ax.plot(a[:,100])

    # ax_a.set_title('streak')
    # ax_b.set_title('bmp')
    # ax_c.set_title('calcium')

    a_ymax = np.max(a)*1.5 # 0.01

    ax_a.set_ylim([0,a_ymax])
    ax_b.set_ylim([0,np.max(b)*1.1])
    # ax_c.set_ylim([0,5])
    ax_c.set_ylim([0,np.max(c)*1.1])
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
    
    ant_a, = ax_a.plot( ant_x, [0,np.max(a)], lw=1, c='k', linestyle='dashed')
    ant_b, = ax_b.plot( ant_x, [0,np.max(b)], lw=1, c='k', linestyle='dashed')
    ant_c, = ax_c.plot( ant_x, [0,np.max(c)], lw=1, c='k', linestyle='dashed')
    ant_v, = ax_v.plot( ant_x, [0,np.max(v)], lw=1, c='k', linestyle='dashed')

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
        line_c, = ax_c.plot([], [],lw=3, c='C1',label='Ca2+\nactivity')
        line_v, = ax_v.plot([], [],lw=3, c='C9',label='cVG1')
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
    
    