__version__ = (2, 9, 2)
# meta developer: @foxy437
# what new: Search upgraded, and searching speed improved, bug fix.

import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from .. import loader, utils
import re
import os
import gdown
import inspect
import io
import ast
    
class FHeta(loader.Module):
    '''Module for searching modules! Upload your modules to FHeta via fheta_bot.t.me!'''
    strings = {"name": "FHeta"}

    repos = [
        "C0dwiz/H.Modules",
        "Fixyres/Modules",
        "AmoreForever/amoremods",
        "vsecoder/hikka_modules",
        "iamnalinor/FTG-modules",
        "musiczhara0/sosat",
        "Den4ikSuperOstryyPer4ik/Astro-modules",
        "hikariatama/ftg",
        "N3rcy/modules",
        "FajoX1/FAmods",
        "kayt3m/modules",
        "sqlmerr/hikka_mods",
        "Ijidishurka/modules",
        "dorotorothequickend/DorotoroModules",
        "kezuhiro-web/modules",
        "coddrago/modules",
        "Slaik78/ModulesHikkaFromSlaik",
        "Daniel1236n29/Modules_hikka",
        "D4n13l3k00/FTG-Modules",
        "chebupelka10/HikkaModules",
        "KorenbZla/Hikka",
        "Vsakoe/HK",
        "anon97945/hikka-mods",
        "N3rcy/modules",
        "MuRuLOSE/HikkaModulesRepo",
        "shadowhikka/sh.modules",
        "amm1edev/ame_repo",
        "1jpshiro/hikka-modules",
        "MoriSummerz/ftg-mods",
        "dekkusudev/mm-hikka-mods",
        "idiotcoders/idiotmodules"
    ]

    def __init__(self):
        file_id = "1j1MG4wpPv0JPHOyctCRkHTDAgUD-Nh_v"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = "token.txt"
        gdown.download(url, output, quiet=False)
        with open(output, "r") as file:
            self.token = file.read().strip()

    @loader.command()
    async def fheta(self, message):
        '''<query> - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>")
            return

        await utils.answer(message, "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>")
        modules = await self.search_modules_parallel(args)

        if not modules:
            args = args.replace(" ", "")
            modules = await self.search_modules_parallel(args)

        if not modules:
            await utils.answer(message, "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching by name failed, starting to searching by command...</b>\n\n<emoji document_id=5325783112309817646>❕</emoji> <b>This is a long process, approximate waiting time is 2-3 minutes.</b>")
            modules = await self.search_modules_by_command_parallel(args)

        if not modules:
            await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>")
        else:
            results = ""
            seen_modules = set()
            result_index = 1

            for module in modules:
                repo_url = f"https://github.com/{module['repo']}"
                download_url = module['download_url']

                commands_section = ""
                if module['commands']:
                    commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd['name']}</code> {cmd['description']}" for cmd in module['commands']])
                    commands_section = f"\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}"

                description_section = ""
                description = await self.get_module_description(download_url)
                if description:
                    description_section = f"\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}"

                author_info = await self.get_author_from_file(download_url)
                module_name = module['name'].replace('.py', '')
                module_key = f"{module_name}_{author_info}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                result = f"<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {result_index} for:</b> <code>{args}</code>\n<b>{module_name}</b> by {author_info}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{self.get_prefix()}dlm {download_url}</code>{description_section}{commands_section}\n\n\n"
                results += result
                result_index += 1

            await utils.answer(message, results)
            
    @loader.command()
    async def fupdate(self, message):
        '''- check update.'''
        module_name = "FHeta"
        module = self.lookup(module_name)
        sys_module = inspect.getmodule(module)

        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"{module_name}.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")
        
        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        headers = {'Authorization': f'token {self.token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()

                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# what new:") else ""
                    
                else:
                    await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>Failed to fetch the FHeta.</b>")
                    return

        if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
            await utils.answer(message, f"<emoji document_id=5436040291507247633>🎉</emoji> <b>You have the actual</b> <code>FHeta (v{correct_version_str})</code><b>.</b>")
        else:
            update_message = (
                f"<emoji document_id=5260293700088511294>⛔️</emoji> <b>You have the old version </b><code>FHeta (v{correct_version_str})</code><b>.</b>\n\n"
                f"<emoji document_id=5382357040008021292>🆕</emoji> <b>New version</b> <code>v{new_version}</code><b> available!</b>\n"
            )
            if what_new:
                update_message += f"<emoji document_id=5307761176132720417>⁉️</emoji> <b>What’s new:</b><code> {what_new}</code>\n\n"
            update_message += (
                f"<emoji document_id=5298820832338915986>🔄</emoji> <b>To update type: <code>{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py</code></b>"
            )
            await utils.answer(message, update_message)
                                  
    async def search_modules_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_modules_by_command_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo_by_command(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_repo(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return [
                    {
                        "name": item['name'],
                        "repo": repo,
                        "commands": await self.get_commands_from_module(item['download_url'], session),
                        "download_url": item['download_url']
                    }
                    for item in data if item['name'].endswith('.py') and query.lower() in item['name'].lower()
                ]
            return []

    async def search_modules_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_modules_by_command_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo_by_command(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_repo_by_command(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                result = []
                for item in data:
                    if item['name'].endswith('.py'):
                        commands = await self.get_commands_from_module(item['download_url'], session) or ["<emoji document_id=5427052514094619126>🙅‍♂️</emoji>"]
                        if any(isinstance(cmd, dict) and 'name' in cmd and query.lower() in cmd['name'].lower() for cmd in commands):
                            result.append({
                                "name": item['name'],
                                "repo": repo,
                                "commands": commands,
                                "download_url": item['download_url']
                            })
                return result
            return []

    async def get_commands_from_module(self, download_url, session):
        async with session.get(download_url) as response:
            if response.status == 200:
                content = await response.text()
                return self.extract_commands(content)
        return {}

    async def get_author_from_file(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    author_line = next((line for line in content.split('\n') if line.startswith("# meta developer:")), None)
                    if author_line:
                        return author_line.split(":")[1].strip()
        return "???"

    async def get_module_description(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and any(
                            isinstance(base, ast.Attribute) and base.attr == "Module" 
                            for base in node.bases
                        ):
                            return ast.get_docstring(node) or ""
        return ""

    @staticmethod
    def extract_commands(content):
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        commands = []
        def get_decorator_names(decorator_list):
            return [ast.unparse(decorator) for decorator in decorator_list]

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for class_body_node in node.body:
                    if isinstance(class_body_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        decorators = get_decorator_names(class_body_node.decorator_list)
                        is_loader_command = any("command" in decorator for decorator in decorators)

                        if is_loader_command or class_body_node.name.endswith("cmd"):
                            method_docstring = ast.get_docstring(class_body_node)
                            command_name = class_body_node.name
                            if command_name.endswith("cmd"):
                                command_name = command_name[:-3]

                            command_info = {
                                "name": command_name,
                                "description": method_docstring or ""
                            }
                            commands.append(command_info)

        return commands
