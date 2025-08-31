# AI/ML Operations with LangGraph and ShadCN UI

A complete structure for running AI/ML operations with NLP LangGraph subgraphs using ShadCN UI components.

## Features

### 🧠 LangGraph Subgraphs
- **Sentiment Analysis**: Analyze emotional tone in text
- **Text Classification**: Categorize text into predefined classes  
- **Named Entity Recognition**: Extract entities and key information
- **Text Summarization**: Generate concise summaries
- **Translation**: Multi-language text translation

### 🎨 Modern UI Components
- Built with ShadCN UI and Tailwind CSS
- Responsive design for all screen sizes
- Real-time task monitoring and results
- Interactive metrics dashboard
- Dark/light mode support

### 📊 ML Operations Features
- Real-time performance metrics
- Task orchestration and pipeline management
- Error handling and retry mechanisms
- Health monitoring and alerting
- Persistent task history

## Project Structure

```
src/
├── app/                    # Next.js app router
│   └── page.tsx           # Main application page
├── components/
│   ├── ui/                # ShadCN UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── tabs.tsx
│   │   └── ...
│   └── ai/                # AI-specific components
│       ├── nlp-task-form.tsx
│       ├── task-results.tsx
│       └── metrics-dashboard.tsx
├── lib/
│   ├── langgraph/         # LangGraph implementation
│   │   ├── base-graph.ts
│   │   ├── nlp-subgraphs.ts
│   │   ├── graph-orchestrator.ts
│   │   └── index.ts
│   └── utils.ts           # Utility functions
└── types/
    └── ai.ts              # TypeScript type definitions
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- OpenAI API key (optional, for enhanced models)
- Python 3.8+ (for LangGraph backend)

### Installation

1. **Clone and setup the project:**
   ```bash
   cd ai-ml-langgraph-ui
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Creating NLP Tasks

1. **Select Task Type**: Choose from sentiment analysis, classification, entity extraction, summarization, or translation
2. **Enter Input Text**: Provide the text you want to process
3. **Submit Task**: The LangGraph orchestrator will process your request using the appropriate subgraph
4. **View Results**: See real-time results with confidence scores and metadata

### Monitoring Performance

- **Metrics Dashboard**: View real-time performance metrics including latency, throughput, and accuracy
- **Task History**: Track all processed tasks with detailed execution information
- **Health Checks**: Monitor the status of all LangGraph subgraphs

### Available Subgraphs

#### Sentiment Analysis Graph
- **Input**: Any text string
- **Output**: Sentiment classification (positive/negative/neutral) with confidence score
- **Use Cases**: Social media monitoring, customer feedback analysis, content moderation

#### Text Classification Graph  
- **Input**: Text to categorize
- **Output**: Category label with confidence score
- **Use Cases**: Document organization, spam detection, content routing

#### Named Entity Recognition Graph
- **Input**: Text containing entities
- **Output**: Extracted entities with labels (PERSON, ORG, LOC, etc.)
- **Use Cases**: Information extraction, knowledge graph construction, data enrichment

#### Summarization Graph
- **Input**: Long-form text
- **Output**: Concise summary
- **Use Cases**: Document summarization, news article condensation, research paper abstracts

#### Translation Graph
- **Input**: Text in source language
- **Output**: Translated text in target language
- **Use Cases**: Multilingual content creation, document translation, communication assistance

## Architecture

### LangGraph Integration

The application uses LangGraph to create sophisticated AI workflows:

```typescript
// Example: Creating a custom subgraph
export class CustomNLPGraph extends BaseLangGraph {
  protected setupGraph(): void {
    this.graph.addNode("preprocess", this.preprocess.bind(this));
    this.graph.addNode("analyze", this.analyze.bind(this));
    this.graph.addNode("postprocess", this.postprocess.bind(this));
    
    this.graph.addEdge(START, "preprocess");
    this.graph.addEdge("preprocess", "analyze");
    this.graph.addEdge("analyze", "postprocess");
    this.graph.addEdge("postprocess", END);
  }
  
  private async preprocess(state: any) { /* ... */ }
  private async analyze(state: any) { /* ... */ }
  private async postprocess(state: any) { /* ... */ }
}
```

### Component Architecture

- **Separation of Concerns**: UI components are separated from business logic
- **Type Safety**: Full TypeScript support with comprehensive type definitions
- **Reusability**: Modular components that can be easily extended
- **Performance**: Optimized rendering with React best practices

### State Management

- **Local State**: React hooks for component-level state
- **Persistent Storage**: LocalStorage for task history
- **Real-time Updates**: Live metrics and status updates

## Customization

### Adding New Task Types

1. **Create a new subgraph** in `src/lib/langgraph/nlp-subgraphs.ts`
2. **Add the task type** to `src/types/ai.ts`
3. **Update the orchestrator** in `graph-orchestrator.ts`
4. **Add UI support** in the task form and results components

### Styling and Theming

The application uses Tailwind CSS with CSS variables for theming:

```css
:root {
  --primary: 221.2 83.2% 53.3%;
  --secondary: 210 40% 96%;
  --accent: 210 40% 96%;
  /* ... more variables */
}
```

### Adding Metrics

Extend the `MLOpsMetrics` interface and update the metrics dashboard:

```typescript
interface CustomMetrics extends MLOpsMetrics {
  customMetric: number;
  anotherMetric: string;
}
```

## Deployment

### Production Build

```bash
npm run build
npm start
```

### Docker Deployment

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables

Required for production:
- `OPENAI_API_KEY`: For enhanced LLM capabilities
- `DATABASE_URL`: For persistent storage
- `NEXT_PUBLIC_API_URL`: API endpoint configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the example implementations in `/examples`

## Roadmap

- [ ] Integration with external ML models
- [ ] Advanced visualization components
- [ ] Batch processing capabilities
- [ ] API endpoint generation
- [ ] Plugin system for custom subgraphs
- [ ] Performance optimization tools
- [ ] Multi-tenant support
- [ ] Advanced security features