"use client";

import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { NLPTask } from "@/types/ai";
import { 
  CheckCircle, 
  XCircle, 
  Clock, 
  Loader2, 
  Brain, 
  FileText, 
  Tag, 
  MessageSquare, 
  Languages,
  TrendingUp,
  TrendingDown,
  Minus
} from "lucide-react";

interface TaskResultsProps {
  tasks: NLPTask[];
}

const taskTypeIcons = {
  sentiment: MessageSquare,
  classification: Tag,
  extraction: Brain,
  summarization: FileText,
  translation: Languages,
};

const statusIcons = {
  pending: Clock,
  processing: Loader2,
  completed: CheckCircle,
  error: XCircle,
};

const statusColors = {
  pending: "text-yellow-500",
  processing: "text-blue-500",
  completed: "text-green-500",
  error: "text-red-500",
};

export function TaskResults({ tasks }: TaskResultsProps) {
  if (tasks.length === 0) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center text-muted-foreground">
            <Brain className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No tasks yet. Create your first NLP task to see results here.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Task Results</h2>
        <div className="text-sm text-muted-foreground">
          {tasks.length} task{tasks.length !== 1 ? 's' : ''}
        </div>
      </div>
      
      {tasks.map((task) => (
        <TaskResultCard key={task.id} task={task} />
      ))}
    </div>
  );
}

function TaskResultCard({ task }: { task: NLPTask }) {
  const TaskIcon = taskTypeIcons[task.type];
  const StatusIcon = statusIcons[task.status];
  const statusColor = statusColors[task.status];

  return (
    <Card className="w-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <TaskIcon className="h-5 w-5" />
            {task.type.charAt(0).toUpperCase() + task.type.slice(1)}
            <span className="text-sm font-normal text-muted-foreground">
              #{task.id}
            </span>
          </CardTitle>
          <div className={`flex items-center gap-2 ${statusColor}`}>
            <StatusIcon className={`h-4 w-4 ${task.status === 'processing' ? 'animate-spin' : ''}`} />
            <span className="text-sm font-medium">
              {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
            </span>
          </div>
        </div>
        {task.confidence !== undefined && (
          <div className="flex items-center gap-2 mt-2">
            <span className="text-sm text-muted-foreground">Confidence:</span>
            <Progress value={task.confidence * 100} className="flex-1 max-w-32" />
            <span className="text-sm font-medium">
              {(task.confidence * 100).toFixed(1)}%
            </span>
          </div>
        )}
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-2">Input</h4>
          <div className="bg-muted p-3 rounded-md text-sm">
            {task.input}
          </div>
        </div>
        
        {task.output && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-2">Output</h4>
            <div className="bg-background border p-3 rounded-md">
              <TaskOutput task={task} />
            </div>
          </div>
        )}
        
        {task.metadata && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 border-t text-xs text-muted-foreground">
            {task.metadata.createdAt && (
              <div>
                <span className="font-medium">Created:</span>
                <br />
                {new Date(task.metadata.createdAt).toLocaleString()}
              </div>
            )}
            {task.metadata.executionTime && (
              <div>
                <span className="font-medium">Duration:</span>
                <br />
                {task.metadata.executionTime}ms
              </div>
            )}
            {task.metadata.step && (
              <div>
                <span className="font-medium">Step:</span>
                <br />
                {task.metadata.step}
              </div>
            )}
            {task.metadata.error && (
              <div className="text-red-500">
                <span className="font-medium">Error:</span>
                <br />
                {task.metadata.error}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function TaskOutput({ task }: { task: NLPTask }) {
  switch (task.type) {
    case 'sentiment':
      return <SentimentOutput output={task.output} confidence={task.confidence} />;
    case 'classification':
      return <ClassificationOutput output={task.output} confidence={task.confidence} />;
    case 'extraction':
      return <ExtractionOutput output={task.output} />;
    case 'summarization':
      return <SummarizationOutput output={task.output} />;
    case 'translation':
      return <TranslationOutput output={task.output} />;
    default:
      return <div className="text-sm">{task.output}</div>;
  }
}

function SentimentOutput({ output, confidence }: { output?: string; confidence?: number }) {
  if (!output) return null;
  
  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive': return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'negative': return <TrendingDown className="h-4 w-4 text-red-500" />;
      default: return <Minus className="h-4 w-4 text-gray-500" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive': return 'text-green-600 bg-green-50 border-green-200';
      case 'negative': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border ${getSentimentColor(output)}`}>
      {getSentimentIcon(output)}
      <span className="font-medium">{output.charAt(0).toUpperCase() + output.slice(1)}</span>
      {confidence && (
        <span className="text-xs opacity-75">({(confidence * 100).toFixed(0)}%)</span>
      )}
    </div>
  );
}

function ClassificationOutput({ output, confidence }: { output?: string; confidence?: number }) {
  if (!output) return null;
  
  return (
    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700">
      <Tag className="h-4 w-4" />
      <span className="font-medium">{output}</span>
      {confidence && (
        <span className="text-xs opacity-75">({(confidence * 100).toFixed(0)}%)</span>
      )}
    </div>
  );
}

function ExtractionOutput({ output }: { output?: string }) {
  if (!output) return null;
  
  try {
    const entities = JSON.parse(output);
    if (Array.isArray(entities)) {
      return (
        <div className="space-y-2">
          {entities.map((entity: any, index: number) => (
            <div key={index} className="flex items-center gap-2 text-sm">
              <span className="px-2 py-1 rounded bg-purple-100 text-purple-700 font-medium">
                {entity.label}
              </span>
              <span>{entity.text}</span>
              {entity.confidence && (
                <span className="text-xs text-muted-foreground">
                  {(entity.confidence * 100).toFixed(0)}%
                </span>
              )}
            </div>
          ))}
        </div>
      );
    }
  } catch (error) {
    // Fallback for non-JSON output
  }
  
  return <div className="text-sm">{output}</div>;
}

function SummarizationOutput({ output }: { output?: string }) {
  if (!output) return null;
  
  return (
    <div className="text-sm leading-relaxed p-3 bg-amber-50 border border-amber-200 rounded">
      {output}
    </div>
  );
}

function TranslationOutput({ output }: { output?: string }) {
  if (!output) return null;
  
  return (
    <div className="text-sm leading-relaxed p-3 bg-emerald-50 border border-emerald-200 rounded">
      {output}
    </div>
  );
}