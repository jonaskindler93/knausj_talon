# NOTE: these are command line commands, not shell-specific bindings
# see shell.talon for shell-specific keybindings
os: linux
tag: terminal
-
(list|lisa): "ls\n"
(list|lisa) long: "ls -al\n"
(list|lisa) <user.text>: "ls {text}"
(list|lisa) (deer|dir): "ls "

# directory and files
(up (dear|dir)|travis): "../"
(cd|deer|dir) <user.text>: "cd {text}"
(cd|deer|dir) up: "cd ..\n"
parent (deer|dir): "cd ..\n"
(cd|deer|dir) home: "cd\n"
(cd|deer|dir) last: "cd -\n"
make (dur|dear|dir|directory): "mkdir "
make (dur|dear|dir|directory) <user.text>: "mkdir {text}"
remove (dur|dear|dir|directory): "rmdir "
remove (dur|dear|dir|directory) <user.ext>: "rmdir {text}"
remove file: "rm "
tree: "tree\n"
temp (dur|dear|dir|directory): "cd /tmp\n"
pop (dur|dear|dir|directory): "popd\n"

# permissions
make executable: "chmod +x "
change ownership: "chown "

# links
sim link: "ln -s "
hard link: "ln "

# finds
list sim links: "find . -maxdepth 1 -type l  -ls\n"
list (directories|folders): "find . -maxdepth 1 -type d  -ls\n"
list files: "find . -maxdepth 1 -type f  -ls\n"

touch: "touch "
# file management
move file: "mv "
copy file: "cp "
show me <user.text>: "cat {text}"
show me: "cat "
less: "less "


clear [screen|page]: "clear\n"

# find
find file: "find . -name "
fuzzy find file:
    insert("find . -name \"**\"")
    key("left")
    key("left")

# grepping

rip: "rg -i "
rip (exact|precise): "rg "

# networking
show (I P|eye pee): "ip addr\n"
show route: "ip route\n"
net stat: "netstat -ant\n"
net cat: "nc -vv "
net cat listener: "nc -v -l -p "
show hosts file: "cat /etc/hosts\n"
edit hosts file: "sudo vi /etc/hosts\n"
tcp dump: "tcpdump "

generate see tags: "ctags --recurse *\n"
generate see scope database:
    insert('find . -name "*.c"')
    insert(' -o -name "*.cpp"')
    insert(' -o -name "*.h"')
    insert(' -o -name "*.hpp"')
    insert(' -o -name "*.py"')
    insert(' -o -name "*.s"')
    insert(' -o -name "*.asm"')
    insert('> cscope.files\n')
    insert("cscope -q -R -b -i cscope.files\n")

process list: "ps -ef\n"
process top: "htop\n"
locate: "locate "
(where am I|print working directory): "pwd\n"

edit here: insert("edit .\n")

edit <user.text>$:
    insert("edit {text}")

edit:
    insert("edit ")

# XXX - ~/.edit/sessions/<tab>
edit session:
    insert("edit -S ")

lazy edit:
    insert("edit ")
    insert("$(find . -not -path '*/\.git/*' -name \"**\")")
    key("left")
    key("left")
    key("left")

lazy edit <user.text>:
    insert("edit ")
    insert("$(find . -not -path '*/\.git/*' -name \"*{text}*\")\n")

find <user.text> inside (python|pie) files:
    insert('$(find . -name \"*.py\") | xargs rg -i "{text}"\n')

find <user.text> inside (python|pie) files less:
    insert('$(find . -name \"*.py\") | xargs rg -i "{text}\" | less\n')

man: "man "
so do: "sudo "
d message: "dmesg"
disk usage: "df -h\n"

# extraction
tar ball: "tar -"
tar ball extract [zip]: "tar -xvzf "
tar ball extract bee zip: "tar -xvjf "
(un zip|extract zip): "unzip "

curl: "curl "
double you get: "wget "
download clipboard:
    insert("wget ")
    edit.paste()
    key(enter)

# because talent doesn't seem to like me saying ./
run script: "./"

# bash convenience stuff
for file loop:
    insert("for FILE in $(ls \"*\"); do \$FILE; done")

network manager log: "sudo journalctl -u NetworkManager.service\n"

# ssh
secure shell: "ssh"
secure shell <user.text>: "ssh {text}\n"
show authorized keys: "vi ~/.ssh/authorized_keys\n"
show pub keys: "cat ~/.ssh/*.pub\n"
edit authorized keys: "vi ~/.ssh/authorized_keys\n"
go secure shell config: "cd ~/.ssh\n"
terminate session:
    key(enter ~ .)

# process management
run top: "htop\n"
pee kill: "pkill "
pee kill <user.text>: "pkill {text}"
kill <number>: "kill -9 {number}"
reboot system: "sudo reboot -h now"
