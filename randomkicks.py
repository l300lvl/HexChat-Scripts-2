import hexchat as hexchat
import random

__module_name__ = 'randomkicks'
__module_author__ = 'Sammael/Valtiel'
__module_version__ = '0.1'
__module_description__ = 'Random kick messages'

kickmsg = ["Your behaviour is not conducive to the desired environment.", "%k, you suck, you know that?", "%c would be better without you, %k."]

def kbquote(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	chan = hexchat.get_info("channel")
	userlist = hexchat.get_list("users")
	
	try: line = random.choice(kickmsg)
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from quotes.txt (Make sure it's in your config folder!), Using default reason if reason was not specified.")
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

	reason = reason.replace('\n', '').replace('\r', '').replace('%k', word[1])
	hexchat.command("raw kick  " + chan + " " + word[1] + " " + ":" + reason + " [Banned]")

	return hexchat.EAT_ALL

def kickquote(word, word_eol, userdata):
	if len(word) <= 1:
		hexchat.emit_print("Notice", __module_name__, "No arguments given.")
		return hexchat.EAT_ALL

	chan = hexchat.get_info("channel")
	userlist = hexchat.get_list("users")
	try: line = random.choice(kickmsg)
	except:
		hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "Failed to grab a line from quotes.txt (Make sure it's in your config folder!)-- Using default reason if reason was not specified.")
		line = "No reason specified."

	try: reason = word_eol[2]
	except IndexError: reason = line

	for user in userlist:
		if user.nick.lower() == word[1].lower(): break

	reason = reason.replace('\n', '').replace('\r', '').replace('%k', word[1])
	if user.nick.lower() == word[1].lower():
		hexchat.command("raw kick  " + chan + " " + word[1] + " " + ":" + reason)

	else: hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "User not found.")
	return hexchat.EAT_ALL

hexchat.hook_command("kick", kickquote, help="/kick Kicks a user.")
hexchat.hook_command("kickban", kbquote, help="/kickban Kicks and bans a user.")
hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "%s by %s loaded. You are using version %s of the script." % (__module_name__, __module_author__, __module_version__))