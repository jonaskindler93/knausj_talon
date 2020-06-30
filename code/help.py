from typing import Set,Tuple,List
from talon import Module, Context, actions, imgui, Module, registry, ui
import math

mod = Module()
mod.list('help_contexts', desc='list of available contexts')
mod.mode("help", "mode for commands that are available only when help is visible")
setting_help_max_contexts_per_page = mod.setting('help_max_contexts_per_page', type=int, default=20, desc="Max contexts to display per page in help")
setting_help_max_command_lines_per_page = mod.setting('help_max_command_lines_per_page', type=int, default=50, desc="Max lines of command to display per page in help")

ctx = Context()
#context name -> commands
context_command_map = {}

#context name -> actual context
context_map = {}

current_context_page = 1
sorted_context_map_keys = None

selected_context = None
selected_context_page = 1

total_page_count = 1

cached_active_contexts_list = []

max_commands_per_page = 15

live_update = True
cached_window_title = None
show_enabled_contexts_only = False

def update_title(): 
    global live_update
    global show_enabled_contexts_only
    global cached_window_title

    if live_update:
        if gui_context_help.showing:
            if selected_context == None:
                refresh_context_command_map(show_enabled_contexts_only) 
            else:
                update_active_contexts_cache(registry.active_contexts())

#todo: dynamic rect?
@imgui.open(y=0,software=False)
def gui_alphabet(gui: imgui.GUI):
    global alphabet
    gui.text("Alphabet help")
    gui.line()

    for key,val in alphabet.items():
        gui.text("{}: {}".format(val, key))

    gui.spacer()
    if gui.button('close'):
        gui_alphabet.hide()

def format_context_title(context_name: str) -> str:
    global cached_active_contexts_list
    return "{} [{}]".format(
        context_name, 
        "ACTIVE" if context_map.get(context_name, None) in cached_active_contexts_list else "INACTIVE"
    )

def format_context_button(index: int, context_label: str, context_name: str) -> str:
    global cached_active_contexts_list
    global show_enabled_contexts_only

    if not show_enabled_contexts_only:
        return "{}. {}{}".format(index,
            context_label,
            "*" if context_map.get(context_name, None) in cached_active_contexts_list else "",
        )
    else:
        return "{}. {} ".format(
            index,
            context_label
        )

# translates 1-based index -> actual index in sorted_context_map_keys
def get_context_page(index: int) -> int:
    return math.ceil(index / setting_help_max_contexts_per_page.get())

def get_total_context_pages() -> int:
    return math.ceil(len(sorted_context_map_keys) / setting_help_max_contexts_per_page.get())

def get_current_context_page_length() -> int:
    start_index = (current_context_page -1) * setting_help_max_contexts_per_page.get()
    return len(sorted_context_map_keys[start_index:start_index + setting_help_max_contexts_per_page.get()])

def get_command_line_count(command: Tuple[str, str]) -> int:
    """This should be kept in sync with draw_commands
    """
    _, body = command
    lines = len(body.split("\n"))
    if lines == 1:
        return 1
    else:
        return lines + 1

def get_pages(item_line_counts: List[int]) -> List[int]:
    """Given some set of indivisible items with given line counts,
    return the page number each item should appear on.

    If an item will cross a page boundary, it is moved to the next page,
    so that pages may be shorter than the maximum lenth, but not longer. The only
    exception is when an item is longer than the maximum page length, in which
    case that item will be placed on a longer page.
    """
    current_page_line_count = 0
    current_page = 1
    pages = []
    for line_count in item_line_counts:
        if line_count + current_page_line_count > setting_help_max_command_lines_per_page.get():
            if current_page_line_count == 0:
                # Special case, render a larger page.
                page = current_page
                current_page_line_count = 0
            else:
                page = current_page + 1
                current_page_line_count = line_count
            current_page += 1
        else:
            current_page_line_count += line_count
            page = current_page
        pages.append(page)
    return pages

@imgui.open(y=0,software=False)
def gui_context_help(gui: imgui.GUI):
    global context_command_map
    global current_context_page
    global selected_context
    global selected_context_page
    global sorted_context_map_keys
    global show_enabled_contexts_only
    global cached_active_contexts_list
    global total_page_count

    # if no selected context, draw the contexts
    if selected_context is None:
        total_page_count = get_total_context_pages()

        if not show_enabled_contexts_only:
            gui.text("Help: All ({}/{}) (* = active)".format(current_context_page, total_page_count))
        else:
            gui.text("Help: Active Contexts Only ({}/{})".format(current_context_page,total_page_count))

        gui.line()

        current_item_index = 1
        current_selection_index = 1
        for key in sorted_context_map_keys:
            target_page = get_context_page(current_item_index)

            if current_context_page == target_page:
                button_name = format_context_button(current_selection_index, key, ctx.lists['self.help_contexts'][key])

                if gui.button(button_name):
                    selected_context = ctx.lists['self.help_contexts'][key]
                current_selection_index = current_selection_index + 1

            current_item_index += 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button('Next...'):
                actions.user.help_next()

            if gui.button("Previous..."):
                actions.user.help_previous()      
    
    #if there's a selected context, draw the commands for it
    else:
        total_page_count = get_selected_context_command_pages()
        if context_map[selected_context] in cached_active_contexts_list:
            gui.text("{} ({}/{}) [ACTIVE]".format(selected_context, selected_context_page, total_page_count))
        else:
            gui.text("{} ({}/{}) [INACTIVE]".format(selected_context, selected_context_page, total_page_count))

        gui.line()
        
        current_item_index = 1
        for key, val in context_command_map[selected_context].items():
            #print(key + ": " + val)
            target_page = get_command_page(current_item_index)

            if selected_context_page == target_page:
                val = val.split("\n")
                if len(val) > 1:
                    gui.text("{}:".format(key))
                    for line in val:
                        gui.text("    {}".format(line))
                    gui.spacer()
                else:
                    gui.text("{}: {}".format(key, val[0]))
            
            current_item_index += 1

        gui.spacer()
        if total_page_count > 1:
            if gui.button('Next...'):
                actions.user.help_next()
                
            if gui.button("Previous..."):
                actions.user.help_previous()

        if gui.button('Return'):
            actions.user.help_return()

    if gui.button('Refresh'):
        actions.user.help_refresh()

    if gui.button('Close'):
        actions.user.help_hide()

def reset():
    global current_context_page
    global sorted_context_map_keys
    global selected_context
    global selected_context_page
    global cached_window_title
    global show_enabled_contexts_only 

    current_context_page = 1
    sorted_context_map_keys = None
    selected_context = None
    selected_context_page = 1
    cached_window_title = None
    show_enabled_contexts_only = False

def update_active_contexts_cache(active_contexts):
    #print("update_active_contexts_cache")
    global cached_active_contexts_list
    cached_active_contexts_list = active_contexts

#example usage todo: make a list definable in .talon
#overrides = {"generic browser" : "broswer"}
overrides = {}
def refresh_context_command_map(enabled_only = False):
    global context_command_map
    global context_map
    global sorted_context_map_keys
    global show_enabled_contexts_only 
    global cached_window_title
    global context_map

    context_map = {}
    cached_short_context_names = {}
    show_enabled_contexts_only = enabled_only
    cached_window_title = ui.active_window().title
    active_contexts = registry.active_contexts()
    update_active_contexts_cache(active_contexts)
        
    context_command_map = {}
    for context_name, context in registry.contexts.items():
        splits = context_name.split('.')
        if "talon" in splits[-1]:
            short_name = splits[-2].replace("_", " ")
        else:
            short_name = splits[-1].replace("_", " ")

        #print("short name: " + short_name)
        if short_name in overrides:
            short_name = overrides[short_name]

        if enabled_only and context in active_contexts or not enabled_only:
            context_command_map[context_name] = {}
            for __, val in context.commands_get().items():
                #print(str(val.rule.rule) + ": " + val.target.code)
                context_command_map[context_name][str(val.rule.rule)] = val.target.code
            #print(short_name)  
            #print("length: " + str(len(context_command_map[context_name])))
            if len(context_command_map[context_name]) == 0:
                context_command_map.pop(context_name)
            else: 
                cached_short_context_names[short_name] = context_name
                context_map[context_name] = context

    ctx.lists['self.help_contexts'] = cached_short_context_names
    sorted_context_map_keys = sorted(cached_short_context_names)

def refresh_rule_word_map(context_command_map):
    global rule_word_map
    rule_word_map = defaultdict(set)

    for context_name, commands in context_command_map.items():
        for rule in commands:
            tokens = set(token for token in rule.split(' ') if token.isalpha())
            for token in tokens:
                rule_word_map[token].add((context_name, rule))
    
events_registered = False
def register_events(register: bool):
    global events_registered
    if register:
        if not events_registered and live_update:
            events_registered = True
            #registry.register('post:update_contexts', contexts_updated)
            registry.register('update_commands', commands_updated)
    else:
        events_registered = False
        #registry.unregister('post:update_contexts', contexts_updated)
        registry.unregister('update_commands', commands_updated)

@mod.action_class
class Actions:
    def help_alphabet(ab: dict):
        """Provides the alphabet dictionary"""
        # what you say is stored as a trigger
        global alphabet
        alphabet = ab
        reset()
        gui_context_help.hide()        
        gui_alphabet.show()
        register_events(False)
        actions.mode.enable("user.help")

    def help_context_enabled():
        """Display contextual command info"""
        reset()
        refresh_context_command_map(enabled_only=True)
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)
        actions.mode.enable("user.help")       

    def help_context():
        """Display contextual command info"""
        reset()
        refresh_context_command_map()
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)  
        actions.mode.enable("user.help")    

    def help_search(phrase: str):
        """Display command info for search phrase"""
        global search_phrase

        reset()
        search_phrase = phrase
        refresh_context_command_map()
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)
        actions.mode.enable("user.help")      

    def help_selected_context(m: str):
        """Display command info for selected context"""
        global selected_context
        global selected_context_page

        if not gui_context_help.showing:        
            reset()
            refresh_context_command_map()
        else:
            selected_context_page = 1
            update_active_contexts_cache(registry.active_contexts())
        
        selected_context = m
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True) 
        actions.mode.enable("user.help")

    def help_next():
        """Navigates to next page"""
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        if gui_context_help.showing:
            if selected_context is None and search_phrase is None:
                if current_context_page != total_page_count:
                    current_context_page += 1
                else:
                    current_context_page = 1
            else:
                if selected_context_page != total_page_count:
                    selected_context_page += 1
                else:
                    selected_context_page = 1

    def help_select_index(index: int):
        """Select the context by a number"""
        global sorted_context_map_keys, selected_context
        if index < setting_help_max_contexts_per_page.get() and ((current_context_page - 1) * setting_help_max_contexts_per_page.get() + index < len(sorted_context_map_keys)):
            if selected_context is None:
                selected_context = ctx.lists['self.help_contexts'][sorted_context_map_keys[(current_context_page - 1) * setting_help_max_contexts_per_page.get() + index]]
                
    def help_previous():
        """Navigates to previous page"""
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        if gui_context_help.showing:
            if selected_context is None and search_phrase is None:
                if current_context_page != 1:
                    current_context_page -= 1
                else:
                    current_context_page = total_page_count

            else:
                if selected_context_page != 1:
                    selected_context_page -= 1
                else:
                    selected_context_page = total_page_count

    def help_return():
        """Returns to the main help window"""
        global selected_context
        global selected_context_page
        global show_enabled_contexts_only
        
        if gui_context_help.showing:
            refresh_context_command_map(show_enabled_contexts_only)
            selected_context_page = 1
            selected_context = None

    def help_refresh():
        """Refreshes the help"""
        global show_enabled_contexts_only
        global selected_context

        if gui_context_help.showing:
            if selected_context == None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())

    def help_hide():
        """Hides the help"""
        reset()
        gui_alphabet.hide()
        gui_context_help.hide()
        refresh_context_command_map()
        register_events(False)        
        actions.mode.disable("user.help")

@mod.capture
def help_contexts(m) -> str:
    "Returns a context name"

@ctx.capture(rule='{self.help_contexts}')
def help_contexts(m):
    return m.help_contexts

def commands_updated(_):
    update_title()

refresh_context_command_map()

