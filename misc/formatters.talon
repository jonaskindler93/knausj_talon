#Note: Appending $ will anchor the command
#provide both anchored and unachored commands via 'over'
<user.format_text>$: insert(format_text)
<user.format_text> over: insert(format_text)
phrase <user.text>$: insert(user.text)
phrase <user.text> over: insert(user.text)
(say | speak) <user.text>$: insert(user.text)
(say | speak) <user.text> over: insert(user.text)
# word conflicts with vim.py
poke <user.word>: insert(user.word)
#word <user.word>: insert(user.word)
list formatters: user.list_formatters()
hide formatters: user.hide_formatters()
