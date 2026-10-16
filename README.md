# Intent Chatbot

A desktop chatbot built with **Python**, **PyQt6**, and **Sentence Transformers**. The application uses semantic similarity to find the most relevant question in a locally stored knowledge base and returns its associated answer.

Unlike generative chatbots, this project retrieves existing answers instead of generating new ones from scratch.

## Features

- **PyQt6 graphical interface** with Chat Room, Register Q&A, and Questions & Answers tabs.
- **Semantic question matching** using the `all-MiniLM-L6-v2` sentence embedding model.
- **Local model storage** to avoid downloading the model every time the application starts.
- **JSON persistence** for questions, answers, and embeddings.
- **Knowledge-base management** to register, edit, browse, and delete entries.
- **Configurable similarity threshold** to control whether a match is accepted.
- **Formatted chat interface** with separate message frames for the user and assistant.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PyQt6 | Desktop graphical interface |
| Sentence Transformers | Sentence embedding generation |
| all-MiniLM-L6-v2 | Converts questions into numerical vectors |
| PyTorch | Model inference and tensor operations |
| JSON | Persistent storage of questions, answers, and embeddings |

## Project Structure

```text
ChatBot/
├── main.py
├── requirements.txt
├── DB/
│   ├── Question.json
│   └── AnswerEmbed.json
├── models/
│   └── all-MiniLM-L6-v2/
├── Model/
│   ├── Question.py
│   └── AnswerEmbed.py
├── Service/
│   ├── ChatService.py
│   ├── ModelDownloader.py
│   └── RegisterService.py   
└── View/
    ├── MainView.py
    ├── ChatView.py
    ├── RegisterView.py
    └── QuestionsView.py
```

### Main components

- **`main.py`** — Application entry point. Initializes the GUI and opens the main window.
- **`ModelDownloader.py`** — Checks and loads the local sentence embedding model, downloading and saving it when necessary.
- **`Model/Question.py`** — Manages question records and their persistence in `Question.json`.
- **`Model/AnswerEmbed.py`** — Manages answers, question embeddings, and their persistence in `AnswerEmbed.json`.
- **`Service/ChatService.py`** — Encodes incoming questions, calculates similarity scores, and retrieves matching answers.
- **`Service/RegisterService.py`** — Handles registration of question-and-answer entries and embedding generation.
- **`View/MainView.py`** — Main application window and tab management.
- **`View/ChatView.py`** — Chat interface and message display.
- **`View/RegisterView.py`** — Interface for adding question-and-answer entries.
- **`View/QuestionsView.py`** — Interface for browsing, editing, and deleting knowledge-base entries.

## Data Structure

The knowledge base is divided into two JSON files. The records are linked through a shared `QuestionId`.

### 1. `DB/Question.json`

This file stores the registered questions.

Each record contains:

| Field | Type | Description |
|---|---|---|
| `QuestionId` | Integer | Unique identifier for a question |
| `Text` | String | The text of the question |

Example:

```json
[
  {
    "QuestionId": 1,
    "Text": "What is drip irrigation?"
  },
  {
    "QuestionId": 2,
    "Text": "How often should tomato plants be watered?"
  }
]
```

### 2. `DB/AnswerEmbed.json`

This file stores the answer associated with each question and the numerical embedding generated from that question.

Each record contains:

| Field | Type | Description |
|---|---|---|
| `QuestionId` | Integer | Links the record to its question |
| `Text` | String | The answer returned by the chatbot |
| `Questionembedding` | Array of numbers | The embedding generated from the associated question |

Example structure:

```json
[
  {
    "QuestionId": 1,
    "Text": "Drip irrigation delivers water directly to the plant root zone.",
    "Questionembedding": [0.012, -0.084, 0.031]
  }
]
```

**Note:** The embedding values above are illustrative only. The actual `all-MiniLM-L6-v2` model generates a vector containing **384 numerical values**. The complete vector must be stored for actual inference.

### Relationship between the files

```text
Question.json
    |
    | QuestionId = 1
    | Text = "What is drip irrigation?"
    |
    v
AnswerEmbed.json
    |
    | QuestionId = 1
    | Text = "Drip irrigation delivers water directly
    |        to the plant root zone."
    | Questionembedding = [384 numerical values]
    |
    v
    Used for semantic question matching
```

The `QuestionId` acts as the link between the question and its answer. When retrieving an answer, the application uses the matching question ID to locate the associated answer and embedding record.

### Why are the questions and answers separated?

This structure separates the question catalog from the answer and embedding data.

- `Question.json` contains the question text and identifier.
- `AnswerEmbed.json` contains the response and the vector used for semantic matching.
- `QuestionId` connects the two files.

When a question is edited, its embedding must be regenerated to reflect the new question text. When an entry is deleted, its records must be removed from both files.

Both files should remain consistent. A question without a corresponding answer record cannot provide a normal response, and an answer record without a valid question ID is an orphaned record.

## How Semantic Retrieval Works

The chatbot follows a retrieval pipeline:

1. The user enters a question.
2. `ChatService` converts the input into an embedding using `all-MiniLM-L6-v2`.
3. The query embedding is compared against the stored question embeddings.
4. The application selects the entry with the highest similarity score.
5. The score is compared with the configured acceptance threshold.
6. If the score meets the threshold, the associated answer is returned. Otherwise, the chatbot reports that no sufficiently similar answer was found.

The model produces **384-dimensional embeddings**. When embeddings are normalized, cosine similarity can be calculated using the dot product of two vectors.

The default acceptance threshold is `0.60`. This value can be adjusted in the chat interface. A higher threshold generally makes matching stricter, while a lower threshold accepts more loosely related questions.

The threshold should be tuned using representative questions and incorrect-match examples from the intended domain.

## Installation

### Requirements

The current environment uses the following package versions:

```text
PyQt6==6.11.0
sentence-transformers==6.1.0
torch==2.14.1
transformers==5.19.0
numpy==2.2.6
scikit-learn==1.7.2
scipy==1.15.3
huggingface_hub==1.33.0
tokenizers==0.23.3
safetensors==0.8.0
```

These versions reflect the existing Python environment. Compatibility with other Python versions and operating systems should be verified before deployment. Some packages may be transitive dependencies rather than direct imports.

### Setup

1. Install Python.
2. Open a terminal in the project directory.
3. Install the requirements:

```bash
python -m pip install -r requirements.txt
```

4. Launch the application:

```bash
python main.py
```

The first model setup may require an internet connection to download `all-MiniLM-L6-v2`. The model setup code saves it under `models/all-MiniLM-L6-v2/` for subsequent local loading.

## Using the Application

### Chat Room

- Enter a question and press **Send** or Enter.
- Adjust the similarity threshold to control the acceptance score.
- Review the retrieved answer and matching metadata, including similarity score and question ID.

### Register Q&A

Add new questions and their corresponding answers to the knowledge base. The registration service should generate and save an embedding for each question.

### Questions & Answers

Browse existing entries, edit their questions or answers, refresh the table, and delete entries. Editing a question requires updating its stored embedding so future searches use the modified text.

## Data Integrity and Maintenance

- **Persistent storage:** Ensure that save operations write to the intended `DB/` directory. Prefer paths derived from the project location instead of relying on the terminal's current working directory.
- **Consistent IDs:** Keep `QuestionId` values consistent between the two JSON files.
- **Embedding consistency:** Use the same embedding model and normalization settings for registration and query processing.
- **Backups:** Back up both JSON files before bulk changes or deletion.
- **Valid JSON:** Keep both files valid JSON. Avoid manually editing them while the application is running.
- **Duplicate records:** Ensure that updating an existing question replaces its associated answer/embedding record instead of creating duplicates.
- **Error handling:** If saving one JSON file succeeds but saving the other fails, the files may become inconsistent. Stronger persistence logic should handle failures and validate records.

## Limitations

- The chatbot retrieves stored answers; it does not independently generate new answers.
- Matching quality depends on the questions and answers registered in the knowledge base.
- A basic embedding scan compares the input against stored vectors, so search time increases as the knowledge base grows.
- JSON files are simple and portable but do not provide database transactions or concurrent-write protection.
- Running model inference synchronously in the GUI thread can temporarily freeze the interface during slow operations.

## Suggested `.gitignore`

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.env

# Downloaded model files
models/all-MiniLM-L6-v2/
```

Keep the JSON files in version control if they are intended to be part of the distributed starter knowledge base. If they contain private or user-specific data, exclude them and provide clean sample files instead.

icone from Flaticon
link:https://www.flaticon.com/free-icons/robot

## License

Add a license for this project's original code if you intend to distribute it. Review the licenses and terms of the Sentence Transformers model and its dependencies separately.



