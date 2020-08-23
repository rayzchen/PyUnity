from pyunity import *
from .scripts import *

config.faceCulling = False

def main():
    mesh = loader.LoadObj("pyunity/examples/example5/house.obj")

    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 0, -20)

    house = GameObject("House")
    house.transform.rotation = Vector3(-90, 0, 0)
    renderer = house.AddComponent(MeshRenderer)
    renderer.mesh = mesh
    renderer.mat = Material((255, 255, 255))
    house.AddComponent(Rotator)
    
    scene.Add(house)
    
    scene.Run()