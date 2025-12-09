#!/usr/bin/env python3
"""
Simple PBXProj inspector: parse object blocks and report isa per ID.
Then validate that buildPhases referenced by targets are *BuildPhase, and PBXBuildFile.fileRef point to PBXFileReference.
This is a heuristic parser (not full Xcodeproj parser) but good enough for diagnostics.
"""
import re
import sys
from collections import defaultdict

PBX_PATH = 'MesocyclePlanner-iOS/MesocyclePlanner.xcodeproj/project.pbxproj'

obj_re = re.compile(r"^\s*([0-9A-Fa-f]+|\d+)\s*/\*.*\*/\s*=\s*\{" )
isa_re = re.compile(r"^\s*isa\s*=\s*([A-Za-z0-9_]+);")
file_ref_re = re.compile(r"fileRef\s*=\s*([0-9A-Fa-f]+|\d+);")


def parse_blocks(lines):
    objs = {}
    current_id = None
    current_block = []
    for line in lines:
        m = obj_re.match(line)
        if m:
            if current_id is not None:
                objs[current_id] = ''.join(current_block)
            current_id = m.group(1)
            current_block = [line]
        else:
            if current_id is not None:
                current_block.append(line)
    if current_id is not None:
        objs[current_id] = ''.join(current_block)
    return objs


def find_isa(block_text):
    m = isa_re.search(block_text)
    return m.group(1) if m else None


def find_fileRef(block_text):
    m = file_ref_re.search(block_text)
    return m.group(1) if m else None


def main():
    with open(PBX_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    objs = parse_blocks(lines)
    isa_map = {oid: find_isa(b) for oid, b in objs.items()}

    # Report isa counts
    by_isa = defaultdict(list)
    for oid, isa in isa_map.items():
        by_isa[isa].append(oid)

    print('# Summary of isa counts:')
    for isa, ids in sorted(by_isa.items(), key=lambda x: (len(x[1]), x[0]), reverse=True):
        print(f"{isa}: {len(ids)} objects")

    # Validate buildPhases referenced by PBXNativeTarget
    print('\n# Checking PBXNativeTarget.buildPhases references...')
    for oid, block in objs.items():
        if find_isa(block) == 'PBXNativeTarget':
            # find buildPhases list
            m = re.search(r"buildPhases\s*=\s*\((.*?)\);", block, re.S)
            if m:
                entries = re.findall(r"([0-9A-Fa-f]+|\d+)\s*/\*.*?\*/", m.group(1))
                for e in entries:
                    eisa = isa_map.get(e)
                    if not eisa or not eisa.endswith('BuildPhase'):
                        print(f"Target {oid} references buildPhase {e} with isa={eisa}")
            else:
                print(f"Target {oid} has no buildPhases block")

    # Validate PBXBuildFile.fileRef -> PBXFileReference
    print('\n# Checking PBXBuildFile.fileRef references...')
    for oid, block in objs.items():
        if find_isa(block) == 'PBXBuildFile':
            ref = find_fileRef(block)
            risa = isa_map.get(ref)
            if risa != 'PBXFileReference':
                print(f"PBXBuildFile {oid} -> fileRef {ref} (isa={risa})")

    # Look for ids with multiple isa (shouldn't happen in this simple parse) - we already map ids to single block
    print('\n# Done')


if __name__ == '__main__':
    main()
