import hexchat

__module_name__ = 'SVutils'
__module_author__ = 'Sammael/Valtiel'
__module_version__ = '0.0.1a'
__module_description__ = 'Various commands'

def greentext(word, word_eol, userdata):
    if len(word) > 0:
        hexchat.command('say \00303>%s' % word_eol[1])

    return hexchat.EAT_ALL

hexchat.hook_command('gt', greentext)

hexchat.emit_print('Notice', __module_name__ + ' [Plugin]', '%s by %s loaded. You are using version %s of the script.' % (__module_name__, __module_author__, __module_version__))
