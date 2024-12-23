'use strict';

const a = document.createElement('canvas');
document.body.appendChild(a);
a.width = innerWidth;
a.height = innerHeight;
const c = a.getContext("2d");
const d = document;

const zzfxR = 44100;

let brightness, i, frame, rand, lightning, mouseX, zzfxX, zzfx;

zzfxX = new (window.AudioContext || webkitAudioContext);
zzfx = e => {
    let PI2 = Math.PI * 2,
        b = [], i = 0, c = 0, s = 0, length, buffer, source,
        volume = e ? .1 + rand(.2) : .02,
        attack = 3,
        decay = 0,
        sustain = 0,
        release = 3,
        bitCrush = .05 + rand(.05),
        delay = .2 + rand(.2),
        sustainVolume = 1;

    if (e == 1) {
        attack = .1;
        decay = .1;
        sustain = rand();
        release = 3 + rand(2);
        sustainVolume = .5;
        bitCrush = .5 + rand(1);
        delay = .3 + rand(.5);
    }

    attack *= zzfxR;
    decay *= zzfxR;
    sustain *= zzfxR;
    release *= zzfxR;
    delay *= zzfxR;

    for (length = attack + decay + sustain + release + delay | 0;
        i < length; b[i++] = s) {
        if (!(++c % (bitCrush * 100 | 0))) {
            s = Math.random();

            s = s *
                volume * (
                    i < attack ? i / attack :
                        i < attack + decay ?
                            1 - ((i - attack) / decay) * (1 - sustainVolume) :
                            i < attack + decay + sustain ?
                                sustainVolume :
                                i < length - delay ?
                                    (length - i - delay) / release *
                                    sustainVolume :
                                    0);

            s = delay ? s / 2 + (delay > i ? 0 :
                (i < length - delay ? 1 : (length - i) / delay) *
                b[i - delay | 0] / 2) : s;
        }
    }

    buffer = zzfxX.createBuffer(1, length, zzfxR);
    buffer.getChannelData(0).set(b);
    source = zzfxX.createBufferSource();
    source.buffer = buffer;
    source.connect(zzfxX.destination);
    source.start();
    return source;
}

rand = (r = 1) => Math.random() * r;
lightning = (X, Y, V, Z) => c.fillRect(X, Y, Z, Z,
    rand(99) > 98 && Z > 9 && lightning(X, Y, V, rand(Z * .8) + 2),
    Y < a.height && lightning(X + V * Z / 9, Y + Z / 4, rand(99) > 95 ? rand(8) - 4 : V, Z));

brightness = frame = mouseX = 0;

setInterval(_ => {
    c.globalCompositeOperation = 'source-over';
    if (frame)
        c.fillStyle = `hsl(240,30%,${brightness -= 3}%,.1`;

    ++frame % 60 || zzfx();

    if (a.width != innerWidth || a.height != innerHeight) {
        a.width = innerWidth;
        a.height = innerHeight;
    }

    c.fillRect(0, 0, a.width, a.height);

    c.rotate(-.1);
    for (i = 2e3; i--; c.fillStyle = '#fff5')
        c.fillRect(Math.sin(i * i) * a.width + a.width / 2, (2e3 + i) / 2 * (frame / 60 + 9) % (a.height * 2), Math.sin(i), i % 9 - 40);
    c.rotate(.1);

    c.globalCompositeOperation = 'screen';
    c.fillStyle = '#8bf5';
    if (mouseX || rand() < .004 && brightness < 0) {
        brightness = 80 + rand(20);
        lightning(mouseX || rand(a.width), 0, 0, rand(19) + 9);
        zzfx(1);
        mouseX = 0;
    }

    onmousedown = e => mouseX = e.x;
}, 16);
