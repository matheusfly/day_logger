// AI/ML Types for LangGraph Operations
export interface AIMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface NLPTask {
  id: string;
  type: 'sentiment' | 'classification' | 'extraction' | 'summarization' | 'translation';
  input: string;
  output?: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  confidence?: number;
  metadata?: Record<string, any>;
}

export interface LangGraphState {
  messages: AIMessage[];
  currentTask?: NLPTask;
  context: Record<string, any>;
  step: string;
  isProcessing: boolean;
}

export interface SubgraphConfig {
  name: string;
  description: string;
  inputs: string[];
  outputs: string[];
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface GraphNode {
  id: string;
  type: 'llm' | 'tool' | 'condition' | 'human';
  name: string;
  config: Record<string, any>;
}

export interface GraphEdge {
  source: string;
  target: string;
  condition?: string;
}

export interface MLOpsMetrics {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1Score?: number;
  latency: number;
  throughput: number;
  errorRate: number;
}