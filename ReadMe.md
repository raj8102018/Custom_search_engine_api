# Web Search API 
 **Google Search & Sorting:**  
  Performs a Google search using the Custom Search API and then processes and sorts the results with criteria focused on water-related topics. The sorting workflow uses langchain, an LLM (ChatGoogleGenerativeAI), and custom prompt templates to filter and prioritize search results.

## Project Structure

- **app.py:**  
  The main FastAPI application that defines two endpoints:
  - `/search` for executing Google searches and sorting the results.

- **search_app.py:**  
  Implements the workflow for performing a Google search using the Custom Search API, parsing search results, and sorting them based on predefined water-related criteria.

- **requirements.txt:**  
  Lists all Python dependencies required to run the project.

- **docker-compose.yml:**  
  Contains the Docker Compose configuration to containerize and deploy the application.

- **.gitignore & .dockerignore:**  
  Specify files and directories to be excluded from version control and Docker builds.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (if you prefer containerized deployment)

### Setup

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv my_env
   source my_env/bin/activate    # On Windows use: my_env\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the project root and add the following variables with your respective API keys and IDs:

   ```env
   api_key=your_google_api_key
   search_engine_id=your_search_engine_id
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Running the Application

### Locally with Uvicorn

Start the FastAPI application using Uvicorn:

```bash
uvicorn app:app --reload
```

Access the application at [http://localhost:8000](http://localhost:8000).

### Using Docker

1. **Build and Run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

2. The application will be accessible on port 8000.

## API Endpoints

### 1. Google Search

- **URL:** `/search`
- **Method:** POST
- **Payload Example:**

  ```json
  {
      "query": "Chennai"
  }
  ```

- **Response:**  
  A JSON object with sorted search results relevant to groundwater and water management topics.

## Contributing

Contributions are welcome! Please open issues or submit pull requests to help improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For further questions or support, please open an issue in the repository or contact the maintainers.

---

This README provides all the necessary instructions to set up, run, and contribute to the SmartBhujal Backend project. Enjoy building and enhancing your water management solutions!