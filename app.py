from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import requests
from sentence_transformers import SentenceTransformer, util
import pytesseract
from PIL import Image
from io import BytesIO
import base64
import torch

app = Flask(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")
source_data = []

MAIN_URL = "https://tds.s-anand.net/#/2025-01/"
DISCOURSE_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

async def fetch_all_sections_text_and_images(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)

        async def extract_text_and_images_from_page():
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            texts = [tag.get_text(strip=True) for tag in soup.find_all(['p', 'div', 'span', 'li']) if len(tag.get_text(strip=True)) > 50]
            images = [
                requests.compat.urljoin(url, img['src']) 
                for img in soup.find_all('img', src=True)
            ]
            return texts, images

        all_texts, all_images = await extract_text_and_images_from_page()
        section_buttons = await page.query_selector_all("a[href^='#/2025-']")
        visited = set()

        for btn in section_buttons:
            try:
                href = await btn.get_attribute('href')
                if href in visited:
                    continue
                visited.add(href)
                await btn.click()
                await page.wait_for_timeout(2000)
                texts, images = await extract_text_and_images_from_page()
                all_texts.extend(texts)
                all_images.extend(images)
            except Exception as e:
                print(f"Section error: {e}")
        await browser.close()
        return all_texts, all_images

async def fetch_rendered_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        html = await page.content()
        await browser.close()
        return html

def ocr_image_from_url(url):
    try:
        resp = requests.get(url, timeout=10)
        img = Image.open(BytesIO(resp.content))
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        print(f"OCR failed for image {url}: {e}")
        return ""

def ocr_image_from_base64(image_data):
    try:
        header_removed = re.sub('^data:image/.+;base64,', '', image_data)
        img_bytes = base64.b64decode(header_removed)
        img = Image.open(BytesIO(img_bytes))
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        print(f"OCR failed on base64 image: {e}")
        return ""

def load_data():
    print("Scraping all sections and processing content...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tds_texts, tds_images = loop.run_until_complete(fetch_all_sections_text_and_images(MAIN_URL))
    discourse_html = loop.run_until_complete(fetch_rendered_html(DISCOURSE_URL))
    discourse_soup = BeautifulSoup(discourse_html, "html.parser")
    discourse_texts = [tag.get_text(strip=True) for tag in discourse_soup.find_all(['p', 'div', 'span', 'li']) if len(tag.get_text(strip=True)) > 50]
    discourse_images = [requests.compat.urljoin(DISCOURSE_URL, img['src']) for img in discourse_soup.find_all('img', src=True)]

    global source_data
    source_data = []

    def add_entry(text, src):
        if text and len(text) > 50:
            emb = model.encode(text, convert_to_tensor=True)
            source_data.append({"source": src, "text": text, "embedding": emb})

    for t in tds_texts:
        add_entry(t, "tds")

    for url in tds_images:
        text = ocr_image_from_url(url)
        add_entry(text, "tds_image")

    for t in discourse_texts:
        add_entry(t, "discourse")

    for url in discourse_images:
        text = ocr_image_from_url(url)
        add_entry(text, "discourse_image")

def find_best_matches(question_text, top_k=2):
    q_embed = model.encode(question_text, convert_to_tensor=True)
    scores = [(util.pytorch_cos_sim(q_embed, item["embedding"]).item(), item) for item in source_data]
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:top_k]

@app.route("/api/", methods=["POST"])
def answer():
    data = request.get_json()
    question = data.get("question", "")
    base64_img = data.get("image", "")

    if not question and not base64_img:
        return jsonify({"error": "Please provide a question or an image."}), 400

    combined_input = question

    if base64_img:
        image_text = ocr_image_from_base64(base64_img)
        if image_text:
            combined_input += " " + image_text

    top_matches = find_best_matches(combined_input)

    if not top_matches:
        return jsonify({
            "answer": "Sorry, I couldn’t find a relevant answer.",
            "links": []
        })

    answer_texts = [match[1]["text"] for match in top_matches]
    links = []
    for txt in answer_texts:
        found_links = re.findall(r'https?://[^\s")\]]+', txt)
        links.extend(found_links)

    return jsonify({
        "answer": " ".join(answer_texts),
        "links": [{"url": l, "text": "Reference"} for l in list(set(links))[:3]]
    })

if __name__ == "__main__":
    print("Loading data before starting server...")
    load_data()
    print("Data loaded. Starting server.")
    app.run(debug=True, host="0.0.0.0", port=5000)

