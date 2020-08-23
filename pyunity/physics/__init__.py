"""
A basic 3D Physics engine that uses
similar concepts to the Unity
Engine itself. Only supports
non-rotated colliders.

To create an immoveable object, use
math.inf or the provided `infinity`
variable. This will make the object
not be able to move, unless you set
an initial velocity. Then, the
collider will either push everything
it collides with, or bounces it back
at twice the speed.

Example
-------

>>> cube = GameObject("Cube")
>>> collider = cube.AddComponent(AABBoxCollider)
>>> collider.SetSize(-Vector3.one(), Vector3.one())
>>> collider.velocity = Vector3.right()

"""

from .core import *