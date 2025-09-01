"use client";

import React, { useState, useEffect } from "react";
import { NLPTaskForm } from "@/components/ai/nlp-task-form";
import { TaskResults } from "@/components/ai/task-results";
import { MetricsDashboard } from "@/components/ai/metrics-dashboard";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MockOrchestrator } from "@/lib/mock-orchestrator";
import { NLPTask, MLOpsMetrics } from "@/types/ai";
import Link from 'next/link';
import { Brain, Activity, BarChart3, Settings, RefreshCw } from "lucide-react";

declare global {
  interface Window {
    electron: {
      ipcRenderer: {
        sendMessage: (channel: string, args?: unknown[]) => void;
        on: (channel: string, func: (...args: unknown[]) => void) => () => void;
        once: (channel: string, func: (...args: unknown[]) => void) => void;
      };
    };
  }
}

export default function Home() {
  const [tasks, setTasks] = useState<NLPTask[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [orchestrator] = useState(() => new MockOrchestrator());
  const [metrics, setMetrics] = useState<MLOpsMetrics>({
    latency: 0,
    throughput: 0,
    errorRate: 0,
  });

  // Load tasks from localStorage on mount
  useEffect(() => {
    const savedTasks = localStorage.getItem('nlp-tasks');
    if (savedTasks) {
      try {
        setTasks(JSON.parse(savedTasks));
      } catch (error) {
        console.error('Error loading saved tasks:', error);
      }
    }
  }, []);

  // Save tasks to localStorage whenever tasks change
  useEffect(() => {
    if (tasks.length > 0) {
      localStorage.setItem('nlp-tasks', JSON.stringify(tasks));
    }
  }, [tasks]);

  // Update metrics whenever tasks change
  useEffect(() => {
    const aggregatedMetrics = orchestrator.getAggregatedMetrics();
    setMetrics(aggregatedMetrics);
  }, [tasks, orchestrator]);

  const handleTaskSubmit = async (task: NLPTask) => {
    setIsProcessing(true);
    
    // Add task to list with pending status
    const newTask = { ...task, status: 'processing' as const };
    setTasks(prev => [newTask, ...prev]);

    try {
      // Execute the task using LangGraph orchestrator
      const result = await orchestrator.executeTask(task);
      
      // Update the task with results
      setTasks(prev => prev.map(t => 
        t.id === task.id ? result : t
      ));
    } catch (error) {
      console.error('Task execution error:', error);
      
      // Update task with error status
      setTasks(prev => prev.map(t => 
        t.id === task.id 
          ? { 
              ...t, 
              status: 'error' as const, 
              metadata: { 
                ...t.metadata, 
                error: error instanceof Error ? error.message : 'Unknown error' 
              } 
            }
          : t
      ));
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClearTasks = () => {
    setTasks([]);
    localStorage.removeItem('nlp-tasks');
    orchestrator.clearMetrics();
    setMetrics({ latency: 0, throughput: 0, errorRate: 0 });
  };

  const handleHealthCheck = async () => {
    const health = await orchestrator.healthCheck();
    console.log('Graph health check:', health);
    // You could show this in a toast or modal
  };

  const runPython = () => {
    if (window.electron) {
      window.electron.ipcRenderer.sendMessage('run-python-script');
    }
  };

  useEffect(() => {
    if (window.electron) {
        const removeListener = window.electron.ipcRenderer.on('python-script-reply', (message) => {
            console.log('Received from main:', message);
        });
        return () => {
            removeListener();
        };
    }
  }, []);

  const completedTasks = tasks.filter(t => t.status === 'completed').length;
  const errorTasks = tasks.filter(t => t.status === 'error').length;
  const processingTasks = tasks.filter(t => t.status === 'processing').length;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
                <Brain className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">AI/ML NLP Operations</h1>
                <p className="text-muted-foreground">
                  LangGraph Subgraphs with ShadCN UI
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={handleHealthCheck}>
                <Activity className="h-4 w-4 mr-2" />
                Health Check
              </Button>
              <Button variant="outline" size="sm" onClick={handleClearTasks}>
                <RefreshCw className="h-4 w-4 mr-2" />
                Clear All
              </Button>
              <Button variant="outline" size="sm" onClick={runPython}>
                Run Python
              </Button>
              <Link href="/logger">
                <Button variant="outline" size="sm">
                  Go to Logger
                </Button>
              </Link>
            </div>
          </div>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-green-600">{completedTasks}</div>
                <div className="text-sm text-muted-foreground">Completed</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-blue-600">{processingTasks}</div>
                <div className="text-sm text-muted-foreground">Processing</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-red-600">{errorTasks}</div>
                <div className="text-sm text-muted-foreground">Errors</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold">{tasks.length}</div>
                <div className="text-sm text-muted-foreground">Total Tasks</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="tasks" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="tasks" className="flex items-center gap-2">
              <Brain className="h-4 w-4" />
              NLP Tasks
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Results
            </TabsTrigger>
            <TabsTrigger value="metrics" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Metrics
            </TabsTrigger>
          </TabsList>

          <TabsContent value="tasks" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Create New NLP Task</CardTitle>
                <CardDescription>
                  Select a task type and provide input text to process using LangGraph subgraphs.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <NLPTaskForm onSubmit={handleTaskSubmit} isLoading={isProcessing} />
              </CardContent>
            </Card>
            
            {/* Available Graphs Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Available LangGraph Subgraphs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {orchestrator.getAvailableGraphs().map((graph) => (
                    <div key={graph} className="p-3 border rounded-lg bg-muted/50">
                      <div className="font-medium capitalize">{graph}</div>
                      <div className="text-sm text-muted-foreground">
                        {getGraphDescription(graph)}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="results">
            <TaskResults tasks={tasks} />
          </TabsContent>

          <TabsContent value="metrics">
            <MetricsDashboard 
              metrics={metrics} 
              realtimeMetrics={orchestrator.getMetrics()} 
            />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

function getGraphDescription(graph: string): string {
  const descriptions = {
    sentiment: "Analyze emotional tone and sentiment in text",
    classification: "Categorize text into predefined classes",
    extraction: "Extract named entities and key information",
    summarization: "Generate concise summaries of long text",
    translation: "Translate text between different languages",
  };
  return descriptions[graph as keyof typeof descriptions] || "Advanced NLP processing";
}