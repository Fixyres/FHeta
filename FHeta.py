__version__ = (3, 3, 3)
# meta developer: @Foxy437
# change-log: 🎉🎉🎉🎉🎉🎉🎉🎉 ADDED INLINE!!! 
# ©️ Fixyres, 2024
# 🌐 https://github.com/Fixyres/FHeta
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import requests
import asyncio
import aiohttp
from .. import loader, utils
import json
import io
import inspect
from hikkatl.types import Message
from difflib import get_close_matches
import random
from ..types import InlineQuery

@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Upload your modules to FHeta via fheta_robot.t.me!'''
    
    strings = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {index} by query:</b> <code>{query}</code>\n<code>{module_name}</code> by {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Failed to fetch the FHeta.</b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result by query </b><code>{query}</code><b>:</b>\n<code>{module_name}</code> by {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n",
        "inline_no_query": "Enter a query to search.",
        "inline_no_modules_found": "No modules found.",
        "inline_commands": "\n👨‍💻 <b>Commands:</b>\n{commands_list}",
        "inline_description": "\n📁 <b>Description:</b> {description}",
        "inline_result": "<code>{module_name}</code> by {author}\n<b>🖥️ Repository:</b> {repo_url}\n<b>💾 Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_descriptioon": "{description}",
        "inline_no_modules_foound": "Try another request.",
        "inline_noo_query": "Name, command, description, author."
    }

    strings_ru = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Введите запрос для поиска.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>Модули не найдены.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Команды:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Описание:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат {index} по запросу:</b> <code>{query}</code>\n<code>{module_name}</code> от {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Репозиторий:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Не удалось получить данные для FHeta.</b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат по запросу </b><code>{query}</code><b>:</b>\n<code>{module_name}</code> от {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Репозиторий:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n",
        "inline_no_query": "Введите запрос для поиска.",
        "inline_no_modules_found": "Модули не найдены.",
        "inline_commands": "\n👨‍💻 <b>Команды:</b>\n{commands_list}",
        "inline_description": "\n📁 <b>Описание:</b> {description}",
        "inline_result": "<code>{module_name}</code> от {author}\n<b>🖥️ Репозиторий:</b> {repo_url}\n<b>💾 Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_descriptioon": "{description}",
        "inline_no_modules_foound": "Попробуйте другой запрос.",
        "inline_noo_query": "Название, команда, описание, автор."
    }

    @loader.command(ru_doc="(запрос) - искать модули.")
    async def fhetacmd(self, message):
        '''(query) - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_query"])
            return

        await utils.answer(message, self.strings["search"])
        modules = await self.search_modules(args)

        if not modules:
            modules = await self.search_modules(args.replace(" ", ""))

        if not modules:
            modules = await self.get_closest_match(args)

            if modules:
                result = self.strings["closest_match"].format(
                    query=args,
                    module_name=modules[0]["name"],
                    author=modules[0].get("author", "???"),
                    repo_url=f"https://github.com/{modules[0]['repo']}",
                    install_command=f"{self.get_prefix()}{modules[0]['install']}",
                    description=utils.escape_html(modules[0].get("description", "No description")),
                    commands=self.strings["commands"].format(commands_list="\n".join(
                        [f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(cmd['description'])}" for cmd in modules[0].get('commands', [])]))
                )
                await utils.answer(message, result)
            else:
                await utils.answer(message, self.strings["no_modules_found"])
        else:
            seen_modules = set()
            formatted_modules = []
            result_index = 1

            for module in modules:
                try:
                    repo_url = f"https://github.com/{module['repo']}"
                    install = module['install']

                    commands_section = ""
                    if "commands" in module:
                        commands_list = "\n".join(
                            [f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(cmd['description'])}" for cmd in module['commands']]
                        )
                        commands_section = self.strings["commands"].format(commands_list=commands_list)

                    description_section = ""
                    if "description" in module:
                        description_section = self.strings["description"].format(description=utils.escape_html(module["description"]))

                    author_info = utils.escape_html(module.get("author", "???"))
                    module_name = utils.escape_html(module['name'].replace('.py', ''))
                    module_key = f"{module_name}_{author_info}"

                    if module_key in seen_modules:
                        continue
                    seen_modules.add(module_key)

                    result = self.strings["result"].format(
                        index=result_index,
                        query=args,
                        module_name=module_name,
                        author=author_info,
                        repo_url=repo_url,
                        install_command=f"{self.get_prefix()}{install}",
                        description=description_section,
                        commands=commands_section
                    )
                    formatted_modules.append(result)
                    result_index += 1
                except Exception:
                    continue

            if len(formatted_modules) == 1:
                result = self.strings["closest_match"].format(
                    query=args,
                    module_name=module_name,
                    author=author_info,
                    repo_url=repo_url,
                    install_command=f"{self.get_prefix()}{install}",
                    description=description_section,
                    commands=commands_section
                )
                await utils.answer(message, result)
            else:
                results = "".join(formatted_modules)
                await utils.answer(message, results)
    
    @loader.inline_handler(ru_doc="(запрос) - искать модули.")
    async def fheta(self, query: InlineQuery):
        args = query.args
        if not args:
            await query.answer(
                [
                    {
                        "type": "article",
                        "id": "no_query",
                        "title": self.strings["inline_no_query"],
                        "description": self.strings["inline_noo_query"],
                        "input_message_content": {
                            "message_text": self.strings["inline_no_query"],
                            "parse_mode": "HTML",
                        },
                        "thumb_url": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-4EUHOHiKpwRTb4s.png",
                    }
                ]
            )
            return

        modules = await self.search_modules(args)

        if not modules:
            modules = await self.search_modules(args.replace(" ", ""))

        if not modules:
            modules = await self.get_closest_match(args)

        if not modules:
            await query.answer(
                [
                    {
                        "type": "article",
                        "id": "no_modules_found",
                        "title": self.strings["inline_no_modules_found"],
                        "description": self.strings["inline_no_modules_foound"],
                        "input_message_content": {
                            "message_text": self.strings["inline_no_modules_found"],
                            "parse_mode": "HTML",
                        },
                        "thumb_url": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
                    }
                ]
            )
            return

        seen_modules = set()
        results = []
        result_index = 1

        for module in modules:
            try:
                repo_url = f"https://github.com/{module['repo']}"
                install = module['install']

                commands_section = ""
                if "commands" in module:
                    commands_list = "\n".join(
                        [f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(cmd['description'])}" for cmd in module['commands']]
                    )
                    commands_section = self.strings["inline_commands"].format(commands_list=commands_list)

                description_section = ""
                if "description" in module:
                    description_section = self.strings["inline_description"].format(description=f"{utils.escape_html(module['description'])}")

                author_info = utils.escape_html(module.get("author", "???"))
                module_name = utils.escape_html(module['name'].replace('.py', ''))
                module_key = f"{module_name}_{author_info}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                results.append(
                    {
                        "type": "article",
                        "id": f"module_{result_index}",
                        "title": module_name,
                        "description": self.strings["inline_descriptioon"].format(description=utils.escape_html(module["description"])),
                        "input_message_content": {
                            "message_text": self.strings["inline_result"].format(
                                query=args,
                                module_name=module_name,
                                author=author_info,
                                repo_url=repo_url,
                                install_command=f"{self.get_prefix()}{install}",
                                description=description_section,
                                commands=commands_section,
                            ),
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                        },
                        "thumb_url": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png",
                    }
                )
                result_index += 1

                if result_index > 20:
                    break
            except Exception:
                continue

        await query.answer(results)

    async def get_closest_match(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)
                    
                    module_names = [module['name'] for module in modules]
                    closest_matches = get_close_matches(query, module_names, n=1, cutoff=0.5)

                    if closest_matches:
                        module = next((m for m in modules if m['name'] == closest_matches[0]), None)
                        if module:
                            return await self.format_module(module, query)
                    return None

    async def search_modules(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)

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

                    return found_modules

    async def format_module(self, module, query):
        repo_url = f"https://github.com/{module['repo']}"
        install = module['install']

        commands_section = ""
        if "commands" in module:
            commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd['name']}</code> {cmd['description']}" for cmd in module['commands']])
            commands_section = self.strings["commands"].format(commands_list=commands_list)

        description_section = ""
        if "description" in module:
            description_section = self.strings["description"].format(description=module["description"])

        author_info = module.get("author", "???")
        module_name = module['name'].replace('.py', '')

        return self.strings["closest_match"].format(
            query=query,
            module_name=module_name,
            author=author_info,
            repo_url=repo_url,
            install_command=f"{self.get_prefix()}{install}",
            description=description_section,
            commands=commands_section
                )
