import asyncio
from riot_api import get_tournament_schedule, get_clash_time
path_to_api = 'key'
port = 1488
key = open(path_to_api).read()


async def handle_client(reader, writer):
    request = (await reader.read(255)).decode('utf8')
    split_request = request.split()
    val_req = ' '.join(split_request[0:3])
    if (len(val_req) < 3) or (val_req not in valid_requests.keys()):
        response = 'Error: Not a valid request - ' + val_req
    else:
        response = valid_requests[val_req](split_request, key)
        if not response.valid:
            response = 'Error: ' + response.text
        else:
            response = response.text
    writer.write(response.encode('utf8'))
    await writer.drain()
    writer.close()


valid_requests = {'get tournament schedule': get_tournament_schedule, 'get clash time': get_clash_time}
loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 1488))
loop.run_forever()
