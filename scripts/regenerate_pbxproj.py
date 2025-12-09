#!/usr/bin/env python3
"""
Regenerate a copy of the Xcode project file including any missing .swift files.
- Reads MesocyclePlanner.xcodeproj/project.pbxproj
- Finds source Swift files under MesocyclePlanner-iOS (excluding xcodeproj)
- Adds PBXFileReference and PBXBuildFile entries for missing files
- Adds file references to PBXGroup 'Views' (id 105 in this project) and adds build files to PBXSourcesBuildPhase (id 994)
- Writes new project into MesocyclePlanner_regenerated.xcodeproj/project.pbxproj
This is a best-effort helper and doesn't attempt full Xcode project manipulation.
"""
import re
from pathlib import Path
from itertools import count

ROOT = Path('.')
PBX_ORIG = ROOT / 'MesocyclePlanner-iOS' / 'MesocyclePlanner.xcodeproj' / 'project.pbxproj'
OUT_DIR = ROOT / 'MesocyclePlanner-iOS' / 'MesocyclePlanner_regenerated.xcodeproj'
OUT_PBX = OUT_DIR / 'project.pbxproj'

if not PBX_ORIG.exists():
    print('Original pbxproj not found at', PBX_ORIG)
    raise SystemExit(1)

text = PBX_ORIG.read_text(encoding='utf-8')

# collect existing PBXFileReference paths
file_ref_re = re.compile(r"\s*([0-9A-Fa-f]+|\d+)\s*/\*\s*(.*?)\s*\*/\s*=\s*\{\s*isa\s*=\s*PBXFileReference;.*?path\s*=\s*(.*?);", re.S)
existing_paths = {}
for m in file_ref_re.finditer(text):
    oid = m.group(1)
    comment_name = m.group(2)
    pathval = m.group(3).strip().strip('"')
    existing_paths[pathval] = oid

# find all .swift files under MesocyclePlanner-iOS/MesocyclePlanner
swift_files = [p.relative_to('MesocyclePlanner-iOS').as_posix() for p in (ROOT / 'MesocyclePlanner-iOS').rglob('*.swift')]
# normalize to paths as used in pbxproj (relative to group root MesocyclePlanner)
# Many paths in pbxproj are just filenames because sourceTree is <group>
swift_basenames = [Path(p).name for p in swift_files]

# Determine missing files by name
missing = []
for name in swift_basenames:
    found = False
    for k in existing_paths.keys():
        if k.endswith(name):
            found = True
            break
    if not found:
        missing.append(name)

print('Found Swift files:', len(swift_files))
print('Existing file references:', len(existing_paths))
print('Missing entries to add:', len(missing))

if not missing:
    print('Nothing to add; creating copy of original pbxproj as regenerated file')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PBX.write_text(text, encoding='utf-8')
    print('Wrote', OUT_PBX)
    raise SystemExit(0)

# prepare new IDs (choose large numeric IDs to avoid collisions)
id_gen = (str(i) for i in count(1000))

# Build insertion snippets
buildfile_snippets = []
fileref_snippets = []
# We'll add entries to PBXGroup with id 105 (Views) and to PBXSourcesBuildPhase id 994
# Find placements
before_buildfile_end = re.search(r"/\* End PBXBuildFile section \*/", text)
before_fileref_end = re.search(r"/\* End PBXFileReference section \*/", text)
sources_phase_files_re = re.compile(r"(\*/\s*Begin PBXSourcesBuildPhase section\s*\*/.*?files\s*=\s*\()(.*?)(\);)", re.S)
views_group_re = re.compile(r"(105\s*/\* Views \*/\s*=\s*\{.*?children\s*=\s*\()(.*?)(\);)", re.S)

if not before_buildfile_end or not before_fileref_end or not sources_phase_files_re.search(text) or not views_group_re.search(text):
    print('Project layout not as expected; aborting')
    raise SystemExit(1)

sources_match = sources_phase_files_re.search(text)
views_match = views_group_re.search(text)

existing_sources_content = sources_match.group(2)
existing_views_children = views_match.group(2)

new_buildfile_ids = []
new_fileref_ids = []
for name in missing:
    fileref_id = next(id_gen)
    buildfile_id = next(id_gen)
    new_fileref_ids.append((fileref_id, name))
    new_buildfile_ids.append((buildfile_id, fileref_id, name))
    fileref_snippets.append(f"\t\t{fileref_id} /* {name} */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {name}; sourceTree = \"<group>\"; }};\n")
    buildfile_snippets.append(f"\t\t{buildfile_id} /* {name} in Sources */ = {{isa = PBXBuildFile; fileRef = {fileref_id}; }};\n")

# Insert the snippets into copies of the pbxproj text
new_text = text
# Insert buildfiles before End PBXBuildFile section
insert_pos = before_buildfile_end.start()
new_text = new_text[:insert_pos] + ''.join(buildfile_snippets) + new_text[insert_pos:]
# Insert filerefs before End PBXFileReference section
insert_pos = before_fileref_end.start()
new_text = new_text[:insert_pos] + ''.join(fileref_snippets) + new_text[insert_pos:]

# Add the new buildfile ids into PBXSourcesBuildPhase files array (append)
new_sources_content = existing_sources_content
for bid, fid, name in new_buildfile_ids:
    new_sources_content = new_sources_content + f"\n\t\t{bid} /* {name} in Sources */,"
new_text = new_text[:sources_match.start(2)] + new_sources_content + new_text[sources_match.end(2):]

# Add new fileref ids into Views group's children (append)
new_views_children = existing_views_children
for fid, name in new_fileref_ids:
    new_views_children = new_views_children + f"\n\t\t{fid} /* {name} */,"

new_text = new_text[:views_match.start(2)] + new_views_children + new_text[views_match.end(2):]

OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PBX.write_text(new_text, encoding='utf-8')
print('Wrote regenerated pbxproj to', OUT_PBX)
print('You can compare with original and open the regenerated project:')
print('  open', OUT_DIR)