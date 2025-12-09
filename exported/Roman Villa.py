# ----------------------------------------------------
# IMPORT MODULES
# ----------------------------------------------------
import viz
import vizfx 
import vizact
import vizshape
import vizcam
import random
import vizconnect
import tools.grabber 
# ----------------------------------------------------
# CREATE WORLD
# ----------------------------------------------------
viz.go()
vizconnect.go('vizconnect_config.py')
# ----------------------------------------------------
# GROUND
# ----------------------------------------------------
ground = viz.addChild('ground_grass.osgb')
ground.setScale(3,3,3)
viz.MainView.collision(viz.ON)
# ----------------------------------------------------
# SKYDOME
# ----------------------------------------------------
env = viz.addEnvironmentMap('sky.jpg')
sky = viz.add('skydome.dlc')
sky.texture(env)
# ----------------------------------------------------
# IMPORT MODEL
# ----------------------------------------------------
room = viz.addChild('Roman Villa.gltf') 
room.setPosition([0,0,2])
# ----------------------------------------------------
# WINDOW TRANSPARENCY - Simplified
# ----------------------------------------------------
window_names = ['FixedWindow1', 'FixedWindow2']
for window_name in window_names:
    window = room.getChild(window_name)
    if window:
        window.alpha(0.6)
        window.enable(viz.BLEND)
        window.drawOrder(100)
# ----------------------------------------------------
# VIEW & CAMERA SETTINGS
# ----------------------------------------------------
viz.MainWindow.fov(60)
# ----------------------------------------------------
# LIGHTING - REALISTIC SETUP (STRATEGIC LIGHTS VIA VIZFX)
# ----------------------------------------------------
# Disable default headlight (press SPACE to toggle)
headLight = viz.MainView.getHeadLight()
headLight.disable()
vizact.onkeydown(' ', headLight.enable)

#sun = vizfx.addDirectionalLight(euler=(45, -60, 0), color=[1.0, 0.95, 0.8])
#sun.intensity(2.0) # Increased from 1.5 to 2.0
#sun.specular([0.5, 0.5, 0.5])

#vizfx.setAmbientColor([0.45, 0.45, 0.5])
strategic_torch_coords = [
    [16.246, 1.599, 25.291],   # (X=16.246, Y=1.599, Z=25.291)
    [-0.095, 0.402, 21.682],   # (X=-0.095, Y=0.402, Z=21.682)
    [-16.207, 1.599, 31.137],  # (X=-16.207, Y=1.599, Z=31.137)
    [-7.908, 1.599, -3.557],   # (X=-7.908, Y=1.599, Z=-3.557)
    [7.887, 1.599, -3.29],     # (X=7.887, Y=1.599, Z=-3.29)
    [16.246, 1.599, -3.733],   # (X=16.246, Y=1.599, Z=-3.733)
    [-16.189, 1.599, -3.557],  # (X=-16.189, Y=1.599, Z=-3.557)
    [-5.852, 2.111, -32.398]   # (X=-5.852, Y=2.111, Z=-32.398)
]

# ----------------------------------------------------
# ADD STRATEGIC TORCH LIGHTS (Using vizfx.addPointLight)
# ----------------------------------------------------
torch_lights = []

for i, coord in enumerate(strategic_torch_coords):
    torch_light = vizfx.addPointLight(pos=coord)
    
    torch_light.color([1.0, 0.6, 0.2])
    torch_light.intensity(2)
    
    # Set attenuation for localized light falloff
    torch_light.linearAttenuation(0.15) 
    
    torch_lights.append(torch_light)


# ----------------------------------------------------
# TORCH FLICKERING (ENHANCED FLICKER)
# ----------------------------------------------------
def flickerTorch(light):
    # WIDENED RANGE: Set a larger difference (1.0 to 2.0)
    intensity_variation = random.uniform(1.4, 1.6) 
    light.intensity(intensity_variation)

def updateTorches():
    for light in torch_lights:
        flickerTorch(light)

# INCREASED FREQUENCY: 0.05 seconds (20 times per second)
vizact.ontimer(0.15, updateTorches) 

# ----------------------------------------------------
# INTERACTIVE OBJECTS (Unchanged)
# ----------------------------------------------------
item_names = ['Amphorae1', 'Amphorae2','Amphorae3','Amphorae4','Amphorae5','ConcertHarp2','ConcertHarp','Door Leaf 1','Door Leaf 2']
grabber = vizconnect.getRawTool('grabber')
items = []
harps = []
harp_sounds = {}
for item_name in item_names:
    item = room.getChild(item_name)
    if item:
        items.append(item)
        if item_name == 'ConcertHarp' or item_name == 'ConcertHarp2':
            harps.append(item)
            harp_sounds[item] = viz.addAudio('Harp Sound.wav')
            harp_sounds[item].stop()
grabber.setItems(items)

# Detect when something is grabbed
def onGrab(e):
    grabbed_object = e.grabbed
    if grabbed_object in harps:
        harp_sounds[grabbed_object].play()

# Detect when something is released
def onRelease(e):
    released_object = e.released
    if released_object in harps:
        harp_sounds[released_object].stop()

# Register the events
viz.callback(tools.grabber.GRAB_EVENT, onGrab)
viz.callback(tools.grabber.RELEASE_EVENT, onRelease)