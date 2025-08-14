import bpy, json, sys, os

# Command line argument: exercise name
exercise_name = sys.argv[-1]

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE_DIR, "templates/exercise_template.blend")
OUTPUT = os.path.join(BASE_DIR, "output", f"{exercise_name}_final.mov")
EXERCISES_JSON = os.path.join(BASE_DIR, "exercises.json")
MODEL_FBX = os.path.join(BASE_DIR, "models", "male_rigged.fbx")

# Load Blender template
bpy.ops.wm.open_mainfile(filepath=TEMPLATE)

# Import rigged model
bpy.ops.import_scene.fbx(filepath=MODEL_FBX)

# Load exercise keyframes
with open(EXERCISES_JSON) as f:
    exercises = json.load(f)
exercise = next(x for x in exercises if x["name"] == exercise_name)

armature = bpy.data.objects['Armature']  # adjust if different
bpy.context.view_layer.objects.active = armature

# Apply keyframes
for kf in exercise["keyframes"]:
    bone = armature.pose.bones[kf["bone"]]
    if "location" in kf:
        bone.location = kf["location"]
        bone.keyframe_insert(data_path="location", frame=kf["frame"])
    if "rotation_euler" in kf:
        bone.rotation_euler = kf["rotation_euler"]
        bone.keyframe_insert(data_path="rotation_euler", frame=kf["frame"])

# Render settings
scene = bpy.context.scene
scene.render.filepath = OUTPUT
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'QUICKTIME'
scene.render.ffmpeg.codec = 'MJPEG'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 29.97

bpy.ops.render.render(animation=True)
