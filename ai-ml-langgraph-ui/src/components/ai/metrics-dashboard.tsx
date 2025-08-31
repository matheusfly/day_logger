"use client";

import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { MLOpsMetrics } from "@/types/ai";
import { 
  Activity, 
  Clock, 
  Zap, 
  AlertTriangle, 
  Target,
  TrendingUp,
  BarChart3
} from "lucide-react";

interface MetricsDashboardProps {
  metrics: MLOpsMetrics;
  realtimeMetrics?: MLOpsMetrics[];
}

export function MetricsDashboard({ metrics, realtimeMetrics = [] }: MetricsDashboardProps) {
  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">ML Operations Metrics</h2>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Activity className="h-4 w-4" />
          Live Monitoring
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Average Latency"
          value={`${metrics.latency.toFixed(0)}ms`}
          description="Response time per request"
          icon={Clock}
          trend={getTrend(realtimeMetrics.map(m => m.latency))}
          color="blue"
        />
        
        <MetricCard
          title="Throughput"
          value={`${metrics.throughput.toFixed(1)}/s`}
          description="Requests processed per second"
          icon={Zap}
          trend={getTrend(realtimeMetrics.map(m => m.throughput))}
          color="green"
        />
        
        <MetricCard
          title="Error Rate"
          value={`${(metrics.errorRate * 100).toFixed(1)}%`}
          description="Failed requests percentage"
          icon={AlertTriangle}
          trend={getTrend(realtimeMetrics.map(m => m.errorRate))}
          color="red"
        />
        
        <MetricCard
          title="Accuracy"
          value={metrics.accuracy ? `${(metrics.accuracy * 100).toFixed(1)}%` : "N/A"}
          description="Model prediction accuracy"
          icon={Target}
          trend={metrics.accuracy ? getTrend(realtimeMetrics.map(m => m.accuracy || 0)) : null}
          color="purple"
        />
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Performance Metrics
            </CardTitle>
            <CardDescription>
              Detailed performance and quality metrics
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {metrics.precision !== undefined && (
              <MetricBar 
                label="Precision" 
                value={metrics.precision} 
                color="bg-blue-500" 
              />
            )}
            {metrics.recall !== undefined && (
              <MetricBar 
                label="Recall" 
                value={metrics.recall} 
                color="bg-green-500" 
              />
            )}
            {metrics.f1Score !== undefined && (
              <MetricBar 
                label="F1 Score" 
                value={metrics.f1Score} 
                color="bg-purple-500" 
              />
            )}
            {metrics.accuracy !== undefined && (
              <MetricBar 
                label="Accuracy" 
                value={metrics.accuracy} 
                color="bg-amber-500" 
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              System Health
            </CardTitle>
            <CardDescription>
              Real-time system performance indicators
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <HealthIndicator
              label="Latency"
              status={getHealthStatus(metrics.latency, 1000, 'lower')}
              value={`${metrics.latency.toFixed(0)}ms`}
            />
            <HealthIndicator
              label="Throughput"
              status={getHealthStatus(metrics.throughput, 1, 'higher')}
              value={`${metrics.throughput.toFixed(1)}/s`}
            />
            <HealthIndicator
              label="Error Rate"
              status={getHealthStatus(metrics.errorRate * 100, 5, 'lower')}
              value={`${(metrics.errorRate * 100).toFixed(1)}%`}
            />
            {metrics.accuracy !== undefined && (
              <HealthIndicator
                label="Model Accuracy"
                status={getHealthStatus(metrics.accuracy * 100, 80, 'higher')}
                value={`${(metrics.accuracy * 100).toFixed(1)}%`}
              />
            )}
          </CardContent>
        </Card>
      </div>

      {/* Real-time Chart Placeholder */}
      {realtimeMetrics.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Real-time Performance</CardTitle>
            <CardDescription>
              Live metrics over the last {realtimeMetrics.length} requests
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-32 flex items-center justify-center text-muted-foreground">
              <div className="text-center">
                <BarChart3 className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Real-time chart visualization would go here</p>
                <p className="text-xs">Integration with charting library needed</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  trend: 'up' | 'down' | 'stable' | null;
  color: 'blue' | 'green' | 'red' | 'purple';
}

function MetricCard({ title, value, description, icon: Icon, trend, color }: MetricCardProps) {
  const colorClasses = {
    blue: "text-blue-600 bg-blue-50 border-blue-200",
    green: "text-green-600 bg-green-50 border-green-200",
    red: "text-red-600 bg-red-50 border-red-200",
    purple: "text-purple-600 bg-purple-50 border-purple-200",
  };

  const trendIcons = {
    up: "↗️",
    down: "↘️",
    stable: "→",
  };

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
            <Icon className="h-4 w-4" />
          </div>
          {trend && (
            <span className="text-xs text-muted-foreground">
              {trendIcons[trend]}
            </span>
          )}
        </div>
        <div className="mt-4">
          <div className="text-2xl font-bold">{value}</div>
          <div className="text-sm text-muted-foreground">{title}</div>
          <div className="text-xs text-muted-foreground mt-1">{description}</div>
        </div>
      </CardContent>
    </Card>
  );
}

interface MetricBarProps {
  label: string;
  value: number;
  color: string;
}

function MetricBar({ label, value, color }: MetricBarProps) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>{label}</span>
        <span className="font-medium">{(value * 100).toFixed(1)}%</span>
      </div>
      <Progress value={value * 100} className="h-2" />
    </div>
  );
}

interface HealthIndicatorProps {
  label: string;
  status: 'good' | 'warning' | 'error';
  value: string;
}

function HealthIndicator({ label, status, value }: HealthIndicatorProps) {
  const statusColors = {
    good: "bg-green-100 text-green-800 border-green-200",
    warning: "bg-yellow-100 text-yellow-800 border-yellow-200",
    error: "bg-red-100 text-red-800 border-red-200",
  };

  const statusDots = {
    good: "bg-green-500",
    warning: "bg-yellow-500",
    error: "bg-red-500",
  };

  return (
    <div className="flex items-center justify-between p-3 rounded-lg border bg-card">
      <div className="flex items-center gap-3">
        <div className={`w-2 h-2 rounded-full ${statusDots[status]}`} />
        <span className="text-sm font-medium">{label}</span>
      </div>
      <span className={`px-2 py-1 text-xs rounded border ${statusColors[status]}`}>
        {value}
      </span>
    </div>
  );
}

function getTrend(values: number[]): 'up' | 'down' | 'stable' | null {
  if (values.length < 2) return null;
  
  const recent = values.slice(-5);
  const avg1 = recent.slice(0, Math.floor(recent.length / 2)).reduce((a, b) => a + b, 0) / Math.floor(recent.length / 2);
  const avg2 = recent.slice(Math.floor(recent.length / 2)).reduce((a, b) => a + b, 0) / (recent.length - Math.floor(recent.length / 2));
  
  const diff = Math.abs(avg2 - avg1) / avg1;
  if (diff < 0.05) return 'stable';
  return avg2 > avg1 ? 'up' : 'down';
}

function getHealthStatus(value: number, threshold: number, direction: 'higher' | 'lower'): 'good' | 'warning' | 'error' {
  if (direction === 'higher') {
    if (value >= threshold) return 'good';
    if (value >= threshold * 0.8) return 'warning';
    return 'error';
  } else {
    if (value <= threshold) return 'good';
    if (value <= threshold * 1.5) return 'warning';
    return 'error';
  }
}