import json

def split_reqrsp(file):
    f = open(file,"r",encoding='utf-8')
    http_bag = f.read()
    split = http_bag.strip().split("\n\n")
    return split

def http_to_dict(split):
    split = split_reqrsp('http.txt')
    main_dict = {}
    main_dict['src_port']=555
    main_dict['dst_ip']='42.13.226.31'
    main_dict['dst_port']=80
    main_dict['req_head']=split[0]
    main_dict['req_body']=split[1]
    main_dict['rsp_head']=split[2]
    main_dict['rsp_body']=split[3]
    # print(split[0])
    #请求
    split[0] = split[0].strip().split('\n')
    req_headers_dict = {x.split(':')[0].strip():("".join(x.split(':')[1:])).strip().replace('//',"://")for x in split[0]}
    # print(req_headers_dict)
    #req_ct
    if('Content-Type' in req_headers_dict):
        main_dict['req_ct'] = req_headers_dict['Content-Type']
    else:
        main_dict['req_ct'] = ""
    # method
    req_headers_key = list(req_headers_dict.keys())
    fst_line = req_headers_key[0].split(" ")
    main_dict['method']=fst_line[0]
    # api_endpoint
    apiurl = fst_line[1].split("?")
    main_dict['api_endpoint'] = req_headers_dict['Host']+ apiurl[0]
    #domain_url
    main_dict['domain_url'] = req_headers_dict['Host']+fst_line[1]
    #响应
    split[2] = split[2].strip().split('\n')
    rsp_headers_dict = {x.split(':')[0].strip():("".join(x.split(':')[1:])).strip().replace('//',"://")for x in split[2]}
    # print(rsp_headers_dict)
    #rsp_ct
    if('Content-Type' in rsp_headers_dict):
        main_dict['rsp_ct'] = rsp_headers_dict['Content-Type']
    else:
        main_dict['rsp_ct'] = ""
    #status_code
    rsp_headers_key = list(rsp_headers_dict.keys())
    fst_line = rsp_headers_key[0].split(" ")
    main_dict['status_code'] = fst_line[1]

    return main_dict

def  set_srcip_ts(main_dict,num):
    # single_dict = main_dict
    i = 0
    first_ip = 1
    first_ts = 1638372877000
    while i < num:
        main_dict['src_ip'] = first_ip + i
        main_dict['ts'] = first_ts + (i+1)*30
        i = i + 1
        main_json = json.dumps(main_dict)
        with open('test_data.json', 'a+') as json_file:
            json_file.write(main_json + '\n')

if __name__ == '__main__':
    split = split_reqrsp('http.txt')
    main_dict = http_to_dict(split)
    set_srcip_ts(main_dict,100)

    # print(main_dict)