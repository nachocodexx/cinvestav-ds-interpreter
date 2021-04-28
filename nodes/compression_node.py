from node import Node 
class CompressionNode(Node):
    def __init__(self,nodeId,**kwargs):
        self.DOCKER_IMAGE = "nachocode/cinvestav-ds-compression"
        self.nodeId       = nodeId
        self.net          = kwargs.get("network","mynet")
        self.ip           = kwargs.get("ip",None)
        self.host         = kwargs.get("host","0.0.0.0")
        self.port         = kwargs.get("port",6666)
        self.url          = "http://{}:{}/{}".format(self.ip,self.port,self.nodeId)
        self.storage_path = kwargs.get("storage_path","/app/src/tmp")
        self.volume_str   = kwargs.get("volume","/home/nacho/Documents/test/compression")+"/"+str(self.nodeId)

        self.detach       = True
        self.environment  = {"NODE_ID":self.nodeId,"NODE_PORT":self.port,"NODE_HOST":self.host,"STORAGE_PATH":self.storage_path}
    def run(self,client):
        port = {}
        port[self.port]=self.port
        volume = {}
        volume[self.volume_str] ={'bind':self.storage_path,'mode':'rw'}
        container = client.containers.create(
                self.DOCKER_IMAGE,
                detach      = self.detach,
                ports       = port,
                environment = self.environment,
                labels      = {"compression":""},
                name        = self.nodeId,
                volumes     = volume
        )
        net = client.networks.get(self.net)
        net.connect(container,ipv4_address=self.ip)
        container.start()


