from marshmallow import fields, Schema, validate
from schema.base import Base_Schema
from schema.software_definitions import SoftwareDefinition

STORAGE_TYPES = ["S3", "NFS", "iSCSI", "Swift", "CEPH", "GlusterFS", "SSH-FS"]


class ExternalStorageSchema(Base_Schema):
    id = fields.Str(required=True, example="a406874b-dea7-4cd1-9d4e-b82a18ec993b",
                    description="ID of this external Storage type")
    storageType = fields.Str(required=True, example="NFS", enum=STORAGE_TYPES,
                             description="Type of storage type.")
    description = fields.Str(required=False, example="remote nfs drive",
                             description="High level description for this remote storage drive")
    url = fields.Str(required=True, example="nfs://192.168.10.245:2049/data",
                     description="URL for this remote resource")


class InteractsWithSchema(Base_Schema):
    externalStorage = fields.List(fields.Nested(ExternalStorageSchema), required=False,
                                  description="External storage devices description")
    softwareArtifacts = fields.List(fields.Nested(SoftwareDefinition), required=False,
                                    description="Software artifacts interacting with this LCP")
