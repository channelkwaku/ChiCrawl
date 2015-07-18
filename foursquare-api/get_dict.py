import sqlite3
import foursquare

client = foursquare.Foursquare(
		client_id='JZ0P123UOI1WX2UA5GBKJ5R15EG5SXPJPQI43QBW12IX1BBT',
		client_secret='PFPZXOCWBJZULOP4KNPLX2USVTL34PPI1EVH15SIIC4QSZQQ'
		)


# returns a list of triple tuples with the following format:
# (name, latitude, longitude)
def get_venue_info():
	db = sqlite3.connect('../bars3.db')
	c = db.cursor()
	s = 'SELECT name, latitude, longitude FROM bars GROUP BY name'
	r = c.execute(s).fetchall()
	return r


# returns a list of individual words
def get_words(venue_menu):
	result = ''
	menus = venue_menu['menu']['menus']
	if menus.has_key('items'):
		for x in menus['items'][0]['entries']['items']:
			for y in x['entries']['items']:
				result = result + y['name'] + ' '	

	result = result[:-1]
	# converts every character in the menu items to lower case
	result = result.lower()
	result = result.split()
	return result


def get_dict():
	r = get_venue_info()
	result = {}

	for entry in r:
		name = entry[0]
		ll = str(entry[1]) + ',' + str(entry[2])
		info = client.venues.search(params = {'name': name, 'll': ll})
		
		v = {}
		for venue in info['venues']:
			if venue['name'] == name:
				v = venue
				venue_id = venue['id']
				break

		venue_menu = client.venues.menu(venue_id)
		keywords = get_words(venue_menu)
		for word in keywords:
			if result.has_key(word):
				if name not in result[word]:
					result[word].append(name)
			else:
				result[word] = [name]

	return result

# so there is a problem, we are unable to attain the menu for every
# venue possible. in fact, i think we are missing quite a few of them
# we were able to attain the unique venue id for each of them (426)
# however, client.venues.venue(venue_id) doesn't work every time
# so we thought that foursquare simply doesn't provide the menu for these
# venues, which we can't do anything. however, after looking online, we realize
# that foursquare doesn't provide the json datafile for them, but do have the online
# page for it...

# so for right now, for the ones that "don't" have a menu, they are just not part of the dict
# should be fine for now, but we will think of a way to fix that up
