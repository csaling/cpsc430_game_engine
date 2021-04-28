import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup (
    name = "OpenGLPythonTest",
    options = {"build_exe": {"packages": ["pygame", "OpenGL", "PIL", "numpy", "pubsub"]}},
    executables = executables
    )