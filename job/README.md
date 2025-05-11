# FIR-Assist: AI-Powered FIR Analysis Tool

An intelligent web application that helps police officers accurately identify relevant IPC sections and landmark judgments when filing First Information Reports (FIRs).

## Features

- Text and voice input for incident narratives
- AI-powered analysis using Legal-BERT
- Automatic IPC section recommendations with confidence scores
- Related landmark judgments with synopses
- Completely local deployment with Docker

## Tech Stack

- Frontend: React + Tailwind CSS
- Backend: Node.js + Express.js
- Database: MongoDB
- NLP Model: HuggingFace "nlpaueb/legal-bert-base-uncased"
- Speech-to-Text: Vosk
- Containerization: Docker

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Git

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fir-assist
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Development Setup

1. Install dependencies:
   ```bash
   # Backend
   cd backend
   npm install

   # Frontend
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   
   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. Start development servers:
   ```bash
   # Backend
   cd backend
   npm run dev

   # Frontend
   cd frontend
   npm start
   ```

## Project Structure

```
fir-assist/
├── frontend/           # React + Tailwind CSS application
├── backend/           # Node.js + Express API
├── docker-compose.yml # Docker configuration
└── README.md         # Project documentation
```

## API Documentation

### POST /api/analyze

Analyzes an incident narrative and returns relevant IPC sections and judgments.

**Request:**
```json
{
  "narrative": "string"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "code": "IPC 378",
      "title": "Theft",
      "description": "Dishonest removal of movable property",
      "score": 0.93,
      "judgments": [
        {
          "caseName": "State v. Kumar",
          "synopsis": "..."
        }
      ]
    }
  ]
}
```

## License

MIT 