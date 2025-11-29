# main.py
# Enhanced Sentiment Reader + Personal Link-card (NiceGUI + TextBlob)
# Requirements: nicegui, textblob

from nicegui import ui
from textblob import TextBlob
from datetime import datetime
import json
import base64
from io import BytesIO

# ---------- CONFIG ----------
PROFILE_IMAGE = 'image.png'
NAME = "Senith Samaranayake"
TITLE = "Digital Marketer | Growth Strategist | Personal Development Speaker"
LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/senith-samaranayake/", "bi-linkedin"),
    ("YouTube", "https://www.youtube.com/@senith_samaranayake", "bi-youtube"),
    ("WhatsApp", "https://api.whatsapp.com/send?phone=94710120130", "bi-whatsapp"),
    ("Instagram", "https://instagram.com/senith.lokitha", "bi-instagram"),
]

# ---------- STATE ----------
analysis_history = []

# ---------- UTILITIES ----------
def analyze_text_blob(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = "Positive"
        emoji = "😊"
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😔"
    else:
        sentiment = "Neutral"
        emoji = "😐"
    
    try:
        key_phrases = [w.lower() for w, pos in blob.tags if pos.startswith(("NN","JJ"))]
    except Exception:
        key_phrases = [w.lower() for w in blob.words if len(w) > 3]
    
    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "polarity": polarity,
        "polarity_percent": ((polarity + 1) / 2) * 100,
        "subjectivity": subjectivity,
        "subjectivity_label": "Subjective" if subjectivity > 0.5 else "Objective",
        "word_count": len(blob.words),
        "sentence_count": len(blob.sentences),
        "key_phrases": list(dict.fromkeys(key_phrases))[:10],
    }

def deep_analyze_text(text: str):
    """Perform comprehensive deep analysis of the text"""
    blob = TextBlob(text)
    basic_analysis = analyze_text_blob(text)
    
    sentences = list(blob.sentences)
    words = list(blob.words)
    
    # Sentence-by-sentence analysis
    sentence_analysis = []
    for i, sentence in enumerate(sentences, 1):
        sent_blob = TextBlob(str(sentence))
        sentence_analysis.append({
            "number": i,
            "text": str(sentence),
            "polarity": sent_blob.sentiment.polarity,
            "subjectivity": sent_blob.sentiment.subjectivity,
            "word_count": len(sent_blob.words)
        })
    
    # Word frequency analysis
    word_freq = {}
    for word in words:
        word_lower = word.lower()
        if len(word_lower) > 2:
            word_freq[word_lower] = word_freq.get(word_lower, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Analysis metrics
    positive_sentences = [s for s in sentence_analysis if s["polarity"] > 0.1]
    negative_sentences = [s for s in sentence_analysis if s["polarity"] < -0.1]
    neutral_sentences = [s for s in sentence_analysis if -0.1 <= s["polarity"] <= 0.1]
    
    avg_sentence_length = sum(len(s.words) for s in sentences) / len(sentences) if sentences else 0
    complexity_score = sum(s["subjectivity"] for s in sentence_analysis) / len(sentence_analysis) if sentence_analysis else 0
    
    polarities = [s["polarity"] for s in sentence_analysis]
    sentiment_consistency = 1 - (sum(abs(p - basic_analysis["polarity"]) for p in polarities) / len(polarities)) if polarities else 0
    
    return {
        "basic": basic_analysis,
        "sentences": sentence_analysis,
        "word_frequency": top_words,
        "statistics": {
            "total_sentences": len(sentences),
            "total_words": len(words),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "complexity_score": round(complexity_score, 3),
            "sentiment_consistency": round(max(0, sentiment_consistency), 3),
            "positive_sentences": len(positive_sentences),
            "negative_sentences": len(negative_sentences),
            "neutral_sentences": len(neutral_sentences)
        },
        "insights": {
            "dominant_emotion": "Positive" if len(positive_sentences) > len(negative_sentences) else "Negative" if len(negative_sentences) > len(positive_sentences) else "Neutral",
            "emotional_range": round(max(polarities) - min(polarities), 3) if polarities else 0,
            "subjectivity_level": "High" if complexity_score > 0.6 else "Medium" if complexity_score > 0.3 else "Low",
            "consistency_level": "High" if sentiment_consistency > 0.7 else "Medium" if sentiment_consistency > 0.4 else "Low"
        }
    }

def read_profile_image_datauri(path):
    try:
        with open(path, "rb") as f:
            b = base64.b64encode(f.read()).decode("ascii")
        ext = path.split('.')[-1].lower()
        mime = "image/png" if ext in ("png","apng") else f"image/{ext}"
        return f"data:{mime};base64,{b}"
    except Exception:
        svg = """
        <svg xmlns='http://www.w3.org/2000/svg' width='240' height='240' viewBox='0 0 24 24' fill='none' stroke='currentColor'>
          <rect width='24' height='24' rx='4' fill='#e2e8f0'/>
          <circle cx='12' cy='9' r='3' fill='#94a3b8'/>
          <path d='M6 20c1.5-4 10.5-4 12 0' stroke='#64748b' stroke-width='1.2' fill='none'/>
        </svg>
        """
        b = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{b}"

# ---------- UI ----------

# Head CSS + Bootstrap Icons + responsive design
ui.add_head_html('''
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
<style>
:root {
  --glass: rgba(255,255,255,0.06);
  --glass-strong: rgba(255,255,255,0.09);
  --accent-start: #667eea;
  --accent-end: #764ba2;
}
body { 
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; 
  background: linear-gradient(120deg,#0f172a,#071028);
  min-height: 100vh;
  margin: 0;
  padding: 15px;
}
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.profile-img { 
  width:80px; 
  height:80px; 
  border-radius:999px; 
  object-fit:cover; 
  border:3px solid rgba(255,255,255,0.06); 
  box-shadow: 0 10px 30px rgba(0,0,0,0.35); 
}
.social-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin: 0 8px;
  background: linear-gradient(135deg, var(--accent-start), var(--accent-end));
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 18px;
}
.social-icon:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}
.link-btn { 
  padding: 8px 16px; 
  border-radius: 8px; 
  background: linear-gradient(90deg,var(--accent-start),var(--accent-end)); 
  color:white; 
  font-weight:600; 
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
  width: 100%;
  margin-bottom: 8px;
}
.link-btn:hover {
  transform: translateY(-1px);
}
.btn-primary {
  background: linear-gradient(90deg,var(--accent-start),var(--accent-end));
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
  margin-right: 8px;
  margin-bottom: 8px;
}
.btn-primary:hover {
  transform: translateY(-1px);
}
.btn-secondary {
  background: rgba(255,255,255,0.1);
  color: white;
  border: 1px solid rgba(255,255,255,0.2);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 8px;
  margin-bottom: 8px;
}
.btn-secondary:hover {
  background: rgba(255,255,255,0.15);
}
.card-glass { 
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.015)); 
  border-radius: 14px; 
  padding: 20px; 
  border:1px solid rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  margin-bottom: 20px;
}
.glass-strong {
  background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.06)); 
  border-radius: 14px; 
  border:1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(15px);
}
.footer { 
  opacity:0.75; 
  font-size:13px; 
  color: rgba(255,255,255,0.6);
  text-align: center;
  margin-top: 30px;
}
.content-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 20px;
  align-items: start;
  margin-top: 10px;
}

/* Mobile Responsive */
@media (max-width: 968px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  .profile-img { 
    width: 70px; 
    height: 70px; 
  }
  .social-icon {
    width: 35px;
    height: 35px;
    font-size: 16px;
    margin: 0 5px;
  }
  body { 
    padding: 15px; 
  }
  .main-container {
    padding: 0 15px;
  }
  .card-glass {
    padding: 15px;
  }
}

@media (max-width: 640px) {
  .profile-img { 
    width: 60px; 
    height: 60px; 
  }
  .social-icon {
    width: 32px;
    height: 32px;
    font-size: 14px;
    margin: 0 4px;
  }
  body { 
    padding: 10px; 
  }
  .main-container {
    padding: 0 10px;
  }
  .btn-primary, .btn-secondary {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>
''')

# Main container with centered layout
with ui.column().classes('main-container'):
    # Main content grid
    with ui.row().classes('content-grid').style('width:100%;'):
        # Left column: input + results
        with ui.column().classes('flex-1').style('min-width:0;'):
            with ui.card().classes('card-glass'):
                ui.label("✨ Analyze Your Text").classes('text-xl').style('font-weight:700;color:white;')
                text_input = ui.textarea(
                    placeholder="Type or paste text here... (try product reviews, tweets, comments)",
                    value="This product is absolutely amazing! Best purchase I've made this year!"
                ).classes('w-full').props('clearable rows=6').style('background:rgba(255,255,255,0.05);color:white;border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:12px;min-height:120px;')
                
                with ui.row().classes('items-center gap-3').style('margin-top:12px;flex-wrap:wrap;'):
                    def do_analyze():
                        text = text_input.value.strip()
                        if not text:
                            ui.notify("Please enter some text", type='warning')
                            return
                        
                        analysis = analyze_text_blob(text)
                        analysis_record = {
                            "timestamp": datetime.now().isoformat(),
                            "text": text,
                            "sentiment": analysis["sentiment"],
                            "polarity": analysis["polarity"],
                            "subjectivity": analysis["subjectivity"]
                        }
                        analysis_history.append(analysis_record)
                        
                        result_box.clear()
                        with result_box:
                            with ui.card().classes('glass-strong').style('padding:18px;'):
                                ui.html(f"<div style='font-size:48px;text-align:center'>{analysis['emoji']}</div>")
                                ui.label(f"{analysis['sentiment']}").classes('text-lg').style('font-weight:800;text-align:center;margin-top:6px;color:white;')
                                ui.label(f"Score: {analysis['polarity']:.3f}  •  Subjectivity: {analysis['subjectivity']:.3f}").classes('text-sm text-white/60').style('text-align:center;margin-bottom:8px;')
                                
                                with ui.row().classes('gap-6 items-center').style('justify-content:center;margin-top:8px;'):
                                    with ui.card().classes('card-glass').style('padding:8px 12px;min-width:90px;'):
                                        ui.label(f"{analysis['word_count']} words").classes('text-sm').style('font-weight:700;color:white;text-align:center;')
                                    with ui.card().classes('card-glass').style('padding:8px 12px;min-width:120px;'):
                                        ui.label(f"{analysis['sentence_count']} sentences").classes('text-sm text-white/70').style('text-align:center;')
                                
                                if analysis['key_phrases']:
                                    ui.label("🔍 Key words").classes('text-sm text-white/70').style('margin-top:12px;')
                                    with ui.row().classes('gap-2').style('flex-wrap:wrap;margin-top:6px;'):
                                        for kp in analysis['key_phrases'][:8]:
                                            ui.html(f'<span style="padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.03);font-size:13px;color:rgba(255,255,255,0.7)">{kp}</span>')
                        
                        refresh_history_list()
                        ui.notify(f"✨ Analysis complete — {analysis['sentiment']}", type='positive')
                    
                    def do_deep_analyze():
                        text = text_input.value.strip()
                        if not text:
                            ui.notify("Please enter some text for deep analysis", type='warning')
                            return
                        
                        result_box.clear()
                        with result_box:
                            with ui.card().classes('glass-strong').style('padding:18px;text-align:center;'):
                                ui.html('<div style="font-size:32px;margin-bottom:10px;">🧠</div>')
                                ui.label("Performing Deep Analysis...").style('color:white;font-weight:600;')
                                ui.label("Analyzing sentences, words, and patterns").classes('text-sm text-white/60')
                        
                        ui.timer(1.0, lambda: show_deep_result(text), once=True)
                    
                    def show_deep_result(text):
                        deep_analysis = deep_analyze_text(text)
                        
                        analysis_record = {
                            "timestamp": datetime.now().isoformat(),
                            "text": text,
                            "sentiment": deep_analysis["basic"]["sentiment"],
                            "polarity": deep_analysis["basic"]["polarity"],
                            "subjectivity": deep_analysis["basic"]["subjectivity"],
                            "type": "deep_analysis"
                        }
                        analysis_history.append(analysis_record)
                        
                        result_box.clear()
                        with result_box:
                            with ui.card().classes('glass-strong').style('padding:18px;margin-bottom:15px;'):
                                ui.html(f"<div style='font-size:48px;text-align:center'>{deep_analysis['basic']['emoji']}</div>")
                                ui.label(f"📊 Deep Analysis: {deep_analysis['basic']['sentiment']}").classes('text-xl').style('font-weight:800;text-align:center;margin-top:6px;color:white;')
                                ui.label(f"Polarity: {deep_analysis['basic']['polarity']:.3f} | Subjectivity: {deep_analysis['basic']['subjectivity']:.3f}").classes('text-sm text-white/60').style('text-align:center;')
                            
                            with ui.card().classes('glass-strong').style('padding:18px;margin-bottom:15px;'):
                                ui.label("📈 Text Statistics").classes('text-lg').style('font-weight:700;color:white;margin-bottom:10px;')
                                stats = deep_analysis["statistics"]
                                with ui.row().classes('gap-4').style('flex-wrap:wrap;'):
                                    for label, value in [
                                        ("📝 Sentences", stats["total_sentences"]),
                                        ("🔤 Words", stats["total_words"]),
                                        ("📏 Avg Length", f"{stats['avg_sentence_length']:.1f}"),
                                        ("🎯 Consistency", f"{stats['sentiment_consistency']:.2f}")
                                    ]:
                                        with ui.card().classes('card-glass').style('padding:10px;min-width:100px;'):
                                            ui.label(label).classes('text-xs text-white/70').style('text-align:center;')
                                            ui.label(str(value)).classes('text-lg').style('font-weight:700;color:white;text-align:center;')
                            
                            with ui.card().classes('glass-strong').style('padding:18px;margin-bottom:15px;'):
                                ui.label("🔍 Sentence Analysis").classes('text-lg').style('font-weight:700;color:white;margin-bottom:10px;')
                                with ui.column().classes('gap-2').style('max-height:300px;overflow:auto;'):
                                    for sentence in deep_analysis["sentences"][:5]:
                                        sentiment_color = "rgba(34,197,94,0.2)" if sentence["polarity"] > 0.1 else "rgba(239,68,68,0.2)" if sentence["polarity"] < -0.1 else "rgba(107,114,128,0.2)"
                                        with ui.card().style(f'padding:12px;background:{sentiment_color};border:1px solid rgba(255,255,255,0.1);'):
                                            ui.label(f"Sentence {sentence['number']}").classes('text-xs text-white/70')
                                            ui.label(sentence["text"]).classes('text-sm').style('color:white;margin:5px 0;')
                                            ui.label(f"Polarity: {sentence['polarity']:.3f} | Words: {sentence['word_count']}").classes('text-xs text-white/60')
                            
                            with ui.row().classes('gap-4').style('flex-wrap:wrap;'):
                                with ui.card().classes('glass-strong').style('padding:18px;flex:1;min-width:300px;'):
                                    ui.label("💡 Key Insights").classes('text-lg').style('font-weight:700;color:white;margin-bottom:10px;')
                                    insights = deep_analysis["insights"]
                                    for label, value in insights.items():
                                        ui.label(f"{label.replace('_', ' ').title()}: {value}").classes('text-sm text-white/80').style('margin-bottom:5px;')
                                
                                with ui.card().classes('glass-strong').style('padding:18px;flex:1;min-width:300px;'):
                                    ui.label("🏷️ Most Frequent Words").classes('text-lg').style('font-weight:700;color:white;margin-bottom:10px;')
                                    with ui.row().classes('gap-2').style('flex-wrap:wrap;'):
                                        for word, freq in deep_analysis["word_frequency"][:8]:
                                            ui.html(f'<span style="padding:4px 8px;border-radius:12px;background:rgba(255,255,255,0.1);font-size:12px;color:white;">{word} ({freq})</span>')
                        
                        refresh_history_list()
                        ui.notify(f"🧠 Deep Analysis Complete — {deep_analysis['basic']['sentiment']}", type='positive')

                    ui.button("🔍 Quick Analyze", on_click=do_analyze).classes('btn-primary')
                    ui.button("🧠 Deep Analyze", on_click=do_deep_analyze).classes('btn-primary').style('background:linear-gradient(90deg,#8b5cf6,#a855f7);')
                    ui.button("🗑️ Clear", on_click=lambda: setattr(text_input, "value", "")).classes('btn-secondary')

            # Result container
            result_box = ui.column().classes('w-full').style('margin-top:12px;')

        # Right sidebar: app info + profile + examples + history
        with ui.column().style('min-width:320px;'):
            # App title card
            with ui.card().classes('card-glass'):
                with ui.column().classes('items-center'):
                    ui.html('<div style="font-size:32px;margin-bottom:8px;">🧠</div>')
                    ui.label("AI Sentiment Analyzer").classes('text-xl').style('font-weight:800;color:white;margin-bottom:5px;text-align:center;')
                    ui.label("Analyze text sentiment with advanced AI insights").classes('text-xs text-white/70').style('text-align:center;line-height:1.4;')
            
            # Profile card
            with ui.card().classes('card-glass'):
                ui.label("👤 Developer Profile").classes('text-base').style('font-weight:700;color:white;margin-bottom:15px;text-align:center;')
                
                with ui.column().classes('items-center').style('margin-bottom:15px;'):
                    profile_datauri = read_profile_image_datauri(PROFILE_IMAGE)
                    ui.html(f'<img src="{profile_datauri}" alt="profile" class="profile-img">')
                    ui.label(NAME).classes('text-lg').style('font-weight:700;color:white;margin-top:10px;text-align:center;')
                    ui.label(TITLE).classes('text-sm text-white/70').style('line-height:1.4;text-align:center;margin-top:5px;')
                
                ui.label("🌐 Connect with me:").classes('text-sm text-white/70').style('margin-bottom:10px;text-align:center;')
                with ui.row().classes('justify-center').style('flex-wrap:wrap;gap:8px;'):
                    for label, url, icon in LINKS:
                        ui.html(f'''
                            <a href="{url}" target="_blank" class="social-icon" title="{label}">
                                <i class="{icon}"></i>
                            </a>
                        ''')
            
            # Quick examples
            with ui.card().classes('card-glass'):
                ui.label("⚡ Quick Examples").classes('text-base').style('font-weight:700;color:white;margin-bottom:10px;')
                with ui.column().classes('gap-2'):
                    def set_example(v): 
                        text_input.value = v
                    ui.button("😊 Positive example", on_click=lambda:set_example("I absolutely love this product! The quality is outstanding and delivery was super fast. Highly recommend to everyone!")).classes('link-btn')
                    ui.button("😔 Negative example", on_click=lambda:set_example("Very disappointed with this purchase. The item arrived damaged and customer support was unhelpful and rude.")).classes('link-btn')
                    ui.button("😐 Neutral example", on_click=lambda:set_example("The meeting is scheduled for Monday at 10 AM in conference room B. Please confirm your attendance by Friday.")).classes('link-btn')
                    ui.button("📱 Social Media", on_click=lambda:set_example("Just watched an amazing movie! The cinematography was breathtaking but the plot felt a bit rushed. Overall worth watching! #MovieNight")).classes('link-btn')

            # Analysis history
            with ui.card().classes('card-glass'):
                with ui.row().classes('items-center justify-between'):
                    ui.label("📈 Analysis History").classes('text-base').style('font-weight:700;color:white;')
                    ui.button("🗑️", on_click=lambda: (analysis_history.clear(), refresh_history_list(), ui.notify("History cleared", type='warning'))).classes('btn-secondary').style('padding:4px 8px;font-size:12px;')
                history_list = ui.column().classes('gap-2').style('margin-top:8px;max-height:300px;overflow:auto;')

def refresh_history_list():
    history_list.clear()
    if not analysis_history:
        with history_list:
            ui.html('<div style="color:rgba(255,255,255,0.5);padding:12px;text-align:center;font-size:12px;">No analyses yet<br>Try the examples above!</div>')
        return
    
    for entry in reversed(analysis_history[-6:]):
        analysis_type = entry.get('type', 'quick')
        icon = '🧠' if analysis_type == 'deep_analysis' else '🔍'
        bg_color = 'rgba(139,92,246,0.1)' if analysis_type == 'deep_analysis' else 'rgba(255,255,255,0.03)'
        
        with history_list:
            with ui.row().classes('items-start gap-2').style(f'padding:8px;border-radius:8px;background:{bg_color};margin-bottom:6px;border-left:3px solid {"#8b5cf6" if analysis_type == "deep_analysis" else "#64748b"};'):
                ui.label(icon).style('font-size:14px;margin-top:2px;')
                with ui.column().classes('flex-1').style('min-width:0;'):
                    ui.label(entry['text'][:60] + ('...' if len(entry['text'])>60 else '')).classes('text-xs').style('font-weight:600;color:white;line-height:1.3;')
                    ui.label(f"{entry['sentiment']} • {entry['polarity']:.2f}").classes('text-xs text-white/60').style('margin-top:2px;')
                    ui.label(entry['timestamp'].split('T')[-1].split('.')[0]).classes('text-xs text-white/40').style('margin-top:1px;')

# Initialize history
refresh_history_list()

# Footer
ui.html(f'''
    <div class="footer">
        Built with ❤️ — {NAME} • <span style="opacity:.7">NiceGUI • TextBlob • Python</span>
    </div>
''')

# Run the app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Sentiment Reader — Senith", port=8080, reload=True)
