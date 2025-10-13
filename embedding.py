import subprocess
import sys
import os

def install_dependencies():
    packages = {
        "websockets": "websockets==12.0",
        "transformers": "transformers==4.36.2",
        "torch": "torch==2.1.2",
        "numpy": "numpy==1.24.3",
        "accelerate": "accelerate==0.25.0",
        "bitsandbytes": "bitsandbytes==0.41.3.post2"
    }
    
    pip_commands = [
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        [sys.executable, "-m", "pip", "install", "wheel", "setuptools"]
    ]
    
    for cmd in pip_commands:
        try:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    
    for module_name, package_spec in packages.items():
        installed = False
        try:
            __import__(module_name)
            installed = True
        except ImportError:
            pass
        
        if not installed:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_spec],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--no-deps", package_spec],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except:
                    try:
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", "--no-cache-dir", package_spec],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    except:
                        pass
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "huggingface-hub"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

install_dependencies()

import asyncio
import json
import random
import string
import ssl
import websockets
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel, BitsAndBytesConfig

def generate_token(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_gpu_info():
    if not torch.cuda.is_available():
        return None
    
    try:
        total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        return {
            "vram": f"{total_vram:.2f}GB",
            "vram_gb": total_vram
        }
    except:
        return None

def calculate_batch_size(vram_gb):
    if vram_gb < 4:
        return 1
    elif vram_gb < 6:
        return 2
    elif vram_gb < 8:
        return 4
    elif vram_gb < 12:
        return 8
    elif vram_gb < 16:
        return 16
    elif vram_gb < 24:
        return 24
    elif vram_gb < 40:
        return 32
    elif vram_gb < 80:
        return 48
    else:
        return 64

class Embedding:
    def __init__(self, gpu_info):
        self.model_name = "Qwen/Qwen3-Embedding-0.6B"
        self.batch_size = calculate_batch_size(gpu_info["vram_gb"])
        self.tokenizer = None
        self.model = None
        self.last_used = None
        self.unload_task = None
    
    def load_model(self):
        if self.model is not None:
            return
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            use_fast=True
        )
        
        self.model = AutoModel.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            device_map="cuda",
            quantization_config=quantization_config
        )
        self.model.eval()
    
    def unload_model(self):
        if self.model is not None:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
    
    async def schedule_unload(self):
        if self.unload_task is not None:
            self.unload_task.cancel()
        
        async def delayed_unload():
            try:
                await asyncio.sleep(10)
                self.unload_model()
            except asyncio.CancelledError:
                pass
        
        self.unload_task = asyncio.create_task(delayed_unload())
    
    def get_embeddings(self, texts):
        self.load_model()
        
        try:
            all_embeddings = []
            
            for i in range(0, len(texts), self.batch_size):
                batch_texts = texts[i:i + self.batch_size]
                
                with torch.no_grad():
                    inputs = self.tokenizer(
                        batch_texts,
                        padding=True,
                        truncation=True,
                        max_length=8000,
                        return_tensors="pt",
                        return_attention_mask=True
                    ).to("cuda")
                    
                    outputs = self.model(**inputs)
                    attention_mask = inputs["attention_mask"]
                    token_embeddings = outputs.last_hidden_state
                    
                    input_mask_expanded = attention_mask.unsqueeze(-1).expand(
                        token_embeddings.size()
                    ).float()
                    
                    embeddings = torch.sum(
                        token_embeddings * input_mask_expanded, 1
                    ) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                    
                    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                    all_embeddings.append(embeddings.cpu().numpy())
            
            return np.vstack(all_embeddings)
        
        except Exception as e:
            raise

async def handle_message(websocket, embedding_service, message_data):
    try:
        message_type = message_data.get("type")
        
        if message_type == "embedding_request":
            request_id = message_data.get("request_id")
            texts = message_data.get("texts", [])
            
            if not texts:
                await websocket.send(json.dumps({
                    "type": "embedding_response",
                    "request_id": request_id,
                    "error": "No texts provided"
                }))
                return
            
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                embedding_service.get_embeddings,
                texts
            )
            
            await websocket.send(json.dumps({
                "type": "embedding_response",
                "request_id": request_id,
                "embeddings": embeddings.tolist()
            }))
            
            await embedding_service.schedule_unload()
        
        elif message_type == "ping":
            await websocket.send(json.dumps({"type": "pong"}))
    
    except Exception as e:
        pass

async def websocket_client(token, gpu_info):
    uri = "wss://ws.fixyres.com"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    while True:
        try:
            async with websockets.connect(uri, ping_interval=20, ping_timeout=10, ssl=ssl_context, max_size=None) as websocket:
                await websocket.send(json.dumps({
                    "type": "register",
                    "token": token,
                    "vram": gpu_info["vram"]
                }))
                
                embedding_service = Embedding(gpu_info)
                
                async for message in websocket:
                    try:
                        message_data = json.loads(message)
                        await handle_message(websocket, embedding_service, message_data)
                    except:
                        pass
        
        except:
            await asyncio.sleep(5)

async def main():
    gpu_info = get_gpu_info()
    
    if gpu_info is None or gpu_info["vram_gb"] < 2:
        print("Your GPU have less than 2gb vram or don't have cuda!")
        sys.exit(1)
    
    print("Started!")
    
    access_token = generate_token()
    
    await websocket_client(access_token, gpu_info)

if __name__ == "__main__":
    asyncio.run(main())
