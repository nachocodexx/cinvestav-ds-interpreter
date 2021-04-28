from node import Node
class ResultNode(Node):
    def __init__(self,nodeId,**kwargs):
        self.DOCKER_IMAGE    = "nachocode/cinvestav-ds-results"
        self.nodeId          = nodeId
        self.net             = kwargs.get("network","mynet2")
        self.ip              = kwargs.get("ip",None)
        self.host            = kwargs.get("host","0.0.0.0")
        self.port            = kwargs.get("port",6666)
        self.url             = "http://{}:{}/{}".format(self.ip,self.port,self.nodeId)
        self.result_filename = kwargs.get("result_filename","results.csv")
        self.result_path     = kwargs.get("result_path","/app/results")
        self.volume          = kwargs.get("volume","/home/nacho/Documents/test/results")+"/"+str(self.nodeId)
        self.detach          = True
        self.environment  = {
                "NODE_ID":self.nodeId,
                "NODE_PORT":self.port,
                "NODE_HOST":self.host,
                "RESULT_FILENAME":self.result_filename,
                "RESULT_PATH":self.result_path
                }
    def run(self,client):
        port                = {}
        port[self.port]     = self.port
        volume              = {}
        volume[self.volume] = {'bind':self.result_path,'mode':'rw'}
        container = client.containers.create(
                self.DOCKER_IMAGE,
                detach      = self.detach,
                ports       = port,
                environment = self.environment,
                labels      = {"results":""},
                name        = self.nodeId,
                volumes     = volume
        )
        net = client.networks.get(self.net)
        net.connect(container,ipv4_address=self.ip)
        container.start()
    def __str__(self):
        return "StorageNode({},{})".format(self.nodeId,self.url)

