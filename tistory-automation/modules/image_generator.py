import time
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output" / "images"


def generate_image(keyword: str) -> str | None:
    prompt = (
        f"Minimalist medical icon illustration for {keyword}, "
        "flat design, soft blue and mint green, white background, "
        "clean simple shapes only, absolutely no text no letters no writing no numbers, "
        "icon-only infographic style, professional healthcare visual"
    )

    encoded = urllib.parse.quote(prompt)
    seed = int(time.time()) % 10000
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=960&height=540&seed={seed}&nologo=true&model=flux"

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = keyword.replace(" ", "_").replace("/", "_")[:40]
        image_path = OUTPUT_DIR / f"{int(time.time())}_{safe_name}.png"

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            image_path.write_bytes(resp.read())

        return str(image_path)
    except Exception as e:
        print(f"  [이미지] Pollinations 실패: {e}")
        return None
