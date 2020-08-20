map_old = ''
with open('data/map.txt', 'r') as mf:
    map_old = mf.read()

new_map = map_old.replace('government "Republic"', 'government "Uninhabited"')
new_map = new_map.replace('description', 'attributes colonizable\n\tdescription')

with open('data/map.txt', 'w') as mf:
    mf.write(new_map)
