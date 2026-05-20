bl_info = {
	"name" : "SimpleAssist",
	"author" : "lumxiv",
	"description" : "Export custom animations for FFXIV",
	"version": (1, 0, 0),
	"blender" : (4, 5, 4),
	"location" : "3D View > Tools (Right Side) > SimpleAssist",
	"warning" : "",
	"category" : "Animation",
	"wiki_url": 'https://github.com/lumxiv/SimpleAssist',
    "tracker_url": 'https://github.com/lumxiv/SimpleAssist/issues',
}

from . import addon

def register():
	addon.register()

def unregister():
    addon.unregister()