import falcon

class CodeSchema(schema):
    cmds = fields.List(CmdSchema)

class Code(object):
    def __init__(self, status):
        self.status = status

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.__class__