import hexchat
import random
import xchat
import re
from time import localtime, strftime

__module_name__ = 'SVutils'
__module_author__ = 'Sammael/Valtiel'
__module_version__ = '0.1a'
__module_description__ = 'Various commands cobbled together with help from ApolloJustice and Seth/Takeru'

def greentext(word, word_eol, userdata):
	if len(word) > 0:
		hexchat.command('say \00303>%s' % word_eol[1])
	
	return hexchat.EAT_ALL

textfiledir = hexchat.get_info("configdir")

def kbquote(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	chan = hexchat.get_info("channel")
	userlist = hexchat.get_list("users")
	try: line = random.choice(open(textfiledir + "/quotes.txt", "r").readlines())
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from quotes.txt (Make sure it's in your config folder!)-- Using default reason if reason was not specified.")
		line = "No reason specified."

	for user in userlist:
		if user.nick.lower() == word[1].lower(): break

	host = user.host.split('@')[1]

	if user.nick.lower() == word[1].lower():
		hexchat.command("raw mode " + chan + " +b " + host)

	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
		return hexchat.EAT_ALL

	try: reason = word_eol[2]
	except: reason = line

	reason = reason.replace('\n', '').replace('\r', '').replace('%k', word[1]).replace('%c', chan)
	hexchat.command("raw kick  " + chan + " " + word[1] + " " + ":" + reason + " [Banned]")

	return hexchat.EAT_ALL

def kickquote(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	chan = hexchat.get_info("channel")
	userlist = hexchat.get_list("users")
	try: line = random.choice(open(textfiledir + "/quotes.txt", "r").readlines())
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from quotes.txt (Make sure it's in your config folder!)-- Using default reason if reason was not specified.")
		line = "No reason specified."

	try: reason = word_eol[2]
	except IndexError: reason = line

	for user in userlist:
		if user.nick.lower() == word[1].lower(): break

	reason = reason.replace('\n', '').replace('\r', '').replace('%k', word[1]).replace('%c', chan)
	if user.nick.lower() == word[1].lower():
		hexchat.command("raw kick  " + chan + " " + word[1] + " " + ":" + reason)

	else: hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def randslap(word, word_eol, userdata):
	if len (word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL
	try: line = random.choice(open(textfiledir + "/slaps.txt").readlines()).replace('\n', '').replace('\r', '').replace('%k', word[1])
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from slaps.txt (Make sure it's in your config folder!)-- Using default reason if reason was not specified.")
		line = "slaps %k around a bit with a default slap script.".replace('\n', '').replace('\r', '').replace('%k', word[1])
	if len (word) == 2:
		hexchat.command("me " + line.format(word[0]))
		return hexchat.EAT_ALL
	elif len (word) >= 3:
		hexchat.prnt("One nick at a time.")
		return hexchat.EAT_ALL

def hexchatv(word, word_eol, userdata):
	if len(word) <= 1:
		cver = hexchat.get_info('version')
		hexchat.command("me is running HexChat " + cver)
		return hexchat.EAT_ALL
		
def cmsg(word, word_eol, userdata):
	chanstr = word[1].split(",")
	for chan in chanstr:
		hexchat.find_context(channel=chan).command("say " + word_eol[2])
	return hexchat.EAT_ALL
	
def cme(word, word_eol, userdata):
	chanstr = word[1].split(",")
	for chan in chanstr:
		hexchat.find_context(channel=chan).command("me " + word_eol[2])
	return hexchat.EAT_ALL

def flip(word, word_eol, userdata):
	try:
		xchat.command('say %s' % word_eol[1][::-1])
	except:
		xchat.prnt('No text to flip')
		
	return xchat.EAT_ALL

def rainbow(word, word_eol, userdata):
	rainbowstr = ""
	for character in word_eol[1]:
		rainbowstr += '\003' + str(random.randint(2,15)) + character
	hexchat.command("say " + rainbowstr)
	rainbowstr = ""
	return hexchat.EAT_ALL

def find_highlighttab(arg1):
	context = hexchat.find_context(channel=arg1)
	if context == None: # Create a new one in the background
		newtofront = hexchat.get_prefs('gui_tab_newtofront')

		hexchat.command('set -quiet gui_tab_newtofront 0')
		hexchat.command('newserver -noconnect {0}'.format(arg1))
		hexchat.command('set -quiet gui_tab_newtofront {}'.format(newtofront))

		return hexchat.find_context(channel=arg1)
	else:
		return context

def highlight_callback(word, word_eol, user_data):
	
	word = [(word[i] if len(word) > i else '') for i in range(4)]
	
	highlight_context = find_highlighttab('hilight')
	nick = hexchat.get_info("nick")
	chan = hexchat.get_info('channel')
	net = hexchat.get_info("network")
	sendernick = word[0]
	content = word[1]
	mode = word[2]
	idtext = word[3]
	
	if 'RasPi ZNC' in net:
		net = net.replace('RasPi ZNC', '').replace('(', '').replace(')', '')
		net = net.lstrip()
	
	content = re.sub(nick, '\002\00320%s\017' % nick , content, flags=re.IGNORECASE)
	content = content.lstrip()
	
	if user_data == 'Channel Msg Hilight':
		highlight_context.prnt('{0}[\00327{3}\017] [\00323{4}\017] \00326{1}\00322{2}\017 said: \'{5}\''.format(idtext, mode, sendernick, chan, net, content))
	elif user_data == 'Channel Action Hilight':
		highlight_context.prnt(('{0}[\00327{3}\017] [\00323{4}\017] \00326{1}\00322{2}\017 {5}').format(idtext, mode, sendernick, chan, net, content))

	# Can't easily intelligently manage color so lets just ignore it
	highlight_context.command('gui color 3')
	return hexchat.EAT_NONE

def disablechan(word, word_eol, userdata):
	chan = hexchat.get_info('channel')
	hexchat.command("RAW PRIVMSG *status :disablechan " + chan)
	hexchat.command("close")
	hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Parted " + chan + " and disabled it in ZNC.")
	return hexchat.EAT_ALL

def temppart(word, word_eol, userdata):
	chan = hexchat.get_info('channel')
	hexchat.command("raw PART " + chan)
	hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Parted " + chan + " without disabling it in ZNC.")
	return hexchat.EAT_ALL

def sudo(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	chan = hexchat.get_info("channel")
	dothis = word_eol[1]
	hexchat.command("RAW PRIVMSG ChanServ :op " + chan) # Tell chanserv to op me
	hexchat.command("timer 1 " + dothis) # Execute dothis in hexchat
	hexchat.command("timer 1.7 RAW PRIVMSG ChanServ :deop " + chan) # Wait 1 second, then tell chanserv to deop me
	return hexchat.EAT_ALL # Don't pass this as a command to the server

def getinfo(word, word_eol, userdata): # Command for getting various info from hexchat -- http://hexchat.readthedocs.org/en/latest/script_python.html#information-retreiving-functions
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL
	hexchat.emit_print("Notice", __module_name__ + " [Plugin]", hexchat.get_info(word[1])) # Print the result to the hexchat window
	return hexchat.EAT_ALL # Don't pass this as a command to the server

def topicappend(word, word_eol, userdata): # Append a string to the channel topic
	topic = hexchat.get_info("topic") # Get the current topic
	if len(word) <=1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL
	hexchat.command("topic " + topic.rstrip() + " | " + word_eol[1]) # Take the channel topic, strip any whitespace at the end of it, add a separator, add the string, and then set it as the channel topic.
	return hexchat.EAT_ALL # Don't pass this as a command to the server

def improvedignore(word, word_eol, userdata): # Ignores hostmasks instead of nicknames
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL
	for user in users:
		if user.nick.lower() == word[1].lower():
			break
	host = user.host.split('@')[1]

	if user.nick.lower() == word[1].lower():
		hexchat.command("ignore *!*@" + host)
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def improvedunignore(word, word_eol, userdata): # Ignores hostmasks instead of nicknames
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break
	host = user.host.split('@')[1]
	if user.nick.lower() == word[1].lower():
		hexchat.command("unignore *!*@" + host)
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def gethost(word, word_eol, userdata): # Gets a user's hostmask without a full whois
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break

	hexchat.emit_print("Notice", __module_name__ + " [Plugin]", user.nick + "'s hostmask is " + user.host.split('@')[1] )
	return hexchat.EAT_ALL

def quiet(word, word_eol, userdata):
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break
	host = user.host.split('@')[1]

	if '@' in word[1] or '$' in word[1]:
		hexchat.command("raw MODE %s +q %s" % (hexchat.get_info("channel"), word[1]))
		return hexchat.EAT_ALL

	if user.nick.lower() == word[1].lower():
		hexchat.command("raw MODE %s +q *!*@%s" % (hexchat.get_info("channel"), host))
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def unquiet(word, word_eol, userdata):
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break

	host = user.host.split('@')[1]
	if '@' in word[1] or '$' in word[1]:
		hexchat.command("raw MODE %s -q %s" % (hexchat.get_info("channel"), word[1]))
		return hexchat.EAT_ALL
	if user.nick.lower() == word[1].lower():
		hexchat.command("raw MODE %s -q *!*@%s" % (hexchat.get_info("channel"), host))
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def exempt(word, word_eol, userdata):
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break
	host = user.host.split('@')[1]

	if '@' in word[1] or '$' in word[1]:
		hexchat.command("raw MODE %s +e %s" % (hexchat.get_info("channel"), word[1]))
		return hexchat.EAT_ALL

	if user.nick.lower() == word[1].lower():
		hexchat.command("raw MODE %s +e *!*@%s" % (hexchat.get_info("channel"), host))
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

def unexempt(word, word_eol, userdata):
	users = hexchat.get_list("users")
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	for user in users:
		if user.nick.lower() == word[1].lower():
			break
	host = user.host.split('@')[1]

	if '@' in word[1] or '$' in word[1]:
		hexchat.command("raw MODE %s -e %s" % (hexchat.get_info("channel"), word[1]))
		return hexchat.EAT_ALL

	if user.nick.lower() == word[1].lower():
		hexchat.command("raw MODE %s -e *!*@%s" % (hexchat.get_info("channel"), host))
	else:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL


def flagedit(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.command('msg chanserv access ' + hexchat.get_info("channel") + ' list')
		return hexchat.EAT_ALL
	if '#' not in word[1]: hexchat.command('msg chanserv flags ' + hexchat.get_info("channel") + ' ' + word_eol[1])
	if '#' in word[1]: hexchat.command('msg chanserv flags ' + word_eol[1])
	return hexchat.EAT_ALL

def timey(word, eol, data): 
	xchat.command('say It\'s currently: ' + strftime("%I:%M:%S %p", localtime()).lstrip('0'))
	return xchat.EAT_ALL # kills remaining bits of memory

def wrap(word, word_eol, userdata):
	fullstr = word_eol[1].split('|')
	
	title = fullstr[0]
	artist = fullstr[1]
	album = fullstr[2]
	codec = fullstr[3]
	fb2kver = fullstr[4]
	samplerate = fullstr[5]
	bitrate = fullstr[6]
	soundchannels = fullstr[7]
	elapsed = fullstr[8]
	duration = fullstr[9]
	
	if duration == "0:0-1":
		hexchat.command("me np: \00304Playback stopped.\017 [\00325fb2k %s\017]" % fb2kver.replace("foobar2000", '').replace('v', '').lstrip().rstrip())
		return hexchat.EAT_ALL	
	
	hexchat.command("me np:\00306 %s \017by\00307 %s\017 from\00310 %s\017 [\00303%s\017/\00304%s\017] [\00318%s\017|\00322%s\00329kbps\017] [\00325fb2k %s\017]" % (title, artist, album, elapsed, duration, codec, bitrate, fb2kver.replace("foobar2000", '').replace('v', '').lstrip().rstrip()))
	return hexchat.EAT_ALL

def foo(word, word_eol, userdata):
	if len(word) == 1:
		hexchat.command("wp")
	else:
		hexchat.command("wp %s" % word_eol[1])
		
chan = ""
locked = 0
def savemebrother():
	global locked
	if locked == 0:
		hexchat.command('RAW PRIVMSG ChanServ :unban ' + chan)
		hexchat.command('timer 0.5 RAW JOIN ' + chan)
		locked = 1
		return hexchat.EAT_ALL

def resetsavemebrother(word, word_eol, userdata):
	global chan
	global locked
	chan = ""
	locked = 0

def storechan(word, word_eol, userdata):
	global chan
	chan = word[3]
	savemebrother()
	
hexchat.hook_command('gt', greentext, help="/gt Shows the desired text in the famous greentext form")
hexchat.hook_command("kick", kickquote, help="/kick Kicks a user.")
hexchat.hook_command("kickban", kbquote, help="/kickban Kicks and bans a user.")
hexchat.hook_command("slap", randslap, help="/slap Slaps a user.")
hexchat.hook_command("cv", hexchatv, help="/cv Posts what version of HexChat you are running.")
hexchat.hook_command("cmsg", cmsg, help="/cmsg <channels> <text> Messages the listed channels(separated by commas) with the desired text")
hexchat.hook_command("cme", cme, help="/cme <channels> <text> Message the listed channels(separated by commas) with the desired text as an action.")
xchat.hook_command("flip", flip, help="/flip <text> Flips the desired text.")
hexchat.hook_command("rb", rainbow, help="/rb <text> Rainbowfies desired text.")

hexchat.hook_print('Channel Msg Hilight', highlight_callback, 'Channel Msg Hilight')
hexchat.hook_print('Channel Action Hilight', highlight_callback, 'Channel Action Hilight')

hexchat.hook_command("sudo", sudo, help="/sudo Executes a command as op on channels you have flag +o on.")
hexchat.hook_command("getinfo", getinfo, help="/getinfo Returns the result of hexchat.get_info()")
hexchat.hook_command("topicappend", topicappend, help="/topicappend Adds a string to the topic")
hexchat.hook_command("appendtopic", topicappend, help="/appendtopic Adds a string to the topic")
hexchat.hook_command("part", disablechan, help="/part parts and disables chan on znc")
hexchat.hook_command("temppart", temppart, help="/temppart parts without disabling chan on znc")
hexchat.hook_command("ignorehost", improvedignore, help="/ignorehost ignores a user's host")
hexchat.hook_command("unignorehost", improvedunignore, help="/unignorehost ignores a user's host")
hexchat.hook_command("gethost", gethost, help="/gethost gets a user's hostmask")
hexchat.hook_command("quiet", quiet)
hexchat.hook_command("unquiet", unquiet)
hexchat.hook_command("exempt", exempt)
hexchat.hook_command("unexempt", unexempt)
hexchat.hook_command("flags", flagedit)
xchat.hook_command("time",timey,help="/time - display current time")
hexchat.hook_command("reformatwp", wrap)
hexchat.hook_command("fb",foo, help="Usage: wp [  n  |  b  |  p  |  s  |  q   ]                           next  prev  play  stop  pause")

hexchat.hook_server("474", storechan)
hexchat.hook_server("PONG", resetsavemebrother)

hexchat.emit_print('Notice', __module_name__ + ' [Plugin]', '%s by %s loaded. You are using version %s of the script.' % (__module_name__, __module_author__, __module_version__))