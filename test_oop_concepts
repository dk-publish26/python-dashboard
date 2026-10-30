"""Konsolen-Dashboard zur Anzeige von Studienleistungen und Fortschritt."""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from pathlib import Path

DATEN_PFAD = Path(__file__).parent / "studiengang.json"


# ---- Enums ----


class Pruefungsart(Enum):
    """Zulässige Prüfungsarten für Prüfungsleistungen. Werte als Strings für die Anzeige."""

    KLAUSUR = "KLAUSUR"
    HAUSARBEIT = "HAUSARBEIT"
    PORTFOLIO = "PORTFOLIO"
    PROJEKTARBEIT = "PROJEKTARBEIT"


class Status(Enum):
    """Modulstatus – bewusst auf drei Werte beschränkt.
    NICHT_BESTANDEN wird nicht angezeigt (Designentscheidung aus Phase 1).
    """

    OFFEN = "OFFEN"
    BESTANDEN = "BESTANDEN"
    ANERKANNT = "ANERKANNT"


# ---- Domain ----


@dataclass
class Leistungsnachweis(ABC):
    """
    Abstrakte Basisklasse für Leistungsnachweise (Prüfungsleistungen und Anerkennungen).
    Nur Pruefungsleistung und Anerkennung sind konkrete Ausprägungen.
    """

    datum: date

    @property
    @abstractmethod
    def beitrag_status(self) -> Status:
        """Gibt den Status zurück, den dieser Nachweis dem Modul verleiht."""
        ...


@dataclass
class Pruefungsleistung(Leistungsnachweis):
    """Bestandene oder nicht bestandene Prüfung mit Note und Prüfungsart."""

    note: float
    pruefungs_art: Pruefungsart

    def __post_init__(self):
        """Validiert die Note, um sicherzustellen, dass sie zwischen 1.0 und 5.0 liegt.
        Raises:
            ValueError: Wenn die Note außerhalb des erlaubten Bereichs liegt.
        """
        if not 1.0 <= self.note <= 5.0:
            raise ValueError(
                f"Note muss zwischen 1.0 und 5.0 liegen, erhalten: {self.note}"
            )

    @property
    def beitrag_status(self) -> Status:
        """
        Note bis 4,0 gilt als bestanden und darüber bleibt offen, da
        NICHT_BESTANDEN bewusst nicht modelliert wird.
        """
        return Status.BESTANDEN if self.note <= 4.0 else Status.OFFEN


@dataclass
class Anerkennung(Leistungsnachweis):
    """Anerkennung einer externen Leistung für ein Modul als Prüfungsleistungs-Äquivalent."""

    leistung: str
    leistung_institution: str

    @property
    def beitrag_status(self) -> Status:
        """
        Eine Anerkennung verleiht dem Modul immer den Status ANERKANNT
        """
        return Status.ANERKANNT


@dataclass
class Modul:
    """Ein Studienmodul mit Name und ECTS sowie jeweils einer Prüfungsleistung oder Anerkennung als Leistungsnachweis."""

    name: str
    ects: int
    leistungsnachweis: Leistungsnachweis | None = None

    def __post_init__(self):
        """Validiert, dass ECTS größer als 0 ist."""
        if not self.ects > 0:
            raise ValueError(f"ECTS muss größer als 0 sein, erhalten: {self.ects}")

    @property
    def status(self) -> Status:
        """Leitet den Status aus dem Nachweis ab; ohne Nachweis gilt OFFEN."""
        if self.leistungsnachweis is None:
            return Status.OFFEN
        return self.leistungsnachweis.beitrag_status


@dataclass
class Semester:
    """Enthält alle Module eines Semesters."""

    nummer: int
    module: list[Modul] = field(default_factory=list)


@dataclass
class Studiengang:
    """Enthält alle Stammdaten und Ziele des Studiums."""

    name: str
    zielstudiendatum: date
    immatrikulationsdatum: date
    zielnote: float
    semester: list[Semester] = field(default_factory=list)
    gesamt_ects: int = 180

    def __post_init__(self):
        """Prüft Zielnote und Gesamt-ECTS.
        Raises:
            ValueError: Wenn die Zielnote außerhalb von 1,0 bis 5,0 liegt
            oder die Gesamt-ECTS nicht positiv sind.
        """
        if not 1.0 <= self.zielnote <= 5.0:
            raise ValueError(
                f"Zielnote muss zwischen 1.0 und 5.0 liegen, erhalten: {self.zielnote}"
            )
        if not self.gesamt_ects > 0:
            raise ValueError(
                f"Gesamt-ECTS muss größer als 0 sein, erhalten: {self.gesamt_ects}"
            )


@dataclass
class Studienfortschritt:
    """Berechnete Kennzahlen für die Dashboard-Anzeige."""

    erreichte_ects: int = 0
    notendurchschnitt: float | None = None
    prognostiziertes_abschlussdatum: date | None = None


# ---- DTO ----


@dataclass
class ModulDatenDTO:
    """
    Datentransferobjekt für die Anzeige eines Moduls.
    Enthält nur die Daten, die die View benötigt.
    """

    name: str
    ects: int
    status: Status
    semester: int


@dataclass
class DashboardDatenDTO:
    """
    Datentransferobjekt für die Dashboard-Anzeige.
    Fasst Studiengang und berechneten Fortschritt zusammen –
    die View arbeitet nur mit diesem Objekt.
    """

    studiengangsname: str
    erreichte_ects: int
    notendurchschnitt: float | None
    zielnote: float
    zieldatum: date
    prognostiziertes_abschlussdatum: date | None
    module: list[ModulDatenDTO]
    gesamt_ects: int


# ---- Repository ----


class StudiengangRepository(ABC):
    """
    Abstraktes Repository für den Zugriff auf Studiengang-Daten.
    Konkrete Implementierungen entscheiden, ob die Daten im
    Speicher, als JSON oder in einer Datenbank liegen.
    """

    @abstractmethod
    def laden(self) -> Studiengang:
        """Lädt und gibt den aktuellen Studiengang zurück."""
        ...

    @abstractmethod
    def speichern(self, studiengang: Studiengang) -> None:
        """Speichert Änderungen am Studiengang."""
        ...


class InMemoryStudiengangRepository(StudiengangRepository):
    """
    In-Memory-Implementierung des Repositories.
    Festkodierte Testdaten ohne notwendigen Datenzugriff.
    """

    def __init__(self):
        """Initialisiert das Repository mit festkodierten Testdaten."""
        p1 = Pruefungsleistung(
            datum=date(2025, 3, 15),
            note=1.7,
            pruefungs_art=Pruefungsart.KLAUSUR,
        )
        p2 = Pruefungsleistung(
            datum=date(2025, 6, 20),
            note=2.3,
            pruefungs_art=Pruefungsart.PORTFOLIO,
        )
        p3 = Pruefungsleistung(
            datum=date(2025, 6, 20),
            note=5.0,
            pruefungs_art=Pruefungsart.KLAUSUR,
        )
        a1 = Anerkennung(
            datum=date(2024, 10, 1),
            leistung="Medizinische Grundlagen für Informatiker",
            leistung_institution="Ludwig-Maximilians-Universität München",
        )

        m1 = Modul(name="Python", ects=5, leistungsnachweis=p1)
        m2 = Modul(name="E-Health", ects=5, leistungsnachweis=p2)
        m3 = Modul(name="Medizinische Grundlagen", ects=5, leistungsnachweis=a1)
        m4 = Modul(name="Mathematik", ects=5)
        m5 = Modul(name="Statistik", ects=5, leistungsnachweis=p3)

        sem1 = Semester(nummer=1)
        sem1.module.extend([m1, m2])
        sem2 = Semester(nummer=2)
        sem2.module.extend([m3, m4, m5])

        sg = Studiengang(
            name="Medizinische Informatik",
            zielstudiendatum=date(2027, 9, 30),
            immatrikulationsdatum=date(2024, 10, 1),
            zielnote=2.0,
            gesamt_ects=180,
        )
        sg.semester.extend([sem1, sem2])
        self._studiengang = sg

    def laden(self) -> Studiengang:
        """Gibt den gespeicherten Studiengang ohne Kopie zurück."""
        return self._studiengang

    def speichern(self, studiengang: Studiengang) -> None:
        """Ersetzt den Studiengang im Arbeitsspeicher dieser Instanz."""
        self._studiengang = studiengang


class JsonStudiengangRepository(StudiengangRepository):
    """
    JSON-Implementierung des Repositories.
    Lädt und speichert den Studiengang in einer JSON-Datei.
    """

    def __init__(self, dateipfad: str | Path) -> None:
        """Initialisiert das Repository mit dem Pfad zur JSON-Datei.
        Args:
            dateipfad: Pfad zur JSON-Datei, in der der jeweilige Studiengang gespeichert ist.
        """
        self.dateipfad = dateipfad

    def _leistungsnachweis_zu_dict(self, ln: Leistungsnachweis) -> dict:
        """Wandelt eine Prüfung oder Anerkennung in JSON-kompatible Daten um.
        Raises:
            TypeError: Wenn der Nachweistyp nicht unterstützt wird.
        """
        if isinstance(ln, Pruefungsleistung):
            return {
                "typ": "Pruefungsleistung",  # Typ als String für die JSON-Darstellung
                "datum": ln.datum.isoformat(),
                "note": ln.note,
                "pruefungs_art": ln.pruefungs_art.value,
            }
        elif isinstance(ln, Anerkennung):
            return {
                "typ": "Anerkennung",
                "datum": ln.datum.isoformat(),
                "leistung": ln.leistung,
                "leistung_institution": ln.leistung_institution,
            }
        else:
            raise TypeError(f"Unbekannter Leistungsnachweis-Typ: {type(ln)}")

    def _modul_zu_dict(self, modul: Modul) -> dict:
        """Konvertiert ein Modul in ein Dictionary für die JSON-Darstellung.
        Args:
            modul: Ein Modul-Objekt, das konvertiert werden soll.
        Returns:
            dict: Ein Dictionary, das das Modul repräsentiert.
        """
        return {
            "name": modul.name,
            "ects": modul.ects,
            "leistungsnachweis": self._leistungsnachweis_zu_dict(
                modul.leistungsnachweis
            )
            if modul.leistungsnachweis
            else None,
        }

    def _semester_zu_dict(self, semester: Semester) -> dict:
        """Konvertiert ein Semester in ein Dictionary für die JSON-Darstellung.
        Args:
            semester: Ein Semester-Objekt, das konvertiert werden soll.
        Returns:
            dict: Ein Dictionary, das das Semester repräsentiert.
        """
        return {
            "nummer": semester.nummer,
            "module": [self._modul_zu_dict(modul) for modul in semester.module],
        }

    def _studiengang_zu_dict(self, studiengang: Studiengang) -> dict:
        """Konvertiert einen Studiengang in ein Dictionary für die JSON-Darstellung.
        Args:
            studiengang: Ein Studiengang-Objekt, das konvertiert werden soll.
        Returns:
            dict: Ein Dictionary, das den Studiengang repräsentiert.
        """
        return {
            "name": studiengang.name,
            "zielstudiendatum": studiengang.zielstudiendatum.isoformat(),
            "immatrikulationsdatum": studiengang.immatrikulationsdatum.isoformat(),
            "zielnote": studiengang.zielnote,
            "semester": [self._semester_zu_dict(sem) for sem in studiengang.semester],
            "gesamt_ects": studiengang.gesamt_ects,
        }

    def _dict_zu_leistungsnachweis(self, d: dict) -> Leistungsnachweis:
        """Konvertiert ein Dictionary in einen Leistungsnachweis.
        Args:
            d: Ein Dictionary, das den Leistungsnachweis repräsentiert.
        Returns:
            Leistungsnachweis: Ein Objekt der Klasse Pruefungsleistung oder Anerkennung.
        Raises:
            ValueError: Wenn der Leistungsnachweis-Typ nicht unterstützt wird.
        """
        if (
            d["typ"] == "Pruefungsleistung"
        ):  # entscheidet anhand des Typs, welche Unterklasse instanziiert wird
            return Pruefungsleistung(
                datum=date.fromisoformat(d["datum"]),
                note=d["note"],
                pruefungs_art=Pruefungsart(d["pruefungs_art"]),
            )
        elif d["typ"] == "Anerkennung":
            return Anerkennung(
                datum=date.fromisoformat(d["datum"]),
                leistung=d["leistung"],
                leistung_institution=d["leistung_institution"],
            )
        else:
            raise ValueError(f"Unbekannter Leistungsnachweis-Typ: {d['typ']}")

    def _dict_zu_modul(self, d: dict) -> Modul:
        """Erstellt ein Modul mit optionalem Leistungsnachweis aus JSON-Daten.
        Args:
            d: Ein Dictionary, das das Modul repräsentiert.
        Returns:
            Modul: Ein Modul mit seinem Leistungsnachweis (Anerkennung/Prüfungsleistung)
        """
        ln = (
            self._dict_zu_leistungsnachweis(d["leistungsnachweis"])
            if d["leistungsnachweis"]
            else None
        )
        return Modul(name=d["name"], ects=d["ects"], leistungsnachweis=ln)

    def _dict_zu_semester(self, d: dict) -> Semester:
        """Erstellt ein Semester mit seinen Modulen aus JSON-Daten.
        Args:
            d: Ein Dictionary, das das Semester repräsentiert.
        Returns:
            Semester: Ein Semester-Objekt mit seinen Modulen.
        """
        return Semester(
            nummer=d["nummer"],
            module=[self._dict_zu_modul(modul_d) for modul_d in d["module"]],
        )

    def _dict_zu_studiengang(self, d: dict) -> Studiengang:
        """Konvertiert ein Dictionary in ein Studiengang-Objekt.
        Args:
            d: Ein Dictionary, das den Studiengang repräsentiert.
        Returns:
            Studiengang: Ein Studiengang-Objekt, das aus dem Dictionary erstellt wurde.
        """
        return Studiengang(
            name=d["name"],
            zielstudiendatum=date.fromisoformat(d["zielstudiendatum"]),
            immatrikulationsdatum=date.fromisoformat(d["immatrikulationsdatum"]),
            zielnote=d["zielnote"],
            semester=[self._dict_zu_semester(sem_d) for sem_d in d["semester"]],
            gesamt_ects=d.get("gesamt_ects", 180),
        )

    def laden(self) -> Studiengang:
        """Lädt den Studiengang aus der JSON-Datei und gibt ihn zurück.
        Returns:
            Studiengang: Der geladene Studiengang.
        Raises:
            FileNotFoundError: Wenn die JSON-Datei nicht gefunden wird.
            json.JSONDecodeError: Wenn die JSON-Datei nicht korrekt formatiert ist.
        """
        with open(self.dateipfad, "r", encoding="utf-8") as f:
            daten = json.load(f)
        return self._dict_zu_studiengang(daten)

    def speichern(self, studiengang: Studiengang) -> None:
        """Speichert den Studiengang in der JSON-Datei.
        Args:
            studiengang: Der Studiengang, der gespeichert werden soll.
        """
        daten = self._studiengang_zu_dict(studiengang)
        with open(self.dateipfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4, ensure_ascii=False)


# ---- Services ----


class NotenService:
    """Berechnet den ECTS-gewichteten Notendurchschnitt des Studiengangs."""

    def berechne_note(self, studiengang: Studiengang) -> float | None:
        """Berechnet den ECTS-gewichteten Schnitt bestandener Prüfungen.
        Anerkennungen und nicht bestandene Prüfungen zählen nicht mit.
        Gibt None zurück, wenn keine bestandenen Prüfungen vorliegen.
        Das Ergebnis wird auf zwei Nachkommastellen gerundet.
        """
        ects_noten = [
            (modul.ects, modul.leistungsnachweis.note)
            for sem in studiengang.semester
            for modul in sem.module
            if modul.status == Status.BESTANDEN
            and isinstance(modul.leistungsnachweis, Pruefungsleistung)
        ]
        if not ects_noten:
            return None
        gesamt_ects = sum(e for e, _ in ects_noten)
        gewichtete_summe = sum(e * n for e, n in ects_noten)
        return round(gewichtete_summe / gesamt_ects, 2)


class FortschrittService:
    """Berechnet ECTS-Fortschritt und voraussichtliches Abschlussdatum."""

    def berechne_ects(self, studiengang: Studiengang) -> int:
        """Summiert ECTS aller bestandenen und anerkannten Module."""
        return sum(
            modul.ects
            for sem in studiengang.semester
            for modul in sem.module
            if modul.status
            in (
                Status.BESTANDEN,
                Status.ANERKANNT,
            )  # Nur bestandene und anerkannte Module zählen
        )

    def berechne_abschlussdatum(self, studiengang: Studiengang) -> date | None:
        """Schätzt den Abschluss ab heute mit 30 ECTS pro 180 Tagen.
        Das bisherige Studientempo wird nicht berücksichtigt.
        Gibt None zurück, wenn noch keine ECTS erreicht wurden
        oder das ECTS-Ziel bereits erreicht ist.
        """
        erreichte_ects = self.berechne_ects(studiengang)
        if erreichte_ects == 0:
            return None  # Keine ECTS erreicht, kein Abschlussdatum berechenbar
        rest_ects = studiengang.gesamt_ects - erreichte_ects
        if rest_ects <= 0:
            return None  # Alle ECTS erreicht
        # Modellannahme: 30 ECTS pro Semester entsprechen 180 Tagen
        rest_tage = round(rest_ects / 30 * 180)
        return date.today() + timedelta(days=rest_tage)


# ---- Controller ----


class DashboardController:
    """
    Verbindet Repository und Services und gibt ein DashboardDatenDTO zurück.
    Alle Abhängigkeiten werden von außen übergeben (Dependency Injection).
    """

    def __init__(
        self,
        repository: StudiengangRepository,
        noten_service: NotenService,
        fortschritt_service: FortschrittService,
    ) -> None:
        """Initialisiert Repository und Services für den DashboardDatenDTO.
        Args:
            repository: Alle Objekte unter dem Studiengang-Repository gespeichert
            noten_service: Berechnung Notendurchschnitt
            fortschritt_service: Berechnung voraussichtliches Abschlussdatum nach Fortschritt
        """
        self.repository = repository
        self.noten_service = noten_service
        self.fortschritt_service = fortschritt_service

    def lade_daten(self) -> DashboardDatenDTO:
        """Lädt den Studiengang, berechnet den Fortschritt und gibt das DTO zurück."""
        studiengang = self.repository.laden()
        fortschritt = Studienfortschritt(
            erreichte_ects=self.fortschritt_service.berechne_ects(studiengang),
            notendurchschnitt=self.noten_service.berechne_note(studiengang),
            prognostiziertes_abschlussdatum=self.fortschritt_service.berechne_abschlussdatum(
                studiengang
            ),
        )
        module_dtos = [
            ModulDatenDTO(
                name=modul.name,
                ects=modul.ects,
                status=modul.status,
                semester=sem.nummer,
            )
            for sem in studiengang.semester
            for modul in sem.module
        ]
        return DashboardDatenDTO(
            studiengangsname=studiengang.name,
            zieldatum=studiengang.zielstudiendatum,
            zielnote=studiengang.zielnote,
            prognostiziertes_abschlussdatum=fortschritt.prognostiziertes_abschlussdatum,
            erreichte_ects=fortschritt.erreichte_ects,
            notendurchschnitt=fortschritt.notendurchschnitt,
            module=module_dtos,
            gesamt_ects=studiengang.gesamt_ects,
        )


# ---- View ----


class DashboardView:
    """Gibt das Dashboard formatiert auf der Konsole aus."""

    def zeige_dashboard(self, daten: DashboardDatenDTO) -> None:
        """Stellt Studienfortschritt und Modulliste strukturiert dar."""

        if daten.prognostiziertes_abschlussdatum:
            anzeige = daten.prognostiziertes_abschlussdatum.strftime("%d.%m.%Y")
        elif daten.erreichte_ects >= daten.gesamt_ects:
            anzeige = "ECTS-Ziel erreicht"
        else:
            anzeige = "noch nicht berechnet"

        print("=" * 52)
        print(f"  Dashboard: {daten.studiengangsname}")
        print("=" * 52)
        print(f"  Erreichte ECTS        : {daten.erreichte_ects}")
        print(
            f"  Notendurchschnitt     : {daten.notendurchschnitt if daten.notendurchschnitt is not None else 'noch nicht berechnet'}"
        )
        print(f"  Gesch. Abschlussdatum : {anzeige}")
        print(f"  Ziel-Abschlussdatum   : {daten.zieldatum.strftime('%d.%m.%Y')}")
        print(f"  Zielnote              : {daten.zielnote}")
        print()
        print("  Module:")
        for modul in daten.module:
            print(
                f"    - {modul.name} (ECTS: {modul.ects}, Status: {modul.status.value}, Semester: {modul.semester})"
            )


# ---- App (Composition Root) ----


class DashboardApp:
    """
    Einstiegspunkt der Anwendung, verbindet alle Schichten.
    Hier werden Repository, Services, Controller und View
    instanziiert und zusammengesteckt (Composition Root).
    """

    def start(self) -> None:
        """Startet das Dashboard."""
        repository = JsonStudiengangRepository(DATEN_PFAD)
        noten_service = NotenService()
        fortschritt_service = FortschrittService()
        controller = DashboardController(repository, noten_service, fortschritt_service)
        view = DashboardView()
        try:
            try:
                daten = controller.lade_daten()
            except FileNotFoundError:
                init_studiengang = InMemoryStudiengangRepository().laden()
                repository.speichern(init_studiengang)
                daten = controller.lade_daten()

        except (KeyError, TypeError, ValueError) as fehler:
            print(f"Die Studiendaten sind ungültig: {fehler}")
            return

        except OSError as fehler:
            print(f"Fehler beim Lesen oder Schreiben der Datei: {fehler}")
            return

        view.zeige_dashboard(daten)


if __name__ == "__main__":
    DashboardApp().start()
