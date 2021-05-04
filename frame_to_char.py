CHANNELS = 255 * 3
GROUPS = 3

MEDIUM_INT = 0.3
HARD_INT = 0.7
HARD, MEDIUM, SOFT = 'h', 'm', 's'


def get_conversion():
    return {
        'sss': ' ',
        'mmm': '#',
        'hhh': '@',

        'hss': '"',
        'hhs': 'T',
        'shs': '•',
        'shh': '„',
        'ssh': '_',
        'hsh': ';',

        'mss': '`',
        'mms': '~',
        'sms': '∙',
        'smm': '+',
        'ssm': '.',
        'msm': ':',

        'smh': '.',
        'hms': '\'',
        'hsm': '!',
        'msh': '*',
        'shm': '~',
        'mhs': '^',

        'mhm': '÷',
        'hhm': 'Ý',
        'hmm': '7',
        'mhh': '&',
        'mmh': '≡',
        'hmh': '$'
    }


def check_split(width, height, split):
    return not (width % split + height % split)


def convert_weight(weight):
    if weight > HARD_INT:
        return HARD
    elif weight > MEDIUM_INT:
        return MEDIUM
    return SOFT


def weights_to_ascii(weights):
    if len(weights) % GROUPS != 0:
        raise Exception(
            'weights len: %d can\'t be split into %d groups'
            % (len(weights), GROUPS)
        )

    if len(weights) != GROUPS:
        mult = int(len(weights) / GROUPS)
        weights = ''.join([weights[i * mult] for i in range(GROUPS)])

    return get_conversion()[weights]


def get_available_res(frame):
    available = []
    for i in range(2, max(frame.size)):
        if check_split(*frame.size, i):
            available.append(i)

    return available


def build_ascii(pixels, group_split=3):
    n = int(len(pixels) / group_split)
    grouparr = []
    asciiout = ''

    for group in range(group_split):
        start, stop = int(group * n), int(group * n + n)
        vertical = pixels[start: stop]
        merged = [0 for i in range(group_split)]
        for i in range(group_split):
            for j in range(n):
                psum = 0
                for k in range(n):
                    psum += vertical[j][i + k]
                merged[i] += psum / n ** 2
        grouparr.append(merged)
    for col in grouparr:
        out = ''.join([convert_weight(w) for w in col])
        asciiout += weights_to_ascii(out)

    return asciiout


def convert(frame, split=None):
    if not check_split(*frame.size, split):
        raise Exception('bad split: %d for framesize %d %d' % (split, *frame.size))

    width = int(frame.size[0] / split)
    height = int(frame.size[1] / split)

    out = ''

    for i in range(1, height):
        line = ''
        for j in range(1, width):
            blacks = []
            startx = j * split - (split)
            starty = i * split - (split)
            for k in range(1, split + 1):
                for l in range(1, split + 1):
                    px = startx + l
                    py = starty + k

                    pixval = sum(frame.getpixel((px, py))) / CHANNELS
                    blacks.append(pixval)

            black = sum(blacks) / (12 * split)

            rows = []
            for n in range(split):
                rows.append([blacks[(m * split) + n] for m in range(split)])

            line += build_ascii(rows)
        out += "%s\n" % line
    return out
