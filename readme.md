CareerLM
==========

How to Run
------------

### Frontend (React)

1. Install Node.js (if you haven't already) from <https://nodejs.org/en/download/>
2. Install Yarn by running `npm install -g yarn`
3. Go to the `frontend-react` directory and run `yarn install`
4. Run `yarn start` to start the development server
5. Open `http://localhost:3000` in your browser to see the app in action

### Backend (FastAPI)

1. Install Docker from <https://www.docker.com/get-started>
2. Go to the `backend-fastapi` directory and run `docker-compose up`
3. Open `http://localhost:8000/docs` in your browser to see the API documentation

### Running the Full Application

1. Follow the instructions above to run both the frontend and backend
2. The frontend will make requests to the backend to optimize resumes
3. The backend will run the Ollama API to generate alignment suggestions based on the resume and job description
