#defines the various mode commands
mode: all
-
welcome back:
	user.mouse_wake()
	user.history_enable()
	speech.enable()
sleep all:
	user.switcher_hide_running()
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	user.mouse_sleep()
	speech.disable()
    user.system_command('notify-send.sh -t 3000 -f -u low "Sleep All mode"')
	user.engine_sleep()
talon sleep: speech.disable()
(talon wake|key("cmd-shift-ctrl-m")): speech.enable()
dragon mode: speech.disable()
talon mode: speech.enable()
^(dictation mode|dictate)$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.system_command('notify-send.sh -t 3000 -f -u low "Dictation Mode"')
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
[enable] debug mode:
    mode.enable("user.gdb")
    user.system_command('notify-send.sh -t 3000 -f -u low "Debug Mode Enabled"')
disable debug mode:
    mode.disable("user.gdb")
^force see sharp$: user.code_set_language_mode("csharp")
^force see plus plus$: user.code_set_language_mode("cplusplus")
^force go (lang|language)$: user.code_set_language_mode("go")
^force java script$: user.code_set_language_mode("javascript")
^force type script$: user.code_set_language_mode("typescript")
^force markdown$: user.code_set_language_mode("markdown")
^force python$: user.code_set_language_mode("python")
^force talon [language]$: user.code_set_language_mode("talon")
^clear language modes$: user.code_clear_language_mode()
