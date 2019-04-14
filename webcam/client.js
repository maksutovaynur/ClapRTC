var pc = new RTCPeerConnection({
    sdpSemantics: 'unified-plan'
});

// connect audio / video
pc.addEventListener('track', function(evt) {
    if (evt.track.kind == 'video') {
        document.getElementById('video').srcObject = evt.streams[0];
    } else {
        document.getElementById('audio').srcObject = evt.streams[0];
    }
});

function negotiate() {
    pc.addTransceiver('video', {direction: 'recvonly'});
    pc.addTransceiver('audio', {direction: 'recvonly'});
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        sdp_offer = JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
            });
        alert(sdp_offer);
        var sdp_answer = prompt("Enter sdp answer", "<sdp_answer>");
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert(e);
    });
}

function start() {
    document.getElementById('start').style.display = 'none';
    negotiate();
    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';

    // close peer connection
    setTimeout(function() {
        pc.close();
    }, 500);
}
