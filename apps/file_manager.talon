os: windows
app: Windows Explorer
app: explorer.exe
app: Windows Command Processor
app: cmd.exe

os: mac
app: com.apple.finder
app: Terminal
app: iTerm2
app: com.apple.Terminal

os: linux
app: Caja
app: /terminal/
-
settings():
    # enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

force title: user.file_manager_refresh_title()
show options: user.file_manager_show_pickers()
hide options: user.file_manager_hide_pickers()
go pictures: user.file_manager_open_user_directory("Pictures")
go downloads: user.file_manager_open_user_directory("Downloads")
go profile: user.file_manager_open_user_directory("")
go docks: user.file_manager_open_user_directory("Documents")
#go data: user.file_manager_open_directory("%AppData%")
#go talon: user.file_manager_open_directory("%AppData%\Talon")
^go <user.letter>$: user.file_manager_open_volume("{letter}:")
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
daddy: user.file_manager_open_parent()

^follow <user.file_manager_directory_index>$: user.file_manager_open_directory(user.file_manager_directory_index)
^open <user.file_manager_file_index>$: user.file_manager_open_file(user.file_manager_file_index)
^(cell | sell | select) folder <user.file_manager_directory_index>$: user.file_manager_select_directory(user.file_manager_directory_index)
^(cell | sell | select) file <user.file_manager_file_index>$: user.file_manager_select_file(user.file_manager_file_index)

next folders: user.file_manager_next_folder_page()
previous folders: user.file_manager_previous_folder_page()

next files: user.file_manager_next_file_page()
previous files: user.file_manager_previous_file_page()


