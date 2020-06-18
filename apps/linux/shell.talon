os: linux
tag: terminal
-
(rerun|run) last [command]: "!!\n\n"
(chuck|cancel) (it|that): key("ctrl-c")
interrupt: key("ctrl-c")
damn (it|that): key("ctrl-d")

# fzf keybindings
search history: key(ctrl-r)
fuzzy (dir|dear|dur): key(alt-c)
fuzzy (dir|dear|dur) <user.text>:
    key(alt-c)
    insert("{text}")

# zsh commands
reload shell config: "source ~/.zshrc\n"

# zsh autosuggestions plugin
(got|run) (it|that): key(ctrl-o)
found [it]: key(ctrl-g)
keep [it]: key(ctrl-f)
