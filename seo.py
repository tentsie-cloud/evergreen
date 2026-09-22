"""Shared metadata and factual structured data; no ratings, prices or stock claims."""
import json
from html import escape

def metadata(config, title, description, path, page_schema=None):
    base = config['site_url'].rstrip('/')
    url = base + path
    is_error = path == '/404.html'
    image = base + '/assets/evergreen-nursery-social.jpg'
    business_id = base + '/#business'
    business = {
        '@type': 'GardenStore', '@id': business_id,
        'name': config['business_name'], 'url': base + '/',
        'telephone': config['phone'], 'email': config['email'],
        'image': image, 'logo': base + '/assets/logo.webp',
        'hasMap': config['maps_url'],
        'description': 'Garden and landscaping supplies. Customers can visit and collect at Mott Street Nursery. Enquire about delivery around the M25; availability and arrangements are confirmed individually.',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Mott Street Nursery, Mott Street', 'postalCode': 'E4 7RW', 'addressCountry': 'GB'},
        'areaServed': 'Areas around the M25',
        'openingHoursSpecification': [
            {'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':'08:00','closes':'17:00'},
            {'@type':'OpeningHoursSpecification','dayOfWeek':'Saturday','opens':'08:00','closes':'13:00'},
            {'@type':'OpeningHoursSpecification','dayOfWeek':'Sunday','opens':'00:00','closes':'00:00'}
        ],
        'contactPoint': {'@type':'ContactPoint','contactType':'sales enquiries','telephone':config['phone'],'email':config['email'],'url':'https://wa.me/'+config['whatsapp']},
    }
    page = dict(page_schema or {'@type':'WebPage'})
    page.pop('@context', None)
    page.update({'@id':url+'#page','url':url,'name':title,'description':description,'inLanguage':'en-GB','about':{'@id':business_id},'isPartOf':{'@id':base+'/#website'}})
    graph = [business, {'@type':'WebSite','@id':base+'/#website','url':base+'/','name':config['business_name'],'inLanguage':'en-GB'}, page]
    if path.startswith('/products/'):
        crumbs = [{'@type':'ListItem','position':1,'name':'Home','item':base+'/'}]
        crumbs.append({'@type':'ListItem','position':2,'name':page_schema['name'].split(' | ')[0],'item':url})
        graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})
    def meta(name, value, prop=False):
        return '<meta '+('property' if prop else 'name')+'="'+name+'" content="'+escape(value,quote=True)+'">'
    tags = [meta('description',description), meta('theme-color','#254735')]
    if is_error:
        tags.append(meta('robots','noindex, follow'))
    else:
        tags.append('<link rel="canonical" href="'+escape(url,quote=True)+'">')
    for name,value in {'og:title':title,'og:description':description,'og:type':'website','og:locale':'en_GB','og:site_name':config['business_name'],'og:url':url,'og:image':image,'og:image:width':'1200','og:image:height':'630','og:image:alt':'Trees at Evergreen Garden Supplies, Mott Street Nursery'}.items():
        tags.append(meta(name,value,True))
    for name,value in {'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':description,'twitter:image':image,'twitter:image:alt':'Trees at Evergreen Garden Supplies, Mott Street Nursery'}.items():
        tags.append(meta(name,value))
    tags.append('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph}).replace('<','\\u003c')+'</script>')
    return '\n'.join(tags)
