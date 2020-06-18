#tag: vim
tag: gdb
-

###
# VIM terminal GDB convenience
#
# These only work if you run GDB from inside a vim terminal and you're using
# vim.py automatic mode switching support
#
# It when you're running the terminal for a long time, the line numbers become
# so large they are hard to say, so I support some commands to use relative
# numbers. There is support in vim.talon for swapping between absolute and
# relative numbers relatively easily.
###

# Assumes you are already on a line with hex addresses
# XXX - If your cursor is already on an 0x value, it's a bit weird cuz it
# doesn't count in the search
copy <user.ordinals> (hex value|address):
    insert("/\c0x\n")
    insert("{ordinals-1}n")
    insert("yw")
    insert(":set nohls\n")

(hexdump|matrix) <user.ordinals> (hex value|address):
    insert("/\c0x\n")
    insert("{ordinals-1}n")
    insert("yw")
    insert(":set nohls\n")
    insert("i")
    # XXX - need to make this tweakable
    insert("x/10gx ")
    edit.paste()
    key(enter)

go <user.ordinals> (hex value|address):
    insert("/\c0x\n")
    insert("{ordinals-1}n")
    insert(":set nohls\n")

# XXX - the following have a lot of duplication so it may be worth making
# python function eventually where the majority of the none unique stuff can
# just be called once

(hexdump|matrix) [this] address:
    insert("yiw")
    insert("i")
    insert("x/10gx ")
    edit.paste()
    key(enter)

(hexdump|matrix) line <number>$:
    user.vim_normal_mode_exterm(":{number}\n")
    insert("^")
    insert("/\c0x\n")
    insert("yiw")
    insert(":set nohls\n")
    insert("i")
    sleep(100ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)

# for use with relative number lines
(hexdump|matrix) [relative] up [line] <number>$:
    user.vim_normal_mode_exterm("{number+1}k\n")
    insert("^")
    insert("/\c0x\n")
    insert("yiw")
    insert(":set nohls\n")
    insert("i")
    sleep(100ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)

# for use with relative number lines
(hexdump|matrix) [relative] down [line] <number>$:
    user.vim_normal_mode_exterm("{number+1}j\n")
    insert("^")
    insert("/\c0x\n")
    insert("yiw")
    insert(":set nohls\n")
    insert("i")
    sleep(100ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)

(hexdump|matrix) line <number> <user.ordinals>$:
    user.vim_normal_mode_exterm(":{number}\n")
    insert("^")
    insert("/\c0x\n")
    insert("{ordinals-1}n")
    insert("yw")
    insert(":set nohls\n")
    insert("i")
    sleep(200ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)

# for use with relative number lines
(hexdump|matrix) [relative] down [line] <number> <user.ordinals>$:
    user.vim_normal_mode_exterm("{number+1}j\n")
    insert("^")
    insert("/\c0x\n")
    insert("yiw")
    insert("{ordinals-1}n")
    insert(":set nohls\n")
    insert("i")
    sleep(100ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)

# for use with relative number lines
(hexdump|matrix) [relative] up [line] <number> <user.ordinals>$:
    user.vim_normal_mode_exterm("{number+1}k\n")
    insert("^")
    insert("/\c0x\n")
    insert("yiw")
    insert("{ordinals-1}n")
    insert(":set nohls\n")
    insert("i")
    sleep(100ms)
    # XXX - need to make this tweakable
    insert("x/100gx ")
    edit.paste()
    sleep(100ms)
    key(enter)
