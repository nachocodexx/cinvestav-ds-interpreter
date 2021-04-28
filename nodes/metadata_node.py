from node import Node

class MetadataNode(Node):
    def __init__(self,nodeId,**kwargs):
        self.DOCKER_IMAGE = "nachocode/cinvestav-ds-metadata"
        self.nodeId       = nodeId
        self.net          = kwargs.get("network","mynet") 
        self.port         = kwargs.get('port',6666)
        self.mongoUrl     = kwargs.get("mongo_url","mongodb://166.0.63.254:27017")
        self.enviroment   = {
                                "NODE_ID":self.nodeId,
                                "NODE_PORT":self.port,
                                "NODE_HOST":"0.0.0.0",
                                "MONGODB_URL":self.mongoUrl
                            }
        self.ip            = kwargs.get("ip")
    def run(self,client):
        port = {}
        port[self.port]=self.port
        container = client.containers.create(
                        self.DOCKER_IMAGE,
                        detach      = True,
                        environment = self.enviroment, 
                        ports       = port,
                        labels      = {"metadata":""},
                        name        = self.nodeId,
                )
        net = client.networks.get(self.net)
        net.connect(container,ipv4_address=self.ip)
        container.start()


