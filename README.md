# chat-sentiment-analysis
Solve all sentiment analysis tasks by chat

## Step by Step
- [filetune](chat_sentiment_analysis/llama/finetune.py)
  - nohup sh run.sh chat_sentiment_analysis/llama/finetune.py > autodl.log 2>&1 &
- [inference_llama](chat_sentiment_analysis/llama/inference_llama.py)
  - sh run.sh chat_sentiment_analysis/llama/inference_llama.py
- [inference_alpaca_lora](chat_sentiment_analysis/llama/inference_alpaca_lora.py)
  - sh run.sh chat_sentiment_analysis/llama/inference_alpaca_lora.py
- [inference_gradio](chat_sentiment_analysis/llama/inference_gradio.py)
    - sh run.sh chat_sentiment_analysis/llama/inference_gradio.py
