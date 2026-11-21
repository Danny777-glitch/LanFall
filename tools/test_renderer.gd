extends SceneTree

func _init():
	print("Checking rendering driver...")
	print("Video Adapter: ", RenderingServer.get_video_adapter_name())
	quit()
