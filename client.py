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
        
        ix = []
        i = 0
        
        while True:
            resp = s.recv(32000).decode("utf-8").split('\r\n\r\n')
            if resp == [""]:
                break
            if len(resp) > 1:
                ix.append(resp[1])
            elif i >= 2:
                if len(ix) >= 1:
                    ix[0] += resp[0]
                else:
                    ix.append(resp[0])
            i += 1

        ix_json = json.loads(ix[0])

        all_net_ids = []
        net_ix_lan_by_ixId = {}
        net_id_sum = {}

        # get net ids
        for item in ix_json:
            s = close_open_socket(s, ip, port)
            s.send(("GET /api/ixnets/{0}/ HTTP/1.1\r\n\r\n".format(item)).encode("utf-8"))
            
            net_ix_lan = []
            i = 0
            
            while True:
                resp = s.recv(32000).decode("utf-8").split('\r\n\r\n')
                if resp == [""]:
                    break
                if len(resp) > 1:
                    net_ix_lan.append(resp[1])
                elif i >= 2:
                    if len(net_ix_lan) >= 1:
                        net_ix_lan[0] += resp[0]
                    else:
                        net_ix_lan.append(resp[0])
                i += 1
            
            net_ix_lan_json = json.loads(net_ix_lan[0])
            net_ix_lan_by_ixId[item] = net_ix_lan_json
            
            for item in net_ix_lan_json:
                if item["net_id"] not in all_net_ids:
                    all_net_ids.append(item["net_id"])
                if item["net_id"] in net_id_sum.keys():
                    net_id_sum[item["net_id"]] += 1
                elif item["net_id"] not in net_id_sum.keys():
                    net_id_sum[item["net_id"]] = 1
            
        for item in all_net_ids:
            s = close_open_socket(s, ip, port)
            s.send(("GET /api/netname/{0}/ HTTP/1.1\r\n\r\n".format(item)).encode("utf-8"))
            
            net_names = []
            i = 0

            while True:
                resp = s.recv(1024).decode("utf-8").split('\r\n\r\n')
                if resp == [""]:
                    break
                if len(resp) > 1:
                    net_names.append(resp[1])
                elif i >= 2:
                    if len(net_names) >= 1:
                        net_names[0] += resp[0]
                    else:
                        net_names.append(resp[0])
                i += 1

            net_names_json = json.loads(net_names[0])
            #print(str(item) + ' ' + net_names_json)
            if item not in net_id_sum.keys():
                print(str(item) + '\t' + net_names_json + '\t' + '0')
            else:
                print(str(item) + '\t' + net_names_json + '\t' + str(net_id_sum[item]))

    ##### OPT 2 #####
    elif Opt is 2:
        s = close_open_socket(s, ip, port)
        s.send("GET /api/ix HTTP/1.1\r\n\r\n".encode("utf-8"))
        all_ixs = []
        i = 0
        all_net_ids = []
        while True:
            resp = s.recv(1024).decode("utf-8")
            if resp == "":
                break
            elif i > 2:
                all_ixs[2] += resp
            else:
                all_ixs.append(resp)
            i += 1

        all_ixs_json = json.loads(all_ixs[2])
        ix_names = []

        for item in all_ixs_json:
            i = 0

            s = close_open_socket(s, ip, port)
            s.send(("GET /api/ixnets/{0}/ HTTP/1.1\r\n\r\n".format(item["id"])).encode("utf-8"))
            
            ixnets = []
            i = 0
            
            while True:
                resp = s.recv(32000).decode("utf-8").split('\r\n\r\n')
                
                if resp == [""]:
                    break
                if len(resp) > 1:
                    ixnets.append(resp[1])
                elif i >= 2:
                    if len(ixnets) >= 1:
                        ixnets[0] += resp[0]
                    else:
                        ixnets.append(resp[0])
                i += 1
            
            ixnets_json = json.loads(ixnets[0])
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