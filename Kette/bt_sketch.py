# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation

    #parameters
  
    #list
    global geom1_params, toruses, toruses_x, toruses_y, toruses_nx, toruses_ny, torus_lines
    toruses_x = []
    toruses_y = []
    toruses_nx = []
    toruses_ny = []
    torus_lines = []
    #dictionary
    geom1_params = {
        "size": 4,
        "x": 2,
        "y": 3,
        "z": 4,
        "rotation": 45 
        }

    geom1_params = Object.fromEntries(to_js(geom1_params))

    #Materials
    global material, line_material
    color = THREE.Color.new(50,55,55)
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.6
    material.color = THREE.Color.new(255,255,255)

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(0,100,100)

    #Store GUI Parameters once
   
   
    #generate the torus using for loop:
    for i in range(geom1_params.x):
        
        #TORUS
        geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
        geometry.translate((2*geom1_params.size-2)*i,0,0)
        geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * i)
        torus = THREE.Mesh.new(geometry, material)
        toruses_x.append(torus)

        '''scene.add(torus)'''

        #EDGES
        edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
        edges = THREE.LineSegments.new(edges_geom1, line_material)
        torus_lines.append(edges)
        scene.add(edges)
        scene.add(torus)

        

    
    for t in range(geom1_params.y):
        #TORUS 
        geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
        geometry.translate(0, ((-geom1_params.size)*2+2)*t,0)
        geometry.rotateY(math.radians(geom1_params.rotation)/0.5 * t)
        torus = THREE.Mesh.new(geometry, material)
        toruses_y.append(torus)
        #EDGES
        edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
        edges = THREE.LineSegments.new(edges_geom1, line_material)
        torus_lines.append(edges)
        scene.add(edges)
        scene.add(torus)



    for a in range(geom1_params.x):
        #TORUS Negativ X
        geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
        geometry.translate(-((-geom1_params.size)*2+2)*(-a), 0, 0)
        geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * a)
        torus = THREE.Mesh.new(geometry, material)
        toruses_nx.append(torus)
        #EDGES
        edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
        edges = THREE.LineSegments.new(edges_geom1, line_material)
        '''scene.add(edges)'''
        '''scene.add(torus)'''


    for l in range(geom1_params.y):
        #TORUS Negativ Y
        geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
        geometry.translate(0, ((-geom1_params.size)*2+2)*(-l),0)
        geometry.rotateY(math.radians(geom1_params.rotation)/0.5 * l)
        torus = THREE.Mesh.new(geometry, material)
        toruses_ny.append(torus)
        #EDGES
        edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
        edges = THREE.LineSegments.new(edges_geom1, line_material)
        '''scene.add(edges)'''
        '''scene.add(torus)'''


        

    #-----------------------------------------------------------------------
    # USER INTERFACE

    # Set up Mouse orbit control
    global controls
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('parameters')
    param_folder.add(geom1_params, 'size', 2,15,1)
    param_folder.add(geom1_params, 'x', 2,30,1)
    param_folder.add(geom1_params, 'rotation', 0, 270)
    param_folder.open()
    
    
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
#Update the chain

def update_toruses():
    global toruses_x, toruses_y, toruses_nx, toruses_ny, torus_lines, material, line_material
    #make shure you don't have 0 toruses

    if len(toruses_x) != 0:
        if len(toruses_x) != geom1_params.x:
            for torus in toruses_x: scene.remove(torus)
            for edge in torus_lines: scene.remove(edge)
            torus = []
            torus_lines = []
            for i in range(geom1_params.x):
        
                #TORUS
                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                geometry.translate((2*geom1_params.size-2)*i,0,0)
                geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * i)
                torus = THREE.Mesh.new(geometry, material)
                toruses_x.append(torus)

                scene.add(torus)

                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                torus_lines.append(edges)
                '''scene.add(edges)'''

    
            
        else: #if amount doesnt change only update the parameters of existing torus
            for t in range(len(toruses_x)):
                torus = toruses_x[t]
                edges = torus_lines[t]

                #TORUS
                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                
                geometry.translate((2*geom1_params.size-2)*t,0,0)
                geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * t)
                torus = THREE.Mesh.new(geometry, material)
                toruses_x.append(torus)

                scene.add(torus)

                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                torus_lines.append(edges)
                '''scene.add(edges)'''
    else: 
        pass

    '''if len(toruses_y) != 0:
        if len(toruses_y) != geom1_params.y:
            for torus in toruses_y: scene.remove(torus)
            for edge in torus_lines: scene.remove(edge)
            torus = []
            torus_lines = []
            for t in range(geom1_params.y):
        
                 #TORUS 
                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                geometry.translate(0, ((-geom1_params.size)*2+2)*t,0)
                geometry.rotateY(math.radians(geom1_params.rotation)/0.5 * t)
                torus = THREE.Mesh.new(geometry, material)
                toruses_y.append(torus)
                scene.add(torus)
                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                torus_lines.append(edges)
                scene.add(edges)

    
            
        else: #if amount doesnt change only update the parameters of existing torus
            for i in range(len(toruses_y)):
                torus = toruses_y[i]
                edges = torus_lines[i]

                
                
                 #TORUS 
                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                geometry.translate(0, ((-geom1_params.size)*2+2)*i,0)
                geometry.rotateY(math.radians(geom1_params.rotation)/0.5 * i)
                torus = THREE.Mesh.new(geometry, material)
                toruses_y.append(torus)
                scene.add(torus)
                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                torus_lines.append(edges)
                scene.add(edges)
    else: 
        pass''' 

    if len(toruses_nx) != 0:
        if len(toruses_nx) != geom1_params.x:
            for torus in toruses_y: scene.remove(torus)
            for edge in torus_lines: scene.remove(edge)
            torus = []
            torus_lines = []
            for a in range(geom1_params.x):
            
            #TORUS Negativ X

                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                geometry.translate(-((-geom1_params.size)*2+2)*(-a), 0, 0)
                geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * a)
                torus = THREE.Mesh.new(geometry, material)
                toruses_nx.append(torus)
                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                toruses_y.append(torus)
                '''scene.add(edges)'''
                scene.add(torus)

    
            
        else: #if amount doesnt change only update the parameters of existing torus
            for i in range(len(toruses_nx)):
                torus = toruses_nx[i]
                edges = torus_lines[i]

                
                
                #TORUS Negativ X

                geometry = THREE.TorusGeometry.new(geom1_params.size, 1, 10, 10)
                geometry.translate(-((-geom1_params.size)*2+2)*(-i), 0, 0)
                geometry.rotateX(math.radians(geom1_params.rotation)/0.5 * i)
                torus = THREE.Mesh.new(geometry, material)
                toruses_nx.append(torus)
                #EDGES
                edges_geom1 = THREE.EdgesGeometry.new(torus.geometry)
                edges = THREE.LineSegments.new(edges_geom1, line_material)
                torus_lines.append(edges)
                '''scene.add(edges)'''
                scene.add(torus)
    else: 
        pass             

#######################

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_toruses()

    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()