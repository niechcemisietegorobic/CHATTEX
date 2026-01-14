from glide import NodeAddress, GlideClusterClientConfiguration, GlideClusterClient, ServerCredentials
import asyncio

def init_glide():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    addresses = [
        NodeAddress("chattex-sessions-dev-vpx3rr.serverless.use1.cache.amazonaws.com", 6379)
    ]
    config = GlideClusterClientConfiguration(addresses=addresses, use_tls=True)
    glide_client = loop.run_until_complete(
       GlideClusterClient.create(config)
    )
    return glide_client

cache: GlideClusterClient = init_glide()

async def get_all_keys():
    cursor = "0"
    all_keys = []
    while True:
        cursor, keys = await cache.scan(cursor)
        all_keys.extend(keys)
        if cursor == b"0":
            break
    return all_keys

async def get_all_key_values():
    keys = await get_all_keys()
    result = {}
    for key in keys:
        value = await cache.get(key)
        result[key.decode()] = value.decode() if value else None
    return result
