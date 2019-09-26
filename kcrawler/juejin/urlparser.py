def decode_url(url):
    adr, query = url.split("?")
    params = { kv.split("=")[0]:kv.split("=")[1] for kv in query.split("&")}
    return adr, params

def encode_url(url, params):
    query = "&".join(["{}={}".format(k, v) for k, v in params.items()])
    return "{}?{}".format(url, query)

def get_juejin_url(uid, device_id, token, limit=20, targetUid=None):
    url = "https://timeline-merger-ms.juejin.im/v1/get_entry_by_self"
    if not targetUid:
        targetUid = uid
    params = {'src': 'web',
              'uid': uid,
              'device_id': device_id,
              'token': token,
              'targetUid': targetUid,
              'type': 'post',
              'limit': limit,
              'order': 'createdAt'}
    return encode_url(url, params)

def rebuild_juejin_url(url, **argkw):
    params = decode_url(url)[1]
    support_params = ('uid', 'device_id', 'token', 'limit', 'targetUid')
    rebuild_parmas = {}
    for k in support_params:
        rebuild_parmas[k] = params[k]
    for k, v in argkw.items():
        if v and (k in support_params):
            rebuild_parmas[k] = v
    return get_juejin_url(**rebuild_parmas)
