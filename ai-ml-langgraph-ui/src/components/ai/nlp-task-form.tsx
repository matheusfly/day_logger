"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { NLPTask } from "@/types/ai";
import { Brain, FileText, Tag, MessageSquare, Languages } from "lucide-react";

interface NLPTaskFormProps {
  onSubmit: (task: NLPTask) => void;
  isLoading?: boolean;
}

const taskTypes = [
  { value: "sentiment", label: "Sentiment Analysis", icon: MessageSquare, description: "Analyze emotional tone" },
  { value: "classification", label: "Text Classification", icon: Tag, description: "Categorize text content" },
  { value: "extraction", label: "Entity Extraction", icon: Brain, description: "Extract named entities" },
  { value: "summarization", label: "Text Summarization", icon: FileText, description: "Generate concise summaries" },
  { value: "translation", label: "Translation", icon: Languages, description: "Translate between languages" },
] as const;

export function NLPTaskForm({ onSubmit, isLoading }: NLPTaskFormProps) {
  const [taskType, setTaskType] = useState<string>("");
  const [input, setInput] = useState("");
  const [taskId, setTaskId] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!taskType || !input.trim()) return;

    const task: NLPTask = {
      id: taskId || `task-${Date.now()}`,
      type: taskType as NLPTask["type"],
      input: input.trim(),
      status: "pending",
      metadata: {
        createdAt: new Date().toISOString(),
        source: "ui",
      },
    };

    onSubmit(task);
    
    // Reset form
    setInput("");
    setTaskId("");
  };

  const selectedTask = taskTypes.find(t => t.value === taskType);

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {selectedTask && <selectedTask.icon className="h-5 w-5" />}
          Create NLP Task
        </CardTitle>
        <CardDescription>
          {selectedTask ? selectedTask.description : "Select a task type to get started"}
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="taskType" className="text-sm font-medium">
              Task Type
            </label>
            <Select value={taskType} onValueChange={setTaskType}>
              <SelectTrigger>
                <SelectValue placeholder="Select a task type" />
              </SelectTrigger>
              <SelectContent>
                {taskTypes.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    <div className="flex items-center gap-2">
                      <type.icon className="h-4 w-4" />
                      {type.label}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label htmlFor="taskId" className="text-sm font-medium">
              Task ID (Optional)
            </label>
            <Input
              id="taskId"
              placeholder="Enter custom task ID or leave blank for auto-generation"
              value={taskId}
              onChange={(e) => setTaskId(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="input" className="text-sm font-medium">
              Input Text
            </label>
            <Textarea
              id="input"
              placeholder={getPlaceholderText(taskType)}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="min-h-[120px]"
              required
            />
            <div className="text-xs text-muted-foreground">
              {input.length} characters
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button 
            type="submit" 
            disabled={!taskType || !input.trim() || isLoading}
            className="w-full"
          >
            {isLoading ? "Processing..." : "Create Task"}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}

function getPlaceholderText(taskType: string): string {
  switch (taskType) {
    case "sentiment":
      return "Enter text to analyze sentiment (e.g., 'I love this product!')";
    case "classification":
      return "Enter text to classify (e.g., 'Breaking news about technology...')";
    case "extraction":
      return "Enter text to extract entities (e.g., 'John Smith works at Google in California')";
    case "summarization":
      return "Enter long text to summarize...";
    case "translation":
      return "Enter text to translate...";
    default:
      return "Enter your text here...";
  }
}