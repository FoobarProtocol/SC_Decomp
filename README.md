# SC_Decomp
Smart Contract Prompt Decomposition
## Sapper IDE

Sapper IDE is a web-based integrated development environment (IDE) designed to facilitate the creation, management, and deployment of AI services. It leverages the power of AI models such as GPT series and DALL-E, and provides a user-friendly interface for users to interact with these models.

### Features

#### Project Management

Users can create, open, or save AI chain projects. The backend Python code for the AI chain can be downloaded and integrated into other software projects. The IDE also plans to implement a one-click sharing feature for sharing AI chain projects to the AI chain marketplace, as well as deploying AI services to cloud servers.

#### Design View

Users can specify what they want to build. The co-pilot will discuss with the user to clarify and enrich initial ideas, turning them into specific AI service requirements. The co-pilot will also automatically generate an AI chain skeleton based on the AI service requirements.

#### Exploration View

Users can freely chat with the GPT inside the IDE to acquire task knowledge, identify task challenges, and experiment prompts. The co-pilot will summarize the user's interested tasks, preferences, and special considerations.

#### Engine Management

Users can configure and manage the engines used by workers, including foundation models, traditional ML models, external data sources, or APIs. The IDE has pre-installed large language models (GPT series) and text-to-image models (DALL-E).

### Dependencies

The project uses several dependencies including:

- Express.js for server-side operations
- Body-parser for parsing incoming request bodies
- Dotenv for environment variable management
- fs for file system operations
- highlight.js for syntax highlighting
- node-fetch for making HTTP requests
- openai for interacting with the OpenAI API
- path for handling and transforming file paths

#### Usage

The project can be started by running the app.js file, which sets up an Express server and handles various routes for interacting with the AI models and managing projects.

```javascript
app.listen(3333, function (){
    console.log('visit http://localhost:3333/')
})
```

### Conclusion

Sapper IDE is a powerful tool for AI service development, providing a user-friendly interface for interacting with advanced AI models and managing AI projects. It is designed to make AI service development accessible to everyone, regardless of their technical background. 