```json
{
  "zero_shot.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    }
  },
  "ortho_proj.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "spurious prompts": [
      "Portable anteroposterior chest radiograph obtained with the patient supine.",
      "Standard posteroanterior chest radiograph obtained with the patient upright.",
      "A chest tube is in place.",
      "No support devices, lines or tubes are seen.",
      "Central venous catheter and endotracheal tube are in place.",
      "Cardiac monitoring leads and wires overlie the chest.",
      "Radiograph of an elderly patient.",
      "Radiograph of a young adult patient.",
      "Radiograph of a female patient with overlying breast soft tissue shadows.",
      "Radiograph of a male patient.",
      "Low lung volumes due to suboptimal inspiration.",
      "Patient rotation and suboptimal exposure limit image quality."
    ]
  },
  "ortho_cali.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "spurious prompts": [
      "Portable anteroposterior chest radiograph obtained with the patient supine.",
      "Standard posteroanterior chest radiograph obtained with the patient upright.",
      "A chest tube is in place.",
      "No support devices, lines or tubes are seen.",
      "Central venous catheter and endotracheal tube are in place.",
      "Cardiac monitoring leads and wires overlie the chest.",
      "Radiograph of an elderly patient.",
      "Radiograph of a young adult patient.",
      "Radiograph of a female patient with overlying breast soft tissue shadows.",
      "Radiograph of a male patient.",
      "Low lung volumes due to suboptimal inspiration.",
      "Patient rotation and suboptimal exposure limit image quality."
    ],
    "candidate prompts": {
      "no_effusion": [
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, on a portable supine anteroposterior film.",
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, on an upright posteroanterior film.",
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, with a chest tube in place.",
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, with no support devices.",
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, in an elderly patient.",
        "Chest radiograph with sharp costophrenic angles and no pleural effusion, in a young adult patient."
      ],
      "effusion": [
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, on a portable supine anteroposterior film.",
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, on an upright posteroanterior film.",
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, with a chest tube in place.",
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, with no support devices.",
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, in an elderly patient.",
        "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion, in a young adult patient."
      ]
    },
    "lambda": 1000
  },
  "roboshot.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "harmful prompts": [
      ["portable supine anteroposterior chest radiograph", "upright posteroanterior chest radiograph"],
      ["chest tube in place", "no chest tube"],
      ["central lines, endotracheal tube and other support devices", "no support devices"],
      ["cardiac monitoring leads overlying the chest", "no external monitoring leads"],
      ["elderly patient", "young adult patient"],
      ["low lung volumes with poor inspiration", "well-inflated lungs with good inspiration"],
      ["rotated, underexposed portable image", "well-centered, well-exposed image"],
      ["enlarged cardiac silhouette", "normal heart size"]
    ],
    "helpful prompts": [
      ["blunted costophrenic angle", "sharp costophrenic angle"],
      ["meniscus-shaped opacity ascending along the lateral chest wall", "no meniscus sign"],
      ["homogeneous dependent opacity at the lung base", "clear lung bases"],
      ["obscured hemidiaphragm contour", "well-defined hemidiaphragm contour"],
      ["fluid tracking into the interlobar fissures", "thin normal fissures"],
      ["hazy veil-like increased density of one hemithorax", "symmetric lucency of both hemithoraces"],
      ["mediastinal shift away from a large basal opacity", "midline mediastinum"]
    ]
  },
  "prism_mini.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "spurious prompts": [
      "portable supine anteroposterior chest radiograph",
      "upright posteroanterior chest radiograph",
      "chest tube in place",
      "no support devices",
      "central venous catheter and endotracheal tube",
      "cardiac monitoring leads over the chest",
      "elderly patient",
      "young adult patient",
      "female patient with breast shadows",
      "male patient",
      "low lung volumes",
      "rotated, suboptimally exposed image"
    ]
  },
  "prism.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "scene descriptions": [
      "<attribute> demonstrates <finding>.",
      "Chest radiograph, <attribute>, shows <finding>.",
      "<attribute>. Findings: <finding>.",
      "On this <attribute>, there is <finding>.",
      "Impression: <finding> on <attribute>.",
      "<attribute> of the chest reveals <finding>.",
      "Comparison not available. <attribute> shows <finding>.",
      "Single view of the chest, <attribute>: <finding>.",
      "The lungs are evaluated on <attribute>, with <finding>.",
      "<finding> is noted on this <attribute>."
    ],
    "target classes": ["no effusion", "effusion"],
    "target class descriptions": {
      "no effusion": [
        "no pleural effusion",
        "sharp costophrenic angles bilaterally",
        "no evidence of pleural fluid",
        "clear lung bases without effusion",
        "well-defined hemidiaphragms without effusion",
        "no blunting of the costophrenic angles",
        "absence of pleural effusion",
        "normal pleural spaces",
        "no meniscus sign at the lung bases",
        "no pleural fluid collection",
        "costophrenic sulci are clear",
        "no layering pleural fluid"
      ],
      "effusion": [
        "a pleural effusion",
        "blunting of the costophrenic angle due to pleural effusion",
        "a moderate right pleural effusion",
        "a small left pleural effusion",
        "bilateral pleural effusions",
        "a large pleural effusion with meniscus sign",
        "pleural fluid obscuring the hemidiaphragm",
        "layering pleural effusion at the lung base",
        "a meniscus-shaped basal opacity consistent with effusion",
        "fluid tracking into the fissure consistent with effusion",
        "a loculated pleural effusion",
        "hazy hemithorax opacity consistent with layering effusion"
      ]
    },
    "bias classes": ["portable supine AP", "upright PA"],
    "bias class descriptions": {
      "portable supine AP": [
        "a portable anteroposterior radiograph",
        "a supine AP film obtained at the bedside",
        "a portable semi-erect AP view",
        "a bedside ICU radiograph",
        "a portable AP image with monitoring leads",
        "a supine AP film with central venous catheter",
        "a portable AP radiograph with endotracheal tube",
        "a portable AP film with low lung volumes",
        "a rotated portable AP radiograph",
        "an AP supine image with support devices"
      ],
      "upright PA": [
        "a posteroanterior radiograph",
        "an upright PA film",
        "a standard PA and lateral examination",
        "an erect PA chest radiograph obtained in the department",
        "a PA view with good inspiration",
        "a well-centered PA radiograph",
        "an outpatient PA chest film",
        "a PA view without support devices",
        "a standing PA radiograph with full inspiration",
        "a routine upright PA image"
      ]
    },
    "target placeholder": "<finding>",
    "bias placeholder": "<attribute>",
    "hyperparameters": {"num_samples": 500, "lr": 0.1, "epochs": 1, "batch_size": 64, "seeds": [0, 1, 2]}
  },
  "tie.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "spurious prompts": {
      "portable supine AP": "Portable anteroposterior chest radiograph obtained with the patient supine at the bedside.",
      "upright PA": "Standard posteroanterior chest radiograph obtained with the patient upright."
    }
  },
  "fairerclip.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "spurious prompts": {
      "portable supine AP": "Portable anteroposterior chest radiograph obtained with the patient supine at the bedside.",
      "upright PA": "Standard posteroanterior chest radiograph obtained with the patient upright."
    }
  },
  "sem.json": {
    "class prompts": {
      "no_effusion": "Chest radiograph with sharp costophrenic angles and no pleural effusion.",
      "effusion": "Chest radiograph with blunting of the costophrenic angle and meniscus-shaped basal opacity consistent with pleural effusion."
    },
    "bias prompts": {
      "portable supine AP": [
        "Portable anteroposterior chest radiograph.",
        "Supine AP view of the chest obtained at the bedside.",
        "Portable semi-erect AP chest film.",
        "Single portable AP view of the chest.",
        "Bedside chest radiograph in the intensive care unit.",
        "AP supine radiograph with the scapulae projecting over the lungs.",
        "Portable AP film with limited inspiration.",
        "Portable chest radiograph, AP projection.",
        "Supine frontal chest image obtained portably.",
        "AP portable view with magnified cardiac silhouette.",
        "Portable AP chest radiograph, patient rotated.",
        "Bedside AP radiograph with low lung volumes.",
        "Portable AP chest image, technically limited.",
        "Frontal supine chest film obtained at the bedside.",
        "Portable AP study of the chest in a ward patient."
      ],
      "upright PA": [
        "Posteroanterior chest radiograph.",
        "Upright PA view of the chest.",
        "PA and lateral views of the chest.",
        "Erect PA chest radiograph with full inspiration.",
        "Standard PA chest film obtained in the radiology department.",
        "PA view with the scapulae retracted from the lung fields.",
        "Well-centered upright PA radiograph.",
        "Outpatient PA chest radiograph.",
        "Standing PA chest image with good inspiratory effort.",
        "Routine PA chest examination.",
        "PA projection of the chest, adequate exposure.",
        "Upright frontal PA chest film.",
        "PA chest radiograph with well-inflated lungs.",
        "Erect posteroanterior view of the thorax.",
        "Departmental PA chest study."
      ],
      "support devices present": [
        "A chest tube is in place.",
        "Central venous catheter tip projects over the superior vena cava.",
        "Endotracheal tube in satisfactory position.",
        "Nasogastric tube courses below the diaphragm.",
        "Cardiac monitoring leads overlie the chest.",
        "Dual-chamber pacemaker with leads in place.",
        "Right internal jugular line in place.",
        "Pigtail catheter projects over the lower thorax.",
        "Tracheostomy tube in place.",
        "Peripherally inserted central catheter is noted.",
        "Multiple lines and tubes overlie the chest.",
        "Sternotomy wires and mediastinal drains are present.",
        "Surgical clips and drainage catheter are seen.",
        "ECG electrodes and wires project over the thorax.",
        "Support devices are in standard position."
      ],
      "no support devices": [
        "No support devices are seen.",
        "No lines or tubes are present.",
        "No indwelling catheters.",
        "No pacemaker or implanted devices.",
        "No external monitoring leads overlie the chest.",
        "No surgical hardware is seen.",
        "No chest tubes or drains.",
        "Chest radiograph without medical devices.",
        "No foreign bodies or support lines.",
        "No endotracheal or nasogastric tube.",
        "No central venous catheter.",
        "Unremarkable soft tissues without devices.",
        "No sternotomy wires or surgical clips.",
        "No overlying wires or tubing.",
        "Device-free chest radiograph."
      ]
    },
    "extra class prompts": {
      "no_effusion": [
        "No pleural effusion.",
        "Costophrenic angles are sharp bilaterally.",
        "No evidence of pleural fluid.",
        "The pleural spaces are clear.",
        "No blunting of the costophrenic angles.",
        "Hemidiaphragms are well defined without effusion.",
        "No pleural effusion or pneumothorax.",
        "Clear costophrenic sulci without effusion.",
        "There is no pleural effusion identified.",
        "Lung bases are clear with no pleural fluid."
      ],
      "effusion": [
        "Pleural effusion is present.",
        "Blunting of the costophrenic angle consistent with pleural effusion.",
        "Small to moderate pleural effusion.",
        "Bilateral pleural effusions.",
        "Layering pleural effusion at the lung base.",
        "Meniscus-shaped basal opacity compatible with pleural effusion.",
        "Pleural fluid obscures the hemidiaphragm.",
        "Large pleural effusion with adjacent atelectasis.",
        "Fluid tracking along the lateral chest wall and fissure.",
        "Findings consistent with pleural effusion."
      ]
    }
  }
}
```

## Rationale
- **Projection and patient position (portable supine AP vs. upright PA)** is the attribute I think is most likely to be spurious. In hospital archives, effusions are much more common in inpatient and ICU patients, who are usually imaged with portable AP films. Those films also look different on their own: the scapulae overlap the lungs, the heart appears magnified, and supine fluid layers as haze instead of a meniscus. That is why I used it for TIE, FairerCLIP and PRISM.
- **Support devices** (chest tubes, central lines, ET/NG tubes, monitoring leads, pacemakers) are a well-known shortcut. Chest tubes are actually used to treat effusions, and lines mark sicker patients. This is the second attribute in SEM and Ortho-Cali.
- **Age, sex and breast shadows, and image quality** (low lung volumes, rotation, exposure) are weaker demographic or acquisition confounders. Effusion is more common in older patients, and breast shadows can look like hazy basal opacity.
- **Cardiomegaly** appears among the RoboShot harmful pairs because it co-occurs with effusion (heart failure) but does not cause it.
- **Helpful features** are the true radiological signs: costophrenic blunting, the meniscus sign, an obscured hemidiaphragm, fluid in the fissures, layering haze on a supine film, and mediastinal shift.