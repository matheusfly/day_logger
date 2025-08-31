import { NLPTask, MLOpsMetrics } from "@/types/ai";

export class MockOrchestrator {
  private metrics: MLOpsMetrics[] = [];

  constructor() {
    // Initialize with some mock data
  }

  async executeTask(task: NLPTask): Promise<NLPTask> {
    const startTime = Date.now();
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    try {
      let output: string;
      let confidence: number;

      switch (task.type) {
        case 'sentiment':
          const sentiments = ['positive', 'negative', 'neutral'];
          output = sentiments[Math.floor(Math.random() * sentiments.length)];
          confidence = Math.random() * 0.5 + 0.5;
          break;
          
        case 'classification':
          const categories = ['technology', 'sports', 'politics', 'entertainment', 'science'];
          output = categories[Math.floor(Math.random() * categories.length)];
          confidence = Math.random() * 0.4 + 0.6;
          break;
          
        case 'extraction':
          // Mock entity extraction
          const entities = [
            { text: 'John Smith', label: 'PERSON', confidence: 0.95 },
            { text: 'Google', label: 'ORG', confidence: 0.92 },
            { text: 'California', label: 'LOC', confidence: 0.88 }
          ];
          output = JSON.stringify(entities);
          confidence = 0.9;
          break;
          
        case 'summarization':
          output = "This is a mock summary of the input text. It demonstrates the summarization capability of the system.";
          confidence = 0.85;
          break;
          
        case 'translation':
          output = "Ceci est une traduction simulée du texte d'entrée.";
          confidence = 0.92;
          break;
          
        default:
          output = "Processed: " + task.input.substring(0, 50) + "...";
          confidence = 0.8;
      }

      const endTime = Date.now();
      const latency = endTime - startTime;

      // Record metrics
      this.recordMetrics({
        latency,
        throughput: 1000 / latency,
        errorRate: 0,
        accuracy: confidence,
      });

      return {
        ...task,
        output,
        status: 'completed',
        confidence,
        metadata: {
          ...task.metadata,
          executionTime: latency,
          step: 'completed',
          context: { mock: true },
        },
      };

    } catch (error) {
      const endTime = Date.now();
      const latency = endTime - startTime;

      this.recordMetrics({
        latency,
        throughput: 0,
        errorRate: 1,
      });

      return {
        ...task,
        status: 'error',
        metadata: {
          ...task.metadata,
          error: error instanceof Error ? error.message : 'Unknown error',
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
    }

    return results;
  }

  async executeParallelTasks(tasks: NLPTask[]): Promise<NLPTask[]> {
    const promises = tasks.map(task => this.executeTask(task));
    return Promise.all(promises);
  }

  getAvailableGraphs(): string[] {
    return ['sentiment', 'classification', 'extraction', 'summarization', 'translation'];
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

    // Keep only last 1000 metrics
    if (this.metrics.length > 1000) {
      this.metrics = this.metrics.slice(-1000);
    }
  }

  clearMetrics() {
    this.metrics = [];
  }

  async healthCheck(): Promise<Record<string, boolean>> {
    return {
      sentiment: true,
      classification: true,
      extraction: true,
      summarization: true,
      translation: true,
    };
  }
}