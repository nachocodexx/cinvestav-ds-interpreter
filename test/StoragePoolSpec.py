import unittest 
import sys
from unittest import TestCase
sys.path.append('/home/nacho/Programming/Docker/CDS/cinvestav-ds-interpreter/')
from storage_pool import StoragePool
from storage_node import StorageNode
from metadata_node import MetadataNode
from compression_node import CompressionNode
from metadata_node import MetadataNode
from result_node import ResultNode
from _utils import createCompressionNode,createStorageNode,createNodes,createStoragePool,createMetadataNodes,runNodes
import docker
client = docker.from_env()



class StoragePoolSpec(TestCase):
    def show_sp_info(self,sps):
        for sp in sps:
            print("ENVIROMENT: ",sp.environment)
            print("IP ADDRESS: ",sp.ip)
            print("PORT: ",sp.port)
            print("-"*100)

    @unittest.skip("")
    def test_compression(self):
        cp000 = CompressionNode("cp-000",ip="166.0.1.2",port=6967,network="mynet2")
        cp000.run(client)
        
    @unittest.skip("")
    def test_storage_node(self):
        sn000 = StorageNode("sn-000",ip="166.0.1.1",port=6968,network="mynet2")
        print(sn000.environment)
        sn000.run(client)

    @unittest.skip("SKIPPED")
    def test_result(self):

        rs00 = ResultNode("rs-00",ip="166.0.63.200") 
        rs00.run(client)
        print(rs00.environment)
        self.assertTrue(True)

    #@unittest.skip("SKIPPED")
    def test_init(self):

        sp00 = createStoragePool(0,num_storage_nodes=5,num_compression_nodes=5,network="mynet2",replication_factor=3)
        sp01 = createStoragePool(1,num_storage_nodes=5,num_compression_nodes=5,network="mynet2",replication_factor=3)
        #sp02 = createStoragePool(3,num_storage_nodes=10,num_compression_nodes=10,network="mynet2",replication_factor=5)
        sps  = [sp00,sp01]
        self.show_sp_info(sps)
        # 
        mds = createMetadataNodes(3)

        runNodes(client,mds)
        runNodes(client,sps)

        self.assertEqual(1,1)


if __name__ == "__main__":
    unittest.main()
