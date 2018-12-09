import json
import sys
from flask import Flask
app = Flask('TP3')

def main():
    #port = int(sys.argv[1])
    NetFile = open(sys.argv[1], "r")
    IxFile = open(sys.argv[3], "r")
    NetIxlanFile = open(sys.argv[4], "r")

    Netfile_data = Netfile.read()
    Netfile_json = json.loads(Netfile_data)
    print (Netfile_json.keys())

    # print (Netfile_json.values())
    print (Netfile_json["meta"])

    
    @app.route('/')
    def hello():
        return str(Netfile_json["data"])
        # 1) campo id do arquivo net.json
        # 2) campo name do arquivo net.json
        # numero IPX associado a rede - deve ser gerado pelo cliente


    @app.route("/api/ix") # IXPs por rede
    def all_ipx():
        return 'Hello'
    
    @app.route("/api/ixnets/<ix_id>") # Redes por IXP
    def id_redes_ixp():
       return True

    @app.route("/api/netname/<net_id>") # Nome da rede
    def rede_name():
       return True
    
    app.run(use_reloader=True)

if __name__ == "__main__":
    main()