from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import BaremetalServer, Disk, DiskPartition
from resource.hardware_definitions import BaremetalServer as BaremetalServerResource
import json
import os
from test_utils import *
from utils.log import Log  # noqa: E402
from test.testbase import LCPTestBase


class TestMyApp(LCPTestBase):
    def _getBaremetalServer(self):
        json_file = os.path.dirname(
            __file__) + "/examples/bare-metal-server-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    def test_baremetal_server(self):
        server = loadExampleFile("bare-metal-server-example.json")
        bm_server = BaremetalServer(many=False)
        try:
            d = bm_server.load(server)
            print(d)
            assert (True)
        except ValidationError as ve:
            print(ve)
            assert (False)

        """ dict_disk_partitions =self._getTestingPartitionsHD2()
        valid = dp.validate(dict_disk_partitions)
        assert(valid)

        dp = DiskPartition(many=False)
        dict_disk_partitions =self._getTestingPartitionsHD1()
        valid = dp.validate(dict_disk_partitions)
        assert(valid)

        disk_partition = dp.dumps(dict_disk_partitions)

        dsk = Disk()
        dict_disk = self._getTestingDiskHD1()
        valid = dsk.validate(dict_disk)
        assert(valid)
        disk = dsk.dumps(dict_disk) #disk es str!!
        print(disk)"""

    def test_chk(self):
        # bm_server = self._getBaremetalServer()
        bm_server = loadExampleFile("bare-metal-server-example.json")
        diskDevices = bm_server['diskDevices']

        d = {"size": 143.24, "type": "ext4", "name": "/dev/nvme0n1p6"}
        print("Load: ", d)
        # , "size": 0.26, "type": "ext4"}
        DiskPartition().load(d)

        for device in diskDevices:
            try:
                dsk = Disk()
                dsk.load(device)
                print("OK: ", device)
            except ValidationError as ve:
                print("DEV: ", device['diskPartitions'][0])
                DiskPartition().load(device['diskPartitions'][0])
                print(device)
                print(ve)

    def test_get_baremetal_server(self):
        bm_server = loadExampleFile("bare-metal-server-example.json")
        headers = getAuthorizationHeaders()
        BaremetalServerResource.data = []

        result = self.simulate_get("/baremetal", headers=headers)
        print(result.status)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 0

        BaremetalServerResource.update_data(bm_server)
        result = self.simulate_get("/baremetal", headers=headers)
        assert (result.status == "200 OK")
        body = result.json
        assert (type(body) is list)
        assert len(body) == 1

        try:
            bm_schema = BaremetalServer(many=True)
            bm_schema.load(body)
            assert True
        except ValidationError as ve:
            print(ve)
            assert False

    def test_post_baremetal_server(self):
        bm_server_dict = loadExampleFile("bare-metal-server-example.json")
        headers = getAuthorizationHeaders()
        BaremetalServerResource.data = []

        body = json.dumps(bm_server_dict)
        result = self.simulate_post("/baremetal", headers=headers,
                                    body=body)
        assert result.status_code == 201
        assert len(BaremetalServerResource.data) == 1
        assert BaremetalServerResource.data[0]["id"] == bm_server_dict["id"]
