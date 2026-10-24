<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:1a1b27,100:D84BA4&text=Petr%20Sovadina&fontColor=ffffff&fontSize=56&fontAlignY=36&desc=AI%20Engineer%20%C2%B7%20Healthcare%20%C2%B7%20Brno&descAlignY=58&descSize=18&animation=fadeIn" alt="Petr Sovadina — AI Engineer · Healthcare · Brno" width="100%">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&pause=1200&color=D84BA4&center=true&vCenter=true&random=false&width=600&lines=Building+AI+for+Czech+healthcare;MCP+servers+for+Czech+health+data;From+a+family+of+doctors+%E2%80%94+healthcare+is+home)](https://git.io/typing-svg)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-1a1b27?style=for-the-badge&logo=linkedin&logoColor=D84BA4)](https://linkedin.com/in/petrsovadina)
[![Portfolio](https://img.shields.io/badge/Portfolio-1a1b27?style=for-the-badge&logo=vercel&logoColor=D84BA4)](https://portfolio-sovadina.vercel.app)
[![Email](https://img.shields.io/badge/Email-1a1b27?style=for-the-badge&logo=gmail&logoColor=D84BA4)](mailto:petr.sovadina9@gmail.com)

</div>

```ts
// $ whoami
const petr = {
  role: "AI Engineer",
  location: "Brno, CZ",
  building: {
    "Doktůrek.ai": "AI for Czech general practitioners (co-founder)",
    "ABUGO Group": "Claude, MCP & agent workflows for SaaS teams",
    openSource: "MCP servers that plug AI into Czech health data",
  },
  stack: {
    ai: ["Claude", "MCP", "LangGraph", "RAG"],
    code: ["TypeScript", "Python", "Next.js", "Nuxt", "FastAPI"],
    health: ["HL7 FHIR", "Medplum", "SÚKL", "MKN-10/11"],
  },
  workflow: ["spec-first (GitHub Spec Kit)", "Claude Code", "security review before any install"],
  background: "family of doctors — healthcare is home",
  openTo: ["freelance", "consulting"],
} as const;
```

## ⚡ Try it

Czech drug database inside your AI assistant. No install — add the remote MCP server to your client config:

```json
{
  "mcpServers": {
    "sukl": {
      "type": "url",
      "url": "https://sukl-mcp.vercel.app/mcp"
    }
  }
}
```

Need MKN-10, healthcare providers, reimbursements or PubMed too? CzechMedMCP has 60 tools:

```bash
uv tool install git+https://github.com/petrsovadina/CzechMedMCP.git
npx @modelcontextprotocol/inspector czechmedmcp run   # browse all 60 tools
```

## 🔌 How it fits together

```mermaid
flowchart LR
    A["Claude · Cursor · VS Code"] -->|MCP| B["SÚKL MCP Server<br/>9 tools"]
    A -->|MCP| C["CzechMedMCP<br/>60 tools"]
    B --> D[("SÚKL<br/>68k+ medicinal products")]
    C --> E[("SÚKL · MKN-10 · NRPZS<br/>SZV · VZP")]
    C --> F[("PubMed · Europe PMC<br/>bioRxiv · …")]
    classDef pink fill:#D84BA4,stroke:#D84BA4,color:#ffffff
    class B,C pink
```

## ✨ Featured Projects

<table>
<tr>
<td width="50%" valign="top">

### 💊 [SÚKL MCP Server](https://github.com/petrsovadina/SUKL-mcp)
`🟢 live` `9 tools` `68k+ products`

MCP server for the Czech medicinal products database. Typo-tolerant search, ATC lookups, monthly data refresh via CI. Landing page, MCP endpoint and demo chat on a single URL.

`TypeScript` `Next.js 16` `MCP` `Vercel` · [Live demo →](https://sukl-mcp.vercel.app)

</td>
<td width="50%" valign="top">

### 🧰 [CzechMedMCP](https://github.com/petrsovadina/CzechMedMCP)
`🟢 production` `60 tools` `open source`

23 Czech tools (SÚKL, MKN-10, NRPZS, SZV, VZP) and 37 global biomedical ones (PubMed, Europe PMC, bioRxiv). Works with Claude Desktop, Cursor and VS Code.

`Python` `MCP` `uv` `Railway` · [Docs →](https://czech-med-mcp-docs.vercel.app)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📚 [OpenClinical Knowledge Base CZ](https://github.com/petrsovadina/OpenClinical-Knowledge-Base-CZ)
`🧪 research` `open data`

Turns unstructured Czech guidelines, SPCs and regulatory bulletins into structured JSON for RAG and decision support. For research and education — not a medical device under MDR.

`TypeScript` `JSON` `RAG`

</td>
<td width="50%" valign="top">

### 🏷️ [MKN11-coder](https://github.com/DigiMedic/MKN11-coder)
`🧪 prototype`

Assisted ICD-11 (MKN-11) coding: GPT-4 extracts diagnoses from unstructured text, suggests codes and scores each suggestion's confidence.

`TypeScript` `Next.js` `OpenAI`

</td>
</tr>
</table>

<sub>Earlier work under <a href="https://github.com/DigiMedic">DigiMedic</a>: <a href="https://github.com/DigiMedic/Ask-EHDS">Ask-EHDS</a> (EHDS docs for the Czech context) · <a href="https://github.com/DigiMedic/PillSee">PillSee</a> (medication chat, architecture stage) · <a href="https://github.com/DigiMedic/DigiMedic-FHIR-Backend">FHIR backend</a></sub>

## 🛠️ Stack

<div align="center">

[![Core stack](https://skillicons.dev/icons?i=py,ts,nextjs,nuxtjs,fastapi,react,docker,vercel,azure,githubactions&theme=dark&perline=10)](https://skillicons.dev)

![Claude](https://img.shields.io/badge/Claude-1a1b27?style=flat-square&logo=claude&logoColor=D84BA4)
![MCP](https://img.shields.io/badge/MCP-1a1b27?style=flat-square&logo=modelcontextprotocol&logoColor=D84BA4)
![OpenAI](https://img.shields.io/badge/OpenAI-1a1b27?style=flat-square&logo=openai&logoColor=D84BA4)
![LangGraph](https://img.shields.io/badge/LangGraph-1a1b27?style=flat-square&logo=langchain&logoColor=D84BA4)
![LangChain](https://img.shields.io/badge/LangChain-1a1b27?style=flat-square&logo=langchain&logoColor=D84BA4)
![LightRAG](https://img.shields.io/badge/LightRAG-1a1b27?style=flat-square)
![Fastify](https://img.shields.io/badge/Fastify-1a1b27?style=flat-square&logo=fastify&logoColor=D84BA4)
![Railway](https://img.shields.io/badge/Railway-1a1b27?style=flat-square&logo=railway&logoColor=D84BA4)
![n8n](https://img.shields.io/badge/n8n-1a1b27?style=flat-square&logo=n8n&logoColor=D84BA4)

![HL7 FHIR](https://img.shields.io/badge/HL7_FHIR-D84BA4?style=flat-square)
![Medplum](https://img.shields.io/badge/Medplum-D84BA4?style=flat-square)
![SÚKL](https://img.shields.io/badge/S%C3%9AKL-D84BA4?style=flat-square)
![MKN-10/11](https://img.shields.io/badge/MKN--10%2F11-D84BA4?style=flat-square)

</div>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/petrsovadina/petrsovadina/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/petrsovadina/petrsovadina/output/github-snake.svg">
  <img alt="Contribution graph eaten by a snake" src="https://raw.githubusercontent.com/petrsovadina/petrsovadina/output/github-snake.svg">
</picture>

*Open to freelance projects and consulting — especially where AI meets real healthcare data.*

[![Let's connect](https://img.shields.io/badge/Let's_connect-D84BA4?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/petrsovadina)
![Profile Views](https://komarev.com/ghpvc/?username=petrsovadina&color=d84ba4&style=for-the-badge&label=Profile+views)

<img src="https://capsule-render.vercel.app/api?type=waving&height=120&color=0:D84BA4,100:1a1b27&section=footer" alt="" width="100%">

</div>
