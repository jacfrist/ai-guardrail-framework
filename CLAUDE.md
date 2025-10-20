# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI guardrail framework that leverages AWS Bedrock and formal methods to automatically detect unsafe or private data in model outputs. The framework is designed to provide security and privacy guarantees for AI model deployments.

## Current State

This is an early-stage repository. The codebase is currently minimal, with only basic project scaffolding in place.

## AWS Configuration

The project uses AWS Bedrock. AWS credentials are configured via environment variables in `.env`:
- `AWS_BEARER_TOKEN_BEDROCK`: Authentication token for AWS Bedrock API access
- Never commit the `.env` file to version control

## Architecture Considerations

When implementing this framework, consider:

1. **Guardrail Detection Layer**: The core system for analyzing model outputs against safety and privacy rules
2. **Formal Methods Integration**: How formal verification techniques will be applied to guarantee detection properties
3. **AWS Bedrock Integration**: How the framework interfaces with AWS Bedrock services
4. **Rule Definition System**: How safety and privacy rules are defined, stored, and evaluated
5. **Output Analysis Pipeline**: The flow from model output to guardrail evaluation to final decision

## Future Development

As the codebase grows, this file should be updated to include:
- Build and test commands specific to the chosen tech stack
- Architectural patterns and module organization
- Key abstractions and interfaces
- Integration patterns with AWS Bedrock
- Testing strategies for formal verification components
