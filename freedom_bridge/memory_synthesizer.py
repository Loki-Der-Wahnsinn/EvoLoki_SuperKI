import os
import shutil
import json
from datetime import datetime

class MemorySynthesizer:
    """
    Transforms simulated data into real Knowledge Fragments.
    Cleans up the heritage to prevent AI confusion (Neural Drift).
    """
    def __init__(self):
        self.master_root = "P:\\FREEDOM_KI"
        self.knowledge_base = os.path.join(self.master_root, "knowledge_base")
        self.legacy_vault = "E:\\FREEDOM_STORAGE\\backups\\LEGACY_SIMULATION"
        
        self.source_paths = [
            "C:\\Users\\Loki\\Antigravity_Singularity",
            "C:\\Users\\Loki\\.gemini\\antigravity\scratch\\AnalyzingMachine",
            "C:\\Users\\Loki\\.gemini\\antigravity\scratch\\FreedomAI"
        ]
        
        if not os.path.exists(self.legacy_vault):
            os.makedirs(self.legacy_vault)

    def synthesize(self):
        print("--- INITIATING MEMORY SYNTHESIS ---")
        for source in self.source_paths:
            if os.path.exists(source):
                print(f"[*] Processing Legacy Path: {source}")
                self.extract_fragments(source)
                self.eliminate_and_archive(source)
                
        print("--- SYNTHESIS COMPLETE. WORKSPACE PURIFIED. ---")

    def extract_fragments(self, path):
        """ Scans for code patterns and visions to save in the Matrix. """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.js')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Save to Matrix as a DNA Fragment
                            self.save_fragment(file, content, path)
                    except:
                        pass

    def save_fragment(self, name, content, source_origin):
        fragment = {
            "origin": source_origin,
            "synthesized_at": datetime.now().isoformat(),
            "name": name,
            "real_logic_potential": "Verified" if "class" in content or "def" in content else "Vision",
            "content": content
        }
        
        target_dir = os.path.join(self.knowledge_base, "patterns", "dna_fragments")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        target_file = os.path.join(target_dir, f"synthesized_{name}.json").replace(".py.json", ".json")
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(fragment, f, indent=4)

    def eliminate_and_archive(self, path):
        """ Moves old directories to the vault and deletes them from live paths. """
        folder_name = os.path.basename(path)
        archive_target = os.path.join(self.legacy_vault, folder_name)
        
        print(f"[!] Eliminating Legacy: {folder_name} -> Vault")
        # Copy to vault
        if os.path.exists(archive_target):
            shutil.rmtree(archive_target) # Overwrite if exists
        shutil.copytree(path, archive_target)
        
        # Delete from source (The 'Eliminate' step)
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"[WARN] Partial elimination only. File lock on: {path}")

if __name__ == "__main__":
    synthesizer = MemorySynthesizer()
    synthesizer.synthesize()
