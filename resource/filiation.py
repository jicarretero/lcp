from docstring import docstring
from resource.base import Base_Resource
from marshmallow import ValidationError
from schema.response import Created_Response
from falcon import HTTP_NOT_ACCEPTABLE, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from lib.http import HTTP_Method
from utils.sequence import is_list, wrap
from schema.filiation import LCPSonDescription
import json
from lib.lcp_config import LCPConfig

__all__ = [
    'FiliationById',
    'Filiation'
]


class Filiation(Base_Resource):
    # data = {}
    tag = {'name': 'filiation', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/filiation',

    def __init__(self):
        pass

    @docstring(source='filiation/get.yaml')
    def on_get(self, req, resp):
        resp_Data, valid = LCPSonDescription(method=HTTP_Method.GET) \
           .validate(data={})
        child_nodes = LCPConfig().sons
        # for k in Filiation.data:
        #    child_nodes.append(Filiation.data[k])
        resp.body = json.dumps(child_nodes)

    @docstring(source="filiation/post.yaml")
    def on_post(self, req, resp):
        resp_Data, valid = LCPSonDescription(method=HTTP_Method.POST) \
            .validate(data={})
        payload = req.media if isinstance(req.media, list) else [req.media]
        cfg = LCPConfig()
        try:
            lcp = LCPSonDescription(many=True)
            lcp.load(payload)
            valid = lcp.validate(payload)
            for f in payload:
                cfg.setSon(f)
            resp.status = HTTP_CREATED
        except ValidationError as e:
            resp.status = HTTP_NOT_ACCEPTABLE
            print(e.messages)
            resp.body = json.dumps(e.messages)


class FiliationById(Base_Resource):
    tag = {'name': 'filiation', 'description': 'Describes a "son" LCP linked in this service chain.'}
    routes = '/filiation/{id}',

    def __init__(self):
        pass

    @docstring(source='filiation/get_by_id.yaml')
    def on_get(self, req, resp, id):
        resp_Data, valid = LCPSonDescription(method=HTTP_Method.GET) \
            .validate(data={}, id=id)
        cfg = LCPConfig()
        son = cfg.getSonById(id)

        if son is None:
            resp.status = HTTP_NOT_FOUND
        else:
            resp.body = json.dumps(son)

    @docstring(source='filiation/get.yaml')
    def on_delete(self, req, resp, id):
        resp_Data, valid = LCPSonDescription(method=HTTP_Method.DELETE) \
            .validate(data={}, id=id)
        cfg = LCPConfig()
        d = cfg.deleteSonById(id)
        if d is not None:
            resp.body = json.dumps(d)
            resp.status = HTTP_OK
        else:
            resp.status = HTTP_NOT_FOUND



