import os
import time
import pandas as pd
from llama_cpp import Llama
import subprocess

# === 初始化模型（只載入一次）===
MODEL_PATH = "/home/user/code/models/unsloth.Q4_K_M.gguf"
print("[INFO] Model loading...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_gpu_layers=80,
    n_threads=8,
    n_batch=128,
    verbose=False,
)
print("[INFO] Model loading completed")

# === 監控資料夾 ===
INPUT_FOLDER = os.path.expanduser("/home/user/code/final_data")
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

MAC_COLUMN = "Src IP"

# === 封鎖記錄 ===
blocked_macs = set()

def make_prompt(row):
    system = (
        "You are a cybersecurity expert. Based on the provided network packet features, "
        "only answer with 'Yes' if you are confident this is an attack. Otherwise, "
        "respond with 'No'. Do not provide any additional explanation."
    )
    features = ", ".join([f"{col}={row[col]}" for col in row.index if col != MAC_COLUMN])
    user_prompt = f"Here is a network packet data: {features}. Is this an attack?"
    return (
        "<|start_header_id|>system<|end_header_id|>\n\n" + system + "\n\n"
        "<|start_header_id|>user<|end_header_id|>\n\n" + user_prompt + "\n\n"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )

def block_mac(mac):
    if mac in blocked_macs:
        return
    print(f"[firewall] ban MAC：{mac}")
    blocked_macs.add(mac)
    
    #subprocess.run(["nft", "add", "rule", "inet", "fw4", "forward", "iifname", "br-lan", "ether", "saddr", mac, "drop"])

def process_file(file_path):
    print(f"[INFO] process：{file_path}")
    df = pd.read_csv(file_path).dropna().astype(str)

    cols = [
        "Flow Duration", "Total Fwd Packets", "Total Backward Packets", "Flow Bytes/s",
        "Flow Packets/s", "Fwd IAT Mean", "Fwd IAT Std", "SYN Flag Count", "ACK Flag Count",
        "RST Flag Count", "Down/Up Ratio", "Init_Win_bytes_forward", "Init_Win_bytes_backward",
        "Fwd Packets/s", "Bwd Packets/s", MAC_COLUMN
    ]
    df = df[cols]

    prompts = df.drop(columns=[MAC_COLUMN]).apply(make_prompt, axis=1)
    macs = df[MAC_COLUMN].tolist()

    for prompt, mac in zip(prompts, macs):
        output = llm(prompt, max_tokens=20, temperature=0.1, top_p=0.9)
        text = output["choices"][0]["text"].strip().lower()
        #print(text)
        if "yes" in text:
            print('')
            block_mac(mac)

    # 移動已處理檔案
    new_path = os.path.join(PROCESSED_FOLDER, os.path.basename(file_path))
    os.rename(file_path, new_path)
    print(f"[INFO] process file move to {new_path}\n")

def watch_loop():
    print(f"[INFO] folder check：{INPUT_FOLDER}")
    while True:
        files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".csv")]
        for f in files:
            if f == "processed":
                continue
            full_path = os.path.join(INPUT_FOLDER, f)
            process_file(full_path)
        time.sleep(5)

if __name__ == "__main__":
    watch_loop()

