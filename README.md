<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🕺 LodgE README</title>
</head>
<body>
  <div align="center">
    <h1>🕺 LodgE: Coarse-to-Fine Diffusion for Long Dance Generation</h1>
    <p><em>A two-stage diffusion network that generates long-form dance sequences from music, guided by characteristic dance primitives. Originally introduced in <strong>Lodge</strong> (CVPR 2024) by Ronghui Li <em>et al.</em></em></p>
    <p>
      <a href="https://li-ronghui.github.io/lodge">
        <img src="https://img.shields.io/badge/Project-Page-Green" alt="Project Page"/>
      </a>
      <a href="https://arxiv.org/abs/2403.10518">
        <img src="https://img.shields.io/badge/ArXiv-2304.01186-red" alt="ArXiv"/>
      </a>
    </p>
  </div>
  <hr/>

  <h2>📖 Table of Contents</h2>
  <ol>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#environment-setup">Environment Setup</a></li>
    <li><a href="#data-preparation">Data Preparation</a></li>
    <li><a href="#inference-generation">Inference &amp; Generation</a></li>
    <li><a href="#rendering-streamlit-app">Rendering &amp; Streamlit App</a></li>
    <li><a href="#evaluation">Evaluation</a></li>
    <li><a href="#citation">Citation</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#license">License</a></li>
  </ol>
  <hr/>

  <h2 id="project-overview">1. Project Overview</h2>
  <p><strong>Lodge</strong> presents a coarse-to-fine diffusion framework capable of generating extremely long dance sequences in parallel, given a music input. Our two-stage pipeline consists of:</p>
  <ul>
    <li><strong>Local Diffusion</strong>: Models fine-grained, short-term motion primitives.</li>
    <li><strong>Global Diffusion</strong>: Captures long-term temporal structure and global coherence.</li>
  </ul>
  <p>This repo contains code for environment setup, data preprocessing, training, inference, rendering, and a Streamlit demo app for real-time visualization.</p>
  <hr/>

  <h2 id="features">2. Features</h2>
  <ul>
    <li>🎵 Audio-conditioned dance generation</li>
    <li>⏳ Parallel synthesis of sequences spanning minutes</li>
    <li>💃 Support for 22 dance genres (via the FineDance dataset)</li>
    <li>🖥️ Streamlit-based interactive demo</li>
  </ul>
  <hr/>

  <h2 id="prerequisites">3. Prerequisites</h2>
  <ul>
    <li><strong>CUDA 11+</strong></li>
    <li><strong>NVIDIA GPU</strong> (A100 recommended for training)</li>
    <li><strong>Python 3.8+</strong></li>
    <li><strong>Conda</strong> (for environment management)</li>
  </ul>
  <hr/>

  <h2 id="installation">4. Installation</h2>
  <ol>
    <li>
      <p>Clone this forked repo:</p>
      <pre><code>git clone https://github.com/your-username/lodge.git
cd lodge</code></pre>
    </li>
    <li>
      <p>(Optional) Create &amp; activate your Conda env:</p>
      <pre><code>conda env create -f lodge.yml
conda activate lodge</code></pre>
    </li>
  </ol>
  <hr/>

  <h2 id="environment-setup">5. Environment Setup</h2>
  <p>Matches the official EDGE setup. Install dependencies:</p>
  <pre><code>conda env create -f lodge.yml
conda activate lodge</code></pre>
  <p>This installs:</p>
  <ul>
    <li><code>pytorch-lightning==1.9.5</code></li>
    <li>Audio, vision, and data-processing packages</li>
  </ul>
  <hr/>

  <h2 id="data-preparation">6. Data Preparation</h2>
  <p>The <a href="https://github.com/li-ronghui/FineDance">FineDance</a> dataset averages 152.3 s per clip over 22 genres; we use only the 22 body joints for Lodge.</p>
  <ol>
    <li>
      <p>Download raw FineDance from <a href="https://drive.google.com/file/d/1zQvWG9I0H4U3Zrm8d_QD_ehenZvqfQfS/view">Google Drive</a> or <a href="https://pan.baidu.com/s/1gynUC7pMdpsE31wAwq177w?pwd=o9pw">百度云</a> and place in <code>./data</code>.</p>
    </li>
    <li>
      <p>Preprocess:</p>
      <pre><code>python data/code/preprocess.py
python data/code/pre/FineDance_normalizer.py</code></pre>
    </li>
    <li>
      <p><strong>Optional:</strong> Use our preprocessed features. Place under <code>./data/finedance/</code>:</p>
      <pre><code>lodge/data/finedance
├── label_json/
├── motion/     # .npy files
├── music_npy/
├── music_wav/
├── Normalizer.pth
└── smplx_neu_J_1.npy</code></pre>
    </li>
  </ol>
  <hr/>

  <h2 id="inference-generation">7. Inference &amp; Generation</h2>
  <p>Generate dance sequences (soft ∈ [0,1]):</p>
  <pre><code>python infer_lodge.py \\
  --cfg exp/Local_Module/FineDance_FineTuneV2_Local/local_train.yaml \\
  --cfg_assets configs/data/assets.yaml \\
  --soft 1.0</code></pre>
  <hr/>

  <h2 id="rendering-streamlit-app">8. Rendering &amp; Streamlit App</h2>
  <h3>Rendering</h3>
  <p>Switched from <code>ffmpeg</code> to <strong>MoviePy</strong> due to rendering problems:</p>
  <pre><code>python render.py --modir path/to/output/motion_dir</code></pre>

  <h3>Streamlit App</h3>
  <p>Use local or university RTX 3090 (Colab GPU insufficient). No DigitalOcean—host via Streamlit:</p>
  <pre><code>streamlit run app.py</code></pre>
  <p>Upload motion + audio in the UI to get a final synced video.</p>
  <hr/>

  <h2 id="evaluation">9. Evaluation</h2>
  <pre><code>python metric/metrics_finedance.py    # diversity &amp; fidelity
python metric/beat_align_score.py       # beat alignment
python metric/foot_skating.py           # foot contact quality</code></pre>
  <hr/>

  <h2 id="citation">10. Citation</h2>
  <p>If you find this helpful, please ⭐️ and cite:</p>
  <pre><code>@inproceedings{li2024lodge,
  title={Lodge: A coarse to fine diffusion network for long dance generation guided by the characteristic dance primitives},
  author={Li, Ronghui and … and Li, Xiu},
  booktitle={CVPR},
  pages={1524–1534},
  year={2024}
}

@inproceedings{li2023finedance,
  title={FineDance: A fine-grained choreography dataset for 3d full body dance generation},
  author={Li, Ronghui and … and Li, Xiu},
  booktitle={ICCV},
  pages={10234–10243},
  year={2023}
}
</code></pre>
  <hr/>

  <h2 id="acknowledgements">11. Acknowledgements</h2>
  <p>Inspired by <a href="https://github.com/Stanford-TML/EDGE">EDGE</a>, eval scripts from <a href="https://github.com/lisiyao21/Bailando">Bailando</a>, and README style from <strong>follow-your-pose</strong>. Thanks to all authors!</p>
  <hr/>

  <h2 id="license">12. License</h2>
  <p>Released under the MIT License. See <a href="LICENSE">LICENSE</a> for details.</p>
</body>
</html>
