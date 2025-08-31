import "dotenv/config";
import { VoltAgent, VoltOpsClient, Agent } from "@voltagent/core";
import { createPinoLogger } from "@voltagent/logger";
import { VercelAIProvider } from "@voltagent/vercel-ai";
import { anthropic } from "@ai-sdk/anthropic";
import { expenseApprovalWorkflow } from "./workflows";
import { weatherTool } from "./tools";

// Create a logger instance
const logger = createPinoLogger({
  name: "my-ai-agent-app",
  level: "info",
});

const agent = new Agent({
  name: "my-ai-agent-app",
  instructions: "A helpful assistant that can check weather and help with various tasks",
  llm: new VercelAIProvider(),
  model: anthropic("claude-3-5-sonnet-20241022"),
  tools: [weatherTool],
});

new VoltAgent({
  agents: {
    agent,
  },
  workflows: {
    expenseApprovalWorkflow,
  },
  logger,
  voltOpsClient: new VoltOpsClient({
    publicKey: process.env.VOLTAGENT_PUBLIC_KEY || "",
    secretKey: process.env.VOLTAGENT_SECRET_KEY || "",
  }),
});