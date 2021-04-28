from node import Node

class StoragePool(Node):
    def __init__(self,nodeId,**kwargs):
        self.DOCKER_IMAGE      = "nachocode/cinvestav-ds-storage-pool"
        self.nodeId            = nodeId
        self.net               = kwargs.get("network","mynet")
        self.ip                = kwargs.get("ip",None)
        self.port              = kwargs.get("port",6666) 
        self.host              = kwargs.get("host","0.0.0.0")
        self.detach            = kwargs.get("detach",True)
        self.balancer          = kwargs.get("load_balancer","RB")
        self.RF                = kwargs.get("replication_factor",1)
        self.nodes             = kwargs.get("nodes",[] )
        self.compression_nodes = kwargs.get("compression_nodes",[])
        self.start_nodes       = kwargs.get("start_nodes",False)
        self.environment       = {"NODE_PORT":self.port,"NODE_ID":self.nodeId,"NODE_HOST":self.host,"LOAD_BALANCER":self.balancer,"REPLICATION_FACTOR":self.RF}
        self.generateNodesEnviroment()
        self.generateCompressionEnviroment()
    def __runNodes(self,client):
        for node in self.nodes+self.compression_nodes:
            node.run(client)
            #L.debug("Storage node[{}] successfully launched".format(node.nodeId))

    def generateCompressionEnviroment(self):
        attrs   = ["node-id","url"] 
        for i,node in enumerate(self.compression_nodes):
            data = {}
            key  = "COMPRESSION_NODES.{}.{}".format(i,attrs[0])
            data[key]=node.nodeId
            key  = "COMPRESSION_NODES.{}.{}".format(i,attrs[1])
            data[key]=node.url
            self.environment = {**self.environment,**data}
    
    def generateNodesEnviroment(self):
        attrs   = ["node-id","url"] 
        for i,node in enumerate(self.nodes):
            data = {}
            key  = "NODES.{}.{}".format(i,attrs[0])
            data[key]=node.nodeId
            key  = "NODES.{}.{}".format(i,attrs[1])
            data[key]=node.url
            self.environment = {**self.environment,**data}

    def run(self,client):
        port = {}
        port[self.port]=self.port
        container = client.containers.create(
                self.DOCKER_IMAGE,
                detach     = self.detach,
                ports      = port,
                environment = self.environment,
                labels     = {"pool":""},
                name       = self.nodeId
        )
        net = client.networks.get(self.net)
        net.connect(container,ipv4_address=self.ip)
        container.start()
        self.__runNodes(client)
