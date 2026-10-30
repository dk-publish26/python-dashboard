# README - Studium-Dashboard
---
## Zusammenfassung
Eine Python-Projektarbeit zur Studiengangübersicht. 

## Funktionen:
-	Anzeige aller Module pro Semester mit ECTS und Status
-	Fortschritt durch Anerkennungen oder Prüfungsleistungen
-	Berechnung der erreichten ECTS und dem danach gewichteten Notendurchschnitt
-	Berechnung Abschlussdatum nach aktuellem Fortschritt 
-	Anzeige Zielnote und geplantem Abschlussdatum
-	Inkl. Beispieldaten beim Start
  
## Anleitung/Voraussetzung
-	Python-Version (mindestens 3.10), keine zusätzlichen Pakete notwendig
-	Git clone https://github.com/dk-publish26/python-dashboard (für Git-Nutzer) oder Repository als ZIP herunterladen (Grüner Button auf Github verwenden). 
-	Programm starten mit Startbefehl: python dashboard.py
-	Getestet auf Windows

## Berechnungsregeln
-	Modulstatus: Ohne anerkannten Nachweis oder bei Noten über 4.0 bleibt ein Modul offen. Eine bestandene Prüfungsleistung wird als „BESTANDEN“ und eine anerkannte Leistung als „AN-ERKANNT“ gekennzeichnet. 
-	ECTS: Bestandene und anerkannte Module zählen zum Studienfortschritt
-	Notendurchschnitt: nach ECTS-gewichtet werden nur bestandene Prüfungsleistungen mit der jeweiligen Note zur Berechnung herangezogen. Anerkennungen sind davon ausgeschlossen. 
(Noten müssen zwischen 1,0 und 5.0 liegen)
-	Abschlussdatum: Aus den verbleibenden ECTS wird mit der Annahme 30 ECTS pro 180 Tage die Restzeit berechnet. Das voraussichtliche Abschlussdatum ergibt sich aus ausstehenden ECTS geteilt durch den angenommenen Fortschritt. 


