# Prompt-generation brief (given verbatim to a fresh LLM instance with no tools, no file access, no prior context)

You are helping a research benchmark of zero-shot debiasing methods for vision-language models.
Answer ONLY from your general knowledge. Do NOT use any tools, do NOT read or search any files, and do NOT ask questions.

## Task
- Images: chest radiographs (chest X-rays) of adult patients from a large hospital imaging archive.
- Zero-shot binary classification. Class names (use these exact keys): `"no_effusion"` (no pleural effusion) and
  `"effusion"` (pleural effusion present).
- Model: MedCLIP, a medical CLIP-style model. Its text encoder is Bio_ClinicalBERT trained on radiology report
  sentences, so prompts written in English, radiology-report style tend to work best. Keep each prompt under ~40 words.
- The methods below try to stop the classifier from relying on spurious (non-causal) image attributes that may be
  correlated with the label. Which spurious attributes are present in this dataset is NOT given to you: where a method
  needs spurious attributes, propose the ones you consider most plausible for this task from your own domain
  knowledge, as the LLM-based methods (RoboShot, PRISM) do in their papers.

## Output
Return ONE JSON object whose keys are the file names below and whose values are the file contents.
Every file must contain `"class prompts": {"no_effusion": "<prompt>", "effusion": "<prompt>"}` (use the same class
prompts in every file). Placeholders in angle brackets are for you to fill; spurious attribute/value names are yours to
choose.

1. `zero_shot.json`: only `"class prompts"`.
2. `ortho_proj.json` (Ortho-Proj from "Debiasing Vision-Language Models via Biased Prompts", Chuang et al. 2023): `"spurious prompts": [8-16 sentences, each describing
   a spurious attribute value without mentioning the class]`.
3. `ortho_cali.json` (Ortho-Cali from the same paper): same `"spurious prompts"` list as ortho_proj,
   plus `"candidate prompts": {"no_effusion": [5-8 prompts], "effusion": [5-8 prompts]}` where each candidate prompt is
   a class prompt with one spurious attribute value appended; within a class the prompts must differ only in the
   spurious attribute value, and the same values must be used for both classes. Also `"lambda": 1000`.
4. `roboshot.json` (RoboShot, Adila et al. 2024): emulate RoboShot's LLM queries.
   `"harmful prompts"`: answers to "List the spurious differences between chest X-rays with and without pleural
   effusion" as pairs `[["<phrase for one side>", "<phrase for the other side>"], ...]` (5-10 pairs).
   `"helpful prompts"`: answers to "List the true visual differences between chest X-rays with and without pleural
   effusion" in the same pair format (5-10 pairs).
5. `prism_mini.json` (PRISM-mini, ICCV 2025): `"spurious prompts": [8-16 short descriptions of spurious attribute values]`.
6. `prism.json` (PRISM, ICCV 2025), text-only training data:
   `"scene descriptions": [8-12 sentence templates containing both placeholders "<finding>" and "<attribute>"]`,
   `"target classes": ["no effusion", "effusion"]`,
   `"target class descriptions": {"no effusion": [10-20 phrases], "effusion": [10-20 phrases]}` (phrases that fill
   "<finding>"),
   `"bias classes": [2-6 names of spurious attribute values]`,
   `"bias class descriptions": {"<bias class>": [8-12 phrases that fill "<attribute>"], ...}`,
   `"target placeholder": "<finding>"`, `"bias placeholder": "<attribute>"`,
   `"hyperparameters": {"num_samples": 500, "lr": 0.1, "epochs": 1, "batch_size": 64, "seeds": [0, 1, 2]}`.
7. `tie.json` (TIE / TIE*, ICLR 2025): choose the ONE spurious attribute you consider most likely and give one prompt
   per value: `"spurious prompts": {"<value 1>": "<prompt>", "<value 2>": "<prompt>", ...}` (2-4 values).
8. `fairerclip.json` (FairerCLIP, ICLR 2024): same format as tie.json (prompts used to infer spurious-attribute labels
   zero-shot); you may reuse the tie.json attribute.
9. `sem.json` (SEM, CVPR 2026): `"bias prompts": {"<spurious attribute value>": [15-20 captions describing images with
   that value, not mentioning the class], ...}` (2-6 values), and `"extra class prompts": {"no_effusion": [10
   paraphrases of the class prompt], "effusion": [10 paraphrases]}`.

After the JSON, add a short section "Rationale" (max 10 lines) explaining which spurious attributes you proposed and why.
