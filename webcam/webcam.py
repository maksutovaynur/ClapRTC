import asyncio
import json
import os
import platform
import fileinput
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

ROOT = os.path.dirname(__file__)


async def offer(stri):
    print("Enter offer")
    params = json.loads(stri)
    offer = RTCSessionDescription(
        sdp=params['sdp'],
        type=params['type'])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on('iceconnectionstatechange')
    async def on_iceconnectionstatechange():
        print('ICE connection state is %s' % pc.iceConnectionState)
        if pc.iceConnectionState == 'failed':
            await pc.close()
            pcs.discard(pc)

    print("Before webcam")

    # open webcam
    options = {'framerate': '30', 'video_size': '640x480'}
    if platform.system() == 'Darwin':
        player = MediaPlayer('default:none', format='avfoundation', options=options)
    else:
        player = MediaPlayer('/dev/video0', format='v4l2', options=options)

    print("Webcam configured")

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == 'audio' and player.audio:
            pc.addTrack(player.audio)
        elif t.kind == 'video' and player.video:
            pc.addTrack(player.video)

    print("Tracks configured")

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    print("Made SDP answer")

    print(json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }))






pcs = set()


async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()



from aiohttp import web


if __name__ == '__main__':
    stri = input("Enter sdp offer from javascript\n")
    print("Taken sdp offer")
    asyncio.get_event_loop().run_until_complete(offer(stri))
    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=8080, ssl_context=None)
    # asyncio.get_event_loop().run_until_complete(on_shutdown())