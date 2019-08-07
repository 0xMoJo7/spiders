click_depth = 12  # how many links deep to go into webpage
min_wait = 5  # minimum wait time between requests
max_wait = 10  # maximum wait time between requests
min_proxy_pages = 2  # number of times to use list of proxies before fetching new group
max_proxy_pages = 14
debug = True

root_urls = [
	"https://espn.com",
	]

blacklist = [
	"https://t.co",
	"t.umblr.com",
	"messenger.com",
	"itunes.apple.com",
	"l.facebook.com",
	"bit.ly",
	"mediawiki",
	".css",
	".ico",
	".xml",
	"intent/tweet",
	"twitter.com/share",
	"signup",
	"login",
	"dialog/feed?",
	".png",
	".jpg",
	".json",
	".svg",
	".gif",
	"zendesk",
	"clickserve"
	]

