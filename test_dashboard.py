#Test 1: JSON Datenspeicherung
import json

daten = {
    "studiengang": "Medizinische Informatik",
    "ziel_abschluss": "17.11.2028",
    "module": [
        {"name": "Objektorientierte und funktionale Programmierung mit Python (DLBDSOOFPP01_D)", "ects": 5, "status": "BESTANDEN", "note": 1.4}
    ]
}

with open("dashboard.json", "w") as f:
    json.dump(daten, f, indent=2)

with open("dashboard.json", "r") as f:
    geladen = json.load(f)

print(geladen["studiengang"])
for modul in geladen["module"]:
    print(f"{modul['name']}: {modul['note']}")

#Test2: Ausgabe Kommandozeilen
ects_aktuell = 40
ects_gesamt = 180
durchschnitt = 1.65

print("=== Studien-Dashboard ===")
print(f"ECTS:               {ects_aktuell} / {ects_gesamt}")
print(f"Durchschnitt:       {durchschnitt}")
print(f"Abschlussdatum:     17.11.2028")
