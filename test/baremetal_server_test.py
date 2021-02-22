from falcon import testing
from api import api
from reader.arg import Arg_Reader
from about import project, title, version
from marshmallow.exceptions import ValidationError
from schema.hardware_definitions import BaremetalServer, Disk, DiskPartition
import json
import os


class BaremetalServerTesting(testing.TestCase):
    def setUp(self):
        super(BaremetalServerTesting, self).setUp()
        self.db = Arg_Reader.read()
        self.app = api(title=title, version=version,
                       dev_username=self.db.dev_username, dev_password=self.db.dev_password)


class TestMyApp(BaremetalServerTesting):
    def _getBaremetalServer(self):
        json_file = os.path.dirname(
            __file__) + "/examples/bare-metal-server-example.json"
        with open(json_file) as f:
            file_data = f.read()
        return json.loads(file_data)

    def test_baremetal_server(self):
        server = self._getBaremetalServer()
        bm_server = BaremetalServer(many=False)
        try:
            d = bm_server.load(server)
            print(d)
            assert(True)
        except ValidationError as ve:
            print(ve)
            assert(False)

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
        bm_server = self._getBaremetalServer()
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
