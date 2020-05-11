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
]
mapping_vocabulary = {
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
}

mapping_vocabulary.update(dict(zip(simple_vocabulary, simple_vocabulary)))

# Sometimes my capture results in vocabulary words getting inserted as the key
# with the '@' prefix instead of the value, and idk why, but this fixes it by
# manually mapping those in post
def word_map_bug_fix(word: str) -> str:
    if word[0] == "@":
        return mapping_vocabulary[word[1:]] or word
    else:
        return word


mod = Module()


@mod.capture(rule="{user.vocabulary}")
def word(m) -> str:
    return m.vocabulary


@mod.capture(rule="(<user.word> | <phrase>)+")
def text(m) -> str:
    return " ".join(map(word_map_bug_fix, str(m).split(" ")))


mod.list("vocabulary", desc="user vocabulary")

ctx = Context()

ctx.lists["user.vocabulary"] = mapping_vocabulary
