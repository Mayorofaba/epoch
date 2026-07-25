import argparse
import pandas as pd
import random
from pathlib import Path

parser = argparse.ArgumentParser(description='Expand emergency_reports dataset')
parser.add_argument('--target', type=int, default=1000, help='Target total number of rows')
args = parser.parse_args()

path = Path(__file__).parent.parent / "data" / "emergency_reports.csv"
print("Loading", path)
df = pd.read_csv(path, dtype=str, keep_default_na=False, na_filter=False)
print("Current rows", len(df))

df.loc[df["Category"] == "Other", "Category"] = "Cultism"
print("Replaced 'Other' with 'Cultism' in existing rows", len(df[df["Category"] == "Cultism"]))

categories = [
    "Flooding",
    "Power Outage",
    "Water Supply",
    "Road Damage",
    "Waste Management",
    "Public Safety",
    "Theft",
    "Robbery",
    "Burglary",
    "Assault",
    "Kidnapping",
    "Homicide",
    "Road Traffic Accident",
    "Cultism",
]
severities = ["Low", "Medium", "High", "Critical"]

states = {
    "Abia": [
        "Aba North",
        "Aba South",
        "Arochukwu",
        "Bende",
        "Ikwuano",
        "Isiala Ngwa North",
        "Isiala Ngwa South",
        "Isuikwuato",
        "Obi Ngwa",
        "Ohafia",
        "Osisioma Ngwa",
        "Ugwunagbo",
        "Ukwa East",
        "Ukwa West",
        "Umuahia North",
        "Umuahia South",
        "Umu Nneochi",
    ],
    "Adamawa": ["Yola South", "Girei"],
    "Akwa Ibom": ["Uyo", "Eket"],
    "Anambra": ["Onitsha South", "Awka North"],
    "Bauchi": ["Darazo", "Ningi"],
    "Bayelsa": ["Yenagoa", "Sagbama"],
    "Benue": ["Makurdi", "Gboko"],
    "Borno": ["Maiduguri Metropolitan", "Chibok"],
    "Cross River": ["Calabar Municipal", "Ikom"],
    "Delta": ["Ughelli North", "Warri South"],
    "Ebonyi": ["Abakaliki North", "Ikwo"],
    "Edo": ["Oredo", "Uhunmwonde"],
    "Ekiti": ["Ado Ekiti North", "Ikere"],
    "Enugu": ["Enugu North", "Nsukka"],
    "Gombe": ["Akko", "Dukku"],
    "Imo": ["Owerri Municipal", "Orlu"],
    "Jigawa": ["Dutse", "Hadejia"],
    "Kaduna": ["Chikun", "Zaria"],
    "Kano": ["Nassarawa", "Tarauni"],
    "Katsina": ["Funtua", "Kankia"],
    "Kebbi": ["Birnin Kebbi", "Argungu"],
    "Kogi": ["Lokoja", "Idah"],
    "Kwara": ["Ilorin East", "Offa"],
    "Lagos": ["Ikeja", "Alimosho"],
    "Nasarawa": ["Karu", "Akwanga"],
    "Niger": ["Minna", "Suleja"],
    "Ogun": ["Abeokuta North", "Ifo"],
    "Ondo": ["Akure South", "Owo"],
    "Osun": ["Osogbo", "Ife North"],
    "Oyo": ["Ibadan North", "Ogbomosho North"],
    "Plateau": ["Jos North", "Bokkos"],
    "Rivers": ["Port Harcourt City", "Obio/Akpor"],
    "Sokoto": ["Sokoto North", "Binji"],
    "Taraba": ["Jalingo", "Wukari"],
    "Yobe": ["Damaturu", "Potiskum"],
    "Zamfara": ["Gusau", "Tsafe"],
    "FCT": ["Abuja Municipal", "Gwagwalada"],
}

lga_towns = {
    ("Abia", "Aba North"): ["Eziama", "Osusu", "Ogbor Hill", "Umuola", "Ehere"],
    ("Abia", "Aba South"): ["Asaokpuaja", "Abariba", "Ohanku", "Ndiegoro", "Eziukwu"],
    ("Abia", "Arochukwu"): ["Arochukwu Town", "Ibom", "Ututu", "Ihechiowa", "Isu"],
    ("Abia", "Bende"): ["Bende Town", "Alayi", "Igbere", "Item", "Nkpa", "Ugwueke"],
    ("Abia", "Ikwuano"): ["Ariam", "Ibere", "Oboro", "Oloko"],
    ("Abia", "Isiala Ngwa North"): ["Isialangwa", "Ameke", "Uturu", "Okpuala Ngwa"],
    ("Abia", "Isiala Ngwa South"): ["Nvosi", "Ovu-Ngwa", "Ovu-Okwu", "Mbutu", "Okpuisiala"],
    ("Abia", "Isuikwuato"): ["Uturu", "Isuikwuato Town", "Achara-Uturu", "Ezere", "Umuasua"],
    ("Abia", "Obi Ngwa"): ["Obohia", "Ohuru", "Azumini", "Itumbuzo", "Amuzu"],
    ("Abia", "Ohafia"): ["Elu", "Ebem", "Akanu", "Asaga", "Nde Okoro"],
    ("Abia", "Osisioma Ngwa"): ["Osisioma", "Amator", "Umuimo", "Abayi"],
    ("Abia", "Ugwunagbo"): ["Ugwunagbo", "Warduma", "Obegu", "Umugo"],
    ("Abia", "Ukwa East"): ["Akwete", "Azumini", "Ohandu", "Ohambele"],
    ("Abia", "Ukwa West"): ["Oke-Ikpe", "Obingwu", "Omuma-Uzor", "Asa"],
    ("Abia", "Umuahia North"): ["Umuahia Town", "Nkwoegwu", "Ofeme", "Isingwu"],
    ("Abia", "Umuahia South"): ["Ubakala", "Amakama", "Nsirimo", "Old Umuahia"],
    ("Abia", "Umu Nneochi"): ["Nneochi", "Ubahu", "Leru", "Lomta", "Amuda"],
    ("Adamawa", "Yola South"): ["Yola"],
    ("Adamawa", "Girei"): ["Girei"],
    ("Akwa Ibom", "Uyo"): ["Uyo"],
    ("Akwa Ibom", "Eket"): ["Eket"],
    ("Anambra", "Onitsha South"): ["Onitsha"],
    ("Anambra", "Awka North"): ["Awka"],
    ("Bauchi", "Darazo"): ["Darazo"],
    ("Bauchi", "Ningi"): ["Ningi"],
    ("Bayelsa", "Yenagoa"): ["Yenagoa"],
    ("Bayelsa", "Sagbama"): ["Sagbama"],
    ("Benue", "Makurdi"): ["Makurdi"],
    ("Benue", "Gboko"): ["Gboko"],
    ("Borno", "Maiduguri Metropolitan"): ["Maiduguri"],
    ("Borno", "Chibok"): ["Chibok"],
    ("Cross River", "Calabar Municipal"): ["Calabar"],
    ("Cross River", "Ikom"): ["Ikom"],
    ("Delta", "Ughelli North"): ["Ughelli"],
    ("Delta", "Warri South"): ["Warri"],
    ("Ebonyi", "Abakaliki North"): ["Abakaliki"],
    ("Ebonyi", "Ikwo"): ["Ikwo"],
    ("Edo", "Oredo"): ["Benin City"],
    ("Edo", "Uhunmwonde"): ["Uromi"],
    ("Ekiti", "Ado Ekiti North"): ["Ado Ekiti"],
    ("Ekiti", "Ikere"): ["Ikere"],
    ("Enugu", "Enugu North"): ["Enugu"],
    ("Enugu", "Nsukka"): ["Nsukka"],
    ("Gombe", "Akko"): ["Gombe"],
    ("Gombe", "Dukku"): ["Dukku"],
    ("Imo", "Owerri Municipal"): ["Owerri"],
    ("Imo", "Orlu"): ["Orlu"],
    ("Jigawa", "Dutse"): ["Dutse"],
    ("Jigawa", "Hadejia"): ["Hadejia"],
    ("Kaduna", "Chikun"): ["Kaduna"],
    ("Kaduna", "Zaria"): ["Zaria"],
    ("Kano", "Nassarawa"): ["Kano"],
    ("Kano", "Tarauni"): ["Kano"],
    ("Katsina", "Funtua"): ["Funtua"],
    ("Katsina", "Kankia"): ["Kankia"],
    ("Kebbi", "Birnin Kebbi"): ["Birnin Kebbi"],
    ("Kebbi", "Argungu"): ["Argungu"],
    ("Kogi", "Lokoja"): ["Lokoja"],
    ("Kogi", "Idah"): ["Idah"],
    ("Kwara", "Ilorin East"): ["Ilorin"],
    ("Kwara", "Offa"): ["Offa"],
    ("Lagos", "Ikeja"): ["Ikeja"],
    ("Lagos", "Alimosho"): ["Ikeja"],
    ("Nasarawa", "Karu"): ["Mararaba"],
    ("Nasarawa", "Akwanga"): ["Akwanga"],
    ("Niger", "Minna"): ["Minna"],
    ("Niger", "Suleja"): ["Suleja"],
    ("Ogun", "Abeokuta North"): ["Abeokuta"],
    ("Ogun", "Ifo"): ["Ifo"],
    ("Ondo", "Akure South"): ["Akure"],
    ("Ondo", "Owo"): ["Owo"],
    ("Osun", "Osogbo"): ["Osogbo"],
    ("Osun", "Ife North"): ["Ile-Ife"],
    ("Oyo", "Ibadan North"): ["Ibadan"],
    ("Oyo", "Ogbomosho North"): ["Ogbomosho"],
    ("Plateau", "Jos North"): ["Jos"],
    ("Plateau", "Bokkos"): ["Bokkos"],
    ("Rivers", "Port Harcourt City"): ["Port Harcourt"],
    ("Rivers", "Obio/Akpor"): ["Rumuokoro"],
    ("Sokoto", "Sokoto North"): ["Sokoto"],
    ("Sokoto", "Binji"): ["Binji"],
    ("Taraba", "Jalingo"): ["Jalingo"],
    ("Taraba", "Wukari"): ["Wukari"],
    ("Yobe", "Damaturu"): ["Damaturu"],
    ("Yobe", "Potiskum"): ["Potiskum"],
    ("Zamfara", "Gusau"): ["Gusau"],
    ("Zamfara", "Tsafe"): ["Tsafe"],
    ("FCT", "Abuja Municipal"): ["Abuja"],
    ("FCT", "Gwagwalada"): ["Gwagwalada"],
}

random.seed(42)

state_town_pairs = []
for state_name, lgas in states.items():
    for lga_name in lgas:
        towns = lga_towns.get((state_name, lga_name), [lga_name])
        for town_name in towns:
            state_town_pairs.append((state_name, lga_name, town_name))

existing_town_pairs = set(
    tuple(x)
    for x in df[["State", "LocalGovernment", "Town"]].dropna().itertuples(index=False, name=None)
)
existing_category_pairs = set(
    tuple(x)
    for x in df[["State", "LocalGovernment", "Category"]].dropna().itertuples(index=False, name=None)
)

rows = []
idx = len(df) + 1
new_town_pairs = set()
new_category_pairs = set()

# Ensure every Abia LGA has at least one row for every category.
for lga_name in states["Abia"]:
    towns = lga_towns.get(("Abia", lga_name), [lga_name])
    for category in categories:
        if ("Abia", lga_name, category) in existing_category_pairs:
            continue
        town_name = random.choice(towns)
        severity = random.choice(severities)
        desc = f"{category} incident reported in {town_name}, {lga_name}, Abia"
        reporter = f"Reporter {idx}"
        contact = f"080{random.randint(10000000, 99999999)}"
        loc = f"{town_name} main street"
        row = {col: "" for col in df.columns}
        row["ReportID"] = f"RPT{1000000 + idx}"
        row["Description"] = desc
        row["Location"] = loc
        row["DateTime"] = f"2026-07-24T18:{idx % 60:02d}:00"
        row["Category"] = category
        row["Severity"] = severity
        row["ReporterName"] = reporter
        row["ReporterContact"] = contact
        row["Latitude"] = ""
        row["Longitude"] = ""
        row["ImageURL"] = ""
        row["ResponseStatus"] = "pending"
        row["Country"] = "Nigeria"
        row["State"] = "Abia"
        row["LocalGovernment"] = lga_name
        row["Town"] = town_name
        rows.append(row)
        new_category_pairs.add(("Abia", lga_name, category))
        new_town_pairs.add(("Abia", lga_name, town_name))
        idx += 1

# Ensure every Abia town has at least one report.
for state_name, lga_name, town_name in state_town_pairs:
    if state_name != "Abia":
        continue
    if (state_name, lga_name, town_name) in existing_town_pairs:
        continue
    if (state_name, lga_name, town_name) in new_town_pairs:
        continue
    category = random.choice(categories)
    severity = random.choice(severities)
    desc = f"{category} incident reported in {town_name}, {lga_name}, {state_name}"
    reporter = f"Reporter {idx}"
    contact = f"080{random.randint(10000000, 99999999)}"
    loc = f"{town_name} main street"
    row = {col: "" for col in df.columns}
    row["ReportID"] = f"RPT{1000000 + idx}"
    row["Description"] = desc
    row["Location"] = loc
    row["DateTime"] = f"2026-07-24T18:{idx % 60:02d}:00"
    row["Category"] = category
    row["Severity"] = severity
    row["ReporterName"] = reporter
    row["ReporterContact"] = contact
    row["Latitude"] = ""
    row["Longitude"] = ""
    row["ImageURL"] = ""
    row["ResponseStatus"] = "pending"
    row["Country"] = "Nigeria"
    row["State"] = state_name
    row["LocalGovernment"] = lga_name
    row["Town"] = town_name
    rows.append(row)
    new_town_pairs.add((state_name, lga_name, town_name))
    idx += 1

print(f"Added {len(rows)} Abia coverage rows")

# Add random entries until target is reached.
while len(df) + len(rows) < args.target:
    state_name = random.choice(list(states.keys()))
    lga_name = random.choice(states[state_name])
    town_name = random.choice(lga_towns[(state_name, lga_name)])
    category = random.choice(categories)
    severity = random.choice(severities)
    desc = f"{category} incident reported in {town_name}, {lga_name}, {state_name}"
    reporter = f"Reporter {idx}"
    contact = f"080{random.randint(10000000, 99999999)}"
    loc = f"{town_name} main street"
    row = {col: "" for col in df.columns}
    row["ReportID"] = f"RPT{1000000 + idx}"
    row["Description"] = desc
    row["Location"] = loc
    row["DateTime"] = f"2026-07-24T18:{idx % 60:02d}:00"
    row["Category"] = category
    row["Severity"] = severity
    row["ReporterName"] = reporter
    row["ReporterContact"] = contact
    row["Latitude"] = ""
    row["Longitude"] = ""
    row["ImageURL"] = ""
    row["ResponseStatus"] = "pending"
    row["Country"] = "Nigeria"
    row["State"] = state_name
    row["LocalGovernment"] = lga_name
    row["Town"] = town_name
    rows.append(row)
    idx += 1

print(f"Added {len(rows)} total rows")

new_df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
new_df.to_csv(path, index=False)
print("New row count", len(new_df))
