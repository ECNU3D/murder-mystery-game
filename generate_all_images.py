import os
import subprocess
import sys
import argparse

# A dictionary to hold all theme configurations.
THEMES = {
    "jzy": {
        "folder": "荆州宴-三国主题",
        "scripts": {
            "GM_手册.md": {"prompt": "A mysterious ancient Chinese scroll map of Jingzhou, with a bloody dagger lying on it. The style should be dark and gritty, digital painting.", "filename": "gm_cover.png", "alt_text": "GM Manual Cover"},
            "00_公共剧本_v2.md": {"prompt": "A lavish ancient Chinese banquet hall at night, with guests in traditional Hanfu. The atmosphere is tense and full of suspicion. A single empty seat is in the foreground. Cinematic, dramatic lighting.", "filename": "banquet_hall.png", "alt_text": "Jingzhou Banquet"},
            "01_夏侯将军_v2.md": {"prompt": "A proud and arrogant young ancient Chinese general, with a sharp gaze, wearing the armor of Cao Wei. He is holding a magnificent sword. Full body portrait, realistic style.", "filename": "general_xiahou.png", "alt_text": "General Xiahou"},
            "02_朱先生_v2.md": {"prompt": "A wise and calm ancient Chinese scholar and strategist, dressed in the style of Shu Han, holding a feather fan, with a thoughtful expression. Portrait, ink wash painting style.", "filename": "scholar_zhu.png", "alt_text": "Scholar Zhu"},
            "03_乔夫人_v2.md": {"prompt": "An elegant and beautiful ancient Chinese noblewoman from Jiangdong, wearing luxurious silk Hanfu. Her expression is a mix of charm and anxiety. Portrait, detailed digital art.", "filename": "lady_qiao.png", "alt_text": "Lady Qiao"},
            "04_华神医_v2.md": {"prompt": "A mysterious and reclusive ancient Chinese doctor, with a wise but cold look in his eyes, carrying a medicine box. He is standing in the shadow. Moody lighting, realistic.", "filename": "doctor_hua.png", "alt_text": "Doctor Hua"},
            "05_陈月_v2.md": {"prompt": "A beautiful and seemingly innocent young ancient Chinese lady, with tears in her eyes, but a hidden coldness deep within. Close-up portrait, dramatic lighting, photorealistic.", "filename": "chen_yue.png", "alt_text": "Chen Yue"},
            "06_王管家_v2.md": {"prompt": "A loyal but anxious-looking elderly ancient Chinese butler, with a hunched back and worried eyes, holding a lantern in a dark corridor. Realistic style.", "filename": "butler_wang.png", "alt_text": "Butler Wang"},
            "07_小舞_v2.md": {"prompt": "A graceful and beautiful ancient Chinese dancer in a flowing silk dress, her face showing a complex mix of hope and fear. She is in mid-dance. Dynamic pose, watercolor style.", "filename": "dancer_xiaowu.png", "alt_text": "Dancer Xiaowu"}
        },
        "clues": {
            "clue_b": {"prompt": "A gorgeous ancient Chinese dagger with a blurred character 'Xia' engraved on the hilt, placed as evidence on a wooden table. Photorealistic, dramatic lighting.", "filename": "clue_dagger.png", "alt_text": "Clue: A gorgeous dagger", "placeholder_text": "[图片: a gorgeous ancient Chinese dagger with a blurred character 'Xia' engraved on the hilt, placed as evidence.]"},
            "clue_f": {"prompt": "A locked rosewood box with a subtle scratch on the bottom, looking lighter than expected, placed on a silk cushion. Close-up, detailed digital painting.", "filename": "clue_rosewood_box.png", "alt_text": "Clue: A locked rosewood box", "placeholder_text": "[图片: a locked rosewood box with a subtle scratch on the bottom, looking lighter than expected.]"}
        }
    },
    "shz": {
        "folder": "水浒传-风雪山神庙",
        "scripts": {
            "GM_手册.md": {"prompt": "An ancient, snow-covered mountain temple at night, with a roaring fire visible inside. The style is a dramatic, dark ink wash painting.", "filename": "gm_cover.png", "alt_text": "GM Manual Cover"},
            "00_公共剧本.md": {"prompt": "A group of ancient Chinese heroes from the Song Dynasty gathered in a dilapidated temple during a snowstorm. The atmosphere is tense, with suspicion in their eyes. Cinematic, realistic painting.", "filename": "public_script_cover.png", "alt_text": "A gathering in the temple"},
            "01_林冲.md": {"prompt": "A heroic ancient Chinese warrior with a panther-like sharp gaze, holding a spear, his face filled with sorrow and rage. He is standing in a snowstorm. Portrait, digital painting.", "filename": "lin_chong.png", "alt_text": "Lin Chong"},
            "02_鲁智深.md": {"prompt": "A big, strong and tattooed ancient Chinese monk, with a booming laugh and a fiery temper, holding a heavy monk's spade. Full body portrait, dynamic style.", "filename": "lu_zhishen.png", "alt_text": "Lu Zhishen"},
            "03_金翠莲.md": {"prompt": "A beautiful and resilient ancient Chinese woman, dressed in simple clothes, her eyes showing a mix of gratitude and hidden determination. Portrait, watercolor style.", "filename": "jin_cuilian.png", "alt_text": "Jin Cuilian"},
            "04_张教头.md": {"prompt": "An upright and loyal ancient Chinese military instructor, with a righteous but worried expression, holding a letter in his hand. Realistic portrait.", "filename": "zhang_jiaotou.png", "alt_text": "Instructor Zhang"},
            "05_李小二.md": {"prompt": "An honest and simple-looking ancient Chinese innkeeper, with a slightly panicked look on his face, as if he has heard a terrible secret. Close-up portrait.", "filename": "li_xiaoer.png", "alt_text": "Li Xiaoer"},
            "06_富安.md": {"prompt": "A ghostly, transparent figure of a cowardly ancient Chinese servant, his face frozen in terror. Ethereal, spooky style.", "filename": "fu_an_ghost.png", "alt_text": "Fu An's Ghost"},
            "07_沧州府尹.md": {"prompt": "A cunning and shrewd ancient Chinese local official in his official robes, with a calculating look in his eyes. He is stroking his beard thoughtfully. Portrait.", "filename": "prefect_of_cangzhou.png", "alt_text": "Prefect of Cangzhou"}
        },
        "clues": {
            "clue_c": {"prompt": "A delicate golden phoenix hairpin, its tip sharpened and slightly blackened, lying in the snow. Close-up, photorealistic.", "filename": "clue_golden_hairpin.png", "alt_text": "Clue: A golden hairpin", "placeholder_text": "[图片: a delicate golden phoenix hairpin, its tip sharpened and slightly blackened, lying in the snow.]"},
            "clue_d": {"prompt": "Two sets of distinct footprints in the snow outside an ancient temple. One set is very large and deep, the other is small and light. Top-down view, moody lighting.", "filename": "clue_footprints.png", "alt_text": "Clue: Footprints in the snow", "placeholder_text": "[图片: two sets of distinct footprints in the snow outside an ancient temple. One set is very large and deep, the other is small and light.]"}
        }
    },
    "hlm": {
        "folder": "红楼梦-海棠诗社的阴影",
        "scripts": {
            "GM_手册.md": {"prompt": "A grand, ancient Chinese garden at night, covered in light snow. A single lantern illuminates a secluded rockery, hinting at a dark secret. Style of a classical Chinese painting, moody and atmospheric.", "filename": "gm_cover_honglou.png", "alt_text": "GM Manual Cover"},
            "00_公共剧本.md": {"prompt": "A group of elegantly dressed ancient Chinese nobles having a poetry gathering in a garden at night. The mood is tense and suspicious after a shocking event. Cinematic, detailed digital painting.", "filename": "public_script_cover_honglou.png", "alt_text": "A tense gathering"},
            "01_贾宝玉.md": {"prompt": "A handsome, gentle-faced young nobleman from ancient China, with a sentimental expression, wearing luxurious robes and a jade pendant. Portrait, in the style of classical Chinese art.", "filename": "jia_baoyu.png", "alt_text": "Jia Baoyu"},
            "02_王熙凤.md": {"prompt": "A beautiful, powerful and sharp-eyed noblewoman from ancient China, wearing opulent clothing with golden phoenix decorations. Her expression is a mix of authority and cunning. Realistic portrait.", "filename": "wang_xifeng.png", "alt_text": "Wang Xifeng"},
            "03_薛宝钗.md": {"prompt": "An elegant and graceful ancient Chinese lady, with a calm and perfectly composed expression. She is dressed in simple but high-quality silks, holding a round fan. Portrait, watercolor style.", "filename": "xue_baochai.png", "alt_text": "Xue Baochai"},
            "04_贾环.md": {"prompt": "A sullen-looking young man from an ancient Chinese noble family, with a resentful and gloomy look in his eyes, standing in the shadows. Portrait, dramatic lighting.", "filename": "jia_huan.png", "alt_text": "Jia Huan"},
            "05_林黛玉.md": {"prompt": "A frail, ethereal and beautiful young lady from ancient China, with a melancholic and intelligent gaze, holding a handkerchief to her lips. She is surrounded by bamboo. Ink wash painting style.", "filename": "lin_daiyu.png", "alt_text": "Lin Daiyu"},
            "06_晴雯.md": {"prompt": "A pretty and fiery-tempered ancient Chinese maid, with a proud and defiant expression on her face. Close-up portrait, realistic style.", "filename": "qing_wen.png", "alt_text": "Qingwen"},
            "07_薛蟠.md": {"prompt": "A boorish and arrogant-looking wealthy young man from ancient China, dressed in flashy silks, with a brutish expression. He looks like a bully. Portrait.", "filename": "xue_pan.png", "alt_text": "Xue Pan"}
        },
        "clues": {
            "clue_c": {"prompt": "A slightly worn ancient Chinese jade pendant with a simple design, held in a rough-looking hand. Close-up, photorealistic, dramatic lighting.", "filename": "clue_jade_pendant.png", "alt_text": "Clue: A jade pendant", "placeholder_text": "[图片: a slightly worn ancient Chinese jade pendant with a simple design, held in a rough-looking hand.]"}
        }
    },
    "xyj": {
        "folder": "西游记-真假白骨精",
        "scripts": {
            "GM_手册.md": {"prompt": "A desolate and ancient mountain temple at night, filled with an eerie, supernatural light. A figure lies motionless in the center. The style is a dramatic, mystical Chinese fantasy painting.", "filename": "gm_cover_xiyou.png", "alt_text": "GM Manual Cover"},
            "00_公共剧本.md": {"prompt": "A group of divine and demonic beings from ancient Chinese mythology gathered in a dilapidated temple. The atmosphere is tense and full of suspicion. Cinematic, fantasy art style.", "filename": "public_script_cover_xiyou.png", "alt_text": "A gathering of gods and demons"},
            "01_唐三藏.md": {"prompt": "A handsome and devout ancient Chinese monk, wearing a kasaya, his face showing a mix of piety, stubbornness, and inner conflict. Portrait, in the style of classical Buddhist art.", "filename": "tang_sanzang.png", "alt_text": "Tang Sanzang"},
            "02_猪八戒.md": {"prompt": "A comical-looking half-man, half-pig creature from Chinese mythology, with a greedy and cunning expression, holding a nine-toothed rake. Full body portrait, fantasy style.", "filename": "zhu_bajie.png", "alt_text": "Zhu Bajie"},
            "03_沙和尚.md": {"prompt": "A loyal and honest-looking warrior monk from ancient China, with a red beard and wearing a necklace of skulls. His expression is stoic, but his eyes hold a deep secret. Portrait, realistic fantasy style.", "filename": "sha_wujing.png", "alt_text": "Sha Wujing"},
            "04_白骨夫人.md": {"prompt": "A beautiful and deceptive ancient Chinese demoness, disguised as a frail and innocent village girl. Her eyes show a hidden cunning. Portrait, ethereal fantasy art.", "filename": "lady_white_bone.png", "alt_text": "Lady White Bone"},
            "05_太白金星.md": {"prompt": "A wise and benevolent-looking ancient Chinese deity with a long white beard, wearing Taoist robes and holding a whisk. His smile seems to hide a deeper plan. Portrait.", "filename": "taibai_jinxing.png", "alt_text": "Taibai Jinxing"},
            "06_土地公.md": {"prompt": "A short, cheerful but timid-looking old earth god from Chinese mythology, with a long white beard and a staff, peeking out from behind a rock. Whimsical, fantasy style.", "filename": "tudigong.png", "alt_text": "Earth God"},
            "07_黄袍怪.md": {"prompt": "A fierce and powerful ancient Chinese demon king with a yellow robe and a monstrous face, holding a saber. He looks suspicious and alert. Full body portrait, fantasy art.", "filename": "huangpaoguai.png", "alt_text": "Yellow Robe Demon"}
        },
        "clues": {
            "clue_c": {"prompt": "A single, shimmering silver thread from a Taoist whisk, lying on a dusty prayer mat in a dark temple. Close-up, photorealistic, magical lighting.", "filename": "clue_silver_thread.png", "alt_text": "Clue: A silver thread", "placeholder_text": "[图片: a single, shimmering silver thread lying on a dusty prayer mat.]"},
            "clue_d": {"prompt": "A close-up of a dead man's fingernail, with tiny, colorful grains of sand embedded underneath. The sand glitters with a faint magical light. Macro photography, fantasy style.", "filename": "clue_magic_sand.png", "alt_text": "Clue: Colorful sand", "placeholder_text": "[图片: a close-up of a dead man's fingernail, with tiny, colorful grains of sand embedded underneath.]"}
        }
    },
    "shz_zqs": {
        "folder": "水浒传-智取生辰纲",
        "scripts": {
            "GM_手册.md": {"prompt": "A group of ancient Chinese heroes gathered around a table in a rustic tavern, planning a heist. A detailed map is spread on the table. The mood is tense and exciting. Digital painting.", "filename": "gm_cover_zqs.png", "alt_text": "GM Manual Cover"},
            "00_公共剧本.md": {"prompt": "A tense standoff in a rundown ancient Chinese tavern during a heavy rainstorm. On one side are government guards, on the other are mysterious heroes. Cinematic, dramatic lighting.", "filename": "public_script_cover_zqs.png", "alt_text": "Tavern Standoff"},
            "01_杨志.md": {"prompt": "A heroic but frustrated ancient Chinese warrior with a blue birthmark on his face, his hand on his saber, looking desperate and angry. Portrait, realistic style.", "filename": "yang_zhi.png", "alt_text": "Yang Zhi"},
            "02_晁盖.md": {"prompt": "A righteous and respected village leader from ancient China, with a leader's aura, looking determined and thoughtful. Portrait, ink wash painting style.", "filename": "chao_gai.png", "alt_text": "Chao Gai"},
            "03_吴用.md": {"prompt": "A clever and cunning ancient Chinese scholar, holding a folding fan, with a subtle, knowing smile on his face. Portrait, detailed digital art.", "filename": "wu_yong.png", "alt_text": "Wu Yong"},
            "04_白胜.md": {"prompt": "A nimble and shifty-looking man from ancient China, dressed as a commoner, carrying a shoulder pole with two buckets. He looks nervous but cunning. Full body portrait.", "filename": "bai_sheng.png", "alt_text": "Bai Sheng"},
            "05_何九叔.md": {"prompt": "A cautious and experienced elderly coroner from ancient China, holding a magnifying glass and examining a clue, his face showing deep concentration. Realistic portrait.", "filename": "he_jiushu.png", "alt_text": "Coroner He"},
            "06_刘唐.md": {"prompt": "A fiery-tempered ancient Chinese hero with a red birthmark and a wild look in his eyes, looking ready for a fight. Close-up portrait, dynamic style.", "filename": "liu_tang.png", "alt_text": "Liu Tang"},
            "07_何老太.md": {"prompt": "A sharp-eyed and worldly-wise old innkeeper from ancient China, wiping a table but secretly observing her guests. Realistic, character-focused painting.", "filename": "he_laotai.png", "alt_text": "Innkeeper He"}
        },
        "clues": {
            "clue_c": {"prompt": "An elegant ancient Chinese folding fan, with one of its bamboo ribs slightly darker than the others, hinting at a hidden mechanism. Close-up, photorealistic, dramatic lighting.", "filename": "clue_folding_fan.png", "alt_text": "Clue: A folding fan", "placeholder_text": "[图片: an elegant ancient Chinese folding fan, with one of its bamboo ribs slightly darker than the others.]"}
        }
    }
}

def run_command(command, description=""):
    """Runs a command and handles errors."""
    print(f"Executing: {description}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print("Error:", result.stderr.strip(), file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        print(e.stdout.strip(), file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        return False

def process_scripts(theme_config, venv_python):
    """Processes all script files for a theme."""
    print(f"\n--- Processing scripts for theme: {theme_config['folder']} ---")
    script_path = "insert_markdown_image.py"
    for md_file, details in theme_config["scripts"].items():
        full_md_path = os.path.join(theme_config['folder'], md_file)
        if not os.path.exists(full_md_path):
            print(f"Warning: Markdown file '{full_md_path}' not found. Skipping.")
            continue
        
        print(f"Processing {full_md_path}...")
        image_path_in_md = f"./images/{details['filename']}"
        command = [
            venv_python, script_path,
            "--markdown_file", full_md_path,
            "--image_path", image_path_in_md,
            "--alt_text", details["alt_text"]
        ]
        # First, generate the image using the old script's generation capability
        gen_command = [
            venv_python, "insert_image.py",
            "--prompt", details["prompt"],
            "--image_filename", details["filename"],
            "--markdown_file", full_md_path, # Dummy path
            "--alt_text", details["alt_text"]
        ]
        if run_command(gen_command, f"Generate image for {md_file}"):
            # Then, insert the tag using the new script
            run_command(command, f"Insert tag into {md_file}")


def process_clues(theme_config, venv_python):
    """Processes all clue files for a theme using the new robust method."""
    print(f"\n--- Processing clues for theme: {theme_config['folder']} ---")
    gm_manual_path = os.path.join(theme_config['folder'], "GM_手册.md")
    if not os.path.exists(gm_manual_path):
        print(f"Error: GM Manual not found at '{gm_manual_path}'.", file=sys.stderr)
        return

    try:
        with open(gm_manual_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading GM Manual: {e}", file=sys.stderr)
        return

    for clue_name, details in theme_config["clues"].items():
        gen_command = [
            venv_python, "insert_image.py",
            "--prompt", details["prompt"],
            "--image_filename", details["filename"],
            "--markdown_file", gm_manual_path, # Dummy path
            "--alt_text", details["alt_text"]
        ]
        if run_command(gen_command, f"Generate image for clue {details['filename']}"):
            image_tag_to_insert = f"![{details['alt_text']}] (./images/{details['filename']})"
            placeholder = details['placeholder_text']
            if placeholder in content:
                content = content.replace(placeholder, image_tag_to_insert)
                print(f"Placeholder for '{details['filename']}' replaced in memory.")
            else:
                print(f"Warning: Placeholder '{placeholder}' not found in {gm_manual_path}.", file=sys.stderr)
    
    try:
        with open(gm_manual_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccessfully updated {gm_manual_path} with all clue images.")
    except IOError as e:
        print(f"Error writing to GM Manual: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Generate and insert images for murder mystery scripts.")
    parser.add_argument("--theme", required=True, choices=THEMES.keys(), help="The theme to process.")
    parser.add_argument("--target", required=True, choices=['scripts', 'clues', 'all'], help="The target to process: 'scripts', 'clues', or 'all'.")
    args = parser.parse_args()

    theme_config = THEMES.get(args.theme)
    if not theme_config:
        print(f"Error: Theme '{args.theme}' not found in configuration.", file=sys.stderr)
        sys.exit(1)

    venv_python = os.path.join(".venv", "bin", "python")
    if not os.path.exists(venv_python):
        print(f"Error: Could not find Python executable at '{venv_python}'.", file=sys.stderr)
        sys.exit(1)

    if args.target in ['scripts', 'all']:
        process_scripts(theme_config, venv_python)
    
    if args.target in ['clues', 'all']:
        process_clues(theme_config, venv_python)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()