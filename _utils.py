from storage_node import StorageNode
from compression_node import CompressionNode
from storage_pool import StoragePool
from metadata_node import MetadataNode
def createNodes(i,N,fn,**kwargs):
    return list(map(lambda x:fn(*x,**kwargs),zip(range(N),[i]*N)))

def createMetadataNodes(N):
    def __fn(i):
        index  = "{:03d}".format(i)
        nodeId = "md-{}".format(index)
        port   = 40000+i
        ip     = "166.0.63.{}".format(i)
        return MetadataNode(nodeId,port=port,ip=ip,network="mynet2")
    nodes = list(map ( __fn ,range(N)) )
    return nodes
def runNodes(client,nodes):
    for n in nodes:
        n.run(client)


def createStorageNode(i,j,**kwargs):
    spIndex = kwargs.pop("spIndex")
    index  = str(spIndex)+"{:02d}".format(i)
    _index  = "{:03d}".format(i+1)

    nodeId = "sn-{}".format(index)
    port   = int("{}{}".format(3+j,_index  ))
    ip     = "166.0.{}.{}".format(j+1,i+2)
    return StorageNode(nodeId,ip=ip,port=port,**kwargs)


def createCompressionNode(i,j,**kwargs):
    spIndex = kwargs.pop("spIndex")
    index  = str(spIndex)+"{:02d}".format(i)
    nodeId = "cp-{}".format(index)
    port   = int("{}{}".format(3+j,i+500))
    ip     = "166.0.{}.{}".format(j+2,i)
    return CompressionNode(nodeId,port=port,ip=ip,**kwargs)

def createStoragePool(i,**kwargs):
    n      = kwargs.pop("num_storage_nodes",1)
    m      = kwargs.pop("num_compression_nodes",1)
    kwargs['spIndex']=i
    _index = (i*2) 
    index  = "{:03d}".format(i)
    nodeId = "sp-{}".format(index)
    port   = int("{}{}".format(3+i,index ))
    ip     = "166.0.{}.0".format( _index+1)
    sns    = createNodes(_index,n,createStorageNode, **kwargs )
    cps    = createNodes(_index,m,createCompressionNode,**kwargs )
    return StoragePool(nodeId,port=port,ip=ip,nodes=sns,compression_nodes=cps,**kwargs)


