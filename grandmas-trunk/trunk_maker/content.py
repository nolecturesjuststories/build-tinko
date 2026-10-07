"""What is in Grandma's trunk: every document, word for word, with the facts it carries.

The family is fictional: Grandpa Mohan Joshi (born 1935, railway clerk), Grandma Kamla (born 1941), their son Arun
(born 1965, Rohan's father) and daughter Meera (born 14 February 1968). Kamla's sister Savitri lives in Indore.
Mohan joined the railway office in Jabalpur in 1962; the office was transferred to Bombay in March 1968.

Each document has an id (also its file name), a layout (see render.py), metadata used later for search filters and
for the ground truth, and the layout's own fields.
"""

DOCS = [
    # ── The Bombay letter (the payoff: never says "move" or "Mumbai") ─────────────────────────────────────────────
    {
        'id': 'letter_1968_03',
        'layout': 'letter',
        'meta': {'doc_type': 'letter', 'date': '1968-03-09', 'people': ['Mohan', 'Kamla', 'Arun', 'Meera'], 'places': ['Bombay', 'Jabalpur']},
        'hand': 'mohan',
        'ink': 'blue',
        'place': 'Goregaon, Bombay',
        'date': '9th March 1968',
        'greeting': 'My dear Kamla,',
        'body': (
            "We have shifted to Bombay. The whole office came down by the Mail on Tuesday, files, typewriters and all. "
            "The railway has given me a small quarter in Goregaon, two rooms and a kitchen, and the window looks at a "
            "coconut tree.\n\n"
            "The sea is very big, Kamla. Yesterday evening I walked from Dadar to the shore and stood there like a schoolboy. "
            "I thought of you and the children the whole time.\n\n"
            "Give my love to Arun and kiss little Meera for me. Ask Amma to write. I will send the train fare on the "
            "first of the month, and by April you will all be here."
        ),
        'closing': 'Yours always,',
        'sign': 'Mohan',
        'stain': True,
        'seed': 1968003,
    },
    # ── Meera's birth, typed (the clean source for the date) ─────────────────────────────────────────────────────
    {
        'id': 'telegram_1968_02',
        'layout': 'telegram',
        'meta': {'doc_type': 'telegram', 'date': '1968-02-14', 'people': ['Mohan', 'Kamla', 'Meera'], 'places': ['Jabalpur']},
        'origin': 'JABALPUR CITY',
        'date': '14-02-1968',
        'time': '18.25',
        'to': 'SHRI MOHAN JOSHI, C/O RAILWAY OFFICE, JABALPUR',
        'words': ['BLESSED WITH DAUGHTER STOP NAME MEERA STOP', 'BORN 14 FEBRUARY 1968 STOP', 'MOTHER AND CHILD WELL STOP COME SOON', '= SAVITRI'],
        'seed': 1968002,
    },
    # ── The real kheer recipe ────────────────────────────────────────────────────────────────────────────────────
    {
        'id': 'recipe_kheer_1971',
        'layout': 'recipe',
        'meta': {'doc_type': 'recipe', 'date': '1971-10-01', 'people': ['Kamla'], 'places': []},
        'title': 'Kheer (the real one)',
        'year': 'Diwali 1971',
        'ingredients': ['1 litre full-cream milk', '1/4 cup old rice, washed', '1/2 cup sugar', '4 green cardamom, crushed', 'a pinch of saffron in warm milk', '10 almonds, sliced'],
        'method': "Boil the milk, add rice, keep the flame low. Stir slowly, never rush. When it coats the spoon (about 45 minutes) add sugar, cardamom and saffron. Almonds on top.",
        'note': 'Stir slowly, never rush!  - K.',
        'stains': 2,
        'seed': 1971001,
    },
    # ── A 1975 diary page ────────────────────────────────────────────────────────────────────────────────────────
    {
        'id': 'diary_1975_06_14',
        'layout': 'diary',
        'meta': {'doc_type': 'diary', 'date': '1975-06-14', 'people': ['Kamla', 'Mohan', 'Arun', 'Meera'], 'places': ['Goregaon']},
        'year': '1975',
        'day': 'SATURDAY 14 JUNE 1975',
        'entry': (
            "First real rain of the monsoon today. Arun and Meera ran out in it before I could stop them, and came "
            "back laughing like two wet puppies.\n\n"
            "Mohan came home early with good news: he has been promoted to Head Clerk from 1st July. 40 rupees more "
            "every month! I made sheera for everyone. We will save the extra for Arun's college."
        ),
        'stain': True,
        'seed': 1975614,
    },
    # ── An electricity bill (table) ──────────────────────────────────────────────────────────────────────────────
    {
        'id': 'bill_1985_07',
        'layout': 'bill',
        'meta': {'doc_type': 'bill', 'date': '1985-07', 'billing_month': '1985-07', 'amount': 104.00, 'people': ['Mohan'], 'places': ['Goregaon']},
        'consumer': '214-0873-56',
        'name': 'Shri M. K. Joshi',
        'address': 'Flat 6, Shanti Niwas, Goregaon (W)',
        'month': 'JULY 1985',
        'period': '01-07-1985 to 31-07-1985',
        'bill_date': '06-08-1985',
        'due': '20-08-1985',
        'prev': 18342,
        'pres': 18478,
        'rate': 0.62,
        'fixed': 12.00,
        'duty': 7.68,
        'total': 104.00,
        'paid': '14 AUG 1985',
        'seed': 1985007,
    },
    # ── A school report card (form) ──────────────────────────────────────────────────────────────────────────────
    {
        'id': 'report_arun_1979',
        'layout': 'report',
        'meta': {'doc_type': 'report_card', 'date': '1979-04', 'people': ['Arun', 'Mohan'], 'places': ['Goregaon']},
        'school': 'Aarey Road Municipal High School, Goregaon',
        'year': '1978-79',
        'name': 'Arun Mohan Joshi',
        'cls': 'IX  B',
        'roll': '23',
        'subjects': [('English', 71, 'B'), ('Hindi', 78, 'B+'), ('Marathi', 64, 'C'), ('Mathematics', 92, 'A'), ('Science', 86, 'A'), ('History & Geography', 69, 'B')],
        'total': '460 / 600',
        'result': 'Passed, promoted to Class X',
        'remarks': 'Excellent in Mathematics. Must read more English books.',
        'teacher': 'S. Kulkarni',
        'parent_sign': 'M. K. Joshi',
        'seed': 1979001,
    },
]


def L(id_, date, meta_date, people, places, hand, ink, place, greeting, body, closing, sign, seed, **extra):
    """A letter."""
    return {'id': id_, 'layout': 'letter', 'meta': {'doc_type': 'letter', 'date': meta_date, 'people': people, 'places': places},
            'hand': hand, 'ink': ink, 'place': place, 'date': date, 'greeting': greeting, 'body': body, 'closing': closing,
            'sign': sign, 'seed': seed, **extra}


DOCS += [
    # ── Letters 1962–1990 ────────────────────────────────────────────────────────────────────────────────────────
    L('letter_1962_04', '4th April 1962', '1962-04-04', ['Mohan', 'Amma'], ['Jabalpur', 'Sagar'], 'mohan', 'black',
      'Railway Office, Jabalpur', 'Respected Amma,',
      "I have joined the Railway Office here on Monday, 2nd April, as a Junior Clerk in the accounts section. My salary "
      "will be Rs 180 every month, and from the first salary I will send you a new shawl.\n\n"
      "The Head Clerk, Shri Verma, is strict but kind. He checked my handwriting and said it is the neatest in the "
      "office. I thought of Master Tiwari from our school in Sagar, who made us copy whole pages until our letters "
      "stood straight. That old school punishment has finally paid me a salary!\n\n"
      "I am staying with Ramesh in a rented room near the station. Do not worry about food, his mother feeds us both.",
      'Your obedient son,', 'Mohan', 1962004, stain=True),
    L('letter_1964_11', '20th November 1964', '1964-11-20', ['Kamla', 'Savitri', 'Mohan'], ['Jabalpur'], 'kamla', 'royal',
      'Jabalpur', 'Dear Didi,',
      "Our new house in Jabalpur is two rooms with a small courtyard, and the neem tree outside gives shade all "
      "afternoon. Mohan has planted tulsi near the door.\n\n"
      "He works very hard in the railway office and comes home only after seven. On Sundays we walk to the Bhedaghat "
      "falls, it is so beautiful there.\n\n"
      "Didi, I have some happy news which I will tell you properly when you come for Holi. Do not tell Amma yet!",
      'Your loving sister,', 'Kamla', 1964011),
    L('letter_1965_08', '10th August 1965', '1965-08-10', ['Savitri', 'Kamla', 'Arun'], ['Indore', 'Jabalpur'], 'savitri', 'black',
      'Indore', 'My dearest Kamla,',
      "Your telegram reached us on Wednesday and the whole house danced! A son! Amma distributed laddoos to the whole "
      "lane. Arun is a lovely name, strong and bright like the morning sun.\n\n"
      "Rest properly for forty days and do not lift anything heavy. I am sending you a parcel with dry fruits, two "
      "small sweaters I knitted and Amma's old silver bowl for the baby.\n\n"
      "I will come to Jabalpur in October to see my nephew. Tell Mohan he must buy a camera now!",
      'With love,', 'Savitri Didi', 1965008),
    L('letter_1968_02', '16th February 1968', '1968-02-16', ['Mohan', 'Amma', 'Meera', 'Kamla', 'Arun'], ['Jabalpur'], 'mohan', 'blue',
      'Jabalpur', 'Respected Amma,',
      "Your granddaughter has arrived! She was born on Wednesday the 14th, just before sunset, at the railway "
      "hospital. Kamla is well and resting, and the baby is small but very loud.\n\n"
      "We have named her Meera, as you wished. Arun keeps asking when she will be able to play cricket.\n\n"
      "There is more news. Our whole office is being transferred to Bombay next month. I will go first with the "
      "office, and Kamla and the children will follow when the quarter is ready.",
      'Your son,', 'Mohan', 1968021, smudge_year=True),
    L('letter_1971_10', '28th October 1971', '1971-10-28', ['Kamla', 'Savitri'], ['Goregaon', 'Bombay'], 'kamla', 'royal',
      'Goregaon, Bombay', 'Dear Didi,',
      "This Diwali I finally made the kheer the way Amma used to, and Mohan took two helpings and asked for a third. "
      "I have written it down on a card so it is not lost. I am keeping the card in the trunk with our letters.\n\n"
      "The secret is the old rice and the patience. Stir slowly, never rush, just like Amma always said.\n\n"
      "Arun has started school and Meera follows him everywhere. Bombay is noisy but our neighbours are like family.",
      'Your Kamla,', 'Kamla', 1971010),
    L('letter_1975_03', '18th March 1975', '1975-03-18', ['Mohan', 'Kamla'], ['Delhi', 'Bombay'], 'mohan', 'blue',
      'Rail Bhavan, New Delhi', 'Dear Kamla,',
      "The meetings at the Railway Board end on Friday and I will take the Frontier Mail back on Saturday. Delhi is "
      "cold in the mornings and very dusty.\n\n"
      "My senior officer hinted that my name is on the list for Head Clerk. Do not tell anyone until it is "
      "confirmed.\n\n"
      "I bought a red cardigan for Meera and a cricket bat for Arun from Karol Bagh. For you, a surprise.",
      'Yours,', 'Mohan', 1975003),
    L('letter_1975_09', '22nd September 1975', '1975-09-22', ['Savitri', 'Kamla', 'Usha'], ['Indore'], 'savitri', 'black',
      'Indore', 'Dear Kamla,',
      "Usha's wedding is fixed! The boy is an engineer in Bhopal, his family is simple and kind. The wedding will be "
      "on 15th February 1976, so you must all come for at least a week.\n\n"
      "Congratulations to Mohan for becoming Head Clerk. Amma says she always knew he would.\n\n"
      "Please bring your kheer, nobody here makes it like you.",
      'Your Didi,', 'Savitri', 1975009),
    L('letter_1979_11', '15th November 1979', '1979-11-15', ['Mohan', 'Amma', 'Kamla', 'Arun', 'Meera'], ['Goregaon', 'Bombay'], 'mohan', 'blue',
      'Goregaon, Bombay', 'Respected Amma,',
      "Today we signed the papers and Flat 6 in Shanti Niwas is now our own. We have lived here as tenants since 1972 "
      "and now no landlord can ask us to leave. Forty-eight thousand rupees, Amma, all our savings and a loan from the "
      "railway cooperative.\n\n"
      "Kamla cried at the registrar's office and then laughed at herself. Arun wants a bookshelf for his engineering "
      "books and Meera wants a window seat.\n\n"
      "Please come and stay with us this winter. Your room is ready.",
      'Your son,', 'Mohan', 1979011),
    L('letter_1983_07', '21st July 1983', '1983-07-21', ['Arun', 'Mohan', 'Kamla'], ['Pune'], 'young', 'blue',
      'Hostel 3, Pune', 'Dear Papa and Aai,',
      "I reached Pune safely. The College of Engineering is huge and old, with stone buildings and a big ground. My "
      "room-mate is Suresh from Nagpur, he snores but he is good at physics.\n\n"
      "Classes start at eight. The mess food is not like Aai's, please send some ladoos.\n\n"
      "Papa, the lathe workshop is the best thing I have ever seen. I think I want to build machines.",
      'Your son,', 'Arun', 1983007),
    L('letter_1986_05', '30th May 1986', '1986-05-30', ['Meera', 'Arun'], ['Bombay', 'Pune'], 'young', 'royal',
      'Goregaon, Bombay', 'Dada,',
      "I passed my Twelfth with first class! Aai made shrikhand and Papa told the whole building.\n\n"
      "I have decided: I want to be a teacher. I have applied to the teachers' training college in Dadar. Please "
      "tell Papa it is a good job, he listens to you.\n\n"
      "When are you coming home? Your bookshelf is now full of my books.",
      'Your sister,', 'Meera', 1986005),
    L('letter_1990_06', '12th June 1990', '1990-06-12', ['Mohan', 'Arun'], ['Bombay', 'Pune'], 'mohan', 'blue',
      'Goregaon, Bombay', 'Dear Arun,',
      "Your letter about the new job made your mother cry and your father very proud. Design engineer at a machine "
      "tools company, with a salary three times what I earned when I started! Do your work honestly and the rest will "
      "follow.\n\n"
      "I have three more years before I retire from the railway. Your mother wants to visit Indore and see the sea in "
      "Goa, in that order.\n\n"
      "Come home for Ganpati. Bring your friend Anjali if she can come.",
      'Your Papa,', 'Mohan', 1990006),

    # ── Telegrams ────────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'telegram_1965_08', 'layout': 'telegram',
     'meta': {'doc_type': 'telegram', 'date': '1965-08-03', 'people': ['Mohan', 'Kamla', 'Arun'], 'places': ['Jabalpur', 'Indore']},
     'origin': 'JABALPUR', 'date': '03-08-1965', 'time': '21.10', 'to': 'SMT SAVITRI PATHAK, 14 SNEHLATAGANJ, INDORE',
     'words': ['BLESSED WITH SON STOP BORN TODAY 3 AUGUST STOP', 'NAMED ARUN STOP KAMLA AND BABY WELL STOP', '= MOHAN'],
     'seed': 1965803},
    {'id': 'telegram_1997_03', 'layout': 'telegram',
     'meta': {'doc_type': 'telegram', 'date': '1997-03-14', 'people': ['Arun', 'Anjali', 'Mohan', 'Kamla'], 'places': ['Mumbai', 'Pune']},
     'origin': 'PUNE GPO', 'date': '14-03-1997', 'time': '11.05', 'to': 'M K JOSHI, 6 SHANTI NIWAS, GOREGAON W, MUMBAI',
     'words': ['REACHING MUMBAI CENTRAL SUNDAY 7 AM STOP', 'WITH ANJALI STOP NO NEED TO COME TO STATION', '= ARUN'],
     'seed': 1997314},

    # ── Recipe cards ─────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'recipe_dal_1966', 'layout': 'recipe', 'meta': {'doc_type': 'recipe', 'date': '1966-01-01', 'people': ['Kamla'], 'places': []},
     'title': 'Dal Tadka', 'year': '1966', 'ingredients': ['1 cup toor dal', '1 tomato, chopped', '1 tsp turmeric', 'salt to taste', '2 tbsp ghee', '1 tsp cumin, 4 garlic, 2 red chillies'],
     'method': 'Pressure-cook dal with turmeric and salt (3 whistles). Mash, add tomato, simmer. Heat ghee, crackle cumin, garlic and chillies, pour over the dal.',
     'note': "Mohan's favourite on Mondays", 'turmeric': True, 'seed': 1966001},
    {'id': 'recipe_paratha_1969', 'layout': 'recipe', 'meta': {'doc_type': 'recipe', 'date': '1969-01-01', 'people': ['Kamla', 'Arun'], 'places': []},
     'title': 'Aloo Paratha', 'year': '1969', 'ingredients': ['2 cups wheat flour', '3 boiled potatoes', '1 green chilli', 'coriander leaves', 'ajwain, salt', 'ghee for roasting'],
     'method': 'Knead a soft dough. Mash potatoes with chilli, coriander, ajwain and salt. Fill, roll gently, roast with ghee on both sides till golden spots appear.',
     'note': 'Arun eats three!', 'seed': 1969001},
    {'id': 'recipe_ladoo_1974', 'layout': 'recipe', 'meta': {'doc_type': 'recipe', 'date': '1974-01-01', 'people': ['Kamla'], 'places': []},
     'title': 'Besan Ladoo', 'year': '1974', 'ingredients': ['2 cups besan', '3/4 cup ghee', '1 cup powdered sugar', '1/2 tsp cardamom', 'chopped cashews'],
     'method': 'Roast besan in ghee on low heat for 25 minutes till it smells nutty. Cool a little, mix sugar, cardamom and cashews, shape while warm.',
     'note': 'Do not burn the besan!', 'seed': 1974001},
    {'id': 'recipe_poha_1978', 'layout': 'recipe', 'meta': {'doc_type': 'recipe', 'date': '1978-01-01', 'people': ['Kamla', 'Meera'], 'places': []},
     'title': 'Kanda Poha', 'year': '1978', 'ingredients': ['2 cups thick poha', '1 onion', 'peanuts', 'mustard seeds, curry leaves', 'turmeric, salt, sugar', 'lemon and coriander'],
     'method': 'Rinse poha and drain. Fry peanuts, mustard, curry leaves and onion, add turmeric, then poha, salt and a pinch of sugar. Lemon and coriander on top.',
     'note': "Meera's Sunday breakfast", 'turmeric': True, 'seed': 1978001},
    {'id': 'recipe_pickle_1982', 'layout': 'recipe', 'meta': {'doc_type': 'recipe', 'date': '1982-05-01', 'people': ['Kamla'], 'places': []},
     'title': 'Mango Pickle (Amma style)', 'year': 'May 1982', 'ingredients': ['2 kg raw mangoes', '1 cup mustard oil', 'mustard and fenugreek seeds', 'red chilli powder', 'turmeric, salt', 'a pinch of hing'],
     'method': 'Cut mangoes, dry in the sun for a day. Mix spices, add mangoes and warm oil. Keep in the sun for a week, shake the jar every morning.',
     'note': 'Dry jar only!', 'turmeric': True, 'seed': 1982005},

    # ── Diary pages ──────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'diary_1975_01_26', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1975-01-26', 'people': ['Kamla', 'Arun', 'Meera'], 'places': ['Goregaon']},
     'year': '1975', 'day': 'SUNDAY 26 JANUARY 1975',
     'entry': "Republic Day. We heard the parade on the radio and Arun saluted every regiment from the sofa. Meera made a "
              "paper flag and stuck it on the window.\n\nNew diary, new year. I promise to write every week this year.",
     'seed': 1975126},
    {'id': 'diary_1975_11_03', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1975-11-03', 'people': ['Kamla', 'Mohan', 'Arun', 'Meera'], 'places': ['Goregaon']},
     'year': '1975', 'day': 'MONDAY 3 NOVEMBER 1975',
     'entry': "Diwali week. Mohan saved from his Head Clerk raise to buy a new pressure cooker for me and a mixer! "
              "Arun burnt a hole in his shirt with a sparkler. Meera made the rangoli all by herself this year.\n\n"
              "Kheer for 14 people. Stirred for an hour.",
     'stain': True, 'seed': 1975113},
    {'id': 'diary_1983_06_25', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1983-06-25', 'people': ['Kamla', 'Mohan', 'Arun', 'Meera'], 'places': ['Goregaon']},
     'year': '1983', 'day': 'SATURDAY 25 JUNE 1983',
     'entry': "India won the cricket World Cup! We watched the final on the Shettys' television, the whole building "
              "squeezed into their hall. When the last wicket fell Mohan and Arun jumped so high they nearly hit the fan.\n\n"
              "Meera went to bed at 2 am still waving the flag.",
     'seed': 1983625},
    {'id': 'diary_1983_07_16', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1983-07-16', 'people': ['Kamla', 'Arun', 'Mohan'], 'places': ['Pune', 'Goregaon']},
     'year': '1983', 'day': 'SATURDAY 16 JULY 1983',
     'entry': "Arun left for Pune today on the Deccan Queen. Admission to the College of Engineering, first list! "
              "Mohan pretended he had dust in his eye at the station.\n\nPacked: 2 bedsheets, his radio, ladoos, and the "
              "slide rule Mohan used in the railway office.",
     'seed': 1983716},
    {'id': 'diary_1983_12_31', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1983-12-31', 'people': ['Kamla', 'Meera', 'Arun'], 'places': ['Goregaon']},
     'year': '1983', 'day': 'SATURDAY 31 DECEMBER 1983',
     'entry': "Last day of a big year. Arun home for the holidays, taller and thinner. Meera topped her class in the "
              "Class X preliminary exam.\n\nWe bought our own television on instalments, a black-and-white Weston. The "
              "Shettys came to watch with us for a change.",
     'seed': 1983123},
    {'id': 'diary_1991_09_10', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1991-09-10', 'people': ['Kamla', 'Meera', 'Vikram'], 'places': ['Goregaon']},
     'year': '1991', 'day': 'TUESDAY 10 SEPTEMBER 1991',
     'entry': "Meera's engagement today. Vikram Deshpande is a quiet, gentle boy, a teacher at the same school where "
              "Meera teaches. Wedding fixed for 8th December.\n\nMohan sang an old Mukesh song after dinner. Everyone "
              "pretended it was good.",
     'seed': 1991910},
    {'id': 'diary_1991_12_08', 'layout': 'diary', 'meta': {'doc_type': 'diary', 'date': '1991-12-08', 'people': ['Kamla', 'Meera', 'Vikram', 'Mohan', 'Arun'], 'places': ['Dadar']},
     'year': '1991', 'day': 'SUNDAY 8 DECEMBER 1991',
     'entry': "Meera's wedding. She wore my wedding saree, red with gold border, from 1963. I made kheer for 200 "
              "guests with three cooks and it was still the first dish to finish.\n\nThe house is very quiet tonight.",
     'stain': True, 'seed': 1991128},

    # ── House papers ─────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'rent_agreement_1972', 'layout': 'typed',
     'meta': {'doc_type': 'house_paper', 'date': '1972-06-01', 'people': ['Mohan'], 'places': ['Goregaon'], 'rent': 150},
     'letterhead': ['LEAVE AND LICENCE AGREEMENT', 'Stamp paper Rs 5  ·  Bombay'], 'ref': 'Regd. No. GR/1972/0418', 'date': '1st June 1972',
     'title': '',
     'body': ("This agreement is made on the first day of June 1972 at Bombay between Shri Dinkar Rao Patil, owner of Flat "
              "No. 6, Shanti Niwas, S. V. Road, Goregaon (West), Bombay 400 062 (the Licensor) and Shri Mohan Krishna "
              "Joshi, employed with the Railways (the Licensee).\n\n"
              "1. The Licensor permits the Licensee and his family to occupy the said flat, consisting of two rooms, a "
              "kitchen and a bathroom, for a period of eleven months from 1st June 1972, renewable by mutual consent.\n\n"
              "2. The Licensee shall pay a monthly compensation of Rs 150 (Rupees one hundred and fifty only) on or before "
              "the fifth day of every month, and a refundable deposit of Rs 600.\n\n"
              "3. Electricity charges shall be paid by the Licensee directly to the Western Suburbs Electricity Board.\n\n"
              "4. The Licensee shall not sublet the flat or carry out any structural change without written consent.\n\n"
              "5. Either party may end this agreement by giving one month's notice in writing.\n\n"
              "In witness whereof the parties have signed this agreement on the date mentioned above."),
     'sign': ['Licensor: D. R. Patil', 'Licensee: M. K. Joshi', 'Witness: R. G. Shetty'], 'signature': 'M. K. Joshi',
     'seed': 1972601},
    {'id': 'sale_deed_1979', 'layout': 'typed',
     'meta': {'doc_type': 'house_paper', 'date': '1979-11-12', 'people': ['Mohan', 'Kamla'], 'places': ['Goregaon'], 'price': 48000},
     'letterhead': ['SUMMARY OF SALE DEED', 'Office of the Sub-Registrar, Andheri, Bombay Suburban District'],
     'ref': 'Document No. AND/4417/1979', 'date': '12th November 1979', 'title': '',
     'body': ("Property: Flat No. 6, second floor, Shanti Niwas Co-operative Housing Society, S. V. Road, Goregaon (West), "
              "Bombay 400 062. Carpet area 420 square feet.\n\n"
              "Seller: Shri Dinkar Rao Patil.\n\n"
              "Buyers: Shri Mohan Krishna Joshi and Smt. Kamla Mohan Joshi, jointly.\n\n"
              "Consideration: Rs 48,000 (Rupees forty-eight thousand only), paid by cheque on Central Railway Employees' "
              "Co-operative Credit Society Ltd. and by cash.\n\n"
              "Stamp duty paid: Rs 1,440.  Registration fee: Rs 480.\n\n"
              "Possession: The buyers are already in occupation of the flat as licensees since 1st June 1972 and shall "
              "continue in possession as owners from the date of registration."),
     'sign': ['Sub-Registrar, Andheri'], 'stamp': ('REGISTERED', '12 NOV 1979'), 'seed': 1979112},
    {'id': 'house_tax_1986', 'layout': 'typed',
     'meta': {'doc_type': 'house_paper', 'date': '1986-04-18', 'people': ['Mohan'], 'places': ['Goregaon'], 'amount': 212},
     'letterhead': ['MUNICIPAL CORPORATION OF GREATER BOMBAY', 'Assessment & Collection Department  ·  P/South Ward'],
     'ref': 'Receipt No. PS-86-11902', 'date': '18th April 1986', 'title': 'PROPERTY TAX RECEIPT',
     'body': ("Received from Shri M. K. Joshi, owner of Flat 6, Shanti Niwas, Goregaon (West), the sum of Rs 212.00 "
              "(Rupees two hundred and twelve only) towards property tax for the year 1986-87.\n\n"
              "General tax Rs 128.00 · Water tax Rs 54.00 · Education cess Rs 30.00.\n\n"
              "Paid in cash at the ward office counter."),
     'sign': ['Cashier, P/South Ward'], 'stamp': ('PAID', '18 APR 1986'), 'seed': 1986418},

    # ── Report cards ─────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'report_arun_1975', 'layout': 'report', 'meta': {'doc_type': 'report_card', 'date': '1975-04', 'people': ['Arun', 'Mohan'], 'places': ['Goregaon']},
     'school': 'Aarey Road Municipal School, Goregaon', 'year': '1974-75', 'name': 'Arun Mohan Joshi', 'cls': 'V  A', 'roll': '7',
     'subjects': [('English', 66, 'B'), ('Hindi', 81, 'A'), ('Marathi', 70, 'B'), ('Arithmetic', 95, 'A+'), ('General Science', 79, 'B+'), ('Drawing', 58, 'C')],
     'total': '449 / 600', 'result': 'Passed, promoted to Class VI', 'remarks': 'Very quick at sums. Talks too much in class.',
     'teacher': 'M. Fernandes', 'parent_sign': 'M. K. Joshi', 'seed': 1975401},
    {'id': 'report_meera_1979', 'layout': 'report', 'meta': {'doc_type': 'report_card', 'date': '1979-04', 'people': ['Meera', 'Kamla'], 'places': ['Goregaon']},
     'school': 'Aarey Road Municipal School, Goregaon', 'year': '1978-79', 'name': 'Meera Mohan Joshi', 'cls': 'VI  A', 'roll': '15',
     'subjects': [('English', 84, 'A'), ('Hindi', 88, 'A'), ('Marathi', 79, 'B+'), ('Mathematics', 71, 'B'), ('Science', 76, 'B+'), ('Drawing', 90, 'A+')],
     'total': '488 / 600', 'result': 'Passed, promoted to Class VII', 'remarks': 'A born storyteller. Helps her classmates.',
     'teacher': 'M. Fernandes', 'parent_sign': 'Kamla Joshi', 'hand': 'kamla', 'seed': 1979402},
    {'id': 'report_meera_1983', 'layout': 'report', 'meta': {'doc_type': 'report_card', 'date': '1983-04', 'people': ['Meera', 'Mohan'], 'places': ['Goregaon']},
     'school': 'Aarey Road Municipal High School, Goregaon', 'year': '1982-83', 'name': 'Meera Mohan Joshi', 'cls': 'IX  A', 'roll': '4',
     'subjects': [('English', 88, 'A'), ('Hindi', 91, 'A+'), ('Marathi', 85, 'A'), ('Mathematics', 74, 'B+'), ('Science', 80, 'A'), ('History & Geography', 87, 'A')],
     'total': '505 / 600', 'result': 'Passed, promoted to Class X, first in class', 'remarks': 'Outstanding. Should consider teaching or writing.',
     'teacher': 'S. Kulkarni', 'parent_sign': 'M. K. Joshi', 'seed': 1983403},

    # ── Invitations ──────────────────────────────────────────────────────────────────────────────────────────────
    {'id': 'invitation_1963_wedding', 'layout': 'invitation',
     'meta': {'doc_type': 'invitation', 'date': '1963-05-12', 'people': ['Mohan', 'Kamla'], 'places': ['Indore']},
     'top': '|| Shri Ganeshaya Namah ||',
     'lines_before': ['Shri Ramchandra Pathak and Smt. Sushila Pathak', 'request the pleasure of your company', 'at the marriage of their daughter'],
     'names': 'Kamla  with  Mohan',
     'lines_after': ['son of Late Shri Krishna Joshi and Smt. Parvati Joshi of Sagar', 'on Sunday, the 12th of May 1963, at 7 p.m.', 'at Pathak Bhavan, 14 Snehlataganj, Indore'],
     'rsvp': 'Compliments from: Savitri and all the Pathak family', 'seed': 1963512},
    {'id': 'invitation_1991_meera', 'layout': 'invitation',
     'meta': {'doc_type': 'invitation', 'date': '1991-12-08', 'people': ['Meera', 'Vikram', 'Mohan', 'Kamla'], 'places': ['Dadar']},
     'top': '|| Shri Ganeshaya Namah ||',
     'lines_before': ['Shri Mohan Krishna Joshi and Smt. Kamla Joshi', 'invite you to bless', 'the marriage of their daughter'],
     'names': 'Meera  with  Vikram',
     'lines_after': ['son of Shri and Smt. Deshpande, Thane', 'on Sunday, 8th December 1991, at 11.30 a.m.', 'at Shivaji Park Hall, Dadar, Bombay'],
     'rsvp': 'Lunch follows the ceremony', 'seed': 1991120},
    {'id': 'invitation_1993_arun', 'layout': 'invitation',
     'meta': {'doc_type': 'invitation', 'date': '1993-02-14', 'people': ['Arun', 'Anjali', 'Mohan', 'Kamla'], 'places': ['Pune']},
     'top': '|| Shri Ganeshaya Namah ||',
     'lines_before': ['Shri Mohan Krishna Joshi and Smt. Kamla Joshi', 'request your presence at', 'the wedding of their son'],
     'names': 'Arun  with  Anjali',
     'lines_after': ['daughter of Shri and Smt. Kelkar, Pune', 'on Sunday, 14th February 1993, at 10 a.m.', 'at Kelkar Wada, Sadashiv Peth, Pune'],
     'rsvp': 'Reception at 7 p.m., same venue', 'seed': 1993214},

    # ── Ration card and the first job ────────────────────────────────────────────────────────────────────────────
    {'id': 'ration_card_1969', 'layout': 'ration',
     'meta': {'doc_type': 'ration_card', 'date': '1969-01-20', 'people': ['Mohan', 'Kamla', 'Arun', 'Meera'], 'places': ['Goregaon']},
     'office': 'Rationing Office 41-G, Bombay Suburban', 'card_no': 'G/41/20457', 'issued': '20-01-1969',
     'head': 'Mohan Krishna Joshi', 'address': 'Block C-14, Railway Colony, Goregaon (East), Bombay',
     'members': [('Mohan K. Joshi', 'Self', 34), ('Kamla M. Joshi', 'Wife', 28), ('Arun M. Joshi', 'Son', 3), ('Meera M. Joshi', 'Daughter', 'under 1')],
     'shop': 'No. 112, Station Road, Goregaon (E)', 'seed': 1969120},
    {'id': 'appointment_1962', 'layout': 'typed',
     'meta': {'doc_type': 'official_letter', 'date': '1962-03-20', 'people': ['Mohan'], 'places': ['Jabalpur'], 'salary': 180},
     'letterhead': ['OFFICE OF THE DIVISIONAL ACCOUNTS OFFICER', 'Railway Divisional Office, Jabalpur'],
     'ref': 'No. E/Accts/62/117', 'date': '20th March 1962', 'title': 'APPOINTMENT LETTER',
     'body': ("To\nShri Mohan Krishna Joshi\nc/o Shri Ramesh Dubey, near Railway Station, Jabalpur\n\n"
              "With reference to your application and the selection test held on 5th February 1962, you are hereby "
              "appointed as Junior Clerk in the Accounts Section of this office on a temporary basis.\n\n"
              "You will draw a pay of Rs 180 per month in the scale of Rs 110-180, plus admissible allowances.\n\n"
              "You are requested to report for duty at this office on Monday, 2nd April 1962, at 10 a.m., with your "
              "school leaving certificate and two passport photographs."),
     'sign': ['Divisional Accounts Officer', 'Jabalpur'], 'stamp': ('ACCOUNTS', 'JABALPUR'), 'seed': 1962320},
]

# ── Electricity bills, Dec 1984 to Jan 1986 (one Flat 6, Shanti Niwas meter) ───────────────────────────────────────
# The twelve 1985 bills add up to exactly Rs 1,284.00 (the bills tool's answer). Each bill: units x Rs 0.62 + Rs 12
# fixed + electricity duty. The December 1985 bill is dated 6 January 1986: tagging bills by their print date
# instead of their billing month puts it in the wrong year (the Part 3 bug).
MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
LAST_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
BILLS = [  # (year, month, units, total)
    (1984, 12, 121, 94.00),
    (1985, 1, 126, 98.00), (1985, 2, 118, 92.00), (1985, 3, 141, 108.00), (1985, 4, 162, 122.00),
    (1985, 5, 178, 133.00), (1985, 6, 165, 124.00), (1985, 7, 136, 104.00), (1985, 8, 131, 101.00),
    (1985, 9, 129, 99.00), (1985, 10, 134, 103.00), (1985, 11, 130, 99.00), (1985, 12, 132, 101.00),
    (1986, 1, 128, 99.00),
]
assert sum(t for y, m, u, t in BILLS if y == 1985) == 1284.00
reading = 18342 - (121 + 126 + 118 + 141 + 162 + 178 + 165)  # so that July 1985 starts at 18342, as in the sample
for y, m, units, total in BILLS:
    energy = round(units * 0.62, 2)
    duty = round(total - 12.00 - energy, 2)
    assert 0 < duty < energy * 0.15, (y, m, duty)
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    DOCS.append({
        'id': f'bill_{y}_{m:02d}', 'layout': 'bill',
        'meta': {'doc_type': 'bill', 'date': f'{ny}-{nm:02d}-06', 'billing_month': f'{y}-{m:02d}', 'amount': total, 'units': units,
                 'people': ['Mohan'], 'places': ['Goregaon']},
        'consumer': '214-0873-56', 'name': 'Shri M. K. Joshi', 'address': 'Flat 6, Shanti Niwas, Goregaon (W)',
        'month': f'{MONTHS[m - 1]} {y}', 'period': f'01-{m:02d}-{y} to {LAST_DAY[m - 1]}-{m:02d}-{y}',
        'bill_date': f'06-{nm:02d}-{ny}', 'due': f'20-{nm:02d}-{ny}',
        'prev': reading, 'pres': reading + units, 'rate': 0.62, 'fixed': 12.00, 'duty': duty, 'total': total,
        'paid': f'{12 + m % 5} {MONTHS[nm - 1][:3]} {ny}', 'seed': y * 100 + m,
    })
    reading += units

# The July 1985 bill above replaces the hand-written sample at the top of the list.
DOCS = [d for i, d in enumerate(DOCS) if not (d['id'] == 'bill_1985_07' and i < 10)]
