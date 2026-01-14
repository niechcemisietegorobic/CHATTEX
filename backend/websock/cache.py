from glide_sync import NodeAddress, GlideClusterClientConfiguration, GlideClusterClient, ClusterScanCursor

def init_glide():
    addresses = [
        NodeAddress("chattex-sessions-dev-vpx3rr.serverless.use1.cache.amazonaws.com", 6379)
    ]
    config = GlideClusterClientConfiguration(addresses=addresses, use_tls=True)
    glide_client = GlideClusterClient.create(config)
    return glide_client

cache: GlideClusterClient = init_glide()

def get_all_keys():
    cursor = ClusterScanCursor("0")
    all_keys = []
    while True:
        cursor, keys = cache.scan(cursor)
        all_keys.extend(keys)
        if cursor.get_cursor() == b"0":
            break
    return all_keys

def get_all_key_values():
    keys = get_all_keys()
    result = {}
    for key in keys:
        value = cache.get(key)
        result[key.decode()] = value.decode() if value else None
    return result
