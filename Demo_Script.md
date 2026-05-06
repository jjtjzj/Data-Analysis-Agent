# 🎥 2-Minute Demo Strategy: Titanic Dataset

This plan is optimized to hit all the rubrics for your COMPSCI 767 assignment.

---

## ⏱️ Timeline & Script

### 1. Introduction (0:00 - 0:15)
*   **Visual**: Show the Streamlit dashboard home page.
*   **Action**: Upload `titanic.csv`.
*   **Narrative**: "Hi! This is my **Agentic Data Analyst**. Unlike a standard chatbot, this system uses a formal ReAct loop to reason through data problems, execute code in a secure sandbox, and autonomously correct its own mistakes."

### 2. Goal-Directed Reasoning & Tool Use (0:15 - 0:45)
*   **Input**: Ask: *"Who were the 5 oldest passengers that survived?"*
*   **Action**: Zoom in on the **Agent Reasoning** panel while it works.
*   **Narrative**: "I'll start with a specific query. Watch the **Thought** process: the agent identifies that it needs to filter for 'Survived' equals 1 and sort by 'Age'. It then uses its **Python Tool** to execute code. This demonstrates meaningful tool interaction and multi-step planning."

### 3. Visualization & Final Polish (0:45 - 1:15)
*   **Input**: Ask: *"Plot the survival rate by passenger class (Pclass)."*
*   **Visual**: Show the **Status** bar ("Agent is analyzing and plotting...") and the final **plot.png**.
*   **Narrative**: "Now, a more complex task. The agent realizes a bar chart is appropriate here. It groups the data, calculates the mean, and generates a plot. My system intercepts the matplotlib output to render the chart directly in the UI, providing a seamless user experience."

### 4. The "Wow" Factor: Self-Correction (1:15 - 1:45)
*   **Scenario**: Force a mistake. Ask: *"What's the average fare for each Gender?"* (The column is actually `Sex`, not `Gender`).
*   **Visual**: Show the **Red Error Log** followed by the **Blue Correction Attempt**.
*   **Narrative**: "This is where the agent truly shines. I used the word 'Gender,' but the column is named 'Sex.' The agent hits a `KeyError`, but instead of giving up, it analyzes the traceback, realizes the mistake, and **autonomously corrects** its code. This is a core agentic behavior: self-correction through environmental feedback."

### 5. Conclusion & Architecture (1:45 - 2:00)
*   **Visual**: Quickly show the **Sidebar Metrics** and the **Reset** button.
*   **Narrative**: "The system is technically sound, featuring a secure execution sandbox and a transparent reasoning log. It provides professional data insights through a goal-oriented reasoning loop. Thanks for watching my demo!"

---

## 💡 Pro-Tips for the Video:
1.  **Preparation**: Have the Titanic CSV ready on your desktop so the upload is fast.
2.  **Zooming**: Use a screen recording tool (like OBS or Loom) that lets you zoom into the **Agent Reasoning** panel—this is where your "Agentic Behavior" grade (25%) comes from!
3.  **Explanation**: Don't just read the answers; explain *why* it's an agent (e.g., "It's using the ReAct pattern").
4.  **Reproduction**: Mention that the full code and reproduction instructions are available in the GitHub README you just updated.

**Would you like me to help you find a sample Titanic dataset to test this with?**
