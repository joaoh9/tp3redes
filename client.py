import json
import sys
import socket

def close_open_socket(s, ip, port):
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def request_netId(s, ixpId):
    request = ("'GET /api/nixnets/{0} HTTP/1.1\r\n\r\n'".format(ixpId))
    s.send(request.encode("utf-8"))
    return s

def main():
    ip_port = sys.argv[1].split(':')
    ip = ip_port[0]
    port = int(ip_port[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    Opt = int(sys.argv[2])

    if Opt is 1:
        s.send("GET /api/ix HTTP/1.1\r\n\r\n".encode("utf-8"))

        ix = ""

        while True:
            resp = s.recv(1024).decode("utf-8")
            if resp == "":
                break
            ix += resp
        ix = ix.split('\r\n\r\n')

        ix_json = json.loads(ix[1])
        
        all_net_ids = []
        netIxLan_by_ixId = {}
        net_id_sum = {}

        # get net ids
        for item in ix_json:
            ix_id = item["id"]
            s = close_open_socket(s, ip, port)
            s.send(("GET /api/ixnets/{0}/ HTTP/1.1\r\n\r\n".format(ix_id)).encode("utf-8"))
            
            netIxLan = ""
            
            while True:
                resp = s.recv(1024).decode("utf-8")
                if resp == "":
                    break
                netIxLan += resp
            netIxLan = netIxLan.split('\r\n\r\n')

            netIxLan_json = json.loads(netIxLan[1])
            netIxLan_by_ixId[ix_id] = netIxLan_json
            
            for netIxLan in netIxLan_json:
                net_id = netIxLan["net_id"]
                ix_id = netIxLan["ix_id"]
                if net_id not in net_id_sum.keys():
                    net_id_sum[net_id] = {'count': 1, 'ix_ids': [ix_id]}
                elif ix_id not in net_id_sum[net_id]['ix_ids']:
                    net_id_sum[net_id]['count'] += 1
                    net_id_sum[net_id]['ix_ids'].append(ix_id)

        for netId in net_id_sum.keys():
            s = close_open_socket(s, ip, port)
            s.send(("GET /api/netname/{0}/ HTTP/1.1\r\n\r\n".format(netId)).encode("utf-8"))
            
            net_names = ""

            while True:
                resp = s.recv(1024).decode("utf-8")
                if resp == "":
                    break
                net_names += resp
            net_names = net_names.split('\r\n\r\n')

            net_names_json = json.loads(net_names[1])
            
            if netId not in net_id_sum.keys():
                print(str(netId) + '\t' + net_names_json.replace('"','') + '\t' + '0')
            else:
                print(str(netId) + '\t' + net_names_json.replace('"','') + '\t' + str(net_id_sum[netId]['count']))

    ##### OPT 2 #####
    elif Opt is 2:
        s = close_open_socket(s, ip, port)
        s.send("GET /api/ix HTTP/1.1\r\n\r\n".encode("utf-8"))
        
        all_ixs = ""
        
        while True:
            resp = s.recv(1024).decode("utf-8")
            if resp == "":
                break
            all_ixs += resp
        all_ixs = all_ixs.split('\r\n\r\n')

        all_ixs_json = json.loads(all_ixs[1])
        ix_names = []

        for item in all_ixs_json:
            s = close_open_socket(s, ip, port)
            s.send(("GET /api/ixnets/{0}/ HTTP/1.1\r\n\r\n".format(item["id"])).encode("utf-8"))
            
            ixnets = ""
            
            while True:
                resp = s.recv(1024).decode("utf-8")
                if resp == "":
                    break
                ixnets += resp
            ixnets = ixnets.split('\r\n\r\n')

            ixnets_json = json.loads(ixnets[1])
            different_nets = []

            for ixn in ixnets_json:
                if ixn["net_id"] not in different_nets:
                    different_nets.append(ixn["net_id"])

            print(str(item["id"]) + '\t' + item["name"] + '\t' + str(len(different_nets)))

        
    else:
        print('Número de análise incorreto')

    s.close()
    
if __name__ == "__main__":
    main()