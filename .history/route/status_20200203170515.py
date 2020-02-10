from datetime import datetime
import falcon
from marshmallow import fields, Schema
import uuid

class StatusResponseSchema(Schema):
    id = fields.String()
    agents = fields.List(fields.String())
    alive = fields.DateTime()


class Status(object):
    response_schema = StatusResponseSchema()

    def __init__(self, cb_host, cb_port):
        self.data = {
            'id': uuid.uuid1())
            'agents': [],
            'alive': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        }

    def on_get(self, req, resp):
        req.context['result'] = self.data