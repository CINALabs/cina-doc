import os

def check_links(sidebar_path, base_dir):
    print(f"Checking links in {sidebar_path}...")
    if not os.path.exists(sidebar_path):
        print(f"Error: Sidebar {sidebar_path} not found.")
        return False
    
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    links = re.findall(r'\[.*?\]\((.*?)\)', content)
    
    all_ok = True
    for link in links:
        if link == 'README':
            filename = 'README.md'
        else:
            filename = f"{link}.md"
        
        full_path = os.path.join(base_dir, filename)
        if not os.path.exists(full_path):
            print(f"Broken Link: {link} (Expected: {full_path})")
            all_ok = False
        else:
            print(f"OK: {link}")
    
    return all_ok

en_sidebar = r"d:\zWenbo\AI\CINA\docs\en-us\_sidebar.md"
en_dir = r"d:\zWenbo\AI\CINA\docs\en-us"
zh_sidebar = r"d:\zWenbo\AI\CINA\docs\zh-cn\_sidebar.md"
zh_dir = r"d:\zWenbo\AI\CINA\docs\zh-cn"

en_ok = check_links(en_sidebar, en_dir)
zh_ok = check_links(zh_sidebar, zh_dir)

if en_ok and zh_ok:
    print("\nAll links verified successfully!")
else:
    print("\nSome links are broken.")
    exit(1)
