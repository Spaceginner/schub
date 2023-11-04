from sypy import RunConfig


from . import server


server.start(RunConfig(8080))
