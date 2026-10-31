# code | English name | native name | first letter(s) in that language's own script
RAW = """en|English|English|E
hi|Hindi|हिन्दी|हि
te|Telugu|తెలుగు|తె
ta|Tamil|தமிழ்|த
kn|Kannada|ಕನ್ನಡ|ಕ
ml|Malayalam|മലയാളം|മ
bn|Bengali|বাংলা|বা
mr|Marathi|मराठी|म
gu|Gujarati|ગુજરાતી|ગુ
pa|Punjabi|ਪੰਜਾਬੀ|ਪੰ
ur|Urdu|اردو|ا
or|Odia|ଓଡ଼ିଆ|ଓ
as|Assamese|অসমীয়া|অ
ne|Nepali|नेपाली|ने
sa|Sanskrit|संस्कृतम्|सं
sd|Sindhi|سنڌي|س
gom|Konkani|कोंकणी|को
mai|Maithili|मैथिली|मै
doi|Dogri|डोगरी|डो
bho|Bhojpuri|भोजपुरी|भो
mni-Mtei|Meiteilon (Manipuri)|ꯃꯩꯇꯩꯂꯣꯟ|ꯃ
lus|Mizo|Mizo|M
si|Sinhala|සිංහල|සි
es|Spanish|Español|E
fr|French|Français|F
de|German|Deutsch|D
it|Italian|Italiano|I
pt|Portuguese|Português|P
ru|Russian|Русский|Р
ja|Japanese|日本語|日
zh-CN|Chinese (Simplified)|中文|中
zh-TW|Chinese (Traditional)|繁體中文|繁
ko|Korean|한국어|한
ar|Arabic|العربية|ع
fa|Persian|فارسی|ف
he|Hebrew|עברית|ע
tr|Turkish|Türkçe|T
nl|Dutch|Nederlands|N
pl|Polish|Polski|P
uk|Ukrainian|Українська|У
el|Greek|Ελληνικά|Ε
sv|Swedish|Svenska|S
da|Danish|Dansk|D
fi|Finnish|Suomi|S
cs|Czech|Čeština|Č
ro|Romanian|Română|R
hu|Hungarian|Magyar|M
th|Thai|ไทย|ไ
vi|Vietnamese|Tiếng Việt|T
id|Indonesian|Bahasa Indonesia|B
ms|Malay|Bahasa Melayu|B
tl|Filipino|Filipino|F
my|Burmese|မြန်မာ|မ
km|Khmer|ខ្មែរ|ខ
lo|Lao|ລາວ|ລ
sw|Swahili|Kiswahili|K
am|Amharic|አማርኛ|አ
af|Afrikaans|Afrikaans|A
ka|Georgian|ქართული|ქ
hy|Armenian|Հայերեն|Հ
mn|Mongolian|Монгол|М"""
LANGS = [dict(c=c, e=e, n=n, g=g) for c, e, n, g in (l.split("|") for l in RAW.splitlines())]
NAMES = {l["c"]: l["e"] for l in LANGS}
