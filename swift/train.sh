# Exp: https://github.com/modelscope/ms-swift/pull/5307#issuecomment-3219803922
# Before running this script, please run the following `swift rollout` script first
# This script is a example for multi-turn training with dynamic num of rollout outputs
# which means a trajectory of multi turn rollout is split into multiple data
#       see details in thinking_tips_scheduler
# NOTE: for same trajectory, the reward is supported to be the same,
#       here we use the last turn data of each trajectory to compute accuracy reward
#       see details in thinking_tips reward function

# CUDA_VISIBLE_DEVICES=0 \
# swift rollout \
#     --model Qwen/Qwen3-1.7B \
#     --vllm_use_async_engine true \
#     --multi_turn_scheduler thinking_tips_scheduler \
#     --vllm_max_model_len 32768 \
#     --vllm_gpu_memory_utilization 0.8 \
#     --max_turns 3
WANDB_API_KEY=c4dd2823f17eb69f4f12a86f6ff62cbb0a1f34d2 \
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
NPROC_PER_NODE=8 \
swift rlhf \
    --rlhf_type grpo \
    --model /root/paddlejob/workspace/env_run/chuxu/graph_models/qwen2_5vl-7b-sft \
    --model_type qwen2_5_vl \
    --train_type lora \
    --multi_turn_scheduler graph_sample_scheduler \
    --max_turns 5  \
    --external_plugins examples/train/grpo/plugin/plugin.py \
    --reward_funcs external_r1v_acc \
    --loss_scale each_round \
    --use_vllm False \
    --torch_dtype bfloat16 \
    --dataset /root/paddlejob/workspace/env_run/chuxu/graph/data/GRPO_train_graph_sample.jsonl \
    --split_dataset_ratio 0 \
    --max_completion_length 2048 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 1 \
    --learning_rate 1e-6 \
    --gradient_accumulation_steps 2 \
    --steps_per_generation 4 \
    --gradient_checkpointing_kwargs '{"use_reentrant": false}' \
    --save_total_limit 2 \
    --logging_steps 1 \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --dataset_num_proc 4 \
    --num_generations 4 \
    --temperature 1.0 \
    --deepspeed zero2 \
    --log_completions true \
    --log_entropy true \
    --importance_sampling_level sequence \
    --num_iterations 1 \
    --async_generate False \
    --output_dir /root/paddlejob/workspace/env_run/chuxu/graph_models/qwen2_5vl-7b-grpo \
    --report_to wandb 