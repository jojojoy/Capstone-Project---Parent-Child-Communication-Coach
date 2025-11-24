# Parent–Child Communication Coach 👨‍👩‍👧‍👦  

An AI-powered agent that helps parents respond to their children with empathy, clarity, and emotional insight.

This project was created as part of the **Google Agents Intensive – Capstone Project (Nov 2025)**.  
It demonstrates how AI agents can support real-world interpersonal challenges—in this case, helping parents navigate emotionally charged conversations with their kids.

---

## 🌟 Overview

Many parents want to communicate with empathy, especially with teenagers, but struggle in the moment.  
The **Parent–Child Communication Coach** uses multi-step reasoning to:

- Analyze the child’s emotional state  
- Identify underlying needs  
- Suggest three empathetic, non-escalating parent responses  
- Provide coaching tips on *why* these responses work  

This turns the agent into a real-time “parenting co-pilot” during difficult conversations.

---

## 🧠 Architecture

The agent is built using **Gemini 2.0 Flash + Agent Developer Kit (ADK)** and consists of three custom actions:

### 1. `AnalyzeEmotionAction`
Extracts:

- Emotional tone  
- Stress signals  
- Behavioral context  
- Underlying needs  

### 2. `GenerateResponsesAction`
Generates three:

- Empathetic  
- Non-judgmental  
- Age-appropriate  

parent responses.

### 3. `CoachingTipsAction`
Provides:

- Emotional reasoning  
- Parenting strategies  
- Mistakes to avoid  
- Age-specific guidance  

These actions return structured JSON, which is combined into the final agent output.

---

## 🧩 Project Structure

_Example structure (you can adjust to match your actual files):_

```text
Capstone-Project---Parent-Child-Communication-Coach/
│
├── actions/
│   ├── analyze_emotion.py
│   ├── generate_responses.py
│   └── coaching_tips.py
│
├── agent.py          # ADK agent definition
├── main.py           # Entry point / simple CLI or notebook runner
└── README.md

