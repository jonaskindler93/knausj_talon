from talon import Context, Module

simple_vocabulary = [
"nmap",
    "admin",
    "Cisco",
    "Citrix",
    "VPN",
    "DNS",
    "minecraft",
    "mac",
    "slotcar",
    "bibtex",
    "git",
    "numpy",
    "tensorflow",
    "CPC",
    "contrastive predictive coding",
    "autocrane",
    "stellaris",
    "boolean",
    "array",
    "keras",
    "github",
    "azure",
    "timestamp",
    "autocrane",
    "webcam",
    "yeti",
    "subset",
    "azure",
    "zip",    
]

mapping_vocabulary = {
    "i": "I",
    "i'm": "I'm",
    "i've": "I've",
    "i'll": "I'll",
    "i'd": "I'd",
    "corry":"Psiori",  
    "sim see":"SimCLR",
    "herds": "Hertz",
    "pv seen it": "PWC-Net",
    "flownet": "FlowNet2",
    "mobilenet": "MobileNetV2",
    "SSD": "SSD",
    "and stall": "install",
    "recognising": "recognizing",
    "recognise": "recognize",
    "recognised": "recognized",
    "addio": "audio",
    "the vice": "device",
    "ap": "app",
    "curse her": "cursor",
    "i": "I",
    "i'm": "I'm",
    "i've": "I've",
    "i'll": "I'll",
    "i'd": "I'd",
    "mack oh ess": "macOS",
    "mack book": "macbook",
    "vender": "vendor",
    "corry":"Psiori",
    "makefile":"Makefile",
    "see vee":"cv",
    "open see vee":"opencv",
    "mat plot lib":"matplotlib",

}

mapping_vocabulary.update(dict(zip(simple_vocabulary, simple_vocabulary)))

mod = Module()

def remove_dragon_junk(word):
    return str(word).lstrip("\\").split("\\")[0]

@mod.capture(rule='({user.vocabulary} | <word>)')
def word(m) -> str:
    try: return m.vocabulary
    except AttributeError: return remove_dragon_junk(m.word)

@mod.capture(rule='(<user.word> | <phrase>)+')
def text(m) -> str:
    #todo: use actions.dicate.parse_words for better dragon support once supported
    words = str(m).split(' ')
    i = 0
    while i < len(words):
        words[i] = remove_dragon_junk(words[i])
        i += 1

    return ' '.join(words)

mod.list('vocabulary', desc='user vocabulary')

ctx = Context()

# setup the word map too
ctx.settings['dictate.word_map'] = mapping_vocabulary
ctx.lists['user.vocabulary'] = mapping_vocabulary
