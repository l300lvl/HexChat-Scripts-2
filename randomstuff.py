import hexchat
import xchat
import random

__module_name__ = 'FunStuff'
__module_author__ = 'Sammael/Valtiel'
__module_version__ = '0.1'
__module_description__ = 'Various commands for fun use'


def greentext(word, word_eol, userdata):
	if len(word) > 0:
		hexchat.command('say \00303>%s' % word_eol[1])
	
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

c0 = ['filthy', 'dirty', 'stinking']

c1 = ['artless', 'bawdy', 'beslubbering', 'bootless', 'churlish', 'cockered',
'clouted', 'craven', 'currish', 'dankish', 'dissembling', 'droning', 'errant',
'fawning', 'fobbing', 'froward', 'frothy', 'gleeking', 'goatish', 'gorbellied',
'impertinent', 'infectious', 'jarring', 'loggerheaded', 'lumpish', 'mammering',
'mangled', 'mewling', 'paunchy', 'pribbling', 'puking', 'puny', 'qualling', 
'rank', 'reeky', 'rogueish', 'ruttish', 'saucy', 'spleeny', 'spongy', 'surly', 
'tottering', 'unmuzzled', 'vain', 'venomed', 'villainous', 'warped', 'wayward', 
'weedy','whorish', 'yeastly'] # first column...

c2 = ['base-court', 'bat-fowling', 'beef-witted', 'beetle-headed', 'boil-brained',
'clapper-clawed', 'clay-brained', 'common-kissing', 'crook-pated', 'dismal-dreaming',
'dizzy-eyed', 'doghearted', 'dread-bolted', 'earth-vexing', 'elf-skinned', 'fat-kidneyed',
'fen-sucked', 'flap-mouthed', 'fly-bitten', 'folly-fallen', 'fool-born', 'full-gorged',
'guts-griping', 'half-faced', 'hasty-witted', 'hedge-born', 'hell-hated', 'idle-headed',
'ill-breeding', 'ill-nurtured', 'knotty-pated', 'milk-livered', 'motley-minded', 'onion-eyed',
'plume-plucked', 'pottle-deep', 'pox-marked', 'reeling-ripe', 'rough-hewn', 'rude-growing',
'rump-fed', 'shard-borne', 'sheep-biting', 'spur-galled', 'swag-bellied', 'tardy-gaited',
'tickle-brained', 'toad-spotted', 'unchin-snouted', 'weather-bitten'] # second column...

c3 = ['apple-john', 'baggage', 'barnacle', 'bladder', 'boar-pig', 'bugbear', 'bum-bailey',
'canker-blossom', 'clack-dish', 'clotpole', 'coxcomb', 'codpiece', 'death-token', 'dewberry',
'flap-dragon', 'flax-wench', 'flirt-gill', 'foot-licker', 'fustilarian', 'giglet', 'gudgeon',
'haggard', 'harpy', 'hedge-pig', 'horn-beast', 'hugger-mugger', 'joithead', 'lewdster', 'lout',
'maggot-pie', 'malt-worm', 'mammet', 'measle', 'minnow', 'miscreant', 'moldwarp', 'mumble-news',
'nut-hook', 'pidgeon-egg', 'pignut', 'puttock', 'pumpion', 'ratsbane', 'scut', 'skainsmate',
'strumpet', 'varlot', 'vassal', 'whey-face', 'wagtail'] # third column

def cmd_insult(word, word_eol, userdata):
    insult = "thou %s %s %s %s!" %(random.choice(c0), random.choice(c1), random.choice(c2), random.choice(c3))
    channel = hexchat.get_info("channel")
    if len(word) < 2:
        hexchat.command("MSG %s %s" %(channel, insult))
    else:
        hexchat.command("MSG %s %s %s" %(channel, word[1], insult))

def lekker(word, word_eol, userdata):
	if len(word) <= 1:
		chan = hexchat.get_info('channel')
		word = "LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER LEKKER"
		hexchat.command("MSG %s %s" % (chan, word))
		return hexchat.EAT_ALL
	
hexchat.hook_command('gt', greentext, help="/gt <text> Shows the desired text in the famous greentext form")
xchat.hook_command("flip", flip, help="/flip <text> Flips the desired text.")
hexchat.hook_command("rb", rainbow, help="/rb <text> Rainbowfies desired text.")
hexchat.hook_command("insult", cmd_insult, help="/insult [nick] Generates a shakespearean insult, with the option to direct it at a user.")
hexchat.hook_command("lekker", lekker, help="/lekker Spams the best Dutch word ever")

hexchat.emit_print("Notice", __module_name__ + " [Plugin]", "%s by %s loaded. You are using version %s of the script." % (__module_name__, __module_author__, __module_version__))