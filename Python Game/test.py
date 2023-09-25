from ursina import * # import as usual
app = Ursina()       # create app as usual

window.fps_counter.enabled = False # this is just to remove the fps counter

box = Entity(model='cube',         # create cube as before (you can make your own class)
             origin=(0,0.7,-5),    # set origin to behind the player and above a little
             parent=camera,        # make it orientate around the camera
             color=color.red,      # change the color
             texture='shore')      # choose a nice texture

def update():                      # define the auto-called update function
    if held_keys['a']:
        camera.rotation_y -= 10 * time.dt # the time.dt thing makes it adapt to the fps so its smooth
    elif held_keys['d']:
        camera.rotation_y += 10 * time.dt

Sky() # just a textured sky to make sure you can see that you are both rotating
app.run() # run