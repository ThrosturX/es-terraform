# TODO: Take commodity information and make them into events

# event "colonize <aoeu>"
#     government Independent
#     system "<aoeu>"
#     trade *

def create_planet_event(name):
    result = """planet "{0}"
		remove attributes "colonizable"
		add attributes "colonized"
		spaceport `The spaceport is nothing more than a large platform with a couple of tents and some crates and containers`"""
    return result.format(name)

def create_system_event(system, commodities, planets, new_govt):
    def format_trades(trades):
        return '\n\t\t'.join(['trade "{0}" {1}'.format(k, v) for k, v in trades.items()])

    trades = format_trades(commodities)
    p_events = '\n'.join([create_planet_event(x) for x in planets])
    result = \
    """event "colonize {0}"
	system "{0}"
		government "{1}"
		{2}
	{3}
\n""".format(
        system,
        new_govt,
        format_trades(commodities),
        p_events
    )
    print(result)
    return result

class SystemEventReader():
    def __init__(self):
        self.systems = {}
        self.system = None
        self.commodities = {}
        self.colonizable_planets = []

    def read(self, line):
        if line.startswith('system'):
            self.system = line.split(' ', 1)[1]
            return None
        elif line.startswith('\ttrade'):
            parts = line.split(" ")
            np = len(parts)
            key = parts[1]
            value = parts[2]
            if np == 4:
                key = parts[1] + ' ' + parts[2]
                value = parts[3]
            self.commodities[key] = value

        elif line.startswith('\tobject'):
            parts = line.split(' ', 1)
            if len(parts) <= 1:
                return None
            self.colonizable_planets.append(parts[1])

        if not line:
            sys = self.system
            self.systems[sys] = create_system_event(
                sys, self.commodities,
                self.colonizable_planets,
                'Independent'
            )
            self.system = None
            self.commodities = {}
            self.colonizable_planets = []
            return sys

        return None


old_map = ''
new_map = ''
events = ''

def skipper(line):
    bad_starts = [
        '\ttrade',
        '\tspaceport'
    ]
    for bad_start in bad_starts:
        if line.startswith(bad_start):
            return True
    return False

sr = SystemEventReader()
with open('data/map.txt', 'r') as mf:
    commodities = []
    for line in mf:
        sr.read(line.strip('\n'))

        if skipper(line):
            continue

        new_map += line

with open('data/colonization_events.txt', 'w') as ef:
    for key, value in sr.systems.items():
        if not key:
            continue

        ef.write(value)

with open('data/new_map.txt', 'w') as mf:
    mf.write(new_map)
