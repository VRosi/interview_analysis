import re

for file_name in ['one.txt', 'second.txt']:
    print (file_name)
    with open(file_name) as f:
        content = f.read()
        items = re.split(r'\s{2,}(?:&nbsp;\s)*', content)
        print (items)
        results = {}
        results['Goodsign:'] = ' '.join(items[1: items.index('Bad Omen:')])
        results['Bad Omen:'] = ' '.join(items[1+items.index('Bad Omen:'): items.index('Dusk Attack:')])
        results['Dusk Rest:'] = ' '.join(items[1+items.index('Dusk Attack:'):])
        results['Dusk Attack:'] = ' '.join(items[1+items.index('Dusk Attack:'): items.index('Dusk Rest:')])
        results['Dusk Rest:'] = ' '.join(items[1+items.index('Dusk Rest:'):])
        for result in results:
            print (result, results[result])
