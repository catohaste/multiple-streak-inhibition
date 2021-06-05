import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_animated_output(number_of_cells, sample_rate, t, a, b, v, c, save_directory):
    
    a_over_time = a
    
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

    a_ymax = np.max(a)*1.3 # 0.01

    ax_a.set_ylim([0,a_ymax])
    ax_b.set_ylim([0,np.max(b)*1.1])
    # ax_c.set_ylim([0,5])
    ax_c.set_ylim([0,np.max(c)*1.1])
    ax_v.set_ylim([0,np.max(v)*1.1])

    ax_a.set_xticks([0,int(number_of_cells/2), number_of_cells])
    ax_b.set_xticks([0,int(number_of_cells/2), number_of_cells])
    ax_v.set_xticks([0,int(number_of_cells/2), number_of_cells])
    ax_c.set_xticks([0,int(number_of_cells/2), number_of_cells])

    ax_a.set_xticklabels([])
    ax_b.set_xticklabels([])
    ax_v.set_xticklabels([])
    ax_c.set_xticklabels(['pos.', 'ant.', 'pos.'])

    ax_c.set_xlabel("Cell position")

    line_a, = ax_a.plot( a_over_time[:,0], lw=3, c='C0', label='streak')
    line_b, = ax_b.plot( b[:,0], lw=3, c='C1', label='bmp')
    line_c, = ax_c.plot( c[:,0], lw=3, c='C2',label='calcium')
    line_v, = ax_v.plot( v[:,0], lw=3, c='C3',label='vg1')

    text_x_loc = number_of_cells/3
    text_y_loc = 0.85*a_ymax
    time_text = ax_a.text(text_x_loc, text_y_loc,'t = ', fontsize=16)

    ax_a.legend(loc=1)
    ax_b.legend(loc=1)
    ax_c.legend(loc=1)
    ax_v.legend(loc=1)

    plt.tight_layout()

    # plt.show()


    def init():
        line_a, = ax_a.plot([],[], lw=3, c='C0', label='streak')
        line_b, = ax_b.plot([],[], lw=3, c='C1', label='bmp')
        line_c, = ax_c.plot([], [],lw=3, c='C2',label='calcium')
        line_v, = ax_v.plot([], [],lw=3, c='C3',label='vg1')
        time_text.set_text('t = ')
        return line_a, line_b, line_c, line_v, time_text,
    def animate(i):
        line_a.set_data(range(number_of_cells), a_over_time[:,i * sample_rate])
        line_b.set_data(range(number_of_cells), b[:,i * sample_rate])
        line_c.set_data(range(number_of_cells), c[:,i * sample_rate])
        line_v.set_data(range(number_of_cells), v[:,i * sample_rate])
        time_text.set_text('t = ' + "{:.1f}".format(t[i * sample_rate]) +'h')
        return line_a, line_b, line_c, line_v, time_text,

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_frames, blit=False)

    anim.save(save_directory + 'hello.mp4', writer='ffmpeg', fps=10)
    
    return
