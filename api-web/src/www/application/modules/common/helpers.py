import os, ssl, urllib, urllib2, json
import  re


class KubernetesAPI(object):
    def __init__(self):
        self.cafile = '/opt/kubernetes/apiserver-ca.pem'
        self.keyfile = '/opt/kubernetes/apiserver-key.pem'
        self.crtfile = '/opt/kubernetes/apiserver-cert.pem'
        self.url = 'api.test.notasquare.vn'

    def GET(self, url, params = {}):
        ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        ctx.load_cert_chain(certfile=self.crtfile, keyfile=self.keyfile)
        ctx.load_verify_locations(cafile=self.cafile)
        res = urllib2.urlopen("https://" + self.url + "/" + url + "?" + urllib.urlencode(params), context=ctx)
        return res.read()

    def POST(self, url, data = {}):
        ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        ctx.load_cert_chain(certfile=self.crtfile, keyfile=self.keyfile)
        ctx.load_verify_locations(cafile=self.cafile)
        res = urllib2.Request("https://" + self.url + "/" + url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        res = urllib2.urlopen(res, context=ctx)
        return res.read()

    def DELETE(self, url, data = {}):
        ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        ctx.load_cert_chain(certfile=self.crtfile, keyfile=self.keyfile)
        ctx.load_verify_locations(cafile=self.cafile)
        res = urllib2.Request("https://" + self.url + "/" + url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        res.get_method = lambda: 'DELETE'
        res = urllib2.urlopen(res, context=ctx)
        return res.read()


def parse(value, index):
    # value = *, 1, '12,12', '2-2'
    list_pattern = [{'pattern': re.compile(r'(\*{1}$)'), 'type': 'any'},  # any value
                    {'pattern': re.compile(r'([0-9]{1,2}$)'), 'type': 'distance'},  #
                    {'pattern': re.compile(r'([0-9]{1,2})\,([0-9]{1,2})'), 'type': 'value_list'}, # value list separator
                    {'pattern': re.compile(r'([0-9]{1,2})\-([0-9]{1,2})'), 'type': 'range_list'}  # range of values
                    ]
    if index == len(list_pattern):
        return False
    result = re.match(list_pattern[index]['pattern'], value)
    if result:
        if index in [0, 1]:
            if result.groups()[0] == '*':
                return {'type': list_pattern[index]['type'], 'value': result.groups()[0]}
            else:
                return {'type': list_pattern[index]['type'], 'value': int(result.groups()[0])}
        return {'type': list_pattern[index]['type'], 'value': [int(i) for i in result.groups()]}
    # fibonacci
    return parse(value, index + 1)
