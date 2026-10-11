#!/usr/bin/env python3
"""
HisabCulator site generator.

Run from the project root:   python3 tools/build.py

It writes plain static HTML into ./site (shared navbar, footer and head are generated
from one place, so every page stays consistent and SEO tags are real HTML, not injected).
To add a tool: add an entry to TOOLS, add its UI function to UI, add a script in site/assets/js.
"""
import json, os, html, shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')

# ---------------------------------------------------------------- config
SITE_NAME = 'HisabCulator'
SITE_URL = ''                                   # e.g. 'https://hisabculator.com' (no trailing slash). Empty = no canonical/sitemap
CONTACT_EMAIL = 'hello@hisabculator.example'    # TODO: replace with your real address (the contact form uses it)
CONTACT_PHONE = ''                              # optional, leave empty to hide
CONTACT_LOCATION = 'Bangladesh'
SOCIAL = {}                                     # e.g. {'Facebook': 'https://facebook.com/yourpage'}; empty hides the row
DEVELOPER = 'Md. Ashraful Islam'

# ---------------------------------------------------------------- helpers
def L(en, bn):
    return f'<span data-bn="{bn}">{en}</span>'

def esc(s):
    return html.escape(s, quote=True)

ICONS = {
    'calculator': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>',
    'sigma': '<path d="M18 5H6l6 7-6 7h12"/>',
    'percent': '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2"/><circle cx="17" cy="17" r="2"/>',
    'tag': '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="8.5" r="1"/>',
    'currency': '<circle cx="12" cy="12" r="9"/><path d="M15 9.5a3 2.2 0 0 0-3-1.5c-1.7 0-3 .8-3 2s1.2 1.7 3 2 3 .8 3 2-1.300 2-3 2a3 2.200 0 0 1-3-1.500M12 6v2M12 16v2"/>',
    'ruler': '<path d="M3 15L15 3l6 6L9 21z"/><path d="M7 11l2 2M10 8l2 2M13 5l2 2"/>',
    'scale': '<path d="M12 4v16M6 20h12M5 8h14"/><path d="M5 8l-3 7a3 3 0 0 0 6 0zM19 8l-3 7a3 3 0 0 0 6 0z"/>',
    'thermo': '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/>',
    'cap': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
    'book': '<path d="M4 4h10a4 4 0 0 1 4 4v12H8a4 4 0 0 1-4-4z"/><path d="M8 20a4 4 0 0 1-4-4"/>',
    'award': '<circle cx="12" cy="9" r="6"/><path d="M8.500 14L7 22l5-3 5 3-1.500-8"/>',
    'heart': '<path d="M20.800 5.600a5 5 0 0 0-7.100 0L12 7.300l-1.700-1.700a5 5 0 0 0-7.100 7.100L12 21l8.800-8.300a5 5 0 0 0 0-7.100z"/>',
    'flame': '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.900 4.900l1.400 1.400M17.700 17.700l1.400 1.400M2 12h2M20 12h2M4.900 19.100l1.400-1.400M17.700 6.300l1.400-1.400"/>',
    'moon': '<path d="M21 12.800A9 9 0 1 1 11.200 3 7 7 0 0 0 21 12.800z"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'chev': '<path d="M6 9l6 6 6-6"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    'phone': '<path d="M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    'pin': '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.500"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    'swap': '<path d="M7 4L3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7"/>',
}

def ico(name, cls='ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

CATS = [
    ('calculators', 'Calculators', 'ক্যালকুলেটর', 'calculator'),
    ('converters', 'Converters', 'রূপান্তর', 'swap'),
    ('education', 'Education', 'শিক্ষা', 'cap'),
    ('fitness', 'Fitness', 'ফিটনেস', 'heart'),
    ('date-time', 'Date & Time', 'তারিখ ও সময়', 'calendar'),
]
CAT = {c[0]: c for c in CATS}

# ---------------------------------------------------------------- tool registry
TOOLS = [
 dict(cat='calculators', slug='basic', ic='calculator', pop=True, en='Basic Calculator', bn='মৌলিক ক্যালকুলেটর',
      d_en='Quick calculations for everyday use.', d_bn='দৈনন্দিন হিসাবের জন্য দ্রুত ক্যালকুলেটর।',
      meta='Free online basic calculator with percentage, brackets, history and keyboard support. Works in English and Bangla digits.',
      howto=['Type with your keyboard or tap the keys.', 'Use brackets and % when you need them. The answer previews as you type.', 'Press = or Enter to save it to history. Tap a history line to reuse the answer.'],
      example='<code>250 + 15%</code> gives <b>287.5</b> (15% of 250 is added). <code>(120 − 20) ÷ 4</code> gives <b>25</b>.',
      faq=[('How does % work?', 'Alone, 50% means 0.5. After + or −, 10% means 10% of the number before it, so 200 + 10% is 220.'),
           ('Can I type Bangla digits?', 'Yes. ১২ + ৩ works. Turn on বাংলা to see answers in Bangla digits.'),
           ('Is my history saved?', 'The last 15 calculations are kept in your own browser only. Clear them any time.')],
      related=['scientific', 'percentage', 'discount']),
 dict(cat='calculators', slug='scientific', ic='sigma', pop=True, en='Scientific Calculator', bn='বৈজ্ঞানিক ক্যালকুলেটর',
      d_en='Advanced mathematical calculations.', d_bn='ত্রিকোণমিতি, লগ, বর্গমূল ও আরও অনেক ফাংশন।',
      meta='Online scientific calculator with sin, cos, tan, log, ln, square root, powers, factorial, degrees/radians and history.',
      howto=['Pick Degrees or Radians for trigonometry.', 'Type an expression such as sin(30) + 2^3, or use the keys.', 'Press = or Enter. Use Ans to reuse the last answer.'],
      example='<code>sin(30)</code> in degrees is <b>0.5</b>. <code>√(144) + 5!</code> is <b>132</b>. <code>2^10</code> is <b>1024</b>.',
      faq=[('Which functions are supported?', 'sin, cos, tan, asin, acos, atan, ln, log (base 10), sqrt, cbrt, abs, exp, plus π, e, powers (^), factorial (!) and %.'),
           ('Is it safe?', 'Yes. Expressions are read by a small built-in parser. Nothing you type is run as code.'),
           ('Why does tan(90) show an error?', 'In degrees, tan(90) is undefined, so the calculator says so instead of showing a huge number.')],
      related=['basic', 'percentage', 'length']),
 dict(cat='calculators', slug='percentage', ic='percent', pop=True, en='Percentage Calculator', bn='শতকরা ক্যালকুলেটর',
      d_en='Calculate percentages quickly and easily.', d_bn='সহজে শতকরা হিসাব করুন।',
      meta='Percentage calculator: find X% of a number, what percent one number is of another, percentage change, and add or subtract a percentage.',
      howto=['Pick the question that matches yours.', 'Fill in the two numbers.', 'The answer appears as you type.'],
      example='15% of 2,000 is <b>300</b>. 45 is <b>18%</b> of 250. Going from 80 to 100 is a <b>25% increase</b>.',
      faq=[('Percentage change vs. percentage points?', 'Going from 10% to 15% is a 5 percentage point rise, but a 50% increase in the rate itself.'),
           ('Why is "what percent" an error when the second number is 0?', 'You cannot divide by zero, so there is no percentage to show.')],
      related=['discount', 'basic', 'scientific']),
 dict(cat='calculators', slug='discount', ic='tag', pop=False, en='Discount Calculator', bn='ডিসকাউন্ট ক্যালকুলেটর',
      d_en='Find discounts, final prices and savings.', d_bn='ছাড়ের পর দাম ও সাশ্রয় বের করুন।',
      meta='Discount calculator in BDT: final price after one or two discounts, optional VAT, and the discount percentage from original and sale prices.',
      howto=['Enter the original price and the discount %.', 'Add a second discount or VAT only if you need them.', 'Read the final price and how much you save.'],
      example='৳ 2,000 with 20% off and a further 10% off costs <b>৳ 1,440.00</b>. You save ৳ 560.00 (28% in total).',
      faq=[('Are two discounts added together?', 'No. The second discount applies to the already reduced price, so 20% then 10% is 28% in total, not 30%.'),
           ('Which VAT rate should I use?', 'Check the rate that applies to your product. 15% is the standard VAT rate in Bangladesh, but some items differ.')],
      related=['percentage', 'basic', 'currency']),
 dict(cat='converters', slug='currency', ic='currency', pop=True, en='Currency Converter', bn='মুদ্রা রূপান্তর',
      d_en='Convert currencies quickly.', d_bn='এক মুদ্রা থেকে অন্য মুদ্রায় রূপান্তর।',
      meta='Currency converter with BDT, USD, EUR, GBP, INR, SAR, AED and more. Edit rates or fetch the latest ones.',
      howto=['Enter an amount and choose the two currencies.', 'Press "Fetch latest rates" for up-to-date numbers, or edit any rate yourself.', 'Use the swap button to reverse the direction.'],
      example='With USD 1 = BDT 122, <b>USD 50</b> is about <b>BDT 6,100</b>.',
      faq=[('Are these live rates?', 'Not by default. The built-in rates are approximate. "Fetch latest rates" asks a free public service (open.er-api.com) for current numbers; if you are offline it tells you so.'),
           ('Are these the rates my bank or exchange will give me?', 'No. Banks and money changers add their own margin, so use this as a guide only.')],
      related=['discount', 'length', 'weight']),
 dict(cat='converters', slug='length', ic='ruler', pop=False, en='Length Converter', bn='দৈর্ঘ্য রূপান্তর',
      d_en='Convert common length units.', d_bn='মিটার, ফুট, ইঞ্চি, হাতসহ একক রূপান্তর।',
      meta='Length converter for mm, cm, metre, km, inch, foot, yard, mile and the Bangladeshi hat (cubit).',
      howto=['Enter a value.', 'Pick the unit you have and the unit you want.', 'The full table below shows every unit at once.'],
      example='<b>6 ft</b> is <b>1.8288 m</b> or about 182.88 cm. <b>1 hat</b> is 18 inches (0.4572 m).',
      faq=[('How long is a hat?', 'Taken here as 18 inches (0.4572 m), the common cubit. Local usage can vary slightly.')],
      related=['weight', 'temperature', 'scientific']),
 dict(cat='converters', slug='weight', ic='scale', pop=False, en='Weight Converter', bn='ওজন রূপান্তর',
      d_en='Convert different weight units.', d_bn='কেজি, পাউন্ড, মণ, সের, তোলাসহ।',
      meta='Weight converter for kg, gram, pound, ounce, tonne and Bangladeshi units: maund (mon), seer and tola.',
      howto=['Enter a value.', 'Pick the unit you have and the unit you want.', 'Check the table below for every other unit.'],
      example='<b>1 maund (মণ)</b> is about <b>37.32 kg</b>. <b>1 seer (সের)</b> is about <b>0.933 kg</b>. <b>1 tola</b> is about <b>11.66 g</b>.',
      faq=[('What are the maund and seer values?', 'This page uses the metric-standard values: 1 maund = 40 seer = 37.3242 kg, and 1 tola = 11.6638 g.')],
      related=['length', 'temperature', 'bmi']),
 dict(cat='converters', slug='temperature', ic='thermo', pop=False, en='Temperature Converter', bn='তাপমাত্রা রূপান্তর',
      d_en='Convert Celsius, Fahrenheit and other temperature units.', d_bn='সেলসিয়াস, ফারেনহাইট ও কেলভিন।',
      meta='Temperature converter between Celsius, Fahrenheit, Kelvin and Rankine with all results shown together.',
      howto=['Enter a temperature.', 'Choose the scale you have and the one you want.', 'All scales are listed below.'],
      example='<b>37 °C</b> is <b>98.6 °F</b>. <b>0 °C</b> is <b>273.15 K</b>.',
      faq=[('Formula for °C to °F?', '°F = °C × 9/5 + 32.')],
      related=['length', 'weight', 'basic']),
 dict(cat='education', slug='gpa', ic='cap', pop=True, en='GPA Calculator', bn='জিপিএ ক্যালকুলেটর',
      d_en='Pick grades per subject and get your GPA, with 4th subject support.', d_bn='বিষয়ভিত্তিক গ্রেড দিয়ে জিপিএ বের করুন, ৪র্থ বিষয়সহ।',
      meta='GPA calculator for Bangladesh: SSC/HSC 5.00 scale with 4th subject handling, or university 4.00 scale weighted by credits.',
      howto=['Choose the board (5.00) or university (4.00) scale.', 'Choose a grade for every subject. For the board scale, tick the 4th subject if you have one. For university, add credits.', 'Your GPA updates as soon as every row is filled.'],
      example='Six subjects at A+, A+, A, A, A-, B with no 4th subject: (5+5+4+4+3.5+3)/6 = <b>4.08</b>. Add a 4th subject with A+ (5 − 2 = 3 bonus points): (24.5+3)/6 = <b>4.58</b>.',
      faq=[('How does the 4th subject work?', 'Only the points above 2.00 count. A 4th subject with grade point 3.5 adds 1.5 to the total. It can raise your GPA but never lower it, and the GPA stops at 5.00.'),
           ('What if I fail a subject?', 'A grade F in any compulsory subject means the result is fail (GPA 0.00). Failing the 4th subject does not fail you; it just adds nothing.'),
           ('Where do these grade points come from?', 'The standard general-education board scale: A+ 5.00, A 4.00, A- 3.50, B 3.00, C 2.00, D 1.00, F 0.00.')],
      related=['ssc-hsc-gpa', 'cgpa', 'percentage']),
 dict(cat='education', slug='cgpa', ic='book', pop=True, en='CGPA Calculator', bn='সিজিপিএ ক্যালকুলেটর',
      d_en='Calculate university CGPA from semesters or courses.', d_bn='সেমিস্টার বা কোর্স থেকে বিশ্ববিদ্যালয়ের সিজিপিএ হিসাব।',
      meta='CGPA calculator for Bangladeshi universities: credit-weighted CGPA from semester GPAs or individual course grades on the 4.00 scale.',
      howto=['Pick "By semester" (GPA and credits) or "By course" (grade and credits).', 'Fill in each row. Leave unused rows empty.', 'Read your CGPA and total credits.'],
      example='Semester 1: GPA 3.50 with 15 credits. Semester 2: GPA 3.80 with 18 credits. CGPA = (3.50×15 + 3.80×18) / 33 = <b>3.66</b>.',
      faq=[('Why credits?', 'A 4-credit course should count more than a 1-credit one, so each GPA is weighted by its credits.'),
           ('Does my university use the same scale?', 'Most use the UGC 4.00 scale (A+ = 4.00 for 80% and above). Cut-offs differ in places, so check your own grade sheet.')],
      related=['gpa', 'ssc-hsc-gpa', 'percentage']),
 dict(cat='education', slug='ssc-hsc-gpa', ic='award', pop=False, en='SSC/HSC GPA', bn='এসএসসি/এইচএসসি জিপিএ',
      d_en='Enter marks, get grades and your board GPA.', d_bn='নম্বর দিন, গ্রেড ও বোর্ড জিপিএ পান।',
      meta='SSC and HSC GPA calculator from marks: automatic letter grades and grade points, fail detection and 4th subject handling.',
      howto=['Choose SSC or HSC to load a typical subject list, then edit names or add and remove rows.', 'Enter marks out of 100 for each subject. Combine paper 1 and paper 2 into one mark out of 100.', 'Tick the 4th subject. Read your GPA and grade.'],
      example='Marks of 85, 72, 66, 91, 58, 77 and a 4th subject at 80 (A+). Compulsory points: 5+4+3.5+5+3+4 = 24.5. Bonus 5 − 2 = 3. GPA = 27.5 / 6 = <b>4.58</b>.',
      faq=[('Marks to grade table?', '80–100 A+ (5.00), 70–79 A (4.00), 60–69 A- (3.50), 50–59 B (3.00), 40–49 C (2.00), 33–39 D (1.00), below 33 F (0.00).'),
           ('Is this my official result?', 'No. Official results come from your education board. Use this to check or plan. Some subjects have separate pass marks for each part, which this page does not check.')],
      related=['gpa', 'cgpa', 'percentage']),
 dict(cat='fitness', slug='bmi', ic='heart', pop=True, en='BMI Calculator', bn='বিএমআই ক্যালকুলেটর',
      d_en='Check BMI and understand your range.', d_bn='বিএমআই দেখুন এবং আপনার ক্যাটাগরি জানুন।',
      meta='BMI calculator with metric or feet/inches and kg/lb inputs. Choose WHO or South Asian ranges and see your healthy weight range.',
      howto=['Pick metric or feet/inches.', 'Enter height and weight.', 'Choose WHO or Asian ranges and read your category.'],
      example='170 cm and 65 kg: BMI = 65 / 1.7² = <b>22.5</b>, Normal in both WHO and Asian ranges.',
      faq=[('WHO or Asian ranges?', 'WHO: overweight starts at 25. For South Asian adults, the WHO Asia-Pacific guidance uses 23, because health risks rise at lower BMI. Ask your doctor which applies to you.'),
           ('Is BMI reliable?', 'It is a screening number. It does not separate muscle from fat and is not meant for children, pregnancy or athletes.')],
      related=['calorie', 'weight', 'age']),
 dict(cat='fitness', slug='calorie', ic='flame', pop=False, en='Calorie Calculator', bn='ক্যালোরি ক্যালকুলেটর',
      d_en='Estimate daily calorie requirements.', d_bn='প্রতিদিনের ক্যালোরির প্রয়োজন আনুমানিক হিসাব।',
      meta='Daily calorie calculator using the Mifflin-St Jeor equation: BMR, maintenance calories and a target to lose or gain weight.',
      howto=['Enter sex, age, height and weight.', 'Pick your activity level and goal.', 'Read your BMR, maintenance calories and daily target.'],
      example='A 30-year-old man, 175 cm, 72 kg, lightly active: BMR ≈ 1,669 kcal, maintenance ≈ 2,295 kcal.',
      faq=[('Which formula is used?', 'Mifflin-St Jeor: 10×kg + 6.25×cm − 5×age, then +5 for men or −161 for women, times an activity factor.'),
           ('How fast should I lose weight?', 'The "lose" goal subtracts 500 kcal a day, roughly 0.5 kg a week. Slower is fine too. See a doctor or dietitian for medical conditions.')],
      related=['bmi', 'weight', 'age']),
 dict(cat='date-time', slug='age', ic='user', pop=True, en='Age Calculator', bn='বয়স ক্যালকুলেটর',
      d_en='Calculate exact age from date of birth.', d_bn='জন্মতারিখ থেকে সঠিক বয়স হিসাব করুন।',
      meta='Age calculator: exact age in years, months and days, total days and hours lived, weekday of birth and next birthday countdown.',
      howto=['Pick your date of birth.', 'Leave "Age on" as today, or choose another date.', 'Read your age and next birthday.'],
      example='Born 15 March 2000, on 7 October 2026: <b>26 years 6 months 22 days</b>.',
      faq=[('Born on 29 February?', 'In non-leap years the birthday is counted on 1 March.'),
           ('Can I find age on a past or future date?', 'Yes. Change the "Age on" date, for example to the closing date of a job circular.')],
      related=['date-difference', 'time', 'bmi']),
 dict(cat='date-time', slug='date-difference', ic='calendar', pop=False, en='Date Difference', bn='তারিখের ব্যবধান',
      d_en='Find the difference between two dates.', d_bn='দুই তারিখের মধ্যে কত দিন তা বের করুন।',
      meta='Date difference calculator: years, months, days, weeks and weekdays between two dates, with an option to include the end date.',
      howto=['Pick the start and end dates.', 'Tick "include end date" if both days should count.', 'Read the difference.'],
      example='1 January 2026 to 31 March 2026 is <b>2 months 30 days</b>, or <b>89 days</b> (90 if you include the end date).',
      faq=[('What are weekdays?', 'Monday to Friday. Bangladesh weekends are Friday and Saturday, and public holidays are not subtracted, so treat this as a guide for working-day counts.')],
      related=['age', 'time', 'basic']),
 dict(cat='date-time', slug='time', ic='clock', pop=False, en='Time Calculator', bn='সময় ক্যালকুলেটর',
      d_en='Perform time-related calculations.', d_bn='সময় যোগ, বিয়োগ ও ব্যবধান নির্ণয়।',
      meta='Time calculator: add or subtract durations, find the time between two clock times, or add hours and minutes to a clock time.',
      howto=['Pick the card that matches your question.', 'Fill in the fields.', 'Results update as you type.'],
      example='2 h 45 min + 1 h 30 min = <b>4 h 15 min</b>. From 10:30 PM to 6:15 AM is <b>7 h 45 min</b>.',
      faq=[('Can the time go past midnight?', 'Yes. The clock card shows the new time and tells you if it moved to the next or previous day.')],
      related=['date-difference', 'age', 'basic']),
]
TOOL = {t['slug']: t for t in TOOLS}
POPULAR = ['basic', 'scientific', 'gpa', 'cgpa', 'percentage', 'bmi', 'currency', 'age']

def tpath(t):
    return f"{t['cat']}/{t['slug']}.html"

# ---------------------------------------------------------------- form helpers
def field(id, en, bn, ph='', val='', hint='', mode='decimal', cls=''):
    h = f'<p class="hint">{hint}</p>' if hint else ''
    return (f'<div class="field {cls}"><label for="{id}">{L(en, bn)}</label>'
            f'<input type="text" inputmode="{mode}" autocomplete="off" id="{id}" placeholder="{ph}" value="{val}">{h}</div>')

def select(id, en, bn, opts, cls='', attrs=''):
    o = ''.join(f'<option value="{v}" data-bn="{b}">{e}</option>' for v, e, b in opts)
    return f'<div class="field {cls}"><label for="{id}">{L(en, bn)}</label><select id="{id}" {attrs}>{o}</select></div>'

def result(id):
    return f'<div class="result" id="{id}" role="status" aria-live="polite"></div>'

def key(label, v=None, act=None, cls=''):
    a = f'data-act="{act}"' if act else f'data-v="{v if v is not None else label}"'
    return f'<button type="button" class="key {cls}" {a}>{label}</button>'

def numpad():
    r = [key('AC', act='clear', cls='clr'), key('⌫', act='back', cls='op'), key('%', cls='op'), key('÷', cls='op'),
         key('7'), key('8'), key('9'), key('×', cls='op'), key('4'), key('5'), key('6'), key('−', cls='op'),
         key('1'), key('2'), key('3'), key('+', cls='op'), key('0'), key('.'), key('(', cls='op'), key(')', cls='op'),
         key('=', act='eq', cls='eq')]
    return '<div class="keys">' + ''.join(r) + '</div>'

def screen():
    return ('<div class="screen"><label class="sr" for="expr">' + L('Expression', 'এক্সপ্রেশন') + '</label>'
            '<input type="text" id="expr" inputmode="none" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="0">'
            '<output id="res" for="expr" aria-live="polite">0</output></div>')

def history():
    return ('<div class="hist"><div class="hist-h"><strong>' + L('History', 'ইতিহাস') + '</strong>'
            '<button type="button" class="btn ghost sm" id="hist-clear">' + L('Clear', 'মুছুন') + '</button></div><ul id="hist-list"></ul></div>')

def body_fields(extra_top=''):
    return ('<div id="bodyform">' + extra_top +
        '<div class="frow">' + select('bu', 'Units', 'একক', [('metric', 'Metric (cm, kg)', 'মেট্রিক (সেমি, কেজি)'), ('imperial', 'Feet/inches, pounds', 'ফুট/ইঞ্চি, পাউন্ড')]) + '</div>'
        '<div class="frow">'
        '<div class="field" data-u="metric">' + f'<label for="hcm">{L("Height (cm)", "উচ্চতা (সেমি)")}</label><input type="text" inputmode="decimal" id="hcm" placeholder="170" autocomplete="off"></div>'
        '<div class="field" data-u="imperial" hidden>' + f'<label for="hft">{L("Height (feet)", "উচ্চতা (ফুট)")}</label><input type="text" inputmode="decimal" id="hft" placeholder="5" autocomplete="off"></div>'
        '<div class="field" data-u="imperial" hidden>' + f'<label for="hin">{L("Inches", "ইঞ্চি")}</label><input type="text" inputmode="decimal" id="hin" placeholder="7" autocomplete="off"></div>'
        '<div class="field">' + f'<label for="wv"><span data-u="metric">{L("Weight (kg)", "ওজন (কেজি)")}</span><span data-u="imperial" hidden>{L("Weight (lb)", "ওজন (পাউন্ড)")}</span></label><input type="text" inputmode="decimal" id="wv" placeholder="65" autocomplete="off"></div>'
        '</div></div>')

# ---------------------------------------------------------------- tool UIs
def ui_basic():
    return f'<div class="card calc" data-calc="basic">{screen()}{numpad()}{history()}</div>'

def ui_scientific():
    def fnrow(items):
        return ''.join(key(l, v=v, cls='sm') for l, v in items)
    fn = [('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('ln', 'ln('), ('log', 'log('),
          ('sin⁻¹', 'asin('), ('cos⁻¹', 'acos('), ('tan⁻¹', 'atan('), ('√', '√('), ('xʸ', '^'),
          ('π', 'π'), ('e', 'e'), ('∛', 'cbrt('), ('10ˣ', '10^'), ('n!', '!'),
          ('x²', '^2'), ('x⁻¹', '^(-1)'), ('|x|', 'abs('), ('eˣ', 'exp('), ('Ans', 'ans')]
    return ('<div class="card calc sci" data-calc="sci">' + screen() +
        '<div class="modebar"><span class="note">' + L('Trig mode', 'ত্রিকোণমিতি মোড') + '</span><button type="button" class="btn ghost sm" id="angle"></button></div>'
        '<div class="sci-body"><div class="keys fn">' + fnrow(fn) + '</div>' + numpad() + '</div>' + history() + '</div>')

def pct_card(kind, title_en, title_bn, a_en, a_bn, b_en, b_bn, op=''):
    return (f'<div class="card" data-pct="{kind}"><h2>{L(title_en, title_bn)}</h2>{op}<div class="frow">'
            f'<div class="field"><label>{L(a_en, a_bn)}<input type="text" inputmode="decimal" data-k="a" autocomplete="off"></label></div>'
            f'<div class="field"><label>{L(b_en, b_bn)}<input type="text" inputmode="decimal" data-k="b" autocomplete="off"></label></div></div>'
            f'<div class="result" role="status" aria-live="polite"></div></div>')

def ui_percentage():
    opsel = ('<div class="field" style="margin-bottom:1rem"><label>' + L('Action', 'কাজ') + '<select data-k="op"><option value="plus" data-bn="বাড়ান">Increase</option><option value="minus" data-bn="কমান">Decrease</option></select></label></div>')
    return ('<div class="two">' +
        pct_card('of', 'What is X% of Y?', 'Y এর X% কত?', 'Percentage (X)', 'শতকরা (X)', 'Number (Y)', 'সংখ্যা (Y)') +
        pct_card('what', 'X is what % of Y?', 'X হলো Y এর কত শতাংশ?', 'X', 'X', 'Y', 'Y') +
        pct_card('chg', 'Percentage change', 'শতকরা পরিবর্তন', 'From', 'শুরু', 'To', 'শেষ') +
        pct_card('add', 'Increase or decrease by %', 'শতাংশ হারে বাড়ান বা কমান', 'Percentage', 'শতকরা', 'Number', 'সংখ্যা', opsel) + '</div>')

def ui_discount():
    return ('<div class="two"><form class="card" id="disc" onsubmit="return false"><h2>' + L('Price after discount', 'ছাড়ের পর দাম') + '</h2>'
        '<div class="frow">' + field('d-price', 'Original price (৳)', 'আসল দাম (৳)', '2000') + field('d-pct', 'Discount (%)', 'ছাড় (%)', '20') + '</div>'
        '<div class="frow">' + field('d-extra', 'Extra discount (%), optional', 'অতিরিক্ত ছাড় (%), ঐচ্ছিক', '10') + field('d-tax', 'VAT / tax (%), optional', 'ভ্যাট / ট্যাক্স (%), ঐচ্ছিক', '15') + '</div>'
        + result('disc-res') + '</form>'
        '<form class="card" id="rev" onsubmit="return false"><h2>' + L('Find the discount %', 'ছাড়ের শতকরা হার বের করুন') + '</h2>'
        '<div class="frow">' + field('r-orig', 'Original price (৳)', 'আসল দাম (৳)', '1500') + field('r-sale', 'Sale price (৳)', 'বিক্রয় মূল্য (৳)', '1200') + '</div>'
        + result('rev-res') + '</form></div>')

UNITS = {
 'length': dict(type='linear', def_=['m', 'ft'], units=[
   ('mm', 'Millimetre', 'মিলিমিটার', 0.001), ('cm', 'Centimetre', 'সেন্টিমিটার', 0.01), ('m', 'Metre', 'মিটার', 1), ('km', 'Kilometre', 'কিলোমিটার', 1000),
   ('in', 'Inch', 'ইঞ্চি', 0.0254), ('ft', 'Foot', 'ফুট', 0.3048), ('yd', 'Yard', 'গজ', 0.9144), ('mi', 'Mile', 'মাইল', 1609.344), ('hat', 'Hat (cubit)', 'হাত', 0.4572)]),
 'weight': dict(type='linear', def_=['kg', 'lb'], units=[
   ('mg', 'Milligram', 'মিলিগ্রাম', 1e-6), ('g', 'Gram', 'গ্রাম', 0.001), ('kg', 'Kilogram', 'কেজি', 1), ('t', 'Tonne', 'মেট্রিক টন', 1000),
   ('oz', 'Ounce', 'আউন্স', 0.028349523125), ('lb', 'Pound', 'পাউন্ড', 0.45359237), ('tola', 'Tola', 'তোলা', 0.0116638), ('seer', 'Seer', 'সের', 0.93310), ('maund', 'Maund (mon)', 'মণ', 37.3242)]),
 'temperature': dict(type='temp', def_=['C', 'F'], units=[
   ('C', 'Celsius', 'সেলসিয়াস', 1), ('F', 'Fahrenheit', 'ফারেনহাইট', 1), ('K', 'Kelvin', 'কেলভিন', 1), ('R', 'Rankine', 'র‍্যাঙ্কিন', 1)]),
}
SYM = {'mm': 'mm', 'cm': 'cm', 'm': 'm', 'km': 'km', 'in': 'in', 'ft': 'ft', 'yd': 'yd', 'mi': 'mi', 'hat': 'hat', 'mg': 'mg', 'g': 'g', 'kg': 'kg', 't': 't', 'oz': 'oz', 'lb': 'lb',
       'tola': 'tola', 'seer': 'seer', 'maund': 'maund', 'C': '°C', 'F': '°F', 'K': 'K', 'R': '°R'}

def ui_converter(kind):
    u = UNITS[kind]
    cfg = {'type': u['type'], 'def': u['def_'], 'units': [dict(k=k, n=n, bn=b, f=f, s=SYM[k]) for k, n, b, f in u['units']]}
    d0 = '25' if kind == 'temperature' else '1'
    return ('<div class="card"><script type="application/json" id="cv-cfg">' + json.dumps(cfg, ensure_ascii=False) + '</script>'
        '<div class="frow">' + field('cv-val', 'Value', 'মান', d0, d0) +
        '<div class="field"><label for="cv-from">' + L('From', 'থেকে') + '</label><select id="cv-from"></select></div>'
        '<div class="field"><label for="cv-to">' + L('To', 'এতে') + '</label><select id="cv-to"></select></div>'
        '<div class="field swap"><button type="button" class="btn ghost" id="cv-swap" aria-label="Swap units">' + ico('swap') + L('Swap', 'বদল') + '</button></div></div>'
        + result('cv-res') + '<div class="tbl-wrap"><table><thead><tr><th>' + L('Unit', 'একক') + '</th><th>' + L('Value', 'মান') + '</th></tr></thead><tbody id="cv-all"></tbody></table></div></div>')

def ui_currency():
    return ('<div class="card"><div class="frow">' + field('cur-amt', 'Amount', 'পরিমাণ', '100', '100') +
        '<div class="field"><label for="cur-from">' + L('From', 'থেকে') + '</label><select id="cur-from"></select></div>'
        '<div class="field"><label for="cur-to">' + L('To', 'এতে') + '</label><select id="cur-to"></select></div>'
        '<div class="field swap"><button type="button" class="btn ghost" id="cur-swap" aria-label="Swap currencies">' + ico('swap') + L('Swap', 'বদল') + '</button></div></div>'
        + result('cur-res') + '<p class="note" id="cur-status" style="margin-top:1rem"></p>'
        '<div class="cta-row" style="margin-top:.5rem"><button type="button" class="btn" id="cur-fetch">' + L('Fetch latest rates', 'সর্বশেষ রেট আনুন') + '</button>'
        '<button type="button" class="btn ghost" id="cur-reset">' + L('Reset to built-in', 'অন্তর্নির্মিত রেটে ফিরুন') + '</button></div>'
        '<details style="margin-top:1rem"><summary>' + L('View or edit rates (per 1 USD)', 'রেট দেখুন বা পরিবর্তন করুন (১ USD প্রতি)') + '</summary>'
        '<div class="tbl-wrap" style="margin:0 1rem 1rem"><table><thead><tr><th>' + L('Code', 'কোড') + '</th><th>' + L('Currency', 'মুদ্রা') + '</th><th>' + L('Rate', 'রেট') + '</th></tr></thead><tbody id="cur-rates"></tbody></table></div></details></div>')

def ui_gpa():
    return ('<div class="card"><div class="frow">' +
        select('gpa-scale', 'Grading scale', 'গ্রেডিং স্কেল', [('board', 'SSC/HSC board (5.00)', 'এসএসসি/এইচএসসি বোর্ড (৫.০০)'), ('uni', 'University (4.00)', 'বিশ্ববিদ্যালয় (৪.০০)')]) + '</div>'
        '<p class="note" id="gpa-note-board">' + L('Tick one subject as the 4th subject. Only the points above 2.00 are added.', 'একটি বিষয়কে ৪র্থ বিষয় হিসেবে টিক দিন। কেবল ২.০০ এর বেশি পয়েন্ট যোগ হয়।') + '</p>'
        '<p class="note" id="gpa-note-uni" hidden>' + L('GPA is weighted by credits.', 'ক্রেডিট অনুযায়ী ওজন দিয়ে জিপিএ হিসাব হয়।') + '</p>'
        '<div class="rows" id="gpa-rows"></div><button type="button" class="btn ghost" id="gpa-add">+ ' + L('Add subject', 'বিষয় যোগ করুন') + '</button>' + result('gpa-res') + '</div>')

def ui_ssc():
    return ('<div class="card"><div class="frow">' +
        select('sh-level', 'Level', 'স্তর', [('ssc', 'SSC (Science, typical)', 'এসএসসি (বিজ্ঞান, সাধারণ)'), ('hsc', 'HSC (Science, typical)', 'এইচএসসি (বিজ্ঞান, সাধারণ)')]) + '</div>'
        '<p class="note">' + L('Edit names or add and remove subjects to match your own group. Enter total marks out of 100.', 'আপনার বিভাগ অনুযায়ী বিষয়ের নাম বদলান বা যোগ/মুছুন। ১০০ এর মধ্যে মোট নম্বর দিন।') + '</p>'
        '<div class="rows" id="sh-rows"></div><button type="button" class="btn ghost" id="sh-add">+ ' + L('Add subject', 'বিষয় যোগ করুন') + '</button>' + result('sh-res') + '</div>')

def ui_cgpa():
    return ('<div class="card"><div class="tabs" id="cg-tabs"><button type="button" data-mode="sem" aria-pressed="true">' + L('By semester', 'সেমিস্টার অনুযায়ী') + '</button>'
        '<button type="button" data-mode="course" aria-pressed="false">' + L('By course', 'কোর্স অনুযায়ী') + '</button></div>'
        '<p class="note"><span id="cg-h1"></span> · ' + L('Credits', 'ক্রেডিট') + '</p>'
        '<div class="rows" id="cg-rows"></div><button type="button" class="btn ghost" id="cg-add">+ ' + L('Add row', 'সারি যোগ করুন') + '</button>' + result('cg-res') + '</div>')

def ui_bmi():
    return ('<div class="card">' + body_fields() + '<div class="frow">' +
        select('bmi-std', 'Ranges', 'ক্যাটাগরি', [('who', 'WHO (international)', 'ডব্লিউএইচও (আন্তর্জাতিক)'), ('asian', 'Asian (South Asian adults)', 'এশীয় (দক্ষিণ এশীয় প্রাপ্তবয়স্ক)')]) + '</div>' + result('bmi-res') + '</div>')

def ui_calorie():
    top = ('<div class="frow">' + select('c-sex', 'Sex', 'লিঙ্গ', [('male', 'Male', 'পুরুষ'), ('female', 'Female', 'নারী')]) + field('c-age', 'Age (years)', 'বয়স (বছর)', '30') + '</div>')
    low = ('<div class="frow">' + select('c-act', 'Activity level', 'কর্মকাণ্ডের মাত্রা', [
        ('1.2', 'Little or no exercise', 'প্রায় ব্যায়াম নেই'), ('1.375', 'Light (1–3 days a week)', 'হালকা (সপ্তাহে ১–৩ দিন)'), ('1.55', 'Moderate (3–5 days)', 'মাঝারি (৩–৫ দিন)'),
        ('1.725', 'Hard (6–7 days)', 'কঠোর (৬–৭ দিন)'), ('1.9', 'Very hard / physical job', 'খুব কঠোর / শারীরিক কাজ')]) +
        select('c-goal', 'Goal', 'লক্ষ্য', [('maintain', 'Maintain weight', 'ওজন ধরে রাখা'), ('lose', 'Lose weight (−500 kcal)', 'ওজন কমানো (−৫০০ কিলোক্যালরি)'), ('gain', 'Gain weight (+500 kcal)', 'ওজন বাড়ানো (+৫০০ কিলোক্যালরি)')]) + '</div>')
    return '<div class="card">' + body_fields(top) + low + result('cal-res') + '</div>'

def ui_age():
    return ('<div class="card"><div class="frow"><div class="field"><label for="a-dob">' + L('Date of birth', 'জন্মতারিখ') + '</label><input type="date" id="a-dob"></div>'
        '<div class="field"><label for="a-on">' + L('Age on', 'যে তারিখে বয়স') + '</label><input type="date" id="a-on"></div></div>' + result('age-res') + '</div>')

def ui_datediff():
    return ('<div class="card"><div class="frow"><div class="field"><label for="dd-start">' + L('Start date', 'শুরুর তারিখ') + '</label><input type="date" id="dd-start"></div>'
        '<div class="field"><label for="dd-end">' + L('End date', 'শেষের তারিখ') + '</label><input type="date" id="dd-end"></div></div>'
        '<div class="chk"><input type="checkbox" id="dd-inc"><label for="dd-inc">' + L('Include the end date', 'শেষের তারিখ গণনায় ধরুন') + '</label></div>' + result('dd-res') + '</div>')

def dur_fields(p, en, bn):
    return (f'<fieldset style="border:0;padding:0;margin:0 0 1rem"><legend style="font-weight:600;margin-bottom:.4rem">{L(en, bn)}</legend><div class="frow">' +
        field(p + 'd', 'Days', 'দিন', '0') + field(p + 'h', 'Hours', 'ঘণ্টা', '0') + field(p + 'm', 'Minutes', 'মিনিট', '0') + field(p + 's', 'Seconds', 'সেকেন্ড', '0') + '</div></fieldset>')

def ui_time():
    return ('<div class="stack">'
        '<div class="card" id="t-dur"><h2>' + L('Add or subtract durations', 'সময়কাল যোগ বা বিয়োগ') + '</h2>' + dur_fields('a', 'First duration', 'প্রথম সময়কাল') +
        '<div class="frow">' + select('t-op', 'Operation', 'কাজ', [('add', 'Add (+)', 'যোগ (+)'), ('sub', 'Subtract (−)', 'বিয়োগ (−)')]) + '</div>' + dur_fields('b', 'Second duration', 'দ্বিতীয় সময়কাল') + result('t-dur-res') + '</div>'
        '<div class="card" id="t-between"><h2>' + L('Time between two clock times', 'দুই সময়ের মধ্যবর্তী ব্যবধান') + '</h2><div class="frow">'
        '<div class="field"><label for="t-from">' + L('Start', 'শুরু') + '</label><input type="time" id="t-from"></div>'
        '<div class="field"><label for="t-to">' + L('End', 'শেষ') + '</label><input type="time" id="t-to"></div></div>' + result('t-bt-res') + '</div>'
        '<div class="card" id="t-shift"><h2>' + L('Add or subtract from a clock time', 'ঘড়ির সময়ে যোগ বা বিয়োগ') + '</h2><div class="frow">'
        '<div class="field"><label for="t-base">' + L('Time', 'সময়') + '</label><input type="time" id="t-base"></div>' +
        select('t-sh-op', 'Operation', 'কাজ', [('add', 'Add (+)', 'যোগ (+)'), ('sub', 'Subtract (−)', 'বিয়োগ (−)')]) + field('t-sh-h', 'Hours', 'ঘণ্টা', '0') + field('t-sh-m', 'Minutes', 'মিনিট', '0') + '</div>' + result('t-sh-res') + '</div></div>')

UI = {
    'basic': (ui_basic, ['mathparse', 'calc']), 'scientific': (ui_scientific, ['mathparse', 'calc']),
    'percentage': (ui_percentage, ['percentage']), 'discount': (ui_discount, ['discount']),
    'currency': (ui_currency, ['currency']), 'length': (lambda: ui_converter('length'), ['converter']),
    'weight': (lambda: ui_converter('weight'), ['converter']), 'temperature': (lambda: ui_converter('temperature'), ['converter']),
    'gpa': (ui_gpa, ['grading', 'gpa']), 'cgpa': (ui_cgpa, ['grading', 'cgpa']), 'ssc-hsc-gpa': (ui_ssc, ['grading', 'ssc-hsc']),
    'bmi': (ui_bmi, ['body', 'bmi']), 'calorie': (ui_calorie, ['body', 'calorie']),
    'age': (ui_age, ['age']), 'date-difference': (ui_datediff, ['date-diff']), 'time': (ui_time, ['time']),
}

# ---------------------------------------------------------------- layout
SYMS = [('+', 6, 8, 3.2), ('π', 82, 12, 3.6), ('√', 14, 38, 3), ('=', 90, 44, 2.6), ('%', 7, 70, 3), ('×', 76, 78, 3.4), ('Σ', 45, 90, 3.4),
        ('sin', 30, 14, 2.2), ('÷', 56, 28, 2.8), ('x²', 22, 58, 2.6), ('cos', 66, 60, 2.2), ('−', 92, 88, 3), ('tan', 48, 52, 2), ('∞', 38, 74, 3)]

def mathbg():
    s = ''.join(f'<span style="left:{x}%;top:{y}%;font-size:{z}rem;animation-duration:{16 + i * 2}s;animation-delay:-{i * 3}s">{c}</span>' for i, (c, x, y, z) in enumerate(SYMS))
    return f'<div class="mathbg" aria-hidden="true">{s}</div>'

def nav_html(p, active):
    def a(href, label, bn, cur=False):
        return f'<a href="{p}{href}"{" aria-current=page" if cur else ""} data-bn="{bn}">{label}</a>'
    items = [f'<li>{a("index.html", "Home", "হোম", active == "home")}</li>']
    for cid, en, bn, _ in CATS:
        links = ''.join(f'<li>{a(tpath(t), t["en"], t["bn"], active == t["slug"])}</li>' for t in TOOLS if t['cat'] == cid)
        cur = ' cur' if active in [t['slug'] for t in TOOLS if t['cat'] == cid] else ''
        items.append(f'<li class="has-dd"><button type="button" class="nav-btn{cur}" aria-expanded="false" aria-haspopup="true"><span data-bn="{bn}">{en}</span>{ico("chev")}</button><ul class="dd">{links}</ul></li>')
    items.append(f'<li>{a("about.html", "About", "আমাদের কথা", active == "about")}</li>')
    items.append(f'<li>{a("contact.html", "Contact", "যোগাযোগ", active == "contact")}</li>')
    return f'<nav class="nav" id="site-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'

def header(p, active):
    return ('<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap bar">'
        f'<a class="brand" href="{p}index.html" aria-label="HisabCulator home"><img src="{p}assets/img/favicon.svg" alt="" width="32" height="32"><span>Hisab<b>Culator</b></span></a>'
        f'{nav_html(p, active)}<div class="tools"><button type="button" class="icon-btn" id="lang-toggle" aria-label="বাংলায় দেখুন">বাংলা</button>'
        f'<button type="button" class="icon-btn theme-btn" id="theme-toggle" aria-label="Toggle dark mode" data-bn-label="ডার্ক মোড বদলান">{ico("sun", "ico sun")}{ico("moon", "ico moon")}</button>'
        f'<button type="button" class="icon-btn burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="site-nav" data-bn-label="মেনু">{ico("menu")}</button></div></div></header>')

def footer(p):
    def li(href, en, bn): return f'<li><a href="{p}{href}" data-bn="{bn}">{en}</a></li>'
    quick = ''.join([li('index.html', 'Home', 'হোম'), li('index.html#tools', 'All tools', 'সব টুল'), li('index.html#calculators', 'Calculators', 'ক্যালকুলেটর'), li('about.html', 'About', 'আমাদের কথা'), li('contact.html', 'Contact', 'যোগাযোগ')])
    calc = ''.join([li(tpath(TOOL['basic']), 'Basic', 'মৌলিক'), li(tpath(TOOL['scientific']), 'Scientific', 'বৈজ্ঞানিক'), li(tpath(TOOL['gpa']), 'GPA / CGPA', 'জিপিএ / সিজিপিএ'), li(tpath(TOOL['bmi']), 'Fitness (BMI)', 'ফিটনেস (বিএমআই)')])
    return ('<footer class="site-footer"><div class="wrap"><div class="f-grid"><div><a class="brand" href="' + p + 'index.html"><img src="' + p + 'assets/img/favicon.svg" alt="" width="32" height="32"><span>Hisab<b>Culator</b></span></a>'
        '<p style="margin-top:.5rem">' + L('Free calculators for everyday math', 'দৈনন্দিন হিসাবের জন্য বিনামূল্যের ক্যালকুলেটর') + '</p></div>'
        f'<div><h2>{L("Quick links", "দ্রুত লিংক")}</h2><ul>{quick}</ul></div><div><h2>{L("Calculators", "ক্যালকুলেটর")}</h2><ul>{calc}</ul></div></div>'
        '<div class="f-bot">© 2026 HisabCulator · ' + L('All rights reserved', 'সর্বস্বত্ব সংরক্ষিত') + ' · ' + L('Developed by', 'ডেভেলপার:') + ' ' + DEVELOPER + '</div></div></footer>')

HEAD_SCRIPT = ("(function(){try{var t=localStorage.getItem('hc_theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';"
               "document.documentElement.setAttribute('data-theme',t);if(localStorage.getItem('hc_lang')==='bn')document.documentElement.lang='bn'}catch(e){document.documentElement.setAttribute('data-theme','light')}})();")

def page(rel, title, desc, body, active='', scripts=(), ld=()):
    depth = rel.count('/')
    p = '../' * depth
    canon = f'<link rel="canonical" href="{SITE_URL}/{rel}">\n<meta property="og:url" content="{SITE_URL}/{rel}">\n' if SITE_URL else ''
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    scr = ''.join(f'<script src="{p}assets/js/{s}.js" defer></script>\n' for s in ['core'] + list(scripts))
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#F8FAFC">
{canon}<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/css/style.css">
<script>{HEAD_SCRIPT}</script>
{ldj}</head>
<body>
{mathbg()}
{header(p, active)}
<main id="main">
{body}
</main>
{footer(p)}
{scr}</body>
</html>
'''

# ---------------------------------------------------------------- pages
def tool_card(t, p=''):
    return (f'<a class="card tcard cat c-{t["cat"]}" href="{p}{tpath(t)}"><span class="ibox">{ico(t["ic"])}</span>'
            f'<h3>{L(t["en"], t["bn"])}</h3><p>{L(t["d_en"], t["d_bn"])}</p><span class="open">{L("Open Tool", "টুল খুলুন")} {ico("arrow")}</span></a>')

def related(t, p):
    links = ''.join(f'<a class="cat c-{TOOL[s]["cat"]}" href="{p}{tpath(TOOL[s])}"><span class="ibox">{ico(TOOL[s]["ic"])}</span>{L(TOOL[s]["en"], TOOL[s]["bn"])}</a>' for s in t['related'])
    return f'<section class="related"><h2>{L("Related tools", "সম্পর্কিত টুল")}</h2><div class="pop">{links}</div></section>'

def tool_page(t):
    rel = tpath(t); p = '../'
    ui_fn, scripts = UI[t['slug']]
    cid, cen, cbn, _ = CAT[t['cat']]
    title = f'{SITE_NAME} – {t["en"]}'
    steps = ''.join(f'<li>{esc(s)}</li>' for s in t['howto'])
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in t['faq'])
    body = f'''<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{p}index.html" data-bn="হোম">Home</a></li><li><a href="{p}index.html#{cid}" data-bn="{cbn}">{cen}</a></li><li aria-current="page" data-bn="{t["bn"]}">{t["en"]}</li></ol></nav>
<div class="tool-head cat c-{t["cat"]}"><span class="ibox">{ico(t["ic"])}</span><div><h1>{L(t["en"], t["bn"])}</h1><p>{L(t["d_en"], t["d_bn"])}</p></div></div>
<div class="panel" style="max-width:none">{ui_fn()}</div>
<div class="info"><section class="card"><h2>{L("How to use", "ব্যবহার পদ্ধতি")}</h2><ol>{steps}</ol></section>
<section class="card"><h2>{L("Example", "উদাহরণ")}</h2><p class="example">{t["example"]}</p></section></div>
<section class="faq"><h2>{L("Helpful information", "জানা দরকার")}</h2>{faq}</section>
{related(t, p)}
</div>'''
    ld = [
        {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['en'], 'description': t['meta'], 'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'BDT'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]},
    ]
    return page(rel, title, t['meta'], body, active=t['slug'], scripts=scripts, ld=ld)

def home_page():
    blocks = ''
    for cid, en, bn, ic in CATS:
        cards = ''.join(tool_card(t) for t in TOOLS if t['cat'] == cid)
        blocks += f'<div class="cat-block cat c-{cid}"><h3 id="{cid}"><span class="ibox">{ico(ic)}</span>{L(en, bn)}</h3><div class="grid">{cards}</div></div>'
    pop = ''.join(f'<a class="cat c-{TOOL[s]["cat"]}" href="{tpath(TOOL[s])}"><span class="ibox">{ico(TOOL[s]["ic"])}</span>{L(TOOL[s]["en"], TOOL[s]["bn"])}</a>' for s in POPULAR)
    feats = [
        ('Bangla numbers', 'বাংলা সংখ্যা', 'Switch to বাংলা and results show in Bangla digits. You can also type ১২৩ in any field.', 'বাংলা মোডে ফলাফল বাংলা সংখ্যায় দেখায়। যেকোনো ঘরে ১২৩ লিখতেও পারেন।'),
        ('Taka by default', 'ডিফল্ট টাকা', 'The discount calculator works in ৳ and the currency converter starts with BDT.', 'ডিসকাউন্ট ক্যালকুলেটর ৳ এ চলে এবং মুদ্রা রূপান্তর শুরু হয় BDT দিয়ে।'),
        ('SSC/HSC GPA', 'এসএসসি/এইচএসসি জিপিএ', 'Enter marks and get grades, GPA and fail checks on the 5.00 scale.', 'নম্বর দিন, ৫.০০ স্কেলে গ্রেড, জিপিএ ও অকৃতকার্য যাচাই পান।'),
        ('4th subject', '৪র্থ বিষয়', 'Only the points above 2.00 are added, and the GPA never goes above 5.00.', 'শুধু ২.০০ এর বেশি পয়েন্ট যোগ হয় এবং জিপিএ ৫.০০ এর বেশি হয় না।'),
        ('University CGPA', 'বিশ্ববিদ্যালয়ের সিজিপিএ', 'Credit-weighted CGPA on the 4.00 scale, by semester or by course.', '৪.০০ স্কেলে ক্রেডিটভিত্তিক সিজিপিএ, সেমিস্টার বা কোর্স অনুযায়ী।'),
        ('Local units', 'স্থানীয় একক', 'Convert maund, seer, tola and hat along with kg, lb and metres.', 'কেজি, পাউন্ড ও মিটারের পাশাপাশি মণ, সের, তোলা ও হাত রূপান্তর করুন।'),
    ]
    fh = ''.join(f'<div class="card"><h3>{L(a, b)}</h3><p>{L(c, d)}</p></div>' for a, b, c, d in feats)
    why = [
        ('No sign-up', 'সাইন-আপ লাগে না', 'Open a page and use it. There are no accounts.', 'পাতা খুলে ব্যবহার করুন। কোনো অ্যাকাউন্ট নেই।'),
        ('Runs in your browser', 'ব্রাউজারেই চলে', 'Calculations happen on your device. The only network call is the optional "Fetch latest rates" button.', 'হিসাব আপনার ডিভাইসেই হয়। শুধু ঐচ্ছিক "সর্বশেষ রেট আনুন" বোতামে নেটওয়ার্ক ব্যবহার হয়।'),
        ('One tool, one page', 'এক টুল, এক পাতা', 'Every tool has its own address, so you can bookmark exactly the one you use.', 'প্রতিটি টুলের আলাদা ঠিকানা, তাই যেটি ব্যবহার করেন সেটিই বুকমার্ক করা যায়।'),
        ('Works on a phone', 'ফোনেও ঠিকঠাক', 'Large touch targets, light and dark themes, and layouts that fit small screens.', 'বড় বোতাম, লাইট ও ডার্ক থিম এবং ছোট স্ক্রিনে মানানসই লেআউট।'),
    ]
    wh = ''.join(f'<div class="card"><h3>{L(a, b)}</h3><p>{L(c, d)}</p></div>' for a, b, c, d in why)
    body = f'''<section class="hero"><div class="wrap hero-grid"><div>
<p class="brandline">HisabCulator</p><h1>{L("Everyday calculations, made simple.", "দৈনন্দিন হিসাব, এবার সহজে।")}</h1>
<p class="lead">{L("Calculate, convert, check GPA, calculate BMI, find your age and more — all in one place.", "হিসাব করুন, রূপান্তর করুন, জিপিএ দেখুন, বিএমআই মাপুন, বয়স জানুন এবং আরও অনেক কিছু — সবই এক জায়গায়।")}</p>
<div class="cta-row"><a class="btn" href="#tools">{L("Explore All Tools", "সব টুল দেখুন")}</a><a class="btn ghost" href="{tpath(TOOL["basic"])}">{L("Start Calculating", "হিসাব শুরু করুন")}</a></div></div>
<div class="card quick"><h2>{L("Quick check", "দ্রুত হিসাব")}</h2><div class="inline-form"><span>{L("What is", "কত")}</span><label class="sr" for="q-a">%</label><input type="text" inputmode="decimal" id="q-a" value="15" aria-label="Percent"><span>% {L("of", "এর")}</span><label class="sr" for="q-b">Number</label><input type="text" inputmode="decimal" id="q-b" value="2500" aria-label="Number"><span>?</span></div>
<div class="result" id="q-res" role="status" aria-live="polite"></div><p class="note" style="margin:.75rem 0 0"><a href="{tpath(TOOL["percentage"])}">{L("More percentage tools", "আরও শতকরা টুল")}</a></p></div></div></section>
<section class="section alt" id="tools"><div class="wrap"><div class="section-head"><h2>{L("What can you calculate?", "কী কী হিসাব করা যায়?")}</h2><p>{L("Pick a tool. Each one opens on its own page.", "একটি টুল বেছে নিন। প্রতিটি আলাদা পাতায় খোলে।")}</p></div>{blocks}</div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2>{L("Popular tools", "জনপ্রিয় টুল")}</h2></div><div class="pop">{pop}</div></div></section>
<section class="section alt"><div class="wrap"><div class="section-head"><h2>{L("Made with Bangladesh in mind", "বাংলাদেশের কথা মাথায় রেখে তৈরি")}</h2></div><div class="feat">{fh}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2>{L("Why HisabCulator?", "কেন হিসাবকুলেটর?")}</h2></div><div class="feat">{wh}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="card cta"><div><h2>{L("Got a calculation in mind?", "কোনো হিসাব করতে চান?")}</h2><p>{L("Start with the basic calculator, or tell us which tool to add next.", "মৌলিক ক্যালকুলেটর দিয়ে শুরু করুন, অথবা কোন টুল যোগ করতে চান জানান।")}</p></div><div class="cta-row" style="margin:0"><a class="btn" href="{tpath(TOOL["basic"])}">{L("Start Calculating", "হিসাব শুরু করুন")}</a><a class="btn ghost" href="contact.html">{L("Suggest a tool", "টুলের পরামর্শ দিন")}</a></div></div></div></section>'''
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'description': 'Free everyday calculators, converters, GPA, BMI and date tools.'}]
    return page('index.html', 'HisabCulator – Free Calculators, Converters, GPA & BMI', 'HisabCulator: free online calculators and converters for everyday math, SSC/HSC GPA, university CGPA, BMI, age and dates, with Bangla number support.', body, active='home', scripts=['home'], ld=ld)

def about_page():
    body = f'''<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html" data-bn="হোম">Home</a></li><li aria-current="page" data-bn="আমাদের কথা">About</li></ol></nav>
<div class="prose"><h1>{L("About HisabCulator", "হিসাবকুলেটর সম্পর্কে")}</h1>
<p>{L("HisabCulator is a simple online calculation platform designed to make everyday calculations easier. It has calculators, converters, education tools, fitness tools and date tools, each on its own page.", "হিসাবকুলেটর একটি সহজ অনলাইন হিসাব-প্ল্যাটফর্ম, যা দৈনন্দিন হিসাব সহজ করার জন্য তৈরি। এখানে ক্যালকুলেটর, রূপান্তর, শিক্ষা, ফিটনেস ও তারিখের টুল আছে, প্রতিটি আলাদা পাতায়।")}</p>
<h2>{L("Why we built it", "কেন বানানো হলো")}</h2>
<p>{L("Many calculator sites are cluttered, ask you to sign up, or ignore how things work in Bangladesh. HisabCulator focuses on:", "অনেক ক্যালকুলেটর সাইট এলোমেলো, সাইন-আপ চায়, কিংবা বাংলাদেশের প্রয়োজন বোঝে না। হিসাবকুলেটর গুরুত্ব দেয়:")}</p>
<ul><li>{L("Students: GPA, CGPA and SSC/HSC results", "শিক্ষার্থী: জিপিএ, সিজিপিএ ও এসএসসি/এইচএসসি ফলাফল")}</li><li>{L("Everyday calculations: percentages, discounts, unit conversion", "দৈনন্দিন হিসাব: শতকরা, ছাড়, একক রূপান্তর")}</li><li>{L("Bangladesh users: Taka, Bangla digits, local units", "বাংলাদেশের ব্যবহারকারী: টাকা, বাংলা সংখ্যা, স্থানীয় একক")}</li><li>{L("Simple, easy-to-use tools with clear explanations", "সহজ টুল ও পরিষ্কার ব্যাখ্যা")}</li></ul>
<h2>{L("Our goal", "আমাদের লক্ষ্য")}</h2><p>{L("To make useful calculations simple, accessible and easy to understand.", "প্রয়োজনীয় হিসাব সহজ, সবার নাগালে এবং বোধগম্য করে তোলা।")}</p>
<h2>{L("Bangladesh-focused", "বাংলাদেশ কেন্দ্রিক")}</h2>
<ul><li>{L("Bangla number support (type or view ০১২৩৪৫৬৭৮৯)", "বাংলা সংখ্যা সমর্থন (লেখা ও দেখা দুটোই)")}</li><li>{L("BDT in the discount calculator and currency converter", "ডিসকাউন্ট ক্যালকুলেটর ও মুদ্রা রূপান্তরে BDT")}</li><li>{L("SSC/HSC GPA with the 5.00 board scale", "৫.০০ বোর্ড স্কেলে এসএসসি/এইচএসসি জিপিএ")}</li><li>{L("4th subject handling", "৪র্থ বিষয় হিসাব")}</li><li>{L("University CGPA on the 4.00 scale", "৪.০০ স্কেলে বিশ্ববিদ্যালয়ের সিজিপিএ")}</li><li>{L("Maund, seer, tola and hat converters", "মণ, সের, তোলা ও হাত রূপান্তর")}</li></ul>
<h2>{L("Privacy and simplicity", "গোপনীয়তা ও সরলতা")}</h2>
<p>{L("There are no accounts and no sign-up. Calculations run in your browser. Your theme, language, calculator history and any currency rates you edit are saved in your own browser storage, nowhere else. The only request the site makes is when you press “Fetch latest rates” on the currency page, which asks a public exchange-rate service for current numbers. The contact form opens your own email app; it does not send anything by itself.", "কোনো অ্যাকাউন্ট বা সাইন-আপ নেই। হিসাব আপনার ব্রাউজারেই চলে। থিম, ভাষা, ক্যালকুলেটরের ইতিহাস ও আপনার পরিবর্তন করা মুদ্রার রেট শুধু আপনার ব্রাউজারেই থাকে। শুধু মুদ্রা পাতায় “সর্বশেষ রেট আনুন” চাপলে একটি পাবলিক রেট সার্ভিসে অনুরোধ যায়। যোগাযোগ ফর্ম আপনার নিজের ইমেইল অ্যাপ খোলে; নিজে কিছু পাঠায় না।")}</p>
<h2>{L("Developer", "ডেভেলপার")}</h2><p>{L("Designed & Developed by", "ডিজাইন ও ডেভেলপমেন্ট:")} {DEVELOPER}</p>
<p><a class="btn" href="index.html#tools">{L("Explore All Tools", "সব টুল দেখুন")}</a></p></div></div>'''
    return page('about.html', 'HisabCulator – About', 'About HisabCulator: a simple, no-sign-up calculation website built for students and everyday users in Bangladesh, with Bangla number support.', body, active='about')

def contact_page():
    items = [('mail', 'Email', 'ইমেইল', f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>')]
    if CONTACT_PHONE:
        items.append(('phone', 'Phone', 'ফোন', CONTACT_PHONE))
    items.append(('pin', 'Location', 'অবস্থান', CONTACT_LOCATION))
    if SOCIAL:
        items.append(('globe', 'Social media', 'সোশ্যাল মিডিয়া', ' · '.join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL.items())))
    cl = ''.join(f'<li><span class="ibox">{ico(i)}</span><span><small data-bn="{b}">{e}</small>{v}</span></li>' for i, e, b, v in items)
    kinds = [('Bug report', 'ত্রুটি জানান'), ('Tool suggestion', 'টুলের পরামর্শ'), ('General feedback', 'সাধারণ মতামত')]
    ch = ''.join(f'<label><input type="radio" name="kind" value="{i}" data-label="{e}"{" checked" if i == 0 else ""}><span data-bn="{b}">{e}</span></label>' for i, (e, b) in enumerate(kinds))
    body = f'''<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html" data-bn="হোম">Home</a></li><li aria-current="page" data-bn="যোগাযোগ">Contact</li></ol></nav>
<h1>{L("Contact", "যোগাযোগ")}</h1><p style="color:var(--muted);max-width:40rem">{L("Found a bug or want a tool added? Write here.", "কোনো ত্রুটি পেয়েছেন বা নতুন টুল চান? এখানে লিখুন।")}</p>
<div class="contact-grid"><aside class="cpanel"><h2>{L("Get in touch", "যোগাযোগের তথ্য")}</h2><p>{L("Bug reports with the page name and what you typed help the most.", "পাতার নাম ও আপনি কী লিখেছিলেন জানালে ত্রুটি ঠিক করা সহজ হয়।")}</p><ul class="clist">{cl}</ul></aside>
<form class="card" id="contact-form" data-to="{CONTACT_EMAIL}" novalidate-off>
<div class="field" style="margin-bottom:1rem"><span class="label" style="display:block;font-weight:600;font-size:.9rem;margin-bottom:.3rem">{L("What is this about?", "বিষয় কী?")}</span><div class="choice">{ch}</div></div>
<div class="frow"><div class="field"><label for="cf-name">{L("Your name", "আপনার নাম")}</label><input type="text" id="cf-name" required autocomplete="name"></div>
<div class="field"><label for="cf-email">{L("Email address", "ইমেইল ঠিকানা")}</label><input type="email" id="cf-email" required autocomplete="email"></div></div>
<div class="field" style="margin-bottom:1rem"><label for="cf-text">{L("Your message", "আপনার বার্তা")}</label><textarea id="cf-text" required minlength="10"></textarea></div>
<button type="submit" class="btn">{L("Send Message", "বার্তা পাঠান")}</button>
<p class="note" style="margin-top:.75rem">{L("This opens your email app with the message filled in. Nothing is sent or stored by this website.", "এটি আপনার ইমেইল অ্যাপে বার্তা তৈরি করে খোলে। এই ওয়েবসাইট কিছু পাঠায় বা সংরক্ষণ করে না।")}</p>
<p class="note" id="cf-msg" role="status" aria-live="polite"></p></form></div></div>'''.replace(' novalidate-off', '')
    return page('contact.html', 'HisabCulator – Contact', 'Contact HisabCulator to report a bug, suggest a new calculator or share feedback.', body, active='contact', scripts=['contact'])

# ---------------------------------------------------------------- write
def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    write('index.html', home_page())
    write('about.html', about_page())
    write('contact.html', contact_page())
    for t in TOOLS:
        write(tpath(t), tool_page(t))
    write('robots.txt', 'User-agent: *\nAllow: /\n' + (f'Sitemap: {SITE_URL}/sitemap.xml\n' if SITE_URL else ''))
    if SITE_URL:
        urls = ['index.html', 'about.html', 'contact.html'] + [tpath(t) for t in TOOLS]
        write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    print('built', 3 + len(TOOLS), 'pages')

if __name__ == '__main__':
    main()
