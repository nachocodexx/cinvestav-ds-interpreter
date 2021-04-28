import logging as L 
import docker
from storage_node import StorageNode
from storage_pool import StoragePool
from compression_node import CompressionNode
client = docker.from_env()
L.basicConfig(format='[%(levelname)s]: %(message)s',level=L.DEBUG)

if __name__ == "__main__":
    STORAGE_NODES_NUM = 3
    cp00          = CompressionNode("cp-00",port=3000,ip="10.0.0.100")
    #cp00.run(client)
    #print(cp00)

  #  storage_nodes = list(map(createStorageNode,range(STORAGE_NODES_NUM)))
   # print(storage_nodes)
    #sp00  = StoragePool("sp-00",ip="10.0.0.100",port=5000,nodes=storage_nodes)
    #sp00.run(client)
