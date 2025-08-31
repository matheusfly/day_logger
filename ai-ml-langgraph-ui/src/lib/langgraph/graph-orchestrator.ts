import { SentimentAnalysisGraph, TextClassificationGraph, NERGraph, SummarizationGraph } from "./nlp-subgraphs";
import { NLPTask, LangGraphState, MLOpsMetrics } from "@/types/ai";

export class GraphOrchestrator {
  private graphs: Map<string, any> = new Map();
  private metrics: MLOpsMetrics[] = [];

  constructor() {
    this.initializeGraphs();
  }

  private initializeGraphs() {
    this.graphs.set("sentiment", new SentimentAnalysisGraph());
    this.graphs.set("classification", new TextClassificationGraph());
    this.graphs.set("extraction", new NERGraph());
    this.graphs.set("summarization", new SummarizationGraph());
  }

  async executeTask(task: NLPTask): Promise<NLPTask> {
    const startTime = Date.now();
    
    try {
      const graph = this.graphs.get(task.type);
      if (!graph) {
        throw new Error(`Unknown task type: ${task.type}`);
      }

      const compiledGraph = graph.compile();
      
      const initialState = {
        messages: [],
        currentTask: { ...task, status: "processing" as const },
        context: {},
        step: "start",
        isProcessing: true,
      };

      const result = await compiledGraph.invoke(initialState);
      
      const endTime = Date.now();
      const latency = endTime - startTime;

      // Record metrics
      this.recordMetrics({
        latency,
        throughput: 1000 / latency, // tasks per second
        errorRate: 0,
        accuracy: result.currentTask?.confidence,
      });

      return {
        ...task,
        output: result.currentTask?.output || "",
        status: result.currentTask?.status || "completed",
        confidence: result.currentTask?.confidence,
        metadata: {
          ...task.metadata,
          executionTime: latency,
          step: result.step,
          context: result.context,
        },
      };

    } catch (error) {
      const endTime = Date.now();
      const latency = endTime - startTime;

      // Record error metrics
      this.recordMetrics({
        latency,
        throughput: 0,
        errorRate: 1,
      });

      return {
        ...task,
        status: "error",
        metadata: {
          ...task.metadata,
          error: error instanceof Error ? error.message : "Unknown error",
          executionTime: latency,
        },
      };
    }
  }

  async executePipeline(tasks: NLPTask[]): Promise<NLPTask[]> {
    const results: NLPTask[] = [];
    
    for (const task of tasks) {
      const result = await this.executeTask(task);
      results.push(result);
      
      // If a task fails, we might want to stop the pipeline
      if (result.status === "error") {
        console.warn(`Task ${task.id} failed, continuing with pipeline...`);
      }
    }

    return results;
  }

  async executeParallelTasks(tasks: NLPTask[]): Promise<NLPTask[]> {
    const promises = tasks.map(task => this.executeTask(task));
    return Promise.all(promises);
  }

  getAvailableGraphs(): string[] {
    return Array.from(this.graphs.keys());
  }

  getMetrics(): MLOpsMetrics[] {
    return [...this.metrics];
  }

  getAggregatedMetrics(): MLOpsMetrics {
    if (this.metrics.length === 0) {
      return {
        latency: 0,
        throughput: 0,
        errorRate: 0,
      };
    }

    const sum = this.metrics.reduce(
      (acc, metric) => ({
        latency: acc.latency + metric.latency,
        throughput: acc.throughput + metric.throughput,
        errorRate: acc.errorRate + metric.errorRate,
        accuracy: (acc.accuracy || 0) + (metric.accuracy || 0),
      }),
      { latency: 0, throughput: 0, errorRate: 0, accuracy: 0 }
    );

    return {
      latency: sum.latency / this.metrics.length,
      throughput: sum.throughput / this.metrics.length,
      errorRate: sum.errorRate / this.metrics.length,
      accuracy: sum.accuracy / this.metrics.filter(m => m.accuracy).length,
    };
  }

  private recordMetrics(metrics: Partial<MLOpsMetrics>) {
    this.metrics.push({
      latency: metrics.latency || 0,
      throughput: metrics.throughput || 0,
      errorRate: metrics.errorRate || 0,
      accuracy: metrics.accuracy,
      precision: metrics.precision,
      recall: metrics.recall,
      f1Score: metrics.f1Score,
    });

    // Keep only last 1000 metrics to prevent memory issues
    if (this.metrics.length > 1000) {
      this.metrics = this.metrics.slice(-1000);
    }
  }

  clearMetrics() {
    this.metrics = [];
  }

  // Health check for all graphs
  async healthCheck(): Promise<Record<string, boolean>> {
    const health: Record<string, boolean> = {};
    
    for (const [name, graph] of this.graphs) {
      try {
        // Try to compile the graph
        graph.compile();
        health[name] = true;
      } catch (error) {
        console.error(`Health check failed for ${name}:`, error);
        health[name] = false;
      }
    }

    return health;
  }
}