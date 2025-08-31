import { StateGraph, END, START } from "@langchain/langgraph";
import { BaseMessage } from "@langchain/core/messages";
import { LangGraphState, NLPTask, AIMessage } from "@/types/ai";

// Base state interface for all subgraphs
interface BaseGraphState {
  messages: BaseMessage[];
  currentTask?: NLPTask;
  context: Record<string, any>;
  step: string;
  isProcessing: boolean;
}

// Base graph class that all subgraphs extend
export abstract class BaseLangGraph {
  protected graph: StateGraph<BaseGraphState>;
  
  constructor() {
    this.graph = new StateGraph<BaseGraphState>({
      channels: {
        messages: {
          value: (x: BaseMessage[], y: BaseMessage[]) => x.concat(y),
          default: () => [],
        },
        currentTask: {
          value: (x?: NLPTask, y?: NLPTask) => y ?? x,
          default: () => undefined,
        },
        context: {
          value: (x: Record<string, any>, y: Record<string, any>) => ({ ...x, ...y }),
          default: () => ({}),
        },
        step: {
          value: (x: string, y: string) => y ?? x,
          default: () => "start",
        },
        isProcessing: {
          value: (x: boolean, y: boolean) => y ?? x,
          default: () => false,
        },
      },
    });
    
    this.setupGraph();
  }

  protected abstract setupGraph(): void;

  public compile() {
    return this.graph.compile();
  }

  // Common utility methods
  protected async processInput(state: BaseGraphState): Promise<Partial<BaseGraphState>> {
    return {
      step: "processing",
      isProcessing: true,
    };
  }

  protected async handleError(state: BaseGraphState, error: Error): Promise<Partial<BaseGraphState>> {
    console.error("Graph execution error:", error);
    return {
      step: "error",
      isProcessing: false,
      context: {
        ...state.context,
        error: error.message,
      },
    };
  }

  protected async finalizeOutput(state: BaseGraphState): Promise<Partial<BaseGraphState>> {
    return {
      step: "completed",
      isProcessing: false,
    };
  }
}