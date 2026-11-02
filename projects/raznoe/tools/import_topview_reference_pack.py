#!/usr/bin/env python3
"""Import previously generated, SHA-verified Topview scene reference images without generation."""
import argparse
import datetime
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from PIL import Image

PROJECT = Path("projects/raznoe")
CHAR_NUMBERS = {
    "yarik": [1, 2],
    "mama-lena": [3, 4],
    "sonya": [5, 6],
    "anna-sergeevna": [7],
    "bublik": [8],
    "varya": [9],
    "miron": [27, 28, 29],
    "vera": [30, 31],
    "nina": [32, 33],
    "darya": [34],
    "mark": [35],
    "lilya": [36],
    "tuman": [37],
}
KEYFRAME_START = {1: 18, 2: 51}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def save(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def note_path(item):
    return str(item["path"])

def image_role(item):
    n = item["number"]
    if n <= 9 or 27 <= n <= 37:
        label = item["label"].lower()
        return "character_expressions" if ("эмоций" in label or "эмоции" in label) else "character_identity"
    if n in (18, 51):
        return "prop_reference"
    if 10 <= n <= 17 or 38 <= n <= 50:
        return "location_reference"
    return "keyframe"

def true_png(path, target_size=None, previously_existing=False):
    with Image.open(path) as img:
        fmt = img.format
        dimensions = img.size
        if target_size and dimensions != target_size:
            raise ValueError(f"{path}: expected {target_size}, received {dimensions}")
        if fmt == "PNG":
            return dimensions
        if fmt != "JPEG" or not previously_existing:
            raise ValueError(f"{path}: unexpected image format {fmt}")
        converted = img.convert("RGB")
        temp = path.with_suffix(".temporarypng")
        converted.save(temp, format="PNG", optimize=True)
        temp.replace(path)
        return dimensions

def make_image_from_zip(image_bytes, path, orientation):
    # A worker may retry after a fast-forward race. Keep verified processed
    # images in this workflow run's private temp folder, not in the repository.
    # The key is the exact SHA256 of the verified original source image.
    import os
    cache = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "misc-topview-cached-png" / (digest(image_bytes) + ".png")
    expected_size = (1536, 1024) if orientation == "landscape_3_2" else (1080, 1920)
    if cache.exists():
        data = cache.read_bytes()
        with Image.open(io.BytesIO(data)) as tested:
            if tested.format != "PNG" or tested.size != expected_size:
                raise ValueError("Invalid cached image size or format")
        if path.exists() and digest(path.read_bytes()) != digest(data):
            raise RuntimeError(f"Refusing to overwrite different image: {path}")
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return expected_size, digest(data)
    with Image.open(io.BytesIO(image_bytes)) as original:
        if original.format != "PNG":
            raise ValueError(f"{path}: source is not real PNG")
        original.load()
        if orientation == "landscape_3_2":
            if original.size != (1248, 832):
                raise ValueError(f"{path}: unexpected landscape source size {original.size}")
            final = original.convert("RGB").resize((1536, 1024), Image.Resampling.LANCZOS)
        elif orientation == "portrait_9_16":
            if original.size != (768, 1360):
                raise ValueError(f"{path}: unexpected portrait source size {original.size}")
            final = original.convert("RGB").crop((1, 0, 766, 1360)).resize((1080, 1920), Image.Resampling.LANCZOS)
        else:
            raise ValueError(f"{path}: unexpected orientation {orientation}")
    buf = io.BytesIO()
    final.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(data)
    if path.exists() and digest(path.read_bytes()) != digest(data):
        raise RuntimeError(f"Refusing to overwrite different existing image: {path}")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return final.size, digest(data)

def source_inputs(master, items, chars, assets):
    item_by_num = {item["number"]: item for item in items}
    character_labels = {
        "Мирон в скафандре": "miron",
        "Мирон": "miron", "Мама Вера": "vera", "Бабушка Нина": "nina",
        "Дарья Андреевна": "darya", "Доктор Марк Львович": "mark",
        "Парикмахер Лиля": "lilya", "Лошадь Туман": "tuman",
        "Анна Сергеевна": "anna-sergeevna", "Мама Лена": "mama-lena",
        "Соня": "sonya", "Бублик": "bublik", "Варя": "varya", "Ярик": "yarik",
    }
    by_char = {c["id"]: c for c in chars}
    scene_assets = {}
    for a in assets:
        for scene in a["scenes"]:
            scene_assets.setdefault(scene, []).append(a)

    def get_path(scene, name):
        if name.startswith("Лист реквизита:"):
            a = next(a for a in scene_assets[scene] if "props-sheet" in a["id"])
            return a["images"][0]["path"]
        if name.startswith("Мирон в скафандре"):
            return item_by_num[29]["path"]
        for label, cid in sorted(character_labels.items(), key=lambda v: len(v[0]), reverse=True):
            if name.startswith(label):
                return by_char[cid]["model_sheet"]["public_image"]
        candidates = [a for a in scene_assets[scene] if name.startswith(a["name"]) or a["name"].startswith(name)]
        if len(candidates) == 1:
            return candidates[0]["images"][0]["path"]
        raise ValueError(f"No unique image mapping for scene {scene}, name {name!r}; candidates={len(candidates)}")

    master = re.sub(r'<div class="scene-ref-gallery">[\s\S]*?</div>\s*', "", master)
    master = re.sub(r"(?m)^\*\*Входы — уже сохранённые файлы:\*\*[^\n]*\n", "", master)
    master = master.replace("**Референсы по раскадровке (часть готова; актуальные ссылки см. в галерее выше):**", "**Референсы раскадровки (файлы указаны в галерее выше):**")
    plan_pattern = re.compile(r"(?m)^\*\*Референсы \(план\):\*\* ([^\n]+)$")
    count = 0
    scene2_offset = master.index("## Сцена 2")
    def replacement(match):
        nonlocal count
        count += 1
        scene = 2 if match.start() >= scene2_offset else 1
        snippet = master[max(0, match.start() - 9000):match.start()]
        heads = list(re.finditer(r"(?m)^#### (?:2 )?([AB])([1-8]) ·[^\n]*$", snippet))
        if not heads:
            raise ValueError(f"No subsection heading preceding gallery {count}")
        mode, index = heads[-1].group(1), int(heads[-1].group(2))
        refs = re.findall(r"@Image(\d+)\s*=\s*(.*?)(?=\s+·\s+@Image\d+\s*=|$)", match.group(1))
        if not refs:
            raise ValueError(f"No refs at gallery {count}")
        paths = []
        inputs = []
        for image_num, name in refs:
            path = get_path(scene, name.strip())
            if not Path(path).exists():
                raise FileNotFoundError(path)
            inputs.append("@Image" + image_num + " = " + chr(96) + path + chr(96))
            if path not in paths:paths.append(path)
        k_nums = ([index] if mode == "A" else [2*index-1,2*index])
        for k in k_nums:
            path = item_by_num[KEYFRAME_START[scene]+k]["path"]
            if not Path(path).exists():
                raise FileNotFoundError(path)
            if path not in paths:paths.append(path)
        gallery = '<div class="scene-ref-gallery">' + "".join(
            '<figure><a href="' + p + '" target="_blank" rel="noopener"><img src="' + p +
            '" alt="' + Path(p).stem + ' — не одобрено" loading="lazy"></a><figcaption>' +
            Path(p).stem + ' · не одобрено</figcaption></figure>' for p in paths
        ) + '</div>'
        return "**Референсы:** " + match.group(1) + "\n\n**Входы:** " + "; ".join(inputs) + "\n" + gallery
    master = plan_pattern.sub(replacement, master)
    if count != 24:
        raise RuntimeError(f"expected 24 subsection galleries, got {count}")
    if master.count('class="scene-ref-gallery"') != 24:
        raise RuntimeError("Not all galleries populated")
    return master

def run(source_zip, source_map_path):
    project = PROJECT
    if not Path("scripts/projects.py").exists():
        raise RuntimeError("Run from repository root")
    source = load(source_map_path)
    if source["project"] != "raznoe":
        raise ValueError("Invalid source project")
    mapping = source["images"]
    by_n = {x["number"]: x for x in mapping}
    required_numbers = set([1,3,5,7,8] + list(range(9,60)))
    if set(by_n) != required_numbers or len(mapping) != 56:
        raise ValueError("Expected 56 unique Topview source mappings")
    progress_path = project/"references/generation-progress.json"
    progress = load(progress_path)
    items = progress["items"]
    if len(items) != 59:
        raise ValueError("59 items required")
    item_by_num = {it["number"]: it for it in items}
    if set(item_by_num) != set(range(1,60)):
        raise ValueError("Item number gap")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
    with zipfile.ZipFile(source_zip) as z:
        if len(z.namelist()) != 56:
            raise ValueError("Unexpected number of files in downloaded Topview zip")
        for n, origin in sorted(by_n.items()):
            if item_by_num[n]["path"] != origin["path"]:
                raise ValueError(f"Canonical path mismatch for {n}")
            raw = z.read(origin["source_zip_member"])
            if digest(raw) != origin["source_sha256"]:
                raise ValueError(f"Topview original SHA mismatch for {n}")
            if n < 9:continue
            it = item_by_num[n]
            dims, sha = make_image_from_zip(raw, Path(it["path"]), it["orientation"])
            it.update(state="topview_original_imported_unreviewed",
                      sha256=sha, width=dims[0], height=dims[1],
                      source="Topview Codex Creations, original task "+origin["task_id"],
                      source_sha256=origin["source_sha256"], topview_task_id=origin["task_id"],
                      editorial_status="not_approved")
        for n in range(1,9):
            it = item_by_num[n]
            path = Path(it["path"])
            if not path.exists():raise FileNotFoundError(path)
            dims = true_png(path, (1536, 1024), previously_existing=True)
            it.update(sha256=digest(path.read_bytes()), width=dims[0], height=dims[1],editorial_status="not_approved")
            it.pop("image_container_format",None)
            if n>1:it["state"]="owner_original_restored_png"
    progress.update(updated_at=now, existing_images_preserved=8, new_valid_images_this_cycle=51,
                    remaining_images=0,next_number=None,status="references_complete_awaiting_owner_review",
                    editorial_status="not_approved",video_generation_performed=False,topview_queue_modified=False)
    progress["source_warnings"]=[w for w in progress.get("source_warnings",[]) if w.get("numbers") != [2,3,4,5,6,7,8]]
    save(progress_path,progress)

    for scene in (1,2):
        manifest_path = project/f"references/scenes/scene-{scene}/manifest.json"
        manifest=load(manifest_path)
        relevant=[it for it in items if it["scene"]==scene]
        manifest["references"]=[{
            "tag":it["label"].split(" · ")[0],
            "role":image_role(it),
            "path":it["path"], "sha256":it["sha256"],
            "width":it["width"], "height":it["height"],
            "prompt_path":it["prompt_path"],"editorial_status":"not_approved"
        } for it in relevant]
        manifest.update(updated_at=now,status="references_ready",generated_image_count=len(relevant),
                        expected_image_count=len(relevant),planned_references=[],editorial_status="not_approved")
        save(manifest_path,manifest)

    index=load(project/"references/usage-index.json")
    index.update(updated_at=now,generated_image_count=59,generated_orphans=[],
        images=[{"path":it["path"],"scenes":[it["scene"]],
                 "roles":[image_role(it)],"sha256":it["sha256"],
                 "editorial_status":"not_approved"} for it in items])
    save(project/"references/usage-index.json",index)

    chars_path=project/"character-references.json"
    cjson=load(chars_path)
    cjson["updated_at"]=now
    cjson["source"]="59/59 existing scene references recovered and registered; all not_approved; no video generated."
    for c in cjson["characters"]:
        nums=CHAR_NUMBERS[c["id"]]
        primary=item_by_num[nums[0]]
        p=primary["path"]
        c["model_sheet"]["public_image"]=p
        c["model_sheet"]["full_image"]=p
        if nums[0]>=9:
            c["model_sheet"]["source"]="Previously generated Topview reference, restored without re-generation; editorial_status not_approved"
        c["model_sheet"]["additional"]=[item_by_num[n]["path"] for n in nums[1:]]
        c["reference_images"]=[{
            "path":item_by_num[n]["path"],
            "caption":item_by_num[n]["label"] + " · не одобрено",
            "editorial_status":"not_approved",
            "derived_from":[] if n==nums[0] else [p],
            "sha256":item_by_num[n]["sha256"],
            "scenes":c["scenes"]
        } for n in nums]
        prov=c.setdefault("provenance",{})
        prov.update(status="generated",sha256=primary["sha256"],
                    width=primary["width"],height=primary["height"],
                    editorial_status="not_approved",
                    note="Previously generated original saved in canonical GitHub; technical processing does not mean owner approval.")
        prov.pop("planned_reference_images",None)
    for asset in cjson["assets"]:
        current=asset.get("planned_reference_images",[])
        if not current:current=[x["path"] for x in asset.get("images",[])]
        if len(current)!=1:raise ValueError("Asset lacks unique reference path "+asset["id"])
        it=next((it for it in items if it["path"]==current[0]),None)
        if not it:raise ValueError("Unmapped asset path "+str(current))
        asset["images"]=[{"path":it["path"],"caption":asset["name"],
                          "sha256":it["sha256"],"scenes":asset["scenes"],
                          "editorial_status":"not_approved"}]
        asset["provenance"]={"status":"generated","source":"Topview original, no rerender"}
        asset["editorial_status"]="not_approved"
        asset.pop("planned_reference_images",None)
    save(chars_path,cjson)

    master_path=project/"video-prompts.md"
    master=master_path.read_text(encoding="utf-8")
    master=source_inputs(master,items,cjson["characters"],cjson["assets"])
    master,change1=re.subn(r"Сохранено 8 из 26 референсов сцены:[^\n]*", 
               "Все 26 референсов сцены сохранены, но не одобрены владельцем. Видео не запускались.",master)
    master,change2=re.subn(r"Картинок ещё нет \(список[^\n]*", 
               "Все 33 референса сцены сохранены, но не одобрены владельцем. Видео не запускались. Техническая проверка не означает приёмку.",master)
    if change1 != 1 or change2 != 1:
        raise RuntimeError("Readiness strings changed; refusing to overwrite master silently")
    master_path.write_text(master,encoding="utf-8")

    cp=project/"reports/current-work-checkpoint.md"
    before=cp.read_text(encoding="utf-8")
    header=(f"# Разное — референсы C1–C59 сохранены · {now}\n\n"
            "work_id: MISC-S1-S2-REFERENCES\n"
            "Состояние: 59/59 исходных референсов технически сохранены в GitHub (26 + 33). "
            "51 оригинал из Codex Creations без повторной генерации, 8 прежних сохранены. "
            "51 Topview task сопоставлен с отдельным source SHA, проверен формат, размеры 3:2/9:16. "
            "Все not_approved; обе сцены DRAFT, очередь Topview не изменена, видеогенераций 0.\n"
            "Следующее действие: владелец проверяет картинки визуально и отдельно принимает/отклоняет. "
            "Техническое наличие 59/59 не равно художественной приёмке.\n\n---\n\n")
    cp.write_text(header+before,encoding="utf-8")

    reg=project/"work-resume-register.json"
    state=load(reg)
    state["last_updated_at"]=now
    for w in state.get("active_work",[]):
        if w.get("work_id")=="MISC-S1-S2-REFERENCES":
            w.update(status="awaiting_editorial_review",updated_at=now,
                     next_action="Owner image QC/approval for the two draft scenes; no auto approvals.")
            w.setdefault("completed",[]).append(f"{now}: 59/59 original references recovered and indexed; no rerenders, scene draft remains.")
            w["recovery"]={"schema_version":1,"verified_at":now,
                "last_completed":"59 PNG published, 26 in scene 1, 33 in scene 2; status not_approved.",
                "next_action":"Owner editorial review.",
                "checkpoint":{"file":str(cp),
                "sha256":digest(cp.read_bytes())},
                "read_next":["projects/raznoe/references/usage-index.json",
                             "projects/raznoe/references/scenes/scene-1/manifest.json",
                             "projects/raznoe/references/scenes/scene-2/manifest.json"]}
    save(reg,state)
    print("COMPLETE:",len(items),"refs; scene1",26,"scene2",33,"24 galleries; updated",now)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-zip",required=True)
    ap.add_argument("--source-map",required=True)
    args=ap.parse_args()
    run(args.source_zip,args.source_map)

if __name__=="__main__":
    main()
