# AI/ML LangGraph UI - Complete Setup Guide

## 🚀 Quick Start

This project provides a complete structure for running AI/ML operations with NLP LangGraph subgraphs using ShadCN UI components.

### Prerequisites
- Node.js 18+ and npm
- Modern web browser

### Installation & Run

```bash
# Navigate to the project directory
cd ai-ml-langgraph-ui

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:3000
```

## 📁 Project Structure

```
ai-ml-langgraph-ui/
├── src/
│   ├── app/
│   │   ├── page.tsx                 # Main application page
│   │   └── globals.css              # Global styles with ShadCN theme
│   ├── components/
│   │   ├── ui/                      # ShadCN UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── tabs.tsx
│   │   │   └── ...
│   │   └── ai/                      # AI-specific components
│   │       ├── nlp-task-form.tsx    # Task creation form
│   │       ├── task-results.tsx     # Results display
│   │       └── metrics-dashboard.tsx # Performance metrics
│   ├── lib/
│   │   ├── langgraph/               # LangGraph implementation
│   │   │   ├── base-graph.ts        # Base graph class
│   │   │   ├── nlp-subgraphs.ts     # NLP subgraph implementations
│   │   │   ├── graph-orchestrator.ts # Task orchestration
│   │   │   └── index.ts
│   │   ├── mock-orchestrator.ts     # Mock implementation for demo
│   │   └── utils.ts                 # Utility functions
│   └── types/
│       └── ai.ts                    # TypeScript definitions
├── components.json                  # ShadCN UI configuration
├── tailwind.config.ts               # Tailwind CSS configuration
├── .env.example                     # Environment variables template
└── README.md                        # Comprehensive documentation
```

## 🎯 Features Implemented

### ✅ Core Components
- [x] Next.js 15 with App Router
- [x] TypeScript configuration
- [x] ShadCN UI components with Tailwind CSS
- [x] Responsive design system
- [x] Dark/light mode ready

### ✅ AI/ML Infrastructure
- [x] LangGraph subgraph architecture
- [x] NLP task types: sentiment, classification, extraction, summarization, translation
- [x] Task orchestration system
- [x] Performance metrics collection
- [x] Real-time monitoring dashboard

### ✅ UI Components
- [x] Task creation form with validation
- [x] Results display with confidence scores
- [x] Metrics dashboard with health indicators
- [x] Tabbed interface for organization
- [x] Loading states and error handling

### ✅ Mock Implementation
- [x] Fully functional mock orchestrator
- [x] Simulated processing delays
- [x] Realistic confidence scores
- [x] Error simulation capabilities

## 🔧 Usage Instructions

### Creating NLP Tasks

1. **Navigate to NLP Tasks tab**
2. **Select task type** from dropdown:
   - Sentiment Analysis
   - Text Classification  
   - Named Entity Recognition
   - Text Summarization
   - Translation

3. **Enter input text** in the textarea
4. **Click "Create Task"** to process

### Viewing Results

1. **Switch to Results tab** to see all processed tasks
2. **View confidence scores** and execution metadata
3. **See task status** (pending, processing, completed, error)
4. **Expand details** for comprehensive information

### Monitoring Performance

1. **Go to Metrics tab** for performance dashboard
2. **View key metrics**: latency, throughput, error rate, accuracy
3. **Monitor system health** with real-time indicators
4. **Track trends** over time

## 🛠 Development Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking
```

## 🔄 Switching to Real LangGraph

The current implementation uses a mock orchestrator for demonstration. To integrate with real LangGraph:

1. **Install LangGraph dependencies**:
   ```bash
   npm install @langchain/langgraph @langchain/core @langchain/openai
   ```

2. **Update the import in `src/app/page.tsx`**:
   ```typescript
   // Change from:
   import { MockOrchestrator } from "@/lib/mock-orchestrator";
   
   // To:
   import { GraphOrchestrator } from "@/lib/langgraph/graph-orchestrator";
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env.local
   # Add your API keys
   ```

4. **Update orchestrator instantiation**:
   ```typescript
   const [orchestrator] = useState(() => new GraphOrchestrator());
   ```

## 🎨 Customization

### Adding New Task Types

1. **Add to types** in `src/types/ai.ts`
2. **Create subgraph** in `src/lib/langgraph/nlp-subgraphs.ts`
3. **Update orchestrator** in `graph-orchestrator.ts`
4. **Add UI support** in form and results components

### Styling Modifications

- **Colors**: Edit CSS variables in `globals.css`
- **Components**: Modify ShadCN components in `components/ui/`
- **Layout**: Update main page in `src/app/page.tsx`

### Performance Metrics

- **Add metrics**: Extend `MLOpsMetrics` interface
- **Update dashboard**: Modify `metrics-dashboard.tsx`
- **Custom visualizations**: Add charting libraries

## 🚨 Troubleshooting

### Common Issues

1. **Build Errors**: Check TypeScript types and imports
2. **Styling Issues**: Verify Tailwind configuration
3. **Module Resolution**: Ensure path aliases in `tsconfig.json`
4. **Performance**: Monitor bundle size and optimize imports

### Getting Help

- Check the comprehensive README.md
- Review component implementations
- Test with mock data first
- Verify environment configuration

## 🎉 Success Indicators

You'll know everything is working when:

- [x] Application loads at http://localhost:3000
- [x] All three tabs (Tasks, Results, Metrics) are functional
- [x] Task creation form accepts input and processes requests
- [x] Results display with proper formatting and confidence scores
- [x] Metrics dashboard shows performance data
- [x] No console errors in browser developer tools

## 🔮 Next Steps

1. **Integrate real AI models** for production use
2. **Add data persistence** with database integration
3. **Implement user authentication** and multi-tenancy
4. **Add advanced visualizations** with charting libraries
5. **Deploy to production** with proper CI/CD pipeline
6. **Scale with microservices** architecture
7. **Add comprehensive testing** suite
8. **Implement monitoring** and alerting systems

---

**Ready to enhance your AI/ML operations! 🚀**