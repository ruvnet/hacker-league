# NOVA Model Configuration Schema

## Overview

This document defines the schema for NOVA's model configuration files, which specify the available LLM models, their capabilities, and configuration parameters.

## Schema Definition

```yaml
# JSON Schema for models.yaml
$schema: http://json-schema.org/draft-07/schema#
title: NOVA Model Configuration
type: object
required:
  - models

properties:
  models:
    type: object
    required:
      - teacher
      - student
    properties:
      teacher:
        type: array
        items:
          type: object
          required:
            - name
            - provider
            - capabilities
          properties:
            name:
              type: string
              description: Unique identifier for the model
            provider:
              type: string
              enum:
                - anthropic
                - openai
                - meta
                - google
                - local
              description: Model provider/vendor
            api_endpoint:
              type: string
              format: uri
              description: API endpoint for cloud models
            model_id:
              type: string
              description: Provider-specific model identifier
            deployment:
              type: string
              enum:
                - cloud
                - local
              default: cloud
              description: Deployment type
            model_path:
              type: string
              description: Path to model files for local deployment
            capabilities:
              type: array
              items:
                type: string
                enum:
                  - general_reasoning
                  - code_generation
                  - analysis
                  - math
                  - science
                  - creative
              minItems: 1
              description: Model capabilities
            max_tokens:
              type: integer
              minimum: 1
              description: Maximum tokens per request
            context_window:
              type: integer
              minimum: 1
              description: Maximum context window size
            temperature:
              type: number
              minimum: 0
              maximum: 2
              default: 0.7
              description: Sampling temperature
            top_p:
              type: number
              minimum: 0
              maximum: 1
              default: 1
              description: Nucleus sampling parameter
            api_key_env:
              type: string
              description: Environment variable name for API key
            
      student:
        type: object
        required:
          - architectures
          - optimization
        properties:
          architectures:
            type: array
            items:
              type: object
              required:
                - name
                - params
                - size_mb
              properties:
                name:
                  type: string
                  description: Architecture identifier
                description:
                  type: string
                  description: Architecture description
                params:
                  type: string
                  pattern: ^\d+[MBT]$
                  description: Parameter count (e.g., 60M, 1B)
                size_mb:
                  type: integer
                  minimum: 1
                  description: Model size in megabytes
                capabilities:
                  type: array
                  items:
                    type: string
                  description: Supported capabilities
                
          optimization:
            type: object
            required:
              - quantization
              - pruning
              - distillation
            properties:
              quantization:
                type: array
                items:
                  type: string
                  enum:
                    - int8
                    - float16
                    - bfloat16
                    - float32
                description: Supported quantization methods
              pruning:
                type: array
                items:
                  type: string
                  enum:
                    - magnitude
                    - structured
                    - unstructured
                description: Supported pruning methods
              distillation:
                type: array
                items:
                  type: string
                  enum:
                    - vanilla
                    - progressive
                    - attention
                description: Supported distillation methods

## Example Configuration

```yaml
models:
  teacher:
    - name: "claude-2"
      provider: "anthropic"
      api_endpoint: "https://api.anthropic.com/v1"
      model_id: "claude-2"
      deployment: "cloud"
      capabilities:
        - "general_reasoning"
        - "code_generation"
        - "analysis"
      max_tokens: 100000
      context_window: 100000
      temperature: 0.7
      top_p: 1.0
      api_key_env: "ANTHROPIC_API_KEY"
    
    - name: "llama-2-70b"
      provider: "meta"
      deployment: "local"
      model_path: "/models/llama2/70b"
      capabilities:
        - "general_reasoning"
        - "code_generation"
      max_tokens: 4000
      context_window: 4000
      temperature: 0.8

  student:
    architectures:
      - name: "transformer-tiny"
        description: "Tiny transformer for basic tasks"
        params: "60M"
        size_mb: 250
        capabilities:
          - "general_reasoning"
          - "code_generation"
      
      - name: "transformer-small"
        description: "Small transformer for medium tasks"
        params: "250M"
        size_mb: 1000
        capabilities:
          - "general_reasoning"
          - "code_generation"
          - "analysis"

    optimization:
      quantization:
        - "int8"
        - "float16"
      pruning:
        - "magnitude"
        - "structured"
      distillation:
        - "vanilla"
        - "progressive"
```

## Validation Rules

1. **Model Names**
   - Must be unique across all models
   - Should be lowercase with hyphens
   - Maximum length: 64 characters

2. **API Endpoints**
   - Must be valid URLs
   - HTTPS required for cloud deployments
   - Local paths must exist for local deployments

3. **Capabilities**
   - At least one capability required
   - Must be from predefined set
   - Student capabilities must be subset of teacher

4. **Resource Limits**
   - max_tokens ≤ context_window
   - size_mb must be reasonable for architecture
   - params must follow size pattern

5. **Security**
   - API keys must use environment variables
   - Local model paths must be secure
   - Endpoints must use HTTPS

## Usage

The configuration is validated on load:

```python
from nova.config import ModelConfig

# Load and validate configuration
config = ModelConfig.from_yaml("models.yaml")

# Access configuration
teacher_model = config.get_teacher("claude-2")
student_arch = config.get_student_architecture("transformer-tiny")

# Validate compatibility
if config.is_compatible(teacher_model, student_arch):
    print("Models are compatible for distillation")
```

## Error Handling

Configuration errors raise `ModelConfigError` with detailed messages:

```python
try:
    config = ModelConfig.from_yaml("models.yaml")
except ModelConfigError as e:
    print(f"Configuration error: {e}")
    print(f"Location: {e.path}")
    print(f"Details: {e.details}")
```

This schema ensures consistent and valid model configurations across the NOVA system.