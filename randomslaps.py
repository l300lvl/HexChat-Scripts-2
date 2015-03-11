import hexchat as hexchat
import random

__module_name__ = 'randomslaps'
__module_author__ = 'Sammael/Valtiel'
__module_version__ = '0.1'
__module_description__ = 'Random slap messages'

slapmsg =["slaps %k around a bit with a default slap script.", "slaps %k around a bit with a large trout.", "wallops %k around with a Windows Vista Disc.", "throws %k in a room with qjqqyy.", "tosses %k's salad.", "crushes %k's balls underneath a steamroller.", "sticks a piranha in %k's underwear.", "pushes %k in front of a moving train.", "tells %k to go play in traffic.", "slaat %k met een grote lul.", "slår %k med en stor kuk.", "abofetea a %k con un gran pene."]

def randslap(word, word_eol, userdata):
	if len (word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL
	try: line = random.choice(slapmsg).replace('\n', '').replace('\r', '').replace('%k', word[1])
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from the slap variable. Please edit the plugin to add your own slap messages -- Using default slap.")
		line = "slaps %k around a bit with a default slap script.".replace('\n', '').replace('\r', '').replace('%k', word[1])
	if len (word) == 2:
		hexchat.command("me " + line.format(word[0]))
		return hexchat.EAT_ALL
	elif len (word) >= 3:
		hexchat.prnt("One nick at a time.")
		return hexchat.EAT_ALL

hexchat.hook_command("slap", randslap, help="/slap Slaps a user.")

hexchat.emit_print('Notice', __module_name__ + ' [Plugin]', '%s by %s loaded. You are using version %s of the script.' % (__module_name__, __module_author__, __module_version__))