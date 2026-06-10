# AI 论文分析助手 (AI Paper Analyzer)

基于 GPT-4o / Claude / DeepSeek 大语言模型的学术论文智能分析工具。

上传一篇论文 PDF，自动生成结构化分析报告：摘要、研究方法、创新点、关键词，六维度深度解读。

## 功能特性

- 📝 **论文摘要生成** — 200-300 字精准概括论文核心内容
- 🔬 **研究方法提取** — 自动识别实验法、模型法、数据分析法等
- 💡 **创新点识别** — 区分方法创新、应用创新、理论创新
- 🏷️ **关键词提取** — 中英文关键词，按重要性排序
- 📊 **六维度完整报告** — 概要、研究问题、方法、创新、结论、局限性
- 🌐 **Web 可视化界面** — Streamlit 拖拽上传，一键分析
- 🧠 **多模型支持** — GPT-4o、Claude Sonnet、DeepSeek 任选
- ✂️ **智能分块策略** — 自动处理超长论文，保持上下文连贯

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
```

`.env` 文件内容：

```
OPENAI_API_KEY=sk-xxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxx
```

至少配置一个模型的 API Key 即可使用。

### 3. 命令行使用

```bash
# 完整分析一篇论文
python main.py paper.pdf

# 仅生成摘要
python main.py paper.pdf --mode summary

# 指定使用 Claude
python main.py paper.pdf --model claude-sonnet

# 指定输出文件
python main.py paper.pdf --output my_report.md
```

### 4. Web 界面使用

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501`，拖拽上传 PDF 即可分析。

## 项目结构

```
ai-paper-analyzer/
├── main.py              # CLI 命令行入口
├── app.py               # Streamlit Web 界面
├── analyzer.py          # 核心分析引擎
├── pdf_parser.py        # PDF 文本提取与分块
├── llm_client.py        # 多模型统一调用客户端
├── prompts.py           # Prompt 模板库
├── config.py            # 配置管理
├── requirements.txt     # 依赖清单
├── .env.example         # API Key 配置示例
└── README.md
```

## 技术架构

```
┌──────────┐     ┌──────────────┐     ┌────────────┐
│  PDF 上传 │ ──▶ │ PDF 解析模块  │ ──▶ │ 智能分块器  │
└──────────┘     └──────────────┘     └─────┬──────┘
                                            │
              ┌─────────────────────────────┘
              ▼
     ┌────────────────┐     ┌──────────────┐
     │ Prompt 模板引擎 │ ──▶ │ LLM 统一客户端│
     └────────────────┘     └──────┬───────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐ ┌──────────┐ ┌────────────┐
              │  GPT-4o  │ │  Claude  │ │  DeepSeek  │
              └──────────┘ └──────────┘ └────────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │ 结构化报告生成  │
                          └────────────────┘
```

- **PDF 解析**: PyMuPDF 提取文本，支持中英文论文
- **智能分块**: 在句子边界截断，保持 200 字符重叠，确保跨块上下文连贯
- **多模型适配**: 统一封装 OpenAI、Anthropic、DeepSeek API，一行代码切换模型
- **Prompt 工程**: 角色设定 + 结构化要求 + 输出格式约束，确保分析质量一致

## 使用示例

### 命令行输出

```
==================================================
  AI 论文分析助手
  模型: gpt-4o-mini | 模式: full
==================================================
[加载] 正在解析 PDF: attention_is_all_you_need.pdf
  - 标题: Attention Is All You Need
  - 作者: Vaswani et al.
  - 页数: 15
  - 总字符数: 42368

[分析] 生成论文摘要...
[分析] 提取研究方法...
[分析] 提取创新点...
[分析] 提取关键词...

[完成] 分析结束！
[输出] 分析报告已保存到: output/attention_is_all_you_need_分析报告.md
```

### 生成的报告示例

```markdown
# 论文分析报告

## 基本信息
- **标题**: Attention Is All You Need
- **作者**: Vaswani et al.
- **模型**: gpt-4o-mini

## 摘要
本文提出了 Transformer 模型，一种完全基于注意力机制的网络架构...

## 研究方法
- **模型构建法**: 设计并实现了 Transformer 架构，包含多头自注意力...
- **对比实验法**: 在 WMT 2014 英德和英法翻译任务上与现有最佳模型对比...

## 创新点与贡献
1. **[方法创新]** 首次提出纯注意力机制的序列转换模型，摒弃了循环和卷积结构...
2. **[方法创新]** 提出多头注意力机制，使模型能同时关注不同表示子空间...

## 关键词
- Transformer（Transformer）
- Self-Attention（自注意力机制）
- Neural Machine Translation（神经机器翻译）
- Multi-Head Attention（多头注意力）
- Sequence-to-Sequence（序列到序列）
```

## 适用场景

- 📚 **文献调研**: 批量快速理解论文核心内容
- 🔍 **方法对比**: 系统提取不同论文的研究方法进行横向比较
- ✍️ **论文写作**: 分析优秀论文的结构与创新点表达方式
- 🎓 **学术入门**: 帮助新手快速把握领域经典论文的贡献

## 后续计划

- [ ] 支持扫描版 PDF（OCR）
- [ ] 批量论文对比分析
- [ ] 论文引用关系图谱
- [ ] 多语言翻译摘要
- [ ] Docker 一键部署

## License

MIT
