# ✨ LLM-based-post-generator ✨

## Vibe Check: What's This?
This tool is your LinkedIn content bestie! It analyzes an influencer's LinkedIn posts and helps create fire new content that matches their unique style. No more staring at a blank screen wondering what to post!

Imagine: Your fave LinkedIn creator needs fresh content but doesn't have the mental bandwidth. They can just feed their past bangers into this tool, pick a topic, and boom! A new post that sounds exactly like them is ready to drop.

<img src="assets/Screenshot 2025-05-18 175243.png"/>
<img src="assets/Screenshot 2025-05-18 175316.png"/>

## High Level Architecture
```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                             │
│                                                                         │
│  ┌───────────────┐           ┌───────────────┐      ┌───────────────┐   │
│  │ INPUT:        │           │ PARAMETERS:   │      │ OUTPUT:       │   │
│  │ LinkedIn Posts│           │ Topic         │      │ Generated     │   │
│  │ Text Data     │           │ Language      │      │ LinkedIn      │   │
│  │               │           │ Length        │      │ Post          │   │
│  └───────┬───────┘           └───────┬───────┘      └───────▲───────┘   │
│          │                           │                      │           │
└──────────┼───────────────────────────┼──────────────────────┼───────────┘
           │                           │                      │
           ▼                           │                      │
┌──────────────────────┐               │                      │
│                      │               │                      │
│  STAGE 1: ANALYSIS   │               │                      │
│  ┌──────────────────┐│               │                      │
│  │ Topic Extraction ││               │                      │
│  │ Style Analysis   ││               │                      │
│  │ Content Patterns ││               │                      │
│  └──────────────────┘│               │                      │
│                      │               │                      │
└──────────┬───────────┘               │                      │
           │                           │                      │
           ▼                           ▼                      │
┌──────────────────────────────────────────────────┐          │
│                                                  │          │
│              STAGE 2: GENERATION                 │          │
│  ┌───────────────────────────────────────────┐   │          │
│  │            GROQ LLM API                   │   │          │
│  │  ┌─────────────────────────────────────┐  │   │          │
│  │  │     Few-Shot Learning Process       │  │   │          │
│  │  │                                     │  │   │          │
│  │  │  1. Similar Post Selection          │  │   │          │
│  │  │  2. Style Matching                  │  │   │          │
│  │  │  3. Content Generation              │──┼───┼──────────┘
│  │  │                                     │  │   │
│  │  └─────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

## How It Works (The Tech Tea)

### Stage 1: Content Harvesting 🌱
- Collects existing LinkedIn posts
- Extracts key info: Topic, Language, Length, etc.
- Builds a vibe profile of their content

### Stage 2: Content Generation 🚀
- Takes your selected topic, language and length
- Uses similar past posts for style guidance
- Generates a new post that sounds authentically like the original creator

## Getting Started

### Step 1: API Setup
Grab your API key from [Groq](https://console.groq.com/keys) and update the `.env` file with your `GROQ_API_KEY`.

### Step 2: Install the Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the App
```bash
streamlit run main.py
```

### Step 4: Create Content That Slaps

---

Developed by Pramod Baviskar
