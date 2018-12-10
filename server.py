import json
import sys
from flask import Flask, Response
import socket

app = Flask('TP3')

def main():
    port = int(sys.argv[1])

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(('127.0.0.1', port))

    NetFile = open(sys.argv[2], "r")
    Net_data = NetFile.read()
    Net_json = json.loads(Net_data)
    
    IxFile = open(sys.argv[3], "r")
    Ix_data = IxFile.read()
    Ix_json = json.loads(Ix_data)

    NetIxLanFile = open(sys.argv[4], "r")
    NetIxLan_data = NetIxLanFile.read()
    NetIxLan_json = json.loads(NetIxLan_data)
    
    output = open("out.json", "w")
    
    @app.route("/api/ix", methods = ['GET']) # IXPs por rede
    def all_ipx():
        data = Ix_json["data"]
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    
    @app.route("/api/ixnets/<int:ix_id>/", methods = ['GET']) # Redes por IXP
    def id_redes_ixp(ix_id):
        todas_redes = []
        exists = False
        for item in NetIxLan_json["data"]:
            if item["ix_id"] == ix_id:
                todas_redes.append(item)

        js = json.dumps(todas_redes)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Size_of_payload'] = sys.getsizeof(js)
        return resp

    @app.route("/api/netname/<int:net_id>/", methods = ['GET']) # Nome da rede
    def rede_name(net_id):
        for item in Net_json["data"]:
            if item["id"] == net_id:
                name = json.dumps(item["name"])
                break
        
        js = json.dumps(name)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Size_of_payload'] = sys.getsizeof(js)
        return resp

    app.run(use_reloader=True )



if __name__ == "__main__":
    main()