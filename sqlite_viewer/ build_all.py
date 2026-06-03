import os
import shutil
import subprocess

print("=" * 60)
print("SQLite Viewer - Builder for Windows & Linux")
print("Created By CommandO | In Collaboration With XR Studio")
print("=" * 60)

# تنظيف
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")
for f in os.listdir("."):
    if f.endswith(".spec"):
        os.remove(f)

files_to_add = ["config.py", "database.py", "export.py", "viewer.py"]
add_data_args = []
for f in files_to_add:
    add_data_args.append(f"--add-data={f}:.")

# بناء للويندوز
print("\n🔨 Building for Windows...")
cmd = [
    "pyinstaller", "--onefile", "--name=SQLite_Viewer_Windows",
    "--hidden-import=tabulate", "--hidden-import=colorama"
] + add_data_args + ["main.py"]

subprocess.run(cmd)

if os.path.exists("dist/SQLite_Viewer_Windows.exe"):
    shutil.move("dist/SQLite_Viewer_Windows.exe", "SQLite_Viewer_Windows.exe")
    print("✅ SQLite_Viewer_Windows.exe created")

# تنظيف
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")
for f in os.listdir("."):
    if f.endswith(".spec"):
        os.remove(f)

# بناء للينكس
print("\n🔨 Building for Linux...")
cmd = [
    "pyinstaller", "--onefile", "--name=SQLite_Viewer_Linux",
    "--hidden-import=tabulate", "--hidden-import=colorama"
] + add_data_args + ["main.py"]

subprocess.run(cmd)

if os.path.exists("dist/SQLite_Viewer_Linux"):
    shutil.move("dist/SQLite_Viewer_Linux", "SQLite_Viewer_Linux")
    os.chmod("SQLite_Viewer_Linux", 0o755)
    print("✅ SQLite_Viewer_Linux created")

# تنظيف نهائي
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")
for f in os.listdir("."):
    if f.endswith(".spec"):
        os.remove(f)

print("\n" + "=" * 60)
print("✅ Done!")
print("=" * 60)
print("📁 Files created:")
print("   - SQLite_Viewer_Windows.exe  (for Windows)")
print("   - SQLite_Viewer_Linux        (for Linux/macOS)")
print("=" * 60)