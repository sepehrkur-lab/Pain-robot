# ai_client.py
# Fallback AI client: tries memory, then web-search+simple-extract summarizer.
# No API key required. Lightweight, best-effort.

import requests
from bs4 import BeautifulSoup
import time
import re
from memory import QAStorage

USER_AGENT = "Mozilla/5.0 (Android) PainRobot/1.0"

# simple helper to do a DuckDuckGo "html" query (no api)
def ddg_search(query, max_results=3, timeout=8):
    q = query.replace(" ", "+")
    url = f"https://html.duckduckgo.com/html/?q={q}"
    headers = {"User-Agent": USER_AGENT}
    r = requests.post(url, headers=headers, data={"q": query}, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    # DuckDuckGo html results are in "result__a" anchors or "result" divs
    for a in soup.select("a.result__a")[:max_results]:
        href = a.get("href")
        title = a.get_text().strip()
        results.append((title, href))
    # fallback selectors
    if not results:
        for rdiv in soup.select("div.result__snippet")[:max_results]:
            text = rdiv.get_text().strip()
            results.append((text, None))
    return results

# fetch a page and attempt to extract main text
def fetch_text(url, timeout=8):
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # remove scripts/styles
        for s in soup(["script", "style", "noscript", "svg"]):
            s.decompose()
        # try to get article-like text
        article = soup.find("article")
        if article:
            text = article.get_text(" ", strip=True)
        else:
            # join main paragraphs
            ps = soup.find_all("p")
            text = " ".join(p.get_text(" ", strip=True) for p in ps[:8])
        # collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text[:4000]  # limit size
    except Exception:
        return ""

# very simple summarizer: pull first meaningful sentences
def summarize_text(text, max_chars=400):
    if not text:
        return ""
    # split into sentences roughly
    sents = re.split(r'(?<=[.!?])\s+', text)
    out = []
    chars = 0
    for s in sents:
        if len(s.strip()) == 0:
            continue
        if chars + len(s) > max_chars:
            break
        out.append(s.strip())
        chars += len(s)
        if len(out) >= 4:
            break
    return " ".join(out)

# main client
class AIClient:
    def __init__(self, db_path="pain_memory.db"):
        self.mem = QAStorage(db_path)

    def answer(self, question, use_web=True):
        question = question.strip()
        # 1) check local memory
        cached = self.mem.find_answer(question)
        if cached:
            return {"source":"memory", "answer": cached, "cached": True}

        # 2) try simple heuristics / builtins
        builtin = self._builtin_answer(question)
        if builtin:
            self.mem.save_qa(question, builtin, source="builtin")
            return {"source":"builtin", "answer": builtin, "cached": False}

        # 3) fallback: web search + summarize
        if use_web:
            try:
                results = ddg_search(question, max_results=4)
                pieces = []
                for title, href in results:
                    if href:
                        txt = fetch_text(href)
                        if txt:
                            pieces.append((title, summarize_text(txt, max_chars=300)))
                        else:
                            pieces.append((title, ""))
                    else:
                        pieces.append((title, ""))
                    time.sleep(0.4)
                # combine pieces into a reply
                reply_parts = []
                for title, summary in pieces:
                    if summary:
                        reply_parts.append(f"{summary}")
                if reply_parts:
                    answer = " ".join(reply_parts)[:1500]
                    # save to memory
                    self.mem.save_qa(question, answer, source="web")
                    return {"source":"web", "answer": answer, "cached": False}
            except Exception as e:
                # fail silently and continue
                pass

        # 4) final fallback
        fallback = "Sorry — I don't know the answer right now."
        self.mem.save_qa(question, fallback, source="unknown")
        return {"source":"unknown", "answer": fallback, "cached": False}

    def _builtin_answer(self, q):
        # add a few hard-coded facts you requested in conversation
        ql = q.lower()
        if "who made you" in ql or "sepehr" in ql:
            return ("Sepehr is my creator. He made me at age 14 and is from "
                    "Kermanshah province, Ravansar (روانسر).")
        return None

# quick test when run directly
if __name__ == "__main__":
    c = AIClient()
    q = input("Question: ")
    r = c.answer(q)
    print("==ANSWER==")
    print(r["answer"])
