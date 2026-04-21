"""
FLP Organizer - Translations
============================

Single-file translation dictionary for all UI strings.
New languages can be added by extending the `_translations` dict.
"""
from __future__ import annotations
from typing import Dict


# Available languages - code → display name
LANGUAGES: Dict[str, str] = {
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "ru": "Русский",
}

DEFAULT_LANG = "en"


# All translatable strings. The English version is always the source of truth.
_translations: Dict[str, Dict[str, str]] = {
    # --- Header / general ---
    "app_subtitle": {
        "en": "Automatically groups playlist clips by name onto adjacent tracks. Preserves every position, length, color, and property.",
        "de": "Gruppiert Playlist-Clips automatisch nach Namen auf benachbarte Spuren. Behält jede Position, Länge, Farbe und Eigenschaft bei.",
        "es": "Agrupa automáticamente los clips de la lista de reproducción por nombre en pistas adyacentes. Preserva cada posición, longitud, color y propiedad.",
        "fr": "Regroupe automatiquement les clips de la playlist par nom sur des pistes adjacentes. Préserve toutes les positions, longueurs, couleurs et propriétés.",
        "it": "Raggruppa automaticamente le clip della playlist per nome su tracce adiacenti. Preserva posizione, lunghezza, colore e ogni proprietà.",
        "ru": "Автоматически группирует клипы плейлиста по имени на соседних дорожках. Сохраняет позицию, длину, цвет и все свойства.",
    },

    # --- Drop area ---
    "drop_prompt": {
        "en": "Drop your .flp file here   —   or click to browse",
        "de": "Lege deine .flp-Datei hier ab   —   oder klicke zum Auswählen",
        "es": "Arrastra tu archivo .flp aquí   —   o haz clic para buscar",
        "fr": "Déposez votre fichier .flp ici   —   ou cliquez pour parcourir",
        "it": "Trascina qui il tuo file .flp   —   o clicca per sfogliare",
        "ru": "Перетащите сюда файл .flp   —   или нажмите, чтобы выбрать",
    },
    "drop_prompt_batch": {
        "en": "Drop up to 30 .flp files here   —   or click to browse",
        "de": "Lege bis zu 30 .flp-Dateien hier ab   —   oder klicke zum Auswählen",
        "es": "Arrastra hasta 30 archivos .flp aquí   —   o haz clic para buscar",
        "fr": "Déposez jusqu'à 30 fichiers .flp ici   —   ou cliquez pour parcourir",
        "it": "Trascina fino a 30 file .flp qui   —   o clicca per sfogliare",
        "ru": "Перетащите сюда до 30 файлов .flp   —   или нажмите, чтобы выбрать",
    },
    "drop_loaded": {
        "en": "Loaded: {name}   —   click to choose a different file",
        "de": "Geladen: {name}   —   klicke, um eine andere Datei zu wählen",
        "es": "Cargado: {name}   —   haz clic para elegir otro archivo",
        "fr": "Chargé : {name}   —   cliquez pour choisir un autre fichier",
        "it": "Caricato: {name}   —   clicca per scegliere un altro file",
        "ru": "Загружено: {name}   —   нажмите, чтобы выбрать другой файл",
    },
    "batch_loaded": {
        "en": "{count} files loaded   —   click to change selection",
        "de": "{count} Dateien geladen   —   klicke, um die Auswahl zu ändern",
        "es": "{count} archivos cargados   —   haz clic para cambiar selección",
        "fr": "{count} fichiers chargés   —   cliquez pour modifier la sélection",
        "it": "{count} file caricati   —   clicca per modificare selezione",
        "ru": "Загружено файлов: {count}   —   нажмите, чтобы изменить",
    },

    # --- Mode tabs ---
    "mode_single": {
        "en": "Single file",
        "de": "Einzelne Datei",
        "es": "Archivo único",
        "fr": "Fichier unique",
        "it": "File singolo",
        "ru": "Один файл",
    },
    "mode_batch": {
        "en": "Batch (multiple files)",
        "de": "Stapel (mehrere Dateien)",
        "es": "Lote (varios archivos)",
        "fr": "Lot (plusieurs fichiers)",
        "it": "Batch (più file)",
        "ru": "Пакет (несколько файлов)",
    },

    # --- Sort options ---
    "track_order": {
        "en": "Track order",
        "de": "Spurenreihenfolge",
        "es": "Orden de pistas",
        "fr": "Ordre des pistes",
        "it": "Ordine delle tracce",
        "ru": "Порядок дорожек",
    },
    "sort_alpha": {
        "en": "Alphabetical (A–Z)",
        "de": "Alphabetisch (A–Z)",
        "es": "Alfabético (A–Z)",
        "fr": "Alphabétique (A–Z)",
        "it": "Alfabetico (A–Z)",
        "ru": "По алфавиту (А–Я)",
    },
    "sort_first": {
        "en": "By first appearance",
        "de": "Nach erstem Erscheinen",
        "es": "Por primera aparición",
        "fr": "Par première apparition",
        "it": "Per prima apparizione",
        "ru": "По первому появлению",
    },
    "caption_alpha": {
        "en": "Groups are ordered alphabetically, case-insensitive. Good for quickly finding a specific sample or pattern by name.",
        "de": "Gruppen werden alphabetisch geordnet, ohne Groß-/Kleinschreibung zu beachten. Gut, um schnell ein bestimmtes Sample oder Pattern nach Name zu finden.",
        "es": "Los grupos se ordenan alfabéticamente, sin distinguir mayúsculas. Útil para encontrar rápido un sample o patrón por nombre.",
        "fr": "Les groupes sont triés alphabétiquement, sans distinction majuscules/minuscules. Idéal pour retrouver rapidement un sample ou un motif par son nom.",
        "it": "I gruppi sono ordinati alfabeticamente, senza distinzione maiuscole. Utile per trovare rapidamente un sample o pattern per nome.",
        "ru": "Группы упорядочены по алфавиту без учёта регистра. Удобно для быстрого поиска сэмпла или паттерна по имени.",
    },
    "caption_first": {
        "en": "Groups are ordered by the earliest time any of their clips plays. Elements that enter first (kick, bass) end up on top tracks; build-ups, fills, and outros go further down. Good for reading the arrangement top-to-bottom like a timeline.",
        "de": "Gruppen werden nach dem frühesten Zeitpunkt geordnet, an dem einer ihrer Clips spielt. Elemente, die zuerst einsetzen (Kick, Bass), landen oben; Build-ups, Fills und Outros weiter unten. Gut, um das Arrangement von oben nach unten wie eine Timeline zu lesen.",
        "es": "Los grupos se ordenan por el momento más temprano en el que suena cualquiera de sus clips. Los elementos que entran primero (bombo, bajo) quedan arriba; los build-ups, fills y outros van más abajo. Ideal para leer el arreglo de arriba a abajo como una línea de tiempo.",
        "fr": "Les groupes sont triés selon le moment le plus précoce où l'un de leurs clips est joué. Les éléments qui entrent en premier (kick, basse) se retrouvent en haut ; les build-ups, fills et outros plus bas. Parfait pour lire l'arrangement de haut en bas comme une timeline.",
        "it": "I gruppi sono ordinati in base al momento più precoce in cui suona una delle loro clip. Gli elementi che entrano per primi (kick, basso) finiscono in alto; build-up, fill e outro vanno più in basso. Ottimo per leggere l'arrangiamento dall'alto al basso come una timeline.",
        "ru": "Группы упорядочены по самому раннему моменту воспроизведения любого их клипа. То, что звучит первым (бочка, бас), оказывается сверху; build-up, fill и outro — ниже. Удобно читать аранжировку сверху вниз как таймлайн.",
    },

    # --- Sub-sort checkboxes ---
    "subsort_label": {
        "en": "Additional sorting (optional)",
        "de": "Zusätzliche Sortierung (optional)",
        "es": "Orden adicional (opcional)",
        "fr": "Tri supplémentaire (facultatif)",
        "it": "Ordinamento aggiuntivo (opzionale)",
        "ru": "Дополнительная сортировка (по желанию)",
    },
    "sub_by_type": {
        "en": "Group by type (audio / patterns)",
        "de": "Nach Typ gruppieren (Audio / Pattern)",
        "es": "Agrupar por tipo (audio / patrones)",
        "fr": "Grouper par type (audio / motifs)",
        "it": "Raggruppa per tipo (audio / pattern)",
        "ru": "Группировать по типу (аудио / паттерн)",
    },
    "sub_by_length": {
        "en": "Sort by clip length (longer first)",
        "de": "Nach Clip-Länge sortieren (längere zuerst)",
        "es": "Ordenar por duración (largos primero)",
        "fr": "Trier par durée (plus longs d'abord)",
        "it": "Ordina per lunghezza (più lunghi prima)",
        "ru": "Сортировать по длине (длинные первыми)",
    },
    "sub_by_color": {
        "en": "Sort by color (coming soon)",
        "de": "Nach Farbe sortieren (in Kürze)",
        "es": "Ordenar por color (próximamente)",
        "fr": "Trier par couleur (bientôt)",
        "it": "Ordina per colore (in arrivo)",
        "ru": "Сортировать по цвету (скоро)",
    },

    # --- Post-process checkboxes ---
    "postprocess_label": {
        "en": "After reorganizing",
        "de": "Nach der Neuordnung",
        "es": "Después de reorganizar",
        "fr": "Après la réorganisation",
        "it": "Dopo la riorganizzazione",
        "ru": "После реорганизации",
    },
    "opt_rename_tracks": {
        "en": "Auto-rename tracks to match group names",
        "de": "Spuren automatisch anhand der Gruppennamen umbenennen",
        "es": "Renombrar pistas automáticamente según los grupos",
        "fr": "Renommer automatiquement les pistes selon les groupes",
        "it": "Rinomina tracce automaticamente in base ai gruppi",
        "ru": "Автоматически переименовать дорожки по именам групп",
    },
    "opt_color_tracks": {
        "en": "Auto-color tracks (coming soon)",
        "de": "Spuren automatisch einfärben (in Kürze)",
        "es": "Colorear pistas automáticamente (próximamente)",
        "fr": "Colorer automatiquement les pistes (bientôt)",
        "it": "Colora tracce automaticamente (in arrivo)",
        "ru": "Автораскраска дорожек (скоро)",
    },
    "opt_remove_empty": {
        "en": "Remove empty tracks (coming soon)",
        "de": "Leere Spuren entfernen (in Kürze)",
        "es": "Eliminar pistas vacías (próximamente)",
        "fr": "Supprimer les pistes vides (bientôt)",
        "it": "Rimuovi tracce vuote (in arrivo)",
        "ru": "Удалить пустые дорожки (скоро)",
    },

    # --- Tree headers / info ---
    "col_track": {"en": "  Track", "de": "  Spur", "es": "  Pista",
                   "fr": "  Piste", "it": "  Traccia", "ru": "  Дорожка"},
    "col_clips": {"en": "  Clips", "de": "  Clips", "es": "  Clips",
                   "fr": "  Clips", "it": "  Clip", "ru": "  Клипы"},
    "col_name":  {"en": "  Group name", "de": "  Gruppenname", "es": "  Nombre del grupo",
                   "fr": "  Nom du groupe", "it": "  Nome gruppo", "ru": "  Имя группы"},
    "no_file": {
        "en": "No file loaded.",
        "de": "Keine Datei geladen.",
        "es": "No hay archivo cargado.",
        "fr": "Aucun fichier chargé.",
        "it": "Nessun file caricato.",
        "ru": "Файл не загружен.",
    },
    "loading": {
        "en": "Loading: {name}…",
        "de": "Lade: {name}…",
        "es": "Cargando: {name}…",
        "fr": "Chargement : {name}…",
        "it": "Caricamento: {name}…",
        "ru": "Загрузка: {name}…",
    },
    "recomputing": {
        "en": "Recomputing plan…",
        "de": "Plan wird neu berechnet…",
        "es": "Recalculando plan…",
        "fr": "Nouveau calcul du plan…",
        "it": "Ricalcolo del piano…",
        "ru": "Пересчёт плана…",
    },

    # --- Status messages ---
    "ready": {
        "en": "Ready to apply.",
        "de": "Bereit zum Anwenden.",
        "es": "Listo para aplicar.",
        "fr": "Prêt à appliquer.",
        "it": "Pronto all'applicazione.",
        "ru": "Готово к применению.",
    },
    "nothing_to_change": {
        "en": "Already organized — nothing to change.",
        "de": "Bereits organisiert — keine Änderung nötig.",
        "es": "Ya organizado — nada que cambiar.",
        "fr": "Déjà organisé — rien à modifier.",
        "it": "Già organizzato — nessuna modifica necessaria.",
        "ru": "Уже упорядочено — менять нечего.",
    },
    "writing": {
        "en": "Writing…",
        "de": "Schreibe…",
        "es": "Escribiendo…",
        "fr": "Écriture…",
        "it": "Scrittura…",
        "ru": "Запись…",
    },
    "saved": {
        "en": "✓  Saved: {name}",
        "de": "✓  Gespeichert: {name}",
        "es": "✓  Guardado: {name}",
        "fr": "✓  Enregistré : {name}",
        "it": "✓  Salvato: {name}",
        "ru": "✓  Сохранено: {name}",
    },
    "failed_read": {
        "en": "Failed to read file.",
        "de": "Datei konnte nicht gelesen werden.",
        "es": "No se pudo leer el archivo.",
        "fr": "Impossible de lire le fichier.",
        "it": "Impossibile leggere il file.",
        "ru": "Не удалось прочитать файл.",
    },
    "write_failed": {
        "en": "Write failed.",
        "de": "Schreiben fehlgeschlagen.",
        "es": "Error al escribir.",
        "fr": "Échec de l'écriture.",
        "it": "Scrittura fallita.",
        "ru": "Ошибка записи.",
    },

    # --- Buttons ---
    "btn_apply": {
        "en": "Apply & Save",
        "de": "Anwenden & Speichern",
        "es": "Aplicar y guardar",
        "fr": "Appliquer & enregistrer",
        "it": "Applica e salva",
        "ru": "Применить и сохранить",
    },
    "btn_clear": {
        "en": "Clear",
        "de": "Zurücksetzen",
        "es": "Borrar",
        "fr": "Effacer",
        "it": "Pulisci",
        "ru": "Очистить",
    },
    "btn_donate": {
        "en": "Help me build more tools",
        "de": "Hilf mir, mehr Tools zu bauen",
        "es": "Ayúdame a crear más herramientas",
        "fr": "Aidez-moi à créer plus d'outils",
        "it": "Aiutami a costruire altri strumenti",
        "ru": "Помогите создавать больше инструментов",
    },
    "btn_decline": {
        "en": "Decline",
        "de": "Ablehnen",
        "es": "Rechazar",
        "fr": "Refuser",
        "it": "Rifiuta",
        "ru": "Отклонить",
    },
    "btn_agree": {
        "en": "I agree",
        "de": "Ich stimme zu",
        "es": "Acepto",
        "fr": "J'accepte",
        "it": "Accetto",
        "ru": "Согласен",
    },

    # --- Footer ---
    "footer_made_with": {
        "en": "Made with ",
        "de": "Erstellt mit ",
        "es": "Hecho con ",
        "fr": "Fait avec ",
        "it": "Fatto con ",
        "ru": "Сделано с ",
    },
    "footer_by": {
        "en": " by {name}",
        "de": " von {name}",
        "es": " por {name}",
        "fr": " par {name}",
        "it": " da {name}",
        "ru": " от {name}",
    },
    "footer_disclaimer": {
        "en": "This tool is not affiliated with or endorsed by Image-Line.",
        "de": "Dieses Tool ist nicht mit Image-Line verbunden oder von diesem unterstützt.",
        "es": "Esta herramienta no está afiliada a Image-Line ni cuenta con su respaldo.",
        "fr": "Cet outil n'est pas affilié à Image-Line ni approuvé par eux.",
        "it": "Questo strumento non è affiliato né approvato da Image-Line.",
        "ru": "Этот инструмент не связан с Image-Line и не одобрен ей.",
    },

    # --- Language selector ---
    "language_label": {
        "en": "Language",
        "de": "Sprache",
        "es": "Idioma",
        "fr": "Langue",
        "it": "Lingua",
        "ru": "Язык",
    },

    # --- Disclaimer ---
    "disclaimer_title": {
        "en": "Before you start",
        "de": "Bevor du loslegst",
        "es": "Antes de empezar",
        "fr": "Avant de commencer",
        "it": "Prima di iniziare",
        "ru": "Прежде чем начать",
    },
    "disclaimer_text": {
        "en": (
            "FLP Organizer is an independent, non-commercial tool.\n\n"
            "It is NOT affiliated with, endorsed by, or authorised by Image-Line, "
            "makers of FL Studio. FL Studio and the .flp file format are trademarks "
            "and/or property of Image-Line Software.\n\n"
            "This tool modifies .flp project files. Although it is designed to be "
            "safe (it never overwrites your original file), the author provides NO "
            "WARRANTY and accepts NO RESPONSIBILITY for any damage, data loss, or "
            "unexpected behaviour that may result from using this software.\n\n"
            "Always keep a backup of your projects.\n\n"
            "By clicking \"I agree\", you acknowledge that you have read and "
            "understood this disclaimer and accept to use this tool at your own risk."
        ),
        "de": (
            "FLP Organizer ist ein unabhängiges, nicht-kommerzielles Tool.\n\n"
            "Es ist NICHT mit Image-Line, dem Hersteller von FL Studio, verbunden, "
            "von diesem unterstützt oder autorisiert. FL Studio und das .flp-Dateiformat "
            "sind Marken und/oder Eigentum von Image-Line Software.\n\n"
            "Dieses Tool verändert .flp-Projektdateien. Obwohl es auf Sicherheit "
            "ausgelegt ist (die Originaldatei wird nie überschrieben), übernimmt der "
            "Autor KEINE GEWÄHRLEISTUNG und KEINE VERANTWORTUNG für Schäden, "
            "Datenverluste oder unerwartetes Verhalten durch die Nutzung dieser Software.\n\n"
            "Bewahre immer eine Sicherungskopie deiner Projekte auf.\n\n"
            "Durch Klick auf \"Ich stimme zu\" bestätigst du, diesen Haftungsausschluss "
            "gelesen und verstanden zu haben, und nutzt das Tool auf eigene Gefahr."
        ),
        "es": (
            "FLP Organizer es una herramienta independiente y no comercial.\n\n"
            "NO está afiliada, respaldada ni autorizada por Image-Line, creadores de "
            "FL Studio. FL Studio y el formato .flp son marcas comerciales y/o propiedad "
            "de Image-Line Software.\n\n"
            "Esta herramienta modifica archivos de proyecto .flp. Aunque está diseñada "
            "para ser segura (nunca sobrescribe tu archivo original), el autor NO OFRECE "
            "GARANTÍA y NO ASUME RESPONSABILIDAD alguna por daños, pérdida de datos o "
            "comportamientos inesperados derivados del uso de este software.\n\n"
            "Mantén siempre una copia de seguridad de tus proyectos.\n\n"
            "Al hacer clic en \"Acepto\", reconoces que has leído y entendido este aviso "
            "y aceptas usar la herramienta bajo tu propio riesgo."
        ),
        "fr": (
            "FLP Organizer est un outil indépendant et non commercial.\n\n"
            "Il n'est PAS affilié, approuvé ni autorisé par Image-Line, créateurs de "
            "FL Studio. FL Studio et le format .flp sont des marques et/ou la propriété "
            "d'Image-Line Software.\n\n"
            "Cet outil modifie les fichiers de projet .flp. Bien qu'il soit conçu pour "
            "être sûr (il n'écrase jamais votre fichier original), l'auteur ne fournit "
            "AUCUNE GARANTIE et décline TOUTE RESPONSABILITÉ en cas de dommage, perte "
            "de données ou comportement inattendu lié à l'utilisation de ce logiciel.\n\n"
            "Conservez toujours une sauvegarde de vos projets.\n\n"
            "En cliquant sur \"J'accepte\", vous reconnaissez avoir lu et compris cet "
            "avertissement et acceptez d'utiliser l'outil à vos propres risques."
        ),
        "it": (
            "FLP Organizer è uno strumento indipendente e non commerciale.\n\n"
            "NON è affiliato, supportato o autorizzato da Image-Line, sviluppatori di "
            "FL Studio. FL Studio e il formato .flp sono marchi e/o proprietà di "
            "Image-Line Software.\n\n"
            "Questo strumento modifica file di progetto .flp. Anche se è progettato "
            "per essere sicuro (non sovrascrive mai il file originale), l'autore NON "
            "offre ALCUNA GARANZIA e NON si assume ALCUNA RESPONSABILITÀ per danni, "
            "perdite di dati o comportamenti imprevisti derivanti dall'uso del software.\n\n"
            "Mantieni sempre una copia di backup dei tuoi progetti.\n\n"
            "Cliccando \"Accetto\", confermi di aver letto e compreso questo avviso "
            "e di utilizzare lo strumento a tuo rischio."
        ),
        "ru": (
            "FLP Organizer — независимый некоммерческий инструмент.\n\n"
            "Он НЕ связан, не одобрен и не авторизован компанией Image-Line, создателем "
            "FL Studio. FL Studio и формат .flp являются товарными знаками и/или "
            "собственностью Image-Line Software.\n\n"
            "Этот инструмент изменяет файлы проекта .flp. Хотя он разработан с учётом "
            "безопасности (оригинальный файл никогда не перезаписывается), автор НЕ "
            "ПРЕДОСТАВЛЯЕТ НИКАКИХ ГАРАНТИЙ и НЕ НЕСЁТ ОТВЕТСТВЕННОСТИ за любой ущерб, "
            "потерю данных или неожиданное поведение при использовании ПО.\n\n"
            "Всегда храните резервную копию своих проектов.\n\n"
            "Нажимая «Согласен», вы подтверждаете, что прочитали и поняли это уведомление, "
            "и используете инструмент на свой страх и риск."
        ),
    },

    # --- Dialogs / messages ---
    "dlg_save_title": {
        "en": "Save reorganized project as…",
        "de": "Neu geordnetes Projekt speichern unter…",
        "es": "Guardar proyecto reorganizado como…",
        "fr": "Enregistrer le projet réorganisé sous…",
        "it": "Salva progetto riorganizzato come…",
        "ru": "Сохранить переорганизованный проект как…",
    },
    "dlg_save_ok": {
        "en": "File saved successfully:\n{path}\n\nOpen the containing folder?",
        "de": "Datei erfolgreich gespeichert:\n{path}\n\nZielordner öffnen?",
        "es": "Archivo guardado correctamente:\n{path}\n\n¿Abrir la carpeta contenedora?",
        "fr": "Fichier enregistré avec succès :\n{path}\n\nOuvrir le dossier contenant ?",
        "it": "File salvato con successo:\n{path}\n\nAprire la cartella contenitore?",
        "ru": "Файл успешно сохранён:\n{path}\n\nОткрыть содержащую папку?",
    },
    "dlg_err_overwrite": {
        "en": "For safety, you can't overwrite the original file.\nPlease choose a different filename.",
        "de": "Aus Sicherheitsgründen kann die Originaldatei nicht überschrieben werden.\nBitte wähle einen anderen Dateinamen.",
        "es": "Por seguridad, no puedes sobrescribir el archivo original.\nElige un nombre diferente.",
        "fr": "Par sécurité, vous ne pouvez pas écraser le fichier d'origine.\nChoisissez un autre nom.",
        "it": "Per sicurezza non puoi sovrascrivere il file originale.\nScegli un nome diverso.",
        "ru": "В целях безопасности нельзя перезаписывать исходный файл.\nВыберите другое имя.",
    },

    # --- Batch UI ---
    "batch_output_folder": {
        "en": "Output folder:",
        "de": "Zielordner:",
        "es": "Carpeta de salida:",
        "fr": "Dossier de sortie :",
        "it": "Cartella di output:",
        "ru": "Папка вывода:",
    },
    "batch_browse": {
        "en": "Browse…",
        "de": "Durchsuchen…",
        "es": "Examinar…",
        "fr": "Parcourir…",
        "it": "Sfoglia…",
        "ru": "Обзор…",
    },
    "batch_default_folder": {
        "en": "(next to each input file)",
        "de": "(neben jeder Eingabedatei)",
        "es": "(junto a cada archivo de entrada)",
        "fr": "(à côté de chaque fichier d'entrée)",
        "it": "(accanto a ciascun file di input)",
        "ru": "(рядом с каждым входным файлом)",
    },
    "batch_processing": {
        "en": "Processing {i}/{n}: {name}",
        "de": "Verarbeite {i}/{n}: {name}",
        "es": "Procesando {i}/{n}: {name}",
        "fr": "Traitement {i}/{n} : {name}",
        "it": "Elaborazione {i}/{n}: {name}",
        "ru": "Обработка {i}/{n}: {name}",
    },
    "batch_done": {
        "en": "✓  Done — {ok} of {total} files processed successfully.",
        "de": "✓  Fertig — {ok} von {total} Dateien erfolgreich verarbeitet.",
        "es": "✓  Listo — {ok} de {total} archivos procesados correctamente.",
        "fr": "✓  Terminé — {ok} sur {total} fichiers traités avec succès.",
        "it": "✓  Fatto — {ok} di {total} file elaborati con successo.",
        "ru": "✓  Готово — {ok} из {total} файлов успешно обработано.",
    },
    "batch_limit_warn": {
        "en": "Only the first 30 files will be processed.",
        "de": "Nur die ersten 30 Dateien werden verarbeitet.",
        "es": "Solo se procesarán los primeros 30 archivos.",
        "fr": "Seuls les 30 premiers fichiers seront traités.",
        "it": "Solo i primi 30 file verranno elaborati.",
        "ru": "Будут обработаны только первые 30 файлов.",
    },
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Look up a translation. Falls back to English if the key or language
    is missing. Supports `{placeholder}` substitution via kwargs."""
    entry = _translations.get(key, {})
    text = entry.get(lang) or entry.get(DEFAULT_LANG) or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
