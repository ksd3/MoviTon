import RayTracer
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import glob
from PIL import Image
import os
import moviepy.editor as mp

def main():
   
    #raytrace_some_photons()
    a=0.4 #black hole spin
    initial_theta=-0.5 #initial viewing angle - set to -0.5 so the first iteration of the loop will set it to 0

    for frame in range(180):
        initial_theta=initial_theta+0.5
        RayTracer.image(a,initial_theta,frame,wavelength_function=exponential_temperature_decay,unobservable_to_gray=False,set_intensity=False) 
    
    plt.show()
    gr_gif_frames=[]
    newtonian_gif_frames=[]

    gr_images=sorted(glob.glob("*gr_frame*"),key=os.path.getmtime) #glob is infuriating beyond belief to work with - this is the reason i can't upload the precomputed files to anyone because it'll change the creation time
    for i in gr_images:

        new_frame=Image.open(i)
        gr_gif_frames.append(new_frame)
    

    newtonian_images=sorted(glob.glob("*newtonian_frame*"),key=os.path.getmtime)
    for i in newtonian_images:

        new_frame=Image.open(i)
        newtonian_gif_frames.append(new_frame)
    

    gr_gif_frames[0].save("gr.gif",format="GIF",append_images=gr_gif_frames[1:],save_all=True,duration=50)
    newtonian_gif_frames[0].save("newtonian.gif",format="GIF",append_images=newtonian_gif_frames[1:],save_all=True,duration=50)
    clip=mp.VideoFileClip("gr.gif")
    clip.write_videofile("gr_visible.mp4")

    clip=mp.VideoFileClip("newtonian.gif")
    clip.write_videofile("newtonian_visible.mp4")

    #os.system('sudo rm *.png;sudo rm *.npy; sudo rm -r __pycache__')#cleans up the directory - uncomment this if you want to save each frame
    
    return None
 

def exponential_temperature_decay(x_i,y_i):
    
    #realistic temperature decay
    a=0.4 #make sure this is the same as your original spin!
    radius=np.sqrt(x_i**2+y_i**2-a**2)
    initial_lambda=550
    
    true_lambda=initial_lambda*(radius/10)**(3/4)

    return true_lambda

def hot_spiral(x_i,y_i):
    
    #hot spiral in the disk
    a=0.4 #make sure this is the same as your original spin!
    initial_lambda=550
    r=np.sqrt(x_i**2+y_i**2-a**2)    
    extra_lambda=250
    spiral_a=0
    spiral_b=18/np.pi
    phi=np.arctan(y/x)

    if type(phi)!=type(np.zeros(1)):
        if phi<0:
            phi=phi+np.pi
    else:
        for i,placeholder in enumerate(phi):
            if placeholder<0:
                phi[i]=placeholder+np.pi

    spiral_par=r-(spiral_a+spiral_b*phi)
    true_lambda=initial_lambda-extra_lambda*np.exp(-abs(spiral_par)/2.5)

    return true_lambda

def raytrace_some_photons(): #this is just to raytrace photons in 2D - it isn't a temperature function!
    a=[-0.998,-0.9,-0.85,-0.8,-0.71,-0.7,-0.66,-0.6,-0.55,-0.5,-0.44,-0.4,-0.33,-0.3,-0.22,-0.2,-0.11,-0.1,-0.09,-0.07,-0.04,0,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.43,0.5,0.59,0.6,0.62,0.7,0.71,0.8,0.82,0.9,0.92,0.998]
    initial_theta=50
    a0_s=3.4
    b0_s=6.45

    plot_fig,plot_ax,anim_fig,anim_ax,anim=RayTracer.plot_and_start_animating_rays_from_parameters(spins=a,thetas=initial_theta,alphas=a0_s,betas=b0_s)

    plt.show()
    
    
def simple_varying_temperature(x_i,y_i): #sinc temperature approximation - nothing special
    
    scale_factor=0.2
    initial_x,initial_y=3,3
    initial_lambda=480
    
    true_lambda=initial_lambda*(1+scale_factor*np.cos(x_i/initial_x)*np.sin(y_i/initial_y))

    return true_lambda

def cold_spots_on_disk(x_i,y_i):
    
    #this function shows 4 colder spots on the disk
    extra_lambda=200
    initial_x,initial_y=5,5
    initial_lambda=500
    
    true_lambda=initial_lambda
    true_lambda=true_lambda+extra_lambda*np.exp(-((x_i-initial_x)/5)**2)*np.exp(-((y_i-initial_y)/5)**2) 
    true_lambda=true_lambda+extra_lambda*np.exp(-((x_i+initial_x)/5)**2)*np.exp(-((y_i-initial_y)/5)**2) 
    true_lambda=true_lambda+extra_lambda*np.exp(-((x_i-initial_x)/5)**2)*np.exp(-((y_i+initial_y)/5)**2) 
    true_lambda=true_lambda+extra_lambda*np.exp(-((x_i+initial_x)/5)**2)*np.exp(-((y_i+initial_y)/5)**2) 
    true_lambda=true_lambda+extra_lambda*np.exp(-((x_i+initial_x)/5)**2)*np.exp(-((y_i+initial_y)/5)**2)

    return true_lambda

if __name__=="__main__":
    main()

