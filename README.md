
**FIR-Assist**
*AI-powered First Information Report assistant for Indian police stations*
 
FIR-Assist streamlines and fortifies the FIR-filing process by automatically recommending the most relevant IPC (Indian Penal Code) sections and landmark judgments—eliminating manual search, reducing errors, and speeding up investigations.

FIR-Assist supports **dual input modes** to accommodate different user preferences and real-world constraints in police stations. Users can either **type the incident narrative** directly into a simple textarea or use the **voice input feature**, where a “Record” button captures spoken narratives and transcribes them in real time using an open-source speech-to-text engine like Vosk or Whisper. This flexibility ensures the system is accessible even in time-pressured or hands-free scenarios.

Once the narrative is captured, the **backend processes it using Legal-BERT**, a specialized legal variant of BERT from HuggingFace. The model performs **multi-label classification** to predict the **top five most relevant IPC sections**, each accompanied by a **confidence score** ranging from 0 to 1. These predictions are used to query the MongoDB database, which stores detailed metadata for IPC sections and associated legal judgments.

The output includes the **IPC section code**, **title**, a concise **one-line description**, and a **confidence score** indicating the model’s certainty. Additionally, the system surfaces **1–2 landmark judgments** related to each predicted section, along with **brief synopses** to provide context and legal precedence. This helps officers ensure completeness and legal accuracy in FIRs without the need to manually browse through legal texts.

Behind the scenes, FIR-Assist handles **text preprocessing and tokenization** to prepare narratives for the model. Although the current version uses a pretrained model out of the box, the codebase includes a **placeholder for future fine-tuning**, enabling adaptation to real-world FIR data and improving performance over time.

**👨‍💻 Developer Workflow**

1. Clone repo
2. `npm install` in `frontend/` & `backend/`
3. `npm run dev` in both
4. `npm run seed` to populate MongoDB
5. `docker-compose up` (UI, API & MongoDB spin up)
6. Visit `http://localhost:3000` & test

