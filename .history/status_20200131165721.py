import falcon

class Status(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        print(resp)
        resp.body = 'Ciao'