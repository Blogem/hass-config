// based on script by Ich-Eben: https://github.com/dtcooper/raspotify/issues/171#issuecomment-507423901
// add this to /etc/default/raspotify: OPTIONS="--onevent 'node /home/homeassistant/.homeassistant/custom_components/raspotify/main.js'"
// install mqtt in same dir as this script: npm install mqtt --save

var mqtt = require('mqtt');
var client  = mqtt.connect('mqtt://localhost');

client.on('connect', function() {
        client.publish('raspotify/playEvent', process.env.PLAYER_EVENT);
        client.publish('raspotify/trackId', process.env.TRACK_ID);
        client.publish('raspotify/oldTrackId', process.env.OLD_TRACK_ID);
        client.end();
});
