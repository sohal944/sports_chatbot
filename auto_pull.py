import shutil
import os
import time

# Path to the datasets repo and the final_data directory
REPO_DIR = '/home/sohal/sports_chatbot/datasets_repo/datasets'
FINAL_DATA_DIR = '/home/sohal/sports_chatbot/final_data/git_fixtures'

# Function to sync files
def sync_files():
    datasets = ['bundesliga', 'la-liga', 'ligue-1', 'premier-league', 'serie-a']
    for dataset in datasets:
        src_dir = os.path.join(REPO_DIR, dataset)
        dest_dir = os.path.join(FINAL_DATA_DIR, dataset)
        
        # Check if source exists
        if os.path.exists(src_dir):
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)  # Remove existing files in destination
            shutil.copytree(src_dir, dest_dir)  # Copy all contents
            print(f"✅ Synced {dataset} data to final_data.")
        else:
            print(f"❌ {dataset} not found in the repo.")
    
# Function to pull latest updates from the repository
def pull_latest():
    os.chdir(REPO_DIR)
    os.system("git pull origin main")  # Pull the latest changes from the 'main' branch of the repo

# Function to continuously update datasets
def auto_update_loop(interval=60, sync_interval=300):
    while True:
        print("🔄 Pulling latest changes from remote repo...")
        pull_latest()  # Pull the latest updates from the repo
        print("✅ Repo updated!")

        print("📁 Syncing dataset files to final_data...")
        sync_files()  # Sync datasets to final_data directory
        print("🎉 Sync complete!")

        print(f"⏳ Waiting {sync_interval // 60} minutes before next update...\n")
        time.sleep(sync_interval)  # Wait for the specified interval before pulling again

if __name__ == "__main__":
    auto_update_loop(interval=60, sync_interval=300)  # Change the time intervals as needed
